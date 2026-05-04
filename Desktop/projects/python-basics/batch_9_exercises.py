"""
Batch 9: Shorthand if, match, range, math.
Single-line code exercises; 12 questions per session in fixed order.
Same rules as other batches: space normalization, 3 attempts, no overly explicit hints.
"""

import random

from exercise_checks import checker_lists
from session_runner import print_session_footer, print_session_header, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_lists.normalize
_make_exact_check = checker_lists.make_exact_check
_make_exercise = checker_lists.make_exercise


# ---------------------------------------------------------------------------
# Question 1: Shorthand if — format: if (condition): (expression)
# ---------------------------------------------------------------------------
POOL_SHORTHAND_IF = [
    ("Suppose x = True. When x is true, assign 10 to r in one line.", "if x: r = 10"),
    ("Suppose flag = True. When flag is true, assign \"yes\" to out in one line.", "if flag: out = \"yes\""),
]

# ---------------------------------------------------------------------------
# Question 2: Shorthand if... else — format: (expression_1) if (condition) else (expression_2)
# ---------------------------------------------------------------------------
POOL_SHORTHAND_IF_ELSE = [
    ("Suppose a = 5 and b = 3. Store in r the larger of the two.", "r = a if a > b else b"),
    ("Suppose a = 10 and b = 20. Store in r the smaller of a and b.", "r = a if a < b else b"),
]

# ---------------------------------------------------------------------------
# Question 3: Shorthand multiple conditions — format: (expr_1) if (cond_1) else (expr_2) if (cond_2) else (expr_3)
# ---------------------------------------------------------------------------
POOL_SHORTHAND_MULTIPLE = [
    ("Suppose x and y are booleans. Store in r: 1 when x is true, else 2 when y is true, else 3.", "r = 1 if x else 2 if y else 3"),
    ("Suppose a = 1, b = 2, c = 3. Store in r the value a when a > 0, else b when b > 0, else c.", "r = a if a > 0 else b if b > 0 else c"),
]

# ---------------------------------------------------------------------------
# Question 4: Match — several cases (a | b | c)
# ---------------------------------------------------------------------------
POOL_MATCH_CASES = [
    ("You have match n: where n is an integer. Write the case line that matches 1, 2, or 3 and assigns 1 to r.", "case 1|2|3: r = 1"),
    ("You have match n: where n is an integer. Write the case line that matches 0 or 1 and assigns 1 to ok.", "case 0|1: ok = 1"),
]

# ---------------------------------------------------------------------------
# Question 5: Match — default case
# ---------------------------------------------------------------------------
POOL_MATCH_DEFAULT = [
    ("Write the case line that acts as the default in a match and assigns 0 to r.", "case _: r = 0"),
    ("Write the case line that catches all remaining values in a match and assigns -1 to result.", "case _: result = -1"),
]

# ---------------------------------------------------------------------------
# Question 6: Range — start (start and stop)
# ---------------------------------------------------------------------------
POOL_RANGE_START = [
    ("Store in r a range that starts at 2 and ends just before 10.", "r = range(2, 10)"),
    ("Store in r a range that starts at 5 and ends just before 15.", "r = range(5, 15)"),
]

# ---------------------------------------------------------------------------
# Question 7: Range — stop only
# ---------------------------------------------------------------------------
POOL_RANGE_STOP = [
    ("Store in r a range of 10 elements (0 through 9).", "r = range(10)"),
    ("Store in r a range of 5 elements starting at 0.", "r = range(5)"),
]

# ---------------------------------------------------------------------------
# Question 8: Range — start, stop, step
# ---------------------------------------------------------------------------
POOL_RANGE_STEP = [
    ("Store in r a range from 0 to 10 (exclusive) with step 2.", "r = range(0, 10, 2)"),
    ("Store in r a range from 0 to 20 (exclusive) with step 5.", "r = range(0, 20, 5)"),
]

# ---------------------------------------------------------------------------
# Question 9: Math — min
# ---------------------------------------------------------------------------
POOL_MATH_MIN = [
    ("Store in r the smallest of 3, 1, and 4.", "r = min(3, 1, 4)"),
    ("Store in r the minimum of 10, 5, and 8.", "r = min(10, 5, 8)"),
]

# ---------------------------------------------------------------------------
# Question 10: Math — max
# ---------------------------------------------------------------------------
POOL_MATH_MAX = [
    ("Store in r the largest of 3, 1, and 4.", "r = max(3, 1, 4)"),
    ("Store in r the maximum of 10, 5, and 8.", "r = max(10, 5, 8)"),
]

# ---------------------------------------------------------------------------
# Question 11: Math — abs
# ---------------------------------------------------------------------------
POOL_MATH_ABS = [
    ("Store in r the absolute value of -5.", "r = abs(-5)"),
    ("Store in r the absolute value of -10.", "r = abs(-10)"),
]

# ---------------------------------------------------------------------------
# Question 12: Math — pow
# ---------------------------------------------------------------------------
POOL_MATH_POW = [
    ("Store in r the value of 2 raised to the power 3 using the built-in function of two arguments.", "r = pow(2, 3)"),
    ("Store in r the value of 5 raised to the power 2 using the built-in function of two arguments.", "r = pow(5, 2)"),
]


def _pick_batch9_session():
    """Build 12 exercises in fixed order: shorthand if (3), match (2), range (3), math (4)."""
    exercises = []
    exercises.append(_make_exercise(*random.choice(POOL_SHORTHAND_IF)))
    exercises.append(_make_exercise(*random.choice(POOL_SHORTHAND_IF_ELSE)))
    exercises.append(_make_exercise(*random.choice(POOL_SHORTHAND_MULTIPLE)))
    exercises.append(_make_exercise(*random.choice(POOL_MATCH_CASES)))
    exercises.append(_make_exercise(*random.choice(POOL_MATCH_DEFAULT)))
    exercises.append(_make_exercise(*random.choice(POOL_RANGE_START)))
    exercises.append(_make_exercise(*random.choice(POOL_RANGE_STOP)))
    exercises.append(_make_exercise(*random.choice(POOL_RANGE_STEP)))
    exercises.append(_make_exercise(*random.choice(POOL_MATH_MIN)))
    exercises.append(_make_exercise(*random.choice(POOL_MATH_MAX)))
    exercises.append(_make_exercise(*random.choice(POOL_MATH_ABS)))
    exercises.append(_make_exercise(*random.choice(POOL_MATH_POW)))
    return exercises


class Batch9Exercises:
    """
    Batch 9: Shorthand if, match, range, math. 12 questions per session in fixed order.
    """

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def __init__(self):
        pass

    def start_exercises(self):
        """Start the batch 9 exercises sequence."""
        print_session_header("PYTHON BASICS - SHORTHAND IF, MATCH, RANGE, MATH (BATCH 9)")
        print("\nYou will get 12 single-line code questions.")
        print("\nType one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        exercises = _pick_batch9_session()
        completed, not_completed = run_simple_exercises(
            exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)
