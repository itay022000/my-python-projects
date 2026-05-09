"""
Phase 0 safety net for puzzle-rush-game.

Checks:
1) Module import smoke.
2) Generator smoke for all generate_*_challenge callables (easy/medium/hard).
3) Quick CLI entrypoint smoke for each game script.
4) Guard that play_game references generate_true_false_challenge.

Run from this directory:
  python3 verify_phase0_smoke.py
"""

from __future__ import annotations

import ast
import importlib
import inspect
import signal
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


MODULE_NAMES = [
    "array_blitz",
    "vector_battle",
    "matrix_challenge",
    "ufunc_arena",
]

DIFFICULTIES = ("easy", "medium", "hard")
REQUIRED_CHALLENGE_KEYS = {"type", "question", "answer", "hint"}
MAX_GENERATOR_RETRIES = 8


def _load_modules() -> dict[str, object]:
    modules: dict[str, object] = {}
    for name in MODULE_NAMES:
        modules[name] = importlib.import_module(name)
    return modules


def _iter_generator_funcs(mod) -> list[tuple[str, object]]:
    funcs: list[tuple[str, object]] = []
    for name, obj in vars(mod).items():
        if not callable(obj):
            continue
        if not name.startswith("generate_") or not name.endswith("_challenge"):
            continue
        funcs.append((name, obj))
    return sorted(funcs, key=lambda x: x[0])


def _assert_challenge_shape(module_name: str, func_name: str, challenge: dict) -> None:
    assert isinstance(challenge, dict), f"{module_name}.{func_name}: expected dict, got {type(challenge)}"
    missing = REQUIRED_CHALLENGE_KEYS - set(challenge.keys())
    assert not missing, f"{module_name}.{func_name}: missing keys {sorted(missing)}"
    assert isinstance(challenge["question"], str), f"{module_name}.{func_name}: question must be str"
    assert isinstance(challenge["answer"], str), f"{module_name}.{func_name}: answer must be str"
    assert isinstance(challenge["hint"], str), f"{module_name}.{func_name}: hint must be str"
    assert isinstance(challenge["type"], str) and challenge["type"].strip(), (
        f"{module_name}.{func_name}: type must be a non-empty string"
    )


def _run_generator_smoke(modules: dict[str, object]) -> None:
    def _timeout_handler(_signum, _frame):
        raise TimeoutError("challenge generation timed out")

    signal.signal(signal.SIGALRM, _timeout_handler)

    for module_name, mod in modules.items():
        generators = _iter_generator_funcs(mod)
        assert generators, f"{module_name}: no generate_*_challenge functions found"
        for func_name, func in generators:
            for diff in DIFFICULTIES:
                last_error: Exception | None = None
                challenge = None
                for _ in range(MAX_GENERATOR_RETRIES):
                    signal.setitimer(signal.ITIMER_REAL, 1.0)
                    try:
                        challenge = func(diff)
                        last_error = None
                        break
                    except ValueError as exc:
                        # Some generators can rarely sample invalid random ranges.
                        # Retry to avoid flaky smoke runs while still surfacing persistent failures.
                        last_error = exc
                    finally:
                        signal.setitimer(signal.ITIMER_REAL, 0)
                if last_error is not None:
                    raise AssertionError(
                        f"{module_name}.{func_name} failed after {MAX_GENERATOR_RETRIES} retries "
                        f"for difficulty '{diff}': {last_error}"
                    ) from last_error
                assert challenge is not None
                _assert_challenge_shape(module_name, func_name, challenge)


def _run_cli_smoke(modules: dict[str, object]) -> None:
    # Enter easy difficulty, then exit immediately on first challenge.
    for module_name, mod in modules.items():
        with patch("builtins.input", side_effect=["1", "exit"]):
            with redirect_stdout(StringIO()):
                mod.play_game()


def _play_game_references_tf(mod) -> bool:
    source = inspect.getsource(mod.play_game)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "generate_true_false_challenge":
            return True
    return False


def _run_true_false_guard(modules: dict[str, object]) -> None:
    failures: list[str] = []
    for module_name, mod in modules.items():
        assert hasattr(mod, "generate_true_false_challenge"), (
            f"{module_name}: expected generate_true_false_challenge to exist"
        )
        if not _play_game_references_tf(mod):
            failures.append(
                f"{module_name}.play_game does not reference generate_true_false_challenge; "
                "T/F questions are likely not scheduled."
            )
    assert not failures, "\n".join(failures)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))

    print("phase0: loading modules...", flush=True)
    modules = _load_modules()
    print("phase0: generator smoke...", flush=True)
    _run_generator_smoke(modules)
    print("phase0: cli smoke...", flush=True)
    _run_cli_smoke(modules)
    print("phase0: true/false scheduling guard...", flush=True)
    _run_true_false_guard(modules)

    print("verify_phase0_smoke: OK (imports + generators + CLI smoke + T/F scheduling guard).")


if __name__ == "__main__":
    main()
