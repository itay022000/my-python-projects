"""
Parity check: exercise_checks normalizers must match the legacy per-batch
implementations (independent reimplementation for comparison). Run:

  python3 verify_exercise_checks_parity.py
"""

import random
import re
import string

# ---------------------------------------------------------------------------
# Reference normalizers (legacy behavior, copied from pre–shared-module batches)
# ---------------------------------------------------------------------------

def _tighten_operator_spacing(code: str) -> str:
    code = re.sub(r"\s*(==|!=|<=|>=|<<|>>|//|\*\*|:=|\+=|-=|\*=|/=|%=|//=|\*\*=|&=|\|=|\^=)\s*", r"\1", code)
    code = re.sub(r"\s*([<>%&|^~!])\s*", r"\1", code)
    return code


def ref_basic(code: str) -> str:
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = _tighten_operator_spacing(code)
    code = re.sub(r"\s*([=\[\]\(\)])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def ref_lists(code: str) -> str:
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = _tighten_operator_spacing(code)
    code = re.sub(r"\s*([=\[\]\(\):,])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def ref_sets(code: str) -> str:
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = _tighten_operator_spacing(code)
    code = re.sub(r"\{\s+", "{", code)
    code = re.sub(r"\s+\}", "}", code)
    code = re.sub(r"\s*\|\s*=\s*", "|=", code)
    code = re.sub(r"\s*\|\s*", "|", code)
    code = re.sub(r"\s*\.\s*", ".", code)
    code = re.sub(r"\s*([=\[\]\(\):,])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def ref_dicts(code: str) -> str:
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = _tighten_operator_spacing(code)
    code = re.sub(r"\{\s+", "{", code)
    code = re.sub(r"\s+\}", "}", code)
    code = re.sub(r"\s*\.\s*", ".", code)
    code = re.sub(r"\s*([=\[\]\(\):,])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def ref_functions(code: str) -> str:
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = _tighten_operator_spacing(code)
    code = re.sub(r"\s*\.\s*", ".", code)
    code = re.sub(r"\s*([=\[\]\(\):,])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def _rand_code(rng: random.Random, maxlen: int = 48) -> str:
    n = rng.randint(0, maxlen)
    alphabet = string.printable[:95]
    return "".join(rng.choice(alphabet) for _ in range(n))


def main() -> None:
    from exercise_checks import (
        normalize_code_basic,
        normalize_code_dicts,
        normalize_code_functions,
        normalize_code_lists,
        normalize_code_sets,
    )

    pairs = [
        (ref_basic, normalize_code_basic),
        (ref_lists, normalize_code_lists),
        (ref_sets, normalize_code_sets),
        (ref_dicts, normalize_code_dicts),
        (ref_functions, normalize_code_functions),
    ]

    rng = random.Random(0)
    for name_i, (ref, new) in enumerate(pairs):
        for _ in range(5000):
            s = _rand_code(rng)
            if ref(s) != new(s):
                raise SystemExit(
                    f"MISMATCH profile={name_i} input={s!r}\n ref={ref(s)!r}\n new={new(s)!r}"
                )

    # Batch wiring: each batch's _normalize_code must match the module function
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

    for mod in (b1, b2, b3):
        for s in ["x  =  1", "a  +  b", "f  (  x  )"]:
            assert mod._normalize_code(s) == normalize_code_basic(s)

    for mod in (b4, b5, b9):
        for s in ["lst  [  0  ]  =  1", "print  (  1  ,  2  )"]:
            assert mod._normalize_code(s) == normalize_code_lists(s)

    for s in ["{  1  ,  2  }", "s  |  =  t"]:
        assert b6._normalize_code(s) == normalize_code_sets(s)

    for mod in (b7, b10):
        for s in ['d  [  "a"  ]  =  1', "{  1  :  2  }"]:
            assert mod._normalize_code(s) == normalize_code_dicts(s)

    for s in ["def  f  (  )  :  pass", "x  .  y  (  )"]:
        assert b8._normalize_code(s) == normalize_code_functions(s)

    # Exact-check smoke: expected line always passes its checker
    ok, msg = b1._make_exact_check('print("Hello")')('print(  "Hello"  )')
    assert ok and msg == "Correct!"

    print("verify_exercise_checks_parity: all checks passed.")


if __name__ == "__main__":
    main()
