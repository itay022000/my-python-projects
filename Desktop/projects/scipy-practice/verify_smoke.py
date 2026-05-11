"""Quick smoke checks for the interactive SciPy practice app."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch


def run_main_with_inputs(*inputs):
    """Run main.main() with scripted input and return captured output."""
    from main import LAST_UPDATED, main

    output = StringIO()
    with patch("builtins.input", side_effect=list(inputs)), redirect_stdout(output):
        main()
    return LAST_UPDATED, output.getvalue()


def main():
    """Verify the menu can show revision info and exit cleanly."""
    try:
        last_updated, output = run_main_with_inputs("0", "7")
    except ModuleNotFoundError as exc:
        missing = exc.name or str(exc)
        print(f"verify_smoke: missing dependency: {missing}")
        print("Install dependencies with: pip install -r requirements.txt")
        raise SystemExit(1) from exc

    expected = f"Last Updated: {last_updated}"
    if expected not in output:
        raise AssertionError(f"Expected revision output not found: {expected}")
    if "We'll talk later!" not in output:
        raise AssertionError("Expected exit message was not printed")

    print("verify_smoke: OK (menu option 0 + exit)")


if __name__ == "__main__":
    main()
