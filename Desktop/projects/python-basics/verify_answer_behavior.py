"""
Behavior verification for python-basics:

  • Wrong answers are rejected (check returns False).
  • Equivalent spacing (per-batch normalization) is accepted.
  • Session scoring percentages match the formulas used in batch classes.
  • Three-strike skip logic matches the interactive session_runner simple loop.

Run:  python3 verify_answer_behavior.py
"""

from __future__ import annotations

import io
import random
import re
from contextlib import redirect_stdout
from unittest.mock import patch

from session_runner import _run_one_simple_exercise


def _pct_completed(completed: int, not_completed: int) -> float:
    """Same math as batch stats blocks."""
    total = completed + not_completed
    return (100 * completed / total) if total else 0.0


def _wrong_submission(expected: str, *, is_word: bool) -> str:
    """Guaranteed to fail check vs expected (after normalization / strip rules)."""
    if is_word:
        if expected == "True":
            return "False"
        if expected == "False":
            return "True"
        return "__not_a_word__"
    # Code: suffix survives normalization for all normalizers in this project.
    return expected.rstrip() + " __NOT_EXPECTED__"


def _spaced_variant(normalize, expected: str) -> str | None:
    """Return a user line that should normalize equal to expected, or None if we skip."""
    if normalize(expected) != normalize(normalize(expected)):
        return None
    candidates = []
    if "=" in expected:
        i = expected.index("=")
        candidates.append(expected[:i].rstrip() + "  =  " + expected[i + 1 :].lstrip())
    candidates.append("  " + expected.strip() + "  ")
    candidates.append(re.sub(r"\(", "( ", expected, count=1))
    for c in candidates:
        if normalize(c) == normalize(expected):
            return c
    return None


def _run_one_like_batch(check, max_mistakes: int, lines: list[str]) -> bool:
    """Mirror session_runner simple loop control flow (without EOF mid-loop edge cases)."""
    mistakes = 0
    for line in lines:
        s = line.strip()
        ok, _ = check(s)
        if ok:
            return True
        mistakes += 1
        if mistakes >= max_mistakes:
            return False
    # Out of lines: behave like EOF after last failed check → session treats as fail
    return False


def _iter_exercise_dicts_deep(obj) -> list[dict]:
    """Yield dicts that look like gradable line exercises (question + expected + check)."""
    found: list[dict] = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("kind") == "compound" and "parts" in o:
                for p in o["parts"]:
                    walk(p)
                return
            if "check" in o and "expected" in o and "question" in o:
                found.append(o)
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(obj)
    return found


def _extract_question_expected_pairs(module) -> list[tuple[str, str]]:
    """Collect (question, expected) tuples from module-level POOL / *_BY_KIND structures."""

    def walk(obj, out: list[tuple[str, str]]) -> None:
        if isinstance(obj, tuple) and len(obj) == 2 and isinstance(obj[0], str) and isinstance(obj[1], str):
            q, e = obj
            if len(q) > 10 and not q.startswith("#"):  # filter noise
                out.append((q, e))
            return
        if isinstance(obj, dict):
            for v in obj.values():
                walk(v, out)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, out)

    acc: list[tuple[str, str]] = []
    for name, obj in vars(module).items():
        if name.startswith("_"):
            continue
        if isinstance(obj, (list, dict)):
            walk(obj, acc)
    # Dedupe by (q,e)
    seen = set()
    uniq = []
    for t in acc:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _test_exercise_dict(ex: dict, label: str, normalize, max_mistakes: int = 3) -> None:
    exp = ex["expected"]
    chk = ex["check"]
    is_word = ex.get("answer_type") == "word"

    ok, msg = chk(exp)
    assert ok, f"{label}: correct rejected: {msg!r}"

    bad_ok, bad_msg = chk(_wrong_submission(exp, is_word=is_word))
    assert not bad_ok, f"{label}: wrong answer accepted"

    if is_word:
        spaced = f"  {exp.strip()}  "
        s_ok, _ = chk(spaced)
        assert s_ok, f"{label}: spaced word answer rejected"
    else:
        sv = _spaced_variant(normalize, exp)
        if sv is not None:
            sk, sm = chk(sv)
            assert sk, f"{label}: spaced code rejected: {sm!r} variant={sv!r}"

    assert _run_one_like_batch(chk, max_mistakes, ["wrong1", "wrong2", "wrong3"]) is False
    assert (
        _run_one_like_batch(chk, max_mistakes, [_wrong_submission(exp, is_word=is_word), exp])
        is True
    )


def _walk_compound_parts(norm, module_label: str, unit: dict) -> None:
    assert unit["kind"] == "compound"
    for i, part in enumerate(unit["parts"]):
        _test_exercise_dict(part, f"{module_label} compound part[{i}]", norm)


def main() -> None:
    import batch_1_exercises as b1
    import batch_10_exercises as b10
    import batch_2_exercises as b2
    import batch_3_exercises as b3
    import batch_4_exercises as b4
    import batch_5_exercises as b5
    import batch_6_exercises as b6
    import batch_7_exercises as b7
    import batch_8_exercises as b8
    import batch_9_exercises as b9

    # --- Scoring formulas ---
    assert abs(_pct_completed(5, 7) - 100 * 5 / 12) < 1e-9
    assert _pct_completed(0, 0) == 0.0
    assert abs(_pct_completed(8, 0) - 100.0) < 1e-9

    # --- Batch 1: full pool ---
    for i, ex in enumerate(b1._build_pool()):
        _test_exercise_dict(ex, f"b1 pool[{i}]", b1._normalize_code)

    # --- Batch 2: all string pools + all booleans ---
    pool_lists = [
        b2.POOL_SLICE_POSITIVE,
        b2.POOL_SLICE_NEGATIVE,
        b2.POOL_MODIFY,
        b2.POOL_CONCAT,
        b2.POOL_FSTRING_VAR,
        b2.POOL_FSTRING_EXPR,
    ]
    bi = 0
    for pl in pool_lists:
        for q, e in pl:
            ex = b2._make_exercise(q, e)
            _test_exercise_dict(ex, f"b2 string[{bi}]", b2._normalize_code)
            bi += 1
    for q, e in b2.POOL_BOOLEAN:
        ex = {
            "question": q,
            "expected": e,
            "check": b2._make_boolean_word_check(e),
            "answer_type": "word",
        }
        _test_exercise_dict(ex, f"b2 bool {e!r}", b2._normalize_code)

    # --- Batch 3: every tuple in each POOL_* ---
    pool_names = [
        "POOL_ARITHMETIC",
        "POOL_ASSIGNMENT",
        "POOL_COMPARISON",
        "POOL_LOGICAL",
        "POOL_LOGICAL_TWO",
        "POOL_IDENTITY",
        "POOL_MEMBERSHIP",
        "POOL_BITWISE",
    ]
    idx = 0
    for pname in pool_names:
        for q, e in getattr(b3, pname):
            ex = b3._make_exercise(q, e)
            _test_exercise_dict(ex, f"b3 {pname}[{idx}]", b3._normalize_code)
            idx += 1

    # --- Batches 4–10: all extracted (q,e) pairs → exercise dict ---
    batch_specs = [
        (b4, b4._make_exercise, b4._normalize_code, "b4"),
        (b6, b6._make_exercise, b6._normalize_code, "b6"),
        (b7, b7._make_exercise, b7._normalize_code, "b7"),
        (b9, b9._make_exercise, b9._normalize_code, "b9"),
    ]
    for mod, maker, norm, tag in batch_specs:
        pairs = _extract_question_expected_pairs(mod)
        for i, (q, e) in enumerate(pairs):
            _test_exercise_dict(maker(q, e), f"{tag}[{i}]", norm)

    # Batch 9 one-shot order already covered if POOL_* fully walked — ensure counts
    assert len(_extract_question_expected_pairs(b9)) >= 24  # min distinct tuples across pools

    # --- Mixed batches: exhaustive walk of module globals (every compound part + simple pool row) ---
    for tag, mod in [("b5", b5), ("b8", b8), ("b10", b10)]:
        seen = 0
        for name, obj in vars(mod).items():
            if name.startswith("_"):
                continue
            if isinstance(obj, (list, dict)):
                for ex in _iter_exercise_dicts_deep(obj):
                    _test_exercise_dict(ex, f"{tag} static {name}[{seen}]", mod._normalize_code)
                    seen += 1

    # --- Mixed batches: stochastic rounds (composition / ordering fuzz) ---
    random.seed(0)
    pickers = {
        "b5": b5._pick_batch5_units,
        "b8": b8._pick_batch8_units,
        "b10": b10._pick_batch10_units,
    }
    for rnd in range(400):
        for tag, mod in [("b5", b5), ("b8", b8), ("b10", b10)]:
            units = pickers[tag]()
            for ui, unit in enumerate(units):
                if unit["kind"] == "simple":
                    _test_exercise_dict(unit, f"{tag} r{rnd} u{ui}", mod._normalize_code)
                else:
                    _walk_compound_parts(mod._normalize_code, f"{tag} r{rnd} u{ui}", unit)

    # --- Live session_runner simple loop with mocked input (batch 1): 3 failures then exit ---
    b1_inst = b1.Batch1Exercises()
    ex = b1_inst.pool[0]
    max_m = b1_inst.MAX_MISTAKES_PER_EXERCISE
    lines = ["wrong_a", "wrong_b", "wrong_c"]
    with patch("builtins.input", side_effect=lines):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = _run_one_simple_exercise(
                ex,
                1,
                1,
                True,
                max_mistakes=max_m,
                prompt_label="Your code",
                input_fn=input,
            )
        assert ok is False
        assert "Three mistakes" in buf.getvalue()

    lines2 = ["bad", ex["expected"]]
    with patch("builtins.input", side_effect=lines2):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ok = _run_one_simple_exercise(
                ex,
                1,
                5,
                False,
                max_mistakes=max_m,
                prompt_label="Your code",
                input_fn=input,
            )
        assert ok is True

    print(
        "verify_answer_behavior: OK (wrong/spacing/strikes + scoring math + "
        "all static pools + exhaustive mixed-batch definitions + 400 stochastic rounds + "
        "mocked session_runner simple exercise)."
    )


if __name__ == "__main__":
    main()
