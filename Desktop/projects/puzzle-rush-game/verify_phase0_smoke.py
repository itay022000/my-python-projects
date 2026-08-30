"""
Phase 0 safety net for puzzle-rush-game.

Checks:
1) Module import smoke.
2) Generator smoke for all generate_*_challenge callables.
3) main.py menu + game entry smoke.
4) Guard that play_game references generate_true_false_challenge.
5) Array Blitz negative slice edge case (stop at array end).

Run from this directory:
  python3 verify_phase0_smoke.py
"""

from __future__ import annotations

import ast
import importlib
import inspect
import random
import signal
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import numpy as np


MODULE_NAMES = [
    "games.array_blitz",
    "games.vector_battle",
    "games.matrix_challenge",
    "games.ufunc_arena",
]

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
            last_error: Exception | None = None
            challenge = None
            for _ in range(MAX_GENERATOR_RETRIES):
                signal.setitimer(signal.ITIMER_REAL, 1.0)
                try:
                    challenge = func()
                    last_error = None
                    break
                except ValueError as exc:
                    last_error = exc
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
            if last_error is not None:
                raise AssertionError(
                    f"{module_name}.{func_name} failed after {MAX_GENERATOR_RETRIES} retries: "
                    f"{last_error}"
                ) from last_error
            assert challenge is not None
            _assert_challenge_shape(module_name, func_name, challenge)


def _run_main_menu_smoke() -> None:
    import main as main_mod

    with patch("builtins.input", side_effect=["5"]):
        with redirect_stdout(StringIO()):
            main_mod.main()


def _run_cli_smoke(modules: dict[str, object]) -> None:
    # Teach Enter, then exit on first challenge.
    for module_name, mod in modules.items():
        with patch("builtins.input", side_effect=["", "exit"]):
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


def _run_tf_last_order_guard() -> None:
    """Code questions must occupy slots 1–15; T/F must be last (16–20)."""
    from session_common import build_challenge_sequence

    used: set[str] = set()

    def code_factory():
        return {"type": "code", "question": "q", "answer": "a", "hint": ""}

    def tf_factory(*, used_questions=None):
        return {
            "type": "true_false",
            "question": f"tf-{len(used_questions or used)}",
            "answer": "True",
            "hint": "",
        }

    for seed in range(20):
        random.seed(seed)
        seq = build_challenge_sequence(
            [code_factory],
            tf_factory,
            code_count=15,
            tf_count=5,
            used_questions=used,
        )
        assert len(seq) == 20
        types = [factory()["type"] for factory in seq]
        assert types[:15] == ["code"] * 15, f"seed={seed}: expected code in 1–15, got {types}"
        assert types[15:] == ["true_false"] * 5, (
            f"seed={seed}: expected T/F in 16–20, got {types}"
        )


def _run_array_blitz_slice_probe() -> None:
    """
    Regression guard for negative-index slices.

    When stop == len(array), the old code called randint(1, 0) and raised ValueError.
    """
    import games.array_blitz as ab

    for seed in range(500):
        random.seed(seed)
        challenge = ab.generate_slice_challenge()
        _assert_challenge_shape("array_blitz", "generate_slice_challenge", challenge)

    with patch.object(ab.random, "randint", side_effect=[20, 2, 20]):
        with patch.object(ab.np.random, "randint", return_value=np.zeros(20, dtype=int)):
            with patch.object(ab.random, "choice", side_effect=[1, False]):
                challenge = ab.generate_slice_challenge()

    _assert_challenge_shape("array_blitz", "generate_slice_challenge", challenge)
    assert challenge["answer"] == "a[2:-1]"
    assert "negative index" in challenge["question"]


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))

    print("phase0: loading modules...", flush=True)
    modules = _load_modules()
    print("phase0: generator smoke...", flush=True)
    _run_generator_smoke(modules)
    print("phase0: main menu smoke...", flush=True)
    _run_main_menu_smoke()
    print("phase0: cli smoke...", flush=True)
    _run_cli_smoke(modules)
    print("phase0: true/false scheduling guard...", flush=True)
    _run_true_false_guard(modules)
    print("phase0: T/F-last order guard...", flush=True)
    _run_tf_last_order_guard()
    print("phase0: array blitz slice probe...", flush=True)
    _run_array_blitz_slice_probe()

    print(
        "verify_phase0_smoke: OK "
        "(imports + generators + main menu + CLI smoke + T/F guard + "
        "T/F-last order + slice probe)."
    )


if __name__ == "__main__":
    main()
