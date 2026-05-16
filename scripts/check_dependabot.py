from pathlib import Path
from typing import Final, TypeGuard, cast

import yaml

ROOT: Final = Path(__file__).resolve().parents[1]
DEPENDABOT_PATH: Final = ROOT / ".github" / "dependabot.yml"
DEPENDABOT_CONFIG_VERSION: Final = 2
REQUIRED_UPDATES: Final = {
    ("uv", "/backend"),
    ("npm", "/frontend"),
    ("github-actions", "/"),
    ("docker", "/docker"),
    ("terraform", "/infra/terraform"),
}


def is_mapping(value: object) -> TypeGuard[dict[object, object]]:
    """Return whether a value is a YAML mapping.

    Args:
        value: Parsed YAML value.

    Returns:
        True when the value is a mapping.

    Raises:
        None.
    """

    return isinstance(value, dict)


def is_sequence(value: object) -> TypeGuard[list[object]]:
    """Return whether a value is a YAML sequence.

    Args:
        value: Parsed YAML value.

    Returns:
        True when the value is a sequence.

    Raises:
        None.
    """

    return isinstance(value, list)


def require_string(value: object, field_name: str) -> str:
    """Return a required string field.

    Args:
        value: Candidate field value.
        field_name: Field name used in the error message.

    Returns:
        String field value.

    Raises:
        SystemExit: If the field is not a string.
    """

    if not isinstance(value, str):
        raise SystemExit(f"{field_name} must be a string.")
    return value


def main() -> None:
    """Validate the Dependabot configuration used by this template.

    Returns:
        None.

    Raises:
        SystemExit: If the Dependabot configuration is missing or invalid.
        yaml.YAMLError: If the file is not valid YAML.
    """

    raw = DEPENDABOT_PATH.read_text(encoding="utf-8")
    parsed = cast(object, yaml.safe_load(raw))
    if not is_mapping(parsed):
        raise SystemExit(".github/dependabot.yml must be a YAML mapping.")
    if parsed.get("version") != DEPENDABOT_CONFIG_VERSION:
        raise SystemExit(".github/dependabot.yml must set version: 2.")

    updates = parsed.get("updates")
    if not is_sequence(updates):
        raise SystemExit(".github/dependabot.yml must define updates as a list.")

    actual_updates: set[tuple[str, str]] = set()
    for index, update in enumerate(updates):
        if not is_mapping(update):
            raise SystemExit(f"updates[{index}] must be a mapping.")
        ecosystem = require_string(update.get("package-ecosystem"), "package-ecosystem")
        directory = require_string(update.get("directory"), "directory")
        actual_updates.add((ecosystem, directory))

    missing_updates = REQUIRED_UPDATES - actual_updates
    if missing_updates:
        missing = ", ".join(
            f"{ecosystem}:{directory}" for ecosystem, directory in sorted(missing_updates)
        )
        raise SystemExit(f".github/dependabot.yml is missing updates for: {missing}.")


if __name__ == "__main__":
    main()
