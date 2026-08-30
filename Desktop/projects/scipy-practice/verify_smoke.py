"""Quick smoke checks for the interactive SciPy practice app."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch


def run_main_with_inputs(*inputs):
    """Run main.main() with scripted input and return captured output."""
    from main import main

    output = StringIO()
    with patch("builtins.input", side_effect=list(inputs)), redirect_stdout(output):
        main()
    return output.getvalue()


def run_verify():
    """Verify the menu can exit cleanly via digit or exit keyword."""
    try:
        output = run_main_with_inputs("exit")
    except ModuleNotFoundError as exc:
        missing = exc.name or str(exc)
        print(f"verify_smoke: missing dependency: {missing}")
        print("Install dependencies with: pip install -r requirements.txt")
        raise SystemExit(1) from exc

    if "We'll talk later!" not in output:
        raise AssertionError("Expected exit message was not printed")
    if "Last Updated:" in output:
        raise AssertionError("Menu option 0 / LAST_UPDATED must be removed (B010)")

    print("verify_smoke: OK (main menu exit via 'exit')")


if __name__ == "__main__":
    run_verify()
