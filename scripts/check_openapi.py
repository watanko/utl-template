import json
import sys
from pathlib import Path
from typing import Final, cast

ROOT: Final = Path(__file__).resolve().parents[1]
BACKEND_ROOT: Final = ROOT / "backend"
OPENAPI_PATH: Final = ROOT / "docs" / "openapi.json"


def build_openapi_text() -> str:
    """Build the canonical OpenAPI schema text.

    Returns:
        Canonical JSON text for the current backend OpenAPI schema.

    Raises:
        pydantic.ValidationError: If backend settings are invalid.
    """

    sys.path.insert(0, str(BACKEND_ROOT))

    from src.main import create_app

    schema = cast(dict[str, object], create_app().openapi())
    return json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    """Validate that docs/openapi.json matches the backend schema.

    Returns:
        None.

    Raises:
        SystemExit: If docs/openapi.json is stale.
        OSError: If docs/openapi.json cannot be read.
    """

    expected = build_openapi_text()
    actual = OPENAPI_PATH.read_text(encoding="utf-8")
    if actual != expected:
        raise SystemExit("docs/openapi.json is stale. Run `make sync dto`.")


if __name__ == "__main__":
    main()
