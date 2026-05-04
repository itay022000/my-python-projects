"""
Batch 7: Topic 11 (Dictionaries).
Single-line code exercises; 12 questions per session (see _pick_batch7_session).
Only the exact expected answer is accepted for each exercise.

Rules for all questions (apply to new questions unless stated otherwise):
  - Space normalization is applied to every question's answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_dicts
from session_runner import print_session_footer, print_session_header, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_dicts.normalize
_make_exact_check = checker_dicts.make_exact_check
_make_exercise = checker_dicts.make_exercise


# ---------------------------------------------------------------------------
# 1–2: access vs get (pick 1)
# ---------------------------------------------------------------------------
POOL_1_ACCESS_ITEM = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in value the value mapped to \"name\".", "value = d[\"name\"]"),
    ("Suppose d = {\"city\": \"Rome\", \"year\": 2020}. Store in ans the value mapped to \"city\".", "ans = d[\"city\"]"),
]

POOL_2_ACCESS_GET = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in value the value mapped to \"name\" using the safe access form.", "value = d.get(\"name\")"),
    ("Suppose d = {\"city\": \"Rome\", \"year\": 2020}. Store in ans the value mapped to \"city\" using the safe access form.", "ans = d.get(\"city\")"),
]


# ---------------------------------------------------------------------------
# 3–5: all selected every session (one variant per type)
# ---------------------------------------------------------------------------
POOL_3_KEYS = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in ks a dynamic view of all keys in d.", "ks = d.keys()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Store in names a dynamic view of all keys in d.", "names = d.keys()"),
]

POOL_4_VALUES = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in vals a dynamic view of all values in d.", "vals = d.values()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Store in nums a dynamic view of all values in d.", "nums = d.values()"),
]

POOL_5_ITEMS = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in pairs a dynamic view of key-value pairs in d.", "pairs = d.items()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Store in kv a dynamic view of key-value pairs in d.", "kv = d.items()"),
]


# ---------------------------------------------------------------------------
# 6–7: direct change vs update change (pick 1)
# ---------------------------------------------------------------------------
POOL_6_CHANGE_DIRECT = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Change the value mapped to \"age\" so it becomes 21.", "d[\"age\"] = 21"),
    ("Suppose d = {\"score\": 7, \"level\": 1}. Change the value mapped to \"score\" so it becomes 8.", "d[\"score\"] = 8"),
]

POOL_7_CHANGE_UPDATE = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Change the value mapped to \"age\" so it becomes 21 using one dictionary merge-style call.", "d.update({\"age\": 21})"),
    ("Suppose d = {\"score\": 7, \"level\": 1}. Change the value mapped to \"score\" so it becomes 8 using one dictionary merge-style call.", "d.update({\"score\": 8})"),
]


# ---------------------------------------------------------------------------
# 8–9: direct add vs update add (pick 1)
# ---------------------------------------------------------------------------
POOL_8_ADD_DIRECT = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Add the new mapping from \"city\" to \"Paris\".", "d[\"city\"] = \"Paris\""),
    ("Suppose d = {\"x\": 1}. Add the new mapping from \"y\" to 2.", "d[\"y\"] = 2"),
]

POOL_9_ADD_UPDATE = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Add the new mapping from \"city\" to \"Paris\" using one dictionary merge-style call.", "d.update({\"city\": \"Paris\"})"),
    ("Suppose d = {\"x\": 1}. Add the new mapping from \"y\" to 2 using one dictionary merge-style call.", "d.update({\"y\": 2})"),
]


# ---------------------------------------------------------------------------
# 10–15: all selected every session (one variant per type)
# ---------------------------------------------------------------------------
POOL_10_REMOVE_ITEM = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Remove the mapping whose key is \"age\".", "d.pop(\"age\")"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Remove the mapping whose key is \"x\".", "d.pop(\"x\")"),
]

POOL_11_REMOVE_LAST = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Remove and return the last inserted key-value pair.", "d.popitem()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Remove and return the last inserted key-value pair.", "d.popitem()"),
]

POOL_12_CLEAR = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Empty d in place.", "d.clear()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Empty d in place.", "d.clear()"),
]

POOL_13_DELETE = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Delete the name d so the dictionary is no longer referenced.", "del d"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Delete the name d so the dictionary is no longer referenced.", "del d"),
]

POOL_14_COPY_COPY = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in d2 a shallow copy of d using the instance copy operation.", "d2 = d.copy()"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Store in clone a shallow copy of d using the instance copy operation.", "clone = d.copy()"),
]

POOL_15_COPY_DICT = [
    ("Suppose d = {\"name\": \"Ada\", \"age\": 20}. Store in d2 a shallow copy of d using the constructor form.", "d2 = dict(d)"),
    ("Suppose d = {\"x\": 1, \"y\": 2}. Store in clone a shallow copy of d using the constructor form.", "clone = dict(d)"),
]


def _pick_batch7_session():
    """
    12 exercises per session:
      1 of 2: access item / access item with get
      all 3: keys, values, items
      1 of 2: change value direct / change value via update
      1 of 2: add item direct / add item via update
      all 6: remove item, remove last, clear, delete, copy(copy), copy(dict)
    """
    exercises = []

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_1_ACCESS_ITEM)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_2_ACCESS_GET)))

    exercises.append(_make_exercise(*random.choice(POOL_3_KEYS)))
    exercises.append(_make_exercise(*random.choice(POOL_4_VALUES)))
    exercises.append(_make_exercise(*random.choice(POOL_5_ITEMS)))

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_6_CHANGE_DIRECT)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_7_CHANGE_UPDATE)))

    if random.choice([True, False]):
        exercises.append(_make_exercise(*random.choice(POOL_8_ADD_DIRECT)))
    else:
        exercises.append(_make_exercise(*random.choice(POOL_9_ADD_UPDATE)))

    exercises.append(_make_exercise(*random.choice(POOL_10_REMOVE_ITEM)))
    exercises.append(_make_exercise(*random.choice(POOL_11_REMOVE_LAST)))
    exercises.append(_make_exercise(*random.choice(POOL_12_CLEAR)))
    exercises.append(_make_exercise(*random.choice(POOL_13_DELETE)))
    exercises.append(_make_exercise(*random.choice(POOL_14_COPY_COPY)))
    exercises.append(_make_exercise(*random.choice(POOL_15_COPY_DICT)))

    return exercises


class Batch7Exercises:
    """
    Batch 7: Topic 11 (Dictionaries). 12 questions per session.
    """

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        """Start the dictionaries exercises sequence."""
        print_session_header("PYTHON BASICS - DICTIONARIES EXERCISES")
        print("\nYou will get 12 single-line code questions on dictionaries.")
        print("Which topics appear can change from one session to the next.")
        print("Type one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        exercises = _pick_batch7_session()
        completed, not_completed = run_simple_exercises(
            exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)