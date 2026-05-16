import json
import sys
from pathlib import Path
from typing import Final, cast

ROOT: Final = Path(__file__).resolve().parents[1]
BACKEND_ROOT: Final = ROOT / "backend"
OPENAPI_PATH: Final = ROOT / "docs" / "openapi.json"


def main() -> None:
    """Export FastAPI OpenAPI schema for frontend type generation.

    Returns:
        None.

    Raises:
        OSError: If the output file cannot be written.
        pydantic.ValidationError: If backend settings are invalid.
    """

    sys.path.insert(0, str(BACKEND_ROOT))

    from src.main import create_app

    schema = cast(dict[str, object], create_app().openapi())
    OPENAPI_PATH.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
