"""Shared code-answer validation utilities for puzzle-rush-game.

Used only for coding challenges. True/false responses use
``game_common.normalize_true_false_answer`` instead.
"""

from __future__ import annotations

# Matrix transpose coding challenges accept only these two spellings (after whitespace normalize).
_MATRIX_TRANSPOSE_FORMS = frozenset({"matrix.T", "np.transpose(matrix)"})

# Vector Battle short-keyword answers: lowercase stored; also accept listed capitalizations only.
_VECTOR_SHORT_KEYWORDS = {
    "none": frozenset({"none", "None"}),
    "array": frozenset({"array", "Array"}),
    "permutation": frozenset({"permutation", "Permutation"}),
    "shuffle": frozenset({"shuffle", "Shuffle"}),
}


def _vector_short_keyword_match(user: str, correct: str) -> bool:
    forms = _VECTOR_SHORT_KEYWORDS.get(correct)
    return forms is not None and user in forms


def normalize_code(code: str) -> str:
    """
    Collapse whitespace for comparison.

    Identifier casing is preserved: NumPy/Python names are case-sensitive
    (e.g. ``ndim`` vs ``NDIM``, ``.T`` vs ``.t``).
    """
    return "".join(code.split())


def _normalize_choice_replace_true(expr: str) -> str:
    """
    Canonicalize np.random.choice(..., size=k) and replace=True variants.

    For choice calls that include size but omit replace, NumPy defaults to replace=True.
    Keyword detection is case-insensitive only for the ``replace=`` / ``size=`` tokens.
    """
    el = expr.lower()
    if not el.startswith("np.random.choice(") or not expr.endswith(")"):
        return expr

    inner = expr[len("np.random.choice(") : -1]
    inner_l = inner.lower()
    if "size=" not in inner_l:
        return expr

    if "replace=false" in inner_l:
        return expr
    if "replace=true" in inner_l:
        return expr

    return f"np.random.choice({inner},replace=true)"


def validate_code_answer(user_input: str, correct_answer: str, profile: str = "default") -> bool:
    """
    Validate a user code answer against expected answer with per-game profiles.

    Profiles:
      - default: whitespace-collapsed exact comparison (case-sensitive).
      - vector: short keywords none/array/permutation/shuffle accept ``None``/``Array``/etc.;
        choice replace= equivalence (kwarg casing ignored).
      - matrix: tuple-shape whitespace rules; transpose challenges accept only
        ``matrix.T`` or ``np.transpose(matrix)`` (mutually interchangeable).
    """
    user_normalized = normalize_code(user_input)
    correct_normalized = normalize_code(correct_answer)

    if profile == "vector":
        user_normalized = _normalize_choice_replace_true(user_normalized)
        correct_normalized = _normalize_choice_replace_true(correct_normalized)

        if correct_normalized in {"permutation", "shuffle", "none", "array"}:
            if _vector_short_keyword_match(user_normalized, correct_normalized):
                return True
            if correct_normalized in {"permutation", "shuffle"}:
                if (
                    user_normalized == f"np.random.{correct_normalized}"
                    or user_normalized.endswith(f".{correct_normalized}")
                ):
                    return True
            return False

    if profile == "matrix":
        if correct_normalized.startswith("(") and correct_normalized.endswith(")"):
            correct_clean = correct_normalized.strip("()").replace(" ", "")
            user_clean = user_normalized.strip("()").replace(" ", "")
            return user_clean == correct_clean

        # Transpose coding challenges: only matrix.T and np.transpose(matrix) are valid.
        if correct_normalized in _MATRIX_TRANSPOSE_FORMS and user_normalized in _MATRIX_TRANSPOSE_FORMS:
            return True

    return user_normalized == correct_normalized
