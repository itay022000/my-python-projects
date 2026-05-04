"""
Batch 6: Topic 10 (Sets).
Single-line code exercises; 12 questions per session (see _pick_batch6_session).
Only the exact expected answer is accepted for each exercise.

Rules for all questions (apply to new questions unless stated otherwise):
  - Space normalization is applied to every question's answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_sets
from session_runner import print_session_footer, print_session_header, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_sets.normalize
_make_exact_check = checker_sets.make_exact_check
_make_exercise = checker_sets.make_exercise


# ---------------------------------------------------------------------------
# 1–2: membership (pick 1)
# ---------------------------------------------------------------------------
POOL_IN = [
    ("Suppose s = {1, 2, 3}. Store in ok whether the value 2 appears in s.", "ok = 2 in s"),
    ("Suppose s = {10, 20}. Store in found whether 10 appears in s.", "found = 10 in s"),
]

POOL_NOT_IN = [
    ("Suppose s = {1, 2, 3}. Store in missing whether 9 does not appear in s.", "missing = 9 not in s"),
    ("Suppose s = {\"a\", \"b\"}. Store in missing whether \"z\" does not appear in s.", "missing = \"z\" not in s"),
]

# ---------------------------------------------------------------------------
# 3–4: add item vs add set into set (pick 1)
# ---------------------------------------------------------------------------
POOL_ADD_ITEM = [
    ("Suppose s = {1, 2}. Add the single value 3 to s in place.", "s.add(3)"),
    ("Suppose s = {0}. Add the single value 1 to s in place.", "s.add(1)"),
]

POOL_ADD_SET = [
    ("Suppose s = {1, 2} and t = {2, 3}. Update s in place with every element from t.", "s.update(t)"),
    (
        "Suppose s = {1} and t = {2} and u = {3}. Update s in place with every element from t and from u, in one call.",
        "s.update(t, u)",
    ),
]

# ---------------------------------------------------------------------------
# 5–6: remove vs pop (pick 1)
# ---------------------------------------------------------------------------
POOL_REMOVE = [
    ("Suppose s = {1, 2, 3}. Remove the value 2 from s in place (it is present).", "s.remove(2)"),
    ("Suppose s = {9, 8}. Remove the value 9 from s in place (it is present).", "s.remove(9)"),
]

POOL_POP = [
    ("Suppose s = {1, 2, 3}. Remove and return one arbitrary element; store it in x.", "x = s.pop()"),
    ("Suppose s = {7, 8}. Remove and return one arbitrary element; store it in y.", "y = s.pop()"),
]

# ---------------------------------------------------------------------------
# 7–8: clear vs delete the set name (pick 1)
# ---------------------------------------------------------------------------
POOL_CLEAR = [
    ("Suppose s = {1, 2, 3}. Empty the set s in place.", "s.clear()"),
    ("Suppose t = {4, 5}. Empty the set t in place.", "t.clear()"),
]

POOL_DELETE = [
    ("Suppose s = {1, 2, 3}. Delete the name s so the set is no longer referenced.", "del s"),
    ("Suppose t = {0, 1}. Delete the name t so the set is no longer referenced.", "del t"),
]

# ---------------------------------------------------------------------------
# Pairs (9,10), (11,12), (13,14), (15,16) — pick 3 pairs; each pair in order
# ---------------------------------------------------------------------------
PAIR_UNION = [
    _make_exercise(
        "Suppose a = {1, 2} and b = {2, 3}. Store in u a new set that contains every element from a or b.",
        "u = a.union(b)",
    ),
    _make_exercise(
        "Suppose a = {1, 2} and b = {2, 3}. Update a in place so it contains every element from a or b.",
        "a.update(b)",
    ),
]

PAIR_INTERSECTION = [
    _make_exercise(
        "Suppose a = {1, 2, 3} and b = {2, 3, 4}. Store in inter a new set of elements common to a and b.",
        "inter = a.intersection(b)",
    ),
    _make_exercise(
        "Suppose a = {1, 2, 3} and b = {2, 3, 4}. Update a in place so it keeps only elements common to a and b.",
        "a.intersection_update(b)",
    ),
]

PAIR_DIFFERENCE = [
    _make_exercise(
        "Suppose a = {1, 2, 3} and b = {2}. Store in d a new set of elements of a that are not in b.",
        "d = a.difference(b)",
    ),
    _make_exercise(
        "Suppose a = {1, 2, 3} and b = {2}. Update a in place so it drops every element that appears in b.",
        "a.difference_update(b)",
    ),
]

PAIR_SYMMETRIC = [
    _make_exercise(
        "Suppose a = {1, 2} and b = {2, 3}. Store in sd a new set of elements in exactly one of a or b.",
        "sd = a.symmetric_difference(b)",
    ),
    _make_exercise(
        "Suppose a = {1, 2} and b = {2, 3}. Update a in place with the symmetric change given by b.",
        "a.symmetric_difference_update(b)",
    ),
]

OPERATION_PAIRS = [PAIR_UNION, PAIR_INTERSECTION, PAIR_DIFFERENCE, PAIR_SYMMETRIC]

# ---------------------------------------------------------------------------
# 17–18: both each session
# ---------------------------------------------------------------------------
POOL_UNION_MANY = [
    (
        "Suppose a = {1}, b = {2}, and c = {3}. Store in u a new set that is the union of a, b, and c.",
        "u = a.union(b, c)",
    ),
    (
        "Suppose a = {0, 1}, b = {1, 2}, and c = {2, 3}. Store in u a new set that is the union of a, b, and c (using the three-argument form).",
        "u = set.union(a, b, c)",
    ),
]

POOL_FROZEN = [
    ("Suppose s = {1, 2, 3}. Store an immutable set built from s in f.", "f = frozenset(s)"),
    ("Suppose s = {0, 1}. Store an immutable set built from the list [0, 1] in f.", "f = frozenset([0, 1])"),
]


def _pick_batch6_session():
    """
    12 exercises per session:
      1 of 2: membership in / not in
      1 of 2: add item / update with another set
      1 of 2: remove / pop
      1 of 2: clear / del name
      3 of 4 operation pairs (union, intersection, difference, symmetric); each pair in fixed order
      both: union of three sets, frozenset
    """
    exercises = []

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_IN)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_NOT_IN)))

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_ADD_ITEM)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_ADD_SET)))

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_REMOVE)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_POP)))

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_CLEAR)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_DELETE)))

    chosen_pair_indices = random.sample(range(4), 3)
    for idx in chosen_pair_indices:
        pair = OPERATION_PAIRS[idx]
        exercises.append(pair[0])
        exercises.append(pair[1])

    exercises.append(_make_exercise(*random.choice(POOL_UNION_MANY)))
    exercises.append(_make_exercise(*random.choice(POOL_FROZEN)))

    return exercises


class Batch6Exercises:
    """
    Batch 6: Topic 10 (Sets). 12 questions per session.
    """

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        """Start the sets exercises sequence."""
        print_session_header("PYTHON BASICS - SETS EXERCISES")
        print("\nYou will get 12 single-line code questions on sets.")
        print("Which topics appear can change from one session to the next.")
        print("Type one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        exercises = _pick_batch6_session()
        completed, not_completed = run_simple_exercises(
            exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)
