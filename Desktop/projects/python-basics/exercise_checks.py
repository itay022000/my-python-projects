"""
Shared exact-answer checking for python-basics batches.

Each batch uses a specific normalizer so grading matches the previous per-file
implementation byte-for-byte for spacing rules.

Public API:
  - normalize_code_* : normalization functions
  - checker_basic / checker_lists / checker_sets / checker_dicts / checker_functions
    : namespaces with .normalize, .make_exact_check, .make_exercise
  - checker_mixed_* : same plus .make_simple, .make_compound (batches 5, 8, 10)
  - make_multi_check, make_boolean_word_check (batch 2)
"""

import re
from types import SimpleNamespace


# ---------------------------------------------------------------------------
# Normalizers (preserve legacy batch behavior exactly)
# ---------------------------------------------------------------------------

def _tighten_operator_spacing(code: str) -> str:
    """Normalize spacing around symbolic operators across batches."""
    code = re.sub(r"\s*(==|!=|<=|>=|<<|>>|//|\*\*|:=|\+=|-=|\*=|/=|%=|//=|\*\*=|&=|\|=|\^=)\s*", r"\1", code)
    code = re.sub(r"\s*([<>%&|^~!])\s*", r"\1", code)
    return code


def normalize_code_basic(code: str) -> str:
    """Batches 1–3: original bracket punctuation pass without colon or comma in that class."""
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


def normalize_code_lists(code: str) -> str:
    """Batches 4, 5, 9: includes : and , in the punctuation bracket pass."""
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


def normalize_code_sets(code: str) -> str:
    """Batch 6: set literals, |= before |, attribute access, then list-style pass."""
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


def normalize_code_dicts(code: str) -> str:
    """Batches 7, 10: brace + dot tightening; no |= / | set-operator passes."""
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


def normalize_code_functions(code: str) -> str:
    """Batch 8: dot tightening only; no brace normalization."""
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


_WRONG_MSG = "That is not the expected answer. Only the exact required line is accepted."


def _make_exact_check_impl(expected_code: str, normalize):
    expected_normalized = normalize(expected_code)

    def check(user_code: str):
        user_normalized = normalize(user_code)
        if user_normalized == expected_normalized:
            return True, "Correct!"
        return False, _WRONG_MSG

    return check


def _make_exercise_impl(question: str, expected: str, normalize) -> dict:
    return {
        "question": question,
        "expected": expected,
        "check": _make_exact_check_impl(expected, normalize),
    }


def _make_simple_impl(question: str, expected: str, normalize) -> dict:
    return {
        "kind": "simple",
        "question": question,
        "expected": expected,
        "check": _make_exact_check_impl(expected, normalize),
    }


def _make_compound_impl(title: str, parts: list, normalize) -> dict:
    return {
        "kind": "compound",
        "title": title,
        "parts": [
            {"question": q, "expected": e, "check": _make_exact_check_impl(e, normalize)}
            for q, e in parts
        ],
    }


def _bundle(normalize):
    return SimpleNamespace(
        normalize=normalize,
        make_exact_check=lambda expected: _make_exact_check_impl(expected, normalize),
        make_exercise=lambda q, e: _make_exercise_impl(q, e, normalize),
    )


def _bundle_mixed(normalize):
    b = _bundle(normalize)
    return SimpleNamespace(
        normalize=b.normalize,
        make_exact_check=b.make_exact_check,
        make_exercise=b.make_exercise,
        make_simple=lambda q, e: _make_simple_impl(q, e, normalize),
        make_compound=lambda title, parts: _make_compound_impl(title, parts, normalize),
    )


checker_basic = _bundle(normalize_code_basic)
checker_lists = _bundle(normalize_code_lists)
checker_sets = _bundle(normalize_code_sets)
checker_dicts = _bundle(normalize_code_dicts)
checker_functions = _bundle(normalize_code_functions)

checker_mixed_lists = _bundle_mixed(normalize_code_lists)
checker_mixed_functions = _bundle_mixed(normalize_code_functions)
checker_mixed_dicts = _bundle_mixed(normalize_code_dicts)


def make_multi_check(expected_codes: list[str], normalize=normalize_code_basic) -> callable:
    """Batch 2: any of several expected lines after normalization."""
    normalized_set = {normalize(e) for e in expected_codes}

    def check(user_code: str):
        user_normalized = normalize(user_code)
        if user_normalized in normalized_set:
            return True, "Correct!"
        return False, _WRONG_MSG

    return check


def make_boolean_word_check(expected_word: str) -> callable:
    """Batch 2: True/False word answers (no code normalization)."""
    assert expected_word in ("True", "False")

    def check(user_input: str):
        answer = user_input.strip()
        if answer == expected_word:
            return True, "Correct!"
        return False, "Answer must be exactly the word True or the word False (capital T/F, no abbreviation)."

    return check
