import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, TypeGuard, cast

ROOT: Final = Path(__file__).resolve().parents[1]
Mode = Literal["post-tool", "pre-commit", "changed"]
HookEvent = Literal["PostToolUse", "PreToolUse"]
CheckProfile = Literal["fast", "full"]


@dataclass(frozen=True, slots=True)
class CheckCommand:
    """Command selected for changed files.

    Attributes:
        label: Human-readable command label.
        command: Shell command to execute from the repository root.

    """

    label: str
    command: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Result of a selected check command.

    Attributes:
        command: Executed command.
        return_code: Process return code.
        output: Combined command output.

    """

    command: CheckCommand
    return_code: int
    output: str


class CheckFailureError(Exception):
    """Raised when at least one selected check fails.

    Attributes:
        results: Failed command results.

    """

    def __init__(self, results: list[CheckResult]) -> None:
        """Initialize the error.

        Args:
            results: Failed command results.

        Returns:
            None.

        """
        self.results = results
        super().__init__("Changed-file checks failed.")


def is_mapping(value: object) -> TypeGuard[dict[str, object]]:
    """Return whether a value is a string-keyed mapping.

    Args:
        value: Candidate value.

    Returns:
        True when the value is a dictionary.

    Raises:
        None.

    """

    return isinstance(value, dict) and all(isinstance(key, str) for key in value)


def run_git(args: list[str]) -> list[str]:
    """Run git and return non-empty output lines.

    Args:
        args: Git arguments after the `git` executable.

    Returns:
        Non-empty output lines.

    Raises:
        subprocess.CalledProcessError: If git exits with a non-zero code.

    """

    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def normalize_path(path: str) -> str:
    """Return a repository-relative POSIX path.

    Args:
        path: Absolute or relative file path.

    Returns:
        Repository-relative path using `/` separators.

    Raises:
        ValueError: If the path is outside the repository.

    """

    candidate = Path(path)
    absolute = candidate if candidate.is_absolute() else ROOT / candidate
    return absolute.resolve().relative_to(ROOT).as_posix()


def paths_from_hook_input(raw_input: str) -> set[str]:
    """Extract changed paths from Codex hook input.

    Args:
        raw_input: JSON payload passed to the hook on stdin.

    Returns:
        Repository-relative paths found in the hook input.

    Raises:
        json.JSONDecodeError: If the hook input is not valid JSON.

    """

    if not raw_input.strip():
        return set()

    parsed = cast(object, json.loads(raw_input))
    if not is_mapping(parsed):
        return set()

    tool_input = parsed.get("tool_input")
    if not is_mapping(tool_input):
        return set()

    raw_paths: list[str] = []
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            raw_paths.append(value)

    command = tool_input.get("command")
    if isinstance(command, str):
        raw_paths.extend(paths_from_apply_patch(command))

    normalized_paths: set[str] = set()
    for raw_path in raw_paths:
        try:
            normalized_paths.add(normalize_path(raw_path))
        except ValueError:
            continue
    return normalized_paths


def paths_from_apply_patch(command: str) -> list[str]:
    """Extract file paths from an apply_patch command payload.

    Args:
        command: Patch text from Codex `apply_patch` tool input.

    Returns:
        File paths mentioned by patch headers.

    Raises:
        None.

    """

    prefixes = (
        "*** Add File: ",
        "*** Update File: ",
        "*** Delete File: ",
        "*** Move to: ",
    )
    paths: list[str] = []
    for line in command.splitlines():
        for prefix in prefixes:
            if line.startswith(prefix):
                paths.append(line.removeprefix(prefix).strip())
                break
    return paths


def dirty_paths() -> set[str]:
    """Return changed paths in the worktree and index.

    Returns:
        Changed repository-relative paths.

    Raises:
        subprocess.CalledProcessError: If git diff fails.

    """

    paths = set(run_git(["diff", "--name-only"]))
    paths.update(run_git(["diff", "--cached", "--name-only"]))
    return paths


def staged_paths() -> set[str]:
    """Return staged changed paths.

    Returns:
        Staged repository-relative paths.

    Raises:
        subprocess.CalledProcessError: If git diff fails.

    """

    return set(run_git(["diff", "--cached", "--name-only"]))


def stage_paths(paths: set[str]) -> None:
    """Stage paths after automatic fixes.

    Args:
        paths: Repository-relative paths to stage.

    Returns:
        None.

    Raises:
        subprocess.CalledProcessError: If git add fails.

    """

    if paths:
        subprocess.run(["git", "add", "-A", "--", *sorted(paths)], cwd=ROOT, check=True)


def command_for_label(label: str, profile: CheckProfile) -> CheckCommand:
    """Return a check command by label.

    Args:
        label: Command label.
        profile: Check depth profile.

    Returns:
        Check command.

    Raises:
        ValueError: If the label is unknown.

    """

    if profile == "fast":
        commands = {
            "backend": CheckCommand("task check:fast:backend", ("task", "check:fast:backend")),
            "frontend": CheckCommand("task check:fast:frontend", ("task", "check:fast:frontend")),
            "tooling": CheckCommand("task check:fast:tooling", ("task", "check:fast:tooling")),
            "security": CheckCommand("task check:security", ("task", "check:security")),
        }
        return commands[label]

    commands = {
        "backend": CheckCommand("task check:backend", ("task", "check:backend")),
        "frontend": CheckCommand("task check:frontend", ("task", "check:frontend")),
        "tooling": CheckCommand("task check:tooling", ("task", "check:tooling")),
        "security": CheckCommand("task check:security", ("task", "check:security")),
    }
    return commands[label]


def select_commands(paths: set[str], profile: CheckProfile) -> list[CheckCommand]:
    """Select checks for changed paths.

    Args:
        paths: Repository-relative changed paths.
        profile: Check depth profile.

    Returns:
        Ordered check commands.

    Raises:
        None.

    """

    labels: list[str] = []

    def add(label: str) -> None:
        if label not in labels:
            labels.append(label)

    for path in sorted(paths):
        if path.startswith("backend/"):
            add("backend")
        if path.startswith("frontend/"):
            add("frontend")
        if (
            path == "Taskfile.yml"
            or path == "pre-commit.yaml"
            or path.startswith(".codex/")
            or path.startswith(".github/")
            or path.startswith("docker/")
            or path.startswith("infra/terraform/")
            or path.startswith("scripts/")
        ):
            add("tooling")
        if path.startswith(".github/workflows/") or path == "pre-commit.yaml":
            add("security")

    return [command_for_label(label, profile) for label in labels]


def run_command(command: CheckCommand) -> CheckResult:
    """Run one check command.

    Args:
        command: Check command to execute.

    Returns:
        Completed check result.

    Raises:
        None.

    """

    completed = subprocess.run(
        list(command.command),
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return CheckResult(command=command, return_code=completed.returncode, output=output)


def run_commands(commands: list[CheckCommand]) -> list[CheckResult]:
    """Run check commands and stop after the first failure.

    Args:
        commands: Ordered commands to execute.

    Returns:
        Check results.

    Raises:
        CheckFailureError: If a command fails.

    """

    results: list[CheckResult] = []
    failed_results: list[CheckResult] = []
    for command in commands:
        result = run_command(command)
        results.append(result)
        if result.return_code != 0:
            failed_results.append(result)
            raise CheckFailureError(failed_results)
    return results


def format_results(results: list[CheckResult]) -> str:
    """Format check results for hook output.

    Args:
        results: Check results.

    Returns:
        Concise result text.

    Raises:
        None.

    """

    if not results:
        return "変更ファイルに対応する自動チェックはありません。"

    lines = ["自動チェックが成功しました:"]
    lines.extend(f"- {result.command.label}" for result in results)
    return "\n".join(lines)


def format_failure(error: CheckFailureError) -> str:
    """Format a check failure for hook output.

    Args:
        error: Check failure.

    Returns:
        Failure text with command output.

    Raises:
        None.

    """

    result = error.results[0]
    output = result.output.strip()
    if len(output) > 6000:
        output = output[-6000:]
    return f"自動チェックに失敗しました: {result.command.label}\n\n{output}"


def write_post_tool_success(results: list[CheckResult]) -> None:
    """Write successful PostToolUse hook output.

    Args:
        results: Successful check results.

    Returns:
        None.

    Raises:
        OSError: If stdout cannot be written.

    """

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": format_results(results),
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def write_post_tool_failure(error: CheckFailureError) -> None:
    """Write failed PostToolUse hook output.

    Args:
        error: Check failure.

    Returns:
        None.

    Raises:
        OSError: If stdout cannot be written.

    """

    payload = {
        "decision": "block",
        "reason": format_failure(error),
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def write_pre_commit_result(results: list[CheckResult]) -> None:
    """Write successful PreToolUse hook output.

    Args:
        results: Successful check results.

    Returns:
        None.

    Raises:
        OSError: If stdout cannot be written.

    """

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": format_results(results),
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def write_pre_commit_failure(error: CheckFailureError) -> None:
    """Write failed PreToolUse hook output.

    Args:
        error: Check failure.

    Returns:
        None.

    Raises:
        OSError: If stdout cannot be written.

    """

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": format_failure(error),
        }
    }
    print(json.dumps(payload, ensure_ascii=False))


def run_plain(commands: list[CheckCommand]) -> int:
    """Run checks for direct command-line use.

    Args:
        commands: Ordered commands to execute.

    Returns:
        Process exit code.

    Raises:
        None.

    """

    if not commands:
        print("No changed-file checks selected.")
        return 0

    for command in commands:
        result = run_command(command)
        print(result.output, end="")
        if result.return_code != 0:
            return result.return_code
    return 0


def run_post_tool() -> int:
    """Run checks for a Codex PostToolUse hook.

    Returns:
        Hook process exit code.

    Raises:
        json.JSONDecodeError: If stdin is invalid JSON.
        subprocess.CalledProcessError: If git diff fails.

    """

    hook_paths = paths_from_hook_input(sys.stdin.read())
    paths = hook_paths or dirty_paths()
    commands = select_commands(paths, "fast")
    try:
        results = run_commands(commands)
    except CheckFailureError as error:
        write_post_tool_failure(error)
        return 0

    write_post_tool_success(results)
    return 0


def run_pre_commit() -> int:
    """Run checks before an agent executes git commit.

    Returns:
        Hook process exit code.

    Raises:
        subprocess.CalledProcessError: If git diff fails.

    """

    raw_input = sys.stdin.read()
    if not is_git_commit_command(raw_input):
        return 0

    paths = staged_paths()
    commands = select_commands(paths, "full")
    try:
        results = run_commands(commands)
    except CheckFailureError as error:
        write_pre_commit_failure(error)
        return 0

    stage_paths(paths)
    write_pre_commit_result(results)
    return 0


def is_git_commit_command(raw_input: str) -> bool:
    """Return whether a PreToolUse payload is a git commit command.

    Args:
        raw_input: JSON payload passed to the hook on stdin.

    Returns:
        True when the Bash command starts with `git commit`.

    Raises:
        json.JSONDecodeError: If the hook input is not valid JSON.

    """

    if not raw_input.strip():
        return False

    parsed = cast(object, json.loads(raw_input))
    if not is_mapping(parsed):
        return False

    tool_input = parsed.get("tool_input")
    if not is_mapping(tool_input):
        return False

    command = tool_input.get("command")
    return isinstance(command, str) and command.strip().startswith("git commit")


def parse_mode(value: str) -> Mode:
    """Parse a command-line mode.

    Args:
        value: Raw mode value.

    Returns:
        Parsed mode.

    Raises:
        SystemExit: If the mode is unknown.

    """

    if value in {"post-tool", "pre-commit", "changed"}:
        return cast(Mode, value)
    raise SystemExit(f"Unknown mode: {value}")


def main() -> None:
    """Run changed-file checks.

    Returns:
        None.

    Raises:
        SystemExit: If checks fail in direct command-line mode.
    """

    mode = parse_mode(sys.argv[1] if len(sys.argv) > 1 else "changed")
    if mode == "post-tool":
        raise SystemExit(run_post_tool())
    if mode == "pre-commit":
        raise SystemExit(run_pre_commit())

    raise SystemExit(run_plain(select_commands(dirty_paths(), "full")))


if __name__ == "__main__":
    main()
