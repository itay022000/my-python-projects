"""
Batch 5: Topic 9 (Tuples).
Mixed session: 12 single lines across 8 questions (equal weight 12.5% each; session intro states this for the user).
  - 2 of 4 kinds: access, slice, negative index, negative slice
  - 4 fixed questions: unpack, unpack with *, join, multiply
  - 2 of 3 kinds: change item, add item, remove item — each kind is 3 consecutive one-line steps

Only the exact expected answer is accepted for each line. Same normalization and attempt rules as other batches.
Rules for all questions (apply to new questions unless stated otherwise):
  - Space normalization is applied to every answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_mixed_lists
from session_runner import print_session_footer, print_session_header, run_mixed_units_session

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_mixed_lists.normalize
_make_exact_check = checker_mixed_lists.make_exact_check
_make_simple = checker_mixed_lists.make_simple
_make_compound = checker_mixed_lists.make_compound


# ---------------------------------------------------------------------------
# Access (questions 1–4 theme): pick 2 of 4 kinds per session
# ---------------------------------------------------------------------------
ACCESS_BY_KIND = {
    "access": [
        ("Suppose t = (7, 8, 9). Store the value at index 0 in a variable named x.", "x = t[0]"),
        ("Suppose t = (4, 5, 6). Store the value at index 2 in a variable named x.", "x = t[2]"),
    ],
    "access_range": [
        (
            "Suppose t = (10, 20, 30, 40). Store in s the part that starts at index 1 and stops before index 3.",
            "s = t[1:3]",
        ),
        (
            "Suppose t = (1, 2, 3, 4, 5). Store in s the part that starts at index 0 and stops before index 4.",
            "s = t[0:4]",
        ),
    ],
    "negative": [
        ("Suppose t = (1, 2, 3). Store the final element in a variable named u.", "u = t[-1]"),
        ("Suppose t = (9, 8, 7). Store the second-from-last element in a variable named u.", "u = t[-2]"),
    ],
    "negative_range": [
        (
            "Suppose t = (1, 2, 3, 4, 5). Store in seg the slice from index -3 up to but not including index -1.",
            "seg = t[-3:-1]",
        ),
        (
            "Suppose t = (10, 20, 30, 40). Store in seg the slice from index -4 up to but not including index -1.",
            "seg = t[-4:-1]",
        ),
    ],
}

# ---------------------------------------------------------------------------
# Questions 8–11 (fixed order): unpack, unpack *, join, multiply
# ---------------------------------------------------------------------------
POOL_UNPACK = [
    ("Suppose t = (1, 2). Store the two elements in variables a and b (one statement).", "a, b = t"),
    ("Suppose t = (10, 20). Store the two elements in variables x and y (one statement).", "x, y = t"),
]

POOL_UNPACK_STAR = [
    ("Suppose t = (1, 2, 3, 4). Store in a the first, in b the last, and capture the middle with a starred name mid.", "a, *mid, b = t"),
    ("Suppose t = (0, 1, 2, 3). Store in first the first element, in rest everything after the first using a starred name.", "first, *rest = t"),
]

POOL_JOIN = [
    ("Suppose a = (1, 2) and b = (3, 4). Store in out a new tuple that is a followed by b.", "out = a + b"),
    ("Suppose a = (0,) and b = (1, 2). Store in out a new tuple that is a followed by b.", "out = a + b"),
]

POOL_MULTIPLY = [
    ("Suppose t = (1, 2). Store in r a tuple that repeats t three times in a row.", "r = t * 3"),
    ("Suppose t = (0,). Store in r a tuple that repeats t four times in a row.", "r = t * 4"),
]

# ---------------------------------------------------------------------------
# Questions 5–7 theme: 3-line patterns; pick 2 of 3 kinds per session
# ---------------------------------------------------------------------------
CHANGE_VARIANTS = [
    _make_compound(
        "Change one item inside a tuple (3 steps, in order)",
        [
            ("Suppose t = (1, 2, 3). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: replace the element at index 1 of lst with 99.", "lst[1] = 99"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
    _make_compound(
        "Change one item inside a tuple (3 steps, in order)",
        [
            ("Suppose t = (10, 20, 30). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: replace the element at index 0 of lst with 0.", "lst[0] = 0"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
]

ADD_VARIANTS = [
    _make_compound(
        "Add an item by going through a list (3 steps, in order)",
        [
            ("Suppose t = (1, 2). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: append the integer 3 to lst.", "lst.append(3)"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
    _make_compound(
        "Add an item by going through a list (3 steps, in order)",
        [
            ("Suppose t = (0,). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: append the integer 1 to lst.", "lst.append(1)"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
]

REMOVE_VARIANTS = [
    _make_compound(
        "Remove an item by going through a list (3 steps, in order)",
        [
            ("Suppose t = (1, 2, 3, 2). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: remove the first occurrence of the value 2 from lst.", "lst.remove(2)"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
    _make_compound(
        "Remove an item by going through a list (3 steps, in order)",
        [
            ("Suppose t = (9, 8, 9). Step 1: store a list copy of t in lst.", "lst = list(t)"),
            ("Step 2: remove the first occurrence of the value 9 from lst.", "lst.remove(9)"),
            ("Step 3: assign to t a tuple built from lst.", "t = tuple(lst)"),
        ],
    ),
]

COMPOUND_BY_KIND = {
    "change": CHANGE_VARIANTS,
    "add": ADD_VARIANTS,
    "remove": REMOVE_VARIANTS,
}


def _pick_batch5_units():
    """
    Build 8 scored units in session order:
      1–2: two random access kinds (simple each)
      3–4: two random compound kinds (3 lines each: change / add / remove)
      5–8: unpack, unpack*, join, multiply (simple each)
    """
    units = []

    access_kinds = random.sample(list(ACCESS_BY_KIND.keys()), 2)
    for k in access_kinds:
        q, e = random.choice(ACCESS_BY_KIND[k])
        units.append(_make_simple(q, e))

    compound_kinds = random.sample(list(COMPOUND_BY_KIND.keys()), 2)
    for k in compound_kinds:
        units.append(random.choice(COMPOUND_BY_KIND[k]))

    units.append(_make_simple(*random.choice(POOL_UNPACK)))
    units.append(_make_simple(*random.choice(POOL_UNPACK_STAR)))
    units.append(_make_simple(*random.choice(POOL_JOIN)))
    units.append(_make_simple(*random.choice(POOL_MULTIPLY)))

    return units


class Batch5Exercises:
    """
    Batch 5: Topic 9 (Tuples). 8 questions per session; 12 lines of code total.
    """

    EXERCISES_PER_SESSION_UNITS = 8
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        """Start the tuples exercises sequence."""
        print_session_header("PYTHON BASICS - TUPLES EXERCISES")
        print("\nYou will get 8 questions. Each counts the same toward your session score (12.5% per question).")
        print("Two questions ask for three lines of code each; the other six ask for one line each.")
        print("Type one line when prompted. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        units = _pick_batch5_units()
        units_passed, units_failed = run_mixed_units_session(
            units,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(units_passed, units_failed)
