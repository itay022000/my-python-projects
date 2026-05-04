"""
Batch 2: Topics 5–6 (Strings, Booleans).
Single-line code exercises; 7 strings (one random per slot from pools) + 5 booleans = 12 per session.
Only the exact expected answer is accepted for each exercise.

Rules for all questions (apply to new questions and question types unless stated otherwise):
  - Space normalization is applied to every question's answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_basic, make_boolean_word_check
from session_runner import print_session_footer, print_session_header, prompt_label_batch2, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_basic.normalize
_make_exact_check = checker_basic.make_exact_check
_make_exercise = checker_basic.make_exercise
_make_boolean_word_check = make_boolean_word_check


# ---------------------------------------------------------------------------
# String exercise pools: one question randomly chosen per slot per session
# ---------------------------------------------------------------------------

# Slot 1: Slicing [x:y], [x:], or [:y] — string in variable s or t
POOL_SLICE_POSITIVE = [
    ("Suppose s = \"python\". Assign the slice of s from index 1 to 4 (4 exclusive) to a variable named sub.", "sub = s[1:4]"),
    ("Suppose t = \"hello\". Assign the slice of t from index 2 to the end to a variable named tail.", "tail = t[2:]"),
    ("Suppose s = \"python\". Assign the slice of s from the start up to index 3 (3 exclusive) to a variable named sub.", "sub = s[:3]"),
]

# Slot 2: Slicing [-x:-y], [-x:], or [:-y]
POOL_SLICE_NEGATIVE = [
    ("Suppose t = \"hello\". Assign the slice of t from index -3 to -1 (-1 exclusive) to a variable named mid.", "mid = t[-3:-1]"),
    ("Suppose t = \"hello\". Assign the slice of t from index -3 to the end to a variable named tail.", "tail = t[-3:]"),
    ("Suppose s = \"python\". Assign the slice of s from the start up to index -2 (-2 exclusive) to a variable named sub.", "sub = s[:-2]"),
]

# Slots 3+4: Modifying — string in variable s, w, raw, csv, etc.
POOL_MODIFY = [
    ("Suppose s = \"hello\". Assign the uppercase version of s to a variable named upper_s.", "upper_s = s.upper()"),
    ("Suppose w = \"WORLD\". Assign the lowercase version of w to a variable named lower_s.", "lower_s = w.lower()"),
    ("Suppose raw = \"  hi  \". Assign raw with leading and trailing spaces removed to a variable named t.", "t = raw.strip()"),
    ("Suppose s = \"hello\". Assign to a variable named result the string s with every \"l\" replaced by \"L\".", "result = s.replace(\"l\", \"L\")"),
    ("Suppose csv = \"a,b,c\". Assign csv split by comma to a variable named parts.", "parts = csv.split(\",\")"),
]

# Slot 5: Concatenation — two strings in variables a and b
POOL_CONCAT = [
    ("Suppose a = \"Hello\" and b = \" world\". Assign the concatenation of a and b to a variable named greeting.", "greeting = a + b"),
    ("Suppose prefix = \"Score: \" and val = \"100\". Assign the concatenation of prefix and val to a variable named msg.", "msg = prefix + val"),
    ("Suppose x = \"x\" and y = \" = 5\". Assign the concatenation of x and y to a variable named s.", "s = x + y"),
    ("Suppose a = \"A\" and b = \"B\". Assign the concatenation of a and b to a variable named ab.", "ab = a + b"),
]

# Slot 6: F-string with variable — prefix in variable where needed for aesthetics
POOL_FSTRING_VAR = [
    ("Given that the variable name holds \"Alice\", assign to a variable named out the f-string that contains \"Hello, \" followed by the value of name.", "out = f\"Hello, {name}\""),
    ("Given that the variable score holds 42, assign to a variable named msg the f-string that contains \"Score: \" followed by the value of score.", "msg = f\"Score: {score}\""),
    ("Given that the variable x holds 10, assign to a variable named text the f-string that contains \"x = \" followed by the value of x.", "text = f\"x = {x}\""),
]

# Slot 7: F-string with expression — label string in variable
POOL_FSTRING_EXPR = [
    ("Assign to a variable named result the f-string that contains \"Sum: \" followed by the result of 10 + 20.", "result = f\"Sum: {10 + 20}\""),
    ("Assign to a variable named result the f-string that contains \"Diff: \" followed by the result of 20 - 5.", "result = f\"Diff: {20 - 5}\""),
    ("Assign to a variable named result the f-string that contains \"Product: \" followed by the result of 3 * 4.", "result = f\"Product: {3 * 4}\""),
    ("Assign to a variable named result the f-string that contains \"Quotient: \" followed by the result of 20 / 4.", "result = f\"Quotient: {20 / 4}\""),
]


def _pick_string_exercises():
    """Build the 7 string exercises for this session: one random choice per slot."""
    exercises = []
    exercises.append(_make_exercise(*random.choice(POOL_SLICE_POSITIVE)))
    exercises.append(_make_exercise(*random.choice(POOL_SLICE_NEGATIVE)))
    two_modify = random.sample(POOL_MODIFY, 2)
    exercises.append(_make_exercise(*two_modify[0]))
    exercises.append(_make_exercise(*two_modify[1]))
    exercises.append(_make_exercise(*random.choice(POOL_CONCAT)))
    exercises.append(_make_exercise(*random.choice(POOL_FSTRING_VAR)))
    exercises.append(_make_exercise(*random.choice(POOL_FSTRING_EXPR)))
    return exercises


# Boolean evaluation pool: (question, "True" or "False"). 5 chosen at random per session.
# Categories: 1=0, 2=non-zero int, 3=non-zero float, 4=non-zero complex, 5=(x<y), 6=(x>y), 7=(x==y), 8=empty string, 9=non-empty string, 10=None
POOL_BOOLEAN = [
    # 1. The number 0 (False)
    ("What is the truth value of 0? Answer with one word: True or False.", "False"),
    # 2. Non-zero integer (True)
    ("What is the truth value of 1? Answer with one word: True or False.", "True"),
    ("What is the truth value of 42? Answer with one word: True or False.", "True"),
    ("What is the truth value of -7? Answer with one word: True or False.", "True"),
    # 3. Non-zero float (True)
    ("What is the truth value of 1.0? Answer with one word: True or False.", "True"),
    ("What is the truth value of 3.14? Answer with one word: True or False.", "True"),
    ("What is the truth value of -0.5? Answer with one word: True or False.", "True"),
    # 4. Non-zero complex (True)
    ("What is the truth value of 1+0j? Answer with one word: True or False.", "True"),
    ("What is the truth value of 2j? Answer with one word: True or False.", "True"),
    # 5. (x < y)
    ("What is the result of (3 < 5)? Answer with one word: True or False.", "True"),
    ("What is the result of (5 < 3)? Answer with one word: True or False.", "False"),
    ("What is the result of (2 < 2)? Answer with one word: True or False.", "False"),
    ("What is the result of (0 < 1)? Answer with one word: True or False.", "True"),
    ("What is the result of (10 < 4)? Answer with one word: True or False.", "False"),
    # 6. (x > y)
    ("What is the result of (5 > 3)? Answer with one word: True or False.", "True"),
    ("What is the result of (3 > 5)? Answer with one word: True or False.", "False"),
    ("What is the result of (4 > 4)? Answer with one word: True or False.", "False"),
    ("What is the result of (7 > 2)? Answer with one word: True or False.", "True"),
    # 7. (x == y)
    ("What is the result of (5 == 5)? Answer with one word: True or False.", "True"),
    ("What is the result of (5 == 3)? Answer with one word: True or False.", "False"),
    ("What is the result of (0 == 0)? Answer with one word: True or False.", "True"),
    ("What is the result of (1 == 2)? Answer with one word: True or False.", "False"),
    # 8. Empty string (False)
    ("What is the truth value of the empty string \"\"? Answer with one word: True or False.", "False"),
    # 9. Non-empty string (True)
    ("What is the truth value of the string \"a\"? Answer with one word: True or False.", "True"),
    ("What is the truth value of the string \"hello\"? Answer with one word: True or False.", "True"),
    ("What is the truth value of the string \" \"? Answer with one word: True or False.", "True"),
    # 10. None (False)
    ("What is the truth value of None? Answer with one word: True or False.", "False"),
]


def _pick_boolean_exercises():
    """Return 5 boolean exercises chosen at random from the pool (no replacement)."""
    chosen = random.sample(POOL_BOOLEAN, min(5, len(POOL_BOOLEAN)))
    return [
        {"question": q, "expected": e, "check": _make_boolean_word_check(e), "answer_type": "word"}
        for q, e in chosen
    ]


def _pick_batch2_session():
    """Build the full Batch 2 session in fixed order: 7 strings then 5 booleans."""
    return _pick_string_exercises() + _pick_boolean_exercises()


class Batch2Exercises:
    """
    Batch 2: Topics 5–6. 7 strings + 5 booleans = 12 questions per session.
    """

    STRING_COUNT = 7
    BOOLEAN_COUNT = 5
    MAX_MISTAKES_PER_EXERCISE = 3

    def __init__(self):
        pass

    def start_exercises(self):
        """Start the strings and booleans exercises sequence."""
        print_session_header("PYTHON BASICS - STRINGS AND BOOLEANS EXERCISES")
        print("\nYou will get 7 single-line code questions, followed by 5 boolean questions (True or False).")
        print("For questions 1-7, type one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        all_exercises = _pick_batch2_session()
        completed, not_completed = run_simple_exercises(
            all_exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
            prompt_label_for=prompt_label_batch2,
        )
        print_session_footer(completed, not_completed)