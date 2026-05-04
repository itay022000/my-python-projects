"""
Smoke test: imports, pool/session builders, and check(expected) for every batch.

Run from python-basics/:  python3 verify_project_smoke.py
"""

from __future__ import annotations

import random


def _check_simple(ex: dict, label: str) -> None:
    ok, msg = ex["check"](ex["expected"])
    assert ok, f"{label}: expected answer rejected: {msg!r} q={ex['question'][:60]!r}"


def _walk_units(units: list, label: str) -> None:
    for ui, unit in enumerate(units):
        pre = f"{label} unit[{ui}]"
        kind = unit["kind"]
        if kind == "simple":
            _check_simple(unit, pre)
        elif kind == "compound":
            assert "parts" in unit and unit["parts"], pre
            for pi, part in enumerate(unit["parts"]):
                ok, msg = part["check"](part["expected"])
                assert ok, f"{pre} part[{pi}]: {msg!r}"
        else:
            raise AssertionError(f"{pre}: unknown kind {kind!r}")


def main() -> None:
    import batch_1_exercises as b1
    import batch_2_exercises as b2
    import batch_3_exercises as b3
    import batch_4_exercises as b4
    import batch_5_exercises as b5
    import batch_6_exercises as b6
    import batch_7_exercises as b7
    import batch_8_exercises as b8
    import batch_9_exercises as b9
    import batch_10_exercises as b10
    from main import PythonBasics

    # Entry wiring
    app = PythonBasics()
    assert app.batch_1 and app.batch_10

    # --- Batch 1: entire flat pool ---
    pool = b1._build_pool()
    assert len(pool) >= 12, "batch 1 pool too small for documented session"
    for i, ex in enumerate(pool):
        _check_simple(ex, f"b1 pool[{i}]")

    # --- Batches with stochastic sessions: many trials ---
    trials = 300
    random.seed(0)
    for t in range(trials):
        for i, ex in enumerate(b2._pick_batch2_session()):
            _check_simple(ex, f"b2 t{t}[{i}]")
        for i, ex in enumerate(b3._pick_batch3_session(12)):
            _check_simple(ex, f"b3 t{t}[{i}]")
        for i, ex in enumerate(b4._pick_batch4_session()):
            _check_simple(ex, f"b4 t{t}[{i}]")
        _walk_units(b5._pick_batch5_units(), f"b5 t{t}")
        for i, ex in enumerate(b6._pick_batch6_session()):
            _check_simple(ex, f"b6 t{t}[{i}]")
        for i, ex in enumerate(b7._pick_batch7_session()):
            _check_simple(ex, f"b7 t{t}[{i}]")
        _walk_units(b8._pick_batch8_units(), f"b8 t{t}")
        for i, ex in enumerate(b9._pick_batch9_session()):
            _check_simple(ex, f"b9 t{t}[{i}]")
        _walk_units(b10._pick_batch10_units(), f"b10 t{t}")

    # Session sizes (documented UX)
    assert len(b2._pick_batch2_session()) == 12
    assert len(b3._pick_batch3_session(12)) == 12
    assert len(b4._pick_batch4_session()) == 12
    assert len(b5._pick_batch5_units()) == b5.Batch5Exercises.EXERCISES_PER_SESSION_UNITS
    assert len(b6._pick_batch6_session()) == 12
    assert len(b7._pick_batch7_session()) == 12
    assert len(b8._pick_batch8_units()) == b8.Batch8Exercises.EXERCISES_PER_SESSION_UNITS
    assert len(b9._pick_batch9_session()) == 12
    assert len(b10._pick_batch10_units()) == b10.Batch10Exercises.EXERCISES_PER_SESSION_UNITS

    print(f"verify_project_smoke: OK ({trials} stochastic rounds + batch 1 full pool).")


if __name__ == "__main__":
    main()
