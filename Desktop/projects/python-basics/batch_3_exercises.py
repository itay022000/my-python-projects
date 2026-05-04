"""
Batch 3: Topic 7 (Operators).
Single-line code exercises; 12 questions per session, randomly sampled from a pool.
Same rules as Batch 1 and 2: space normalization, 3 attempts, no overly explicit hints.
"""

import random

from exercise_checks import checker_basic
from session_runner import print_session_footer, print_session_header, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_basic.normalize
_make_exact_check = checker_basic.make_exact_check
_make_exercise = checker_basic.make_exercise


# ---------------------------------------------------------------------------
# Operator exercise pools
# Questions 1–2: two arithmetic operators chosen at random, no repeats.
# Questions 3–12: chosen from the rest of the operator pool.
# ---------------------------------------------------------------------------

# Arithmetic only: +, -, *, /, %, //, ** — one (question, expected) per operator
POOL_ARITHMETIC = [
    ("Suppose a = 10 and b = 3. Store their sum in a variable named total.", "total = a + b"),
    ("Suppose a = 20 and b = 7. Store the value of a minus b in a variable named diff.", "diff = a - b"),
    ("Suppose a = 4 and b = 5. Store their product in a variable named prod.", "prod = a * b"),
    ("Suppose a = 20 and b = 4. Store the quotient when a is divided by b in a variable named q.", "q = a / b"),
    ("Suppose a = 17 and b = 5. Store the remainder when a is divided by b in a variable named r.", "r = a % b"),
    ("Suppose a = 17 and b = 4. Store the floor quotient of a by b in a variable named f.", "f = a // b"),
    ("Suppose a = 2 and b = 3. Store a raised to the power b in a variable named p.", "p = a ** b"),
]

# Assignment operators: +=, -=, *=, /=, %=, //=, **=, := — two chosen at random, no repeats (questions 3–4)
POOL_ASSIGNMENT = [
    ("Suppose x = 10. In one line, update x so it increases by 5.", "x += 5"),
    ("Suppose n = 20. In one line, update n so it decreases by 7.", "n -= 7"),
    ("Suppose k = 4. In one line, update k so it is multiplied by 3.", "k *= 3"),
    ("Suppose m = 100. In one line, update m so it is divided by 4.", "m /= 4"),
    ("Suppose n = 17. In one line, update n to the remainder of n divided by 5.", "n %= 5"),
    ("Suppose n = 17. In one line, update n to the floor quotient of n by 4.", "n //= 4"),
    ("Suppose n = 2. In one line, update n to n raised to the power of 3.", "n **= 3"),
    ("In one expression, set a variable x to 10 and test whether that value is greater than 5. Use the operator that assigns and returns in the same step.", "(x := 10) > 5"),
]

# Comparison operators: ==, !=, >, <, >=, <= — two chosen at random, no repeats (questions 5–6)
POOL_COMPARISON = [
    ("Suppose a = 5 and b = 5. Store in eq whether the two values are equal.", "eq = a == b"),
    ("Suppose a = 4 and b = 9. Store in ne whether the two values differ.", "ne = a != b"),
    ("Suppose a = 5 and b = 3. Store in gt whether a is greater than b.", "gt = a > b"),
    ("Suppose a = 3 and b = 7. Store in lt whether a is less than b.", "lt = a < b"),
    ("Suppose a = 10 and b = 4. Store in ge whether a is greater than or equal to b.", "ge = a >= b"),
    ("Suppose a = 3 and b = 7. Store in le whether a is less than or equal to b.", "le = a <= b"),
]

# Logical operators: and, or, not — one chosen at random (question 7)
POOL_LOGICAL = [
    ("Suppose p = True and q = False. Store in r the value of True only when both p and q are true.", "r = p and q"),
    ("Suppose p = True and q = False. Store in r the value of True when at least one of p or q is true.", "r = p or q"),
    ("Suppose flag = True. Store in inv the opposite truth value of flag.", "inv = not flag"),
]

# Two different logical operators in one statement — one chosen at random (question 8)
POOL_LOGICAL_TWO = [
    ("Suppose p = True and q = False. Store in r True only when p is false and q is true.", "r = not p and q"),
    ("Suppose p = True and q = False. Store in r True when p is true or q is false.", "r = p or not q"),
    ("Suppose p = True and q = False. Store in r True only when p is true and q is false.", "r = p and not q"),
    ("Suppose p = True and q = False. Store in r True when p is false or q is true.", "r = not p or q"),
    ("Suppose p = True and q = False. Store in r the negation of \"both p and q are true\".", "r = not (p and q)"),
    ("Suppose p = True and q = False. Store in r the negation of \"at least one of p or q is true\".", "r = not (p or q)"),
]

# Identity operators: is, is not — one chosen at random (question 9)
POOL_IDENTITY = [
    ("Suppose x = None. Store in ok whether x refers to None.", "ok = x is None"),
    ("Suppose a = 10 and b = 10. Store in diff whether a and b are not the same object.", "diff = a is not b"),
]

# Membership operators: in, not in — one chosen at random (question 10)
POOL_MEMBERSHIP = [
    ("Suppose s = \"hello\". Store in found whether the character \"e\" appears in s.", "found = \"e\" in s"),
    ("Suppose s = \"python\". Store in missing whether the character \"z\" does not appear in s.", "missing = \"z\" not in s"),
]

# Bitwise operators: &, |, ^, ~, <<, >> — two chosen at random, no repeats (questions 11–12)
POOL_BITWISE = [
    ("Suppose a = 5 and b = 3. Store in r the bitwise AND of a and b.", "r = a & b"),
    ("Suppose a = 2 and b = 4. Store in r the bitwise OR of a and b.", "r = a | b"),
    ("Suppose a = 5 and b = 3. Store in r the bitwise XOR of a and b.", "r = a ^ b"),
    ("Suppose n = 5. Store in r the bitwise negation of n.", "r = ~n"),
    ("Suppose n = 4. Store in r the value of n shifted left by 1 bit.", "r = n << 1"),
    ("Suppose n = 8. Store in r the value of n shifted right by 2 bits.", "r = n >> 2"),
]


def _pick_batch3_session(count=12):
    """Questions 1–2: arithmetic. 3–4: assignment. 5–6: comparison. 7: one logical. 8: two logical. 9: identity. 10: membership. 11–12: two bitwise (random, no repeat)."""
    arithmetic_two = random.sample(POOL_ARITHMETIC, 2)
    assignment_two = random.sample(POOL_ASSIGNMENT, 2)
    comparison_two = random.sample(POOL_COMPARISON, 2)
    logical_one = [random.choice(POOL_LOGICAL)]
    logical_two = [random.choice(POOL_LOGICAL_TWO)]
    identity_one = [random.choice(POOL_IDENTITY)]
    membership_one = [random.choice(POOL_MEMBERSHIP)]
    bitwise_two = random.sample(POOL_BITWISE, 2)
    chosen = arithmetic_two + assignment_two + comparison_two + logical_one + logical_two + identity_one + membership_one + bitwise_two
    return [_make_exercise(q, e) for q, e in chosen]


class Batch3Exercises:
    """
    Batch 3: Topic 7 (Operators). 12 questions per session, randomly chosen from pool.
    """

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def __init__(self):
        pass

    def start_exercises(self):
        """Start the operators exercises sequence."""
        print_session_header("PYTHON BASICS - OPERATORS EXERCISES")
        print("\nYou will get 12 single-line code questions.")
        print("Type one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        exercises = _pick_batch3_session(self.EXERCISES_PER_SESSION)
        completed, not_completed = run_simple_exercises(
            exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)