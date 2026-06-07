"""
Batch 1: Topics 1–4 (Output, Comments, Variables, Basic data types and casting).
Single-line code exercises; 12 questions per session, randomly sampled.
Only the exact expected answer is accepted for each exercise.

Rules for all questions (apply to new questions and question types unless stated otherwise):
  - Space normalization is applied to every question's answer (no exceptions).
  - Do not give overly explicit hints in question text (e.g. do not name the exact
    function, keyword, or syntax the user must type).
"""

import random

from exercise_checks import checker_basic
from session_runner import print_session_footer, print_session_header, run_simple_exercises

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_basic.normalize
_make_exact_check = checker_basic.make_exact_check
_make_exercise = checker_basic.make_exercise


# ---------------------------------------------------------------------------
# Exercise pools (safe refactor): grouped by topic for readability/coherency.
# Session behavior is preserved by combining all pools into one flat list.
# ---------------------------------------------------------------------------

POOL_OUTPUT = [
    ("Write a single line that prints exactly: Hello", "print(\"Hello\")"),
    ("Write a single line that prints the number 100.", "print(100)"),
    ("Write a single line that prints the string \"Name:\" and the string \"Alice\".", "print(\"Name:\", \"Alice\")"),
    ("Write a single line that prints the text \"Result:\" followed by the number 42.", "print(\"Result:\", 42)"),
    ("Write a single line that prints the text \"x =\" followed by the number 7.", "print(\"x =\", 7)"),
    ("Write a single line that prints the number 3 and then the string \"items\".", "print(3, \"items\")"),
    ("Write a single line that prints the text \"Sum:\" followed by the result of 10 + 20.", "print(\"Sum:\", 10 + 20)"),
    ("Write a single line that prints the text \"Pi:\" followed by the float 3.14.", "print(\"Pi:\", 3.14)"),
    ("Write a single line that prints the text \"Value:\" followed by the number 0.", "print(\"Value:\", 0)"),
    ("Write a single line that prints the string \"OK\" with no newline at the end of the output.", "print(\"OK\", end=\"\")"),
    ("Write a single line that prints the result of 7 * 8.", "print(7 * 8)"),
]

POOL_COMMENTS = [
    ("Write a single-line comment that says: this is a comment.", "# this is a comment"),
    ("Assign the value 5 to a variable named x, and add an inline comment after it: my variable.", "x = 5  # my variable"),
]

POOL_VARIABLES = [
    ("In one statement, assign the same value 10 to two variables: a and b.", "a = b = 10"),
    ("Assign the value 42 to a variable named score.", "score = 42"),
    ("Assign the value 3.14 to a variable named pi.", "pi = 3.14"),
    ("Assign the string \"Python\" to a variable named lang.", "lang = \"Python\""),
    ("Assign the boolean True to a variable named flag.", "flag = True"),
    ("Assign the integer 0 to a variable named count.", "count = 0"),
]

POOL_TYPES_AND_CASTING = [
    ("Assign the integer 42 to a variable named n.", "n = 42"),
    ("Assign the float 2.5 to a variable named x.", "x = 2.5"),
    ("Assign the boolean False to a variable named b.", "b = False"),
    ("Assign the complex number 1+2j to a variable named z (use j notation).", "z = 1 + 2j"),
    ("Assign the complex number 3-4j to a variable named z (use j notation).", "z = 3 - 4j"),
    ("Assign the complex number 0+1j to a variable named z (use j notation).", "z = 0 + 1j"),
    ("Assign the complex number -2j to a variable named z (use j notation).", "z = -2j"),
    ("Assign the complex number with real part 1 and imaginary part 2 to a variable named w (use the constructor form).", "w = complex(1, 2)"),
    ("Assign the complex number with real part 0 and imaginary part 1 to a variable named i_val (use the constructor form).", "i_val = complex(0, 1)"),
    ("Convert the string \"100\" to an integer and assign the result to a variable named num.", "num = int(\"100\")"),
    ("Convert the string \"3.14\" to a float and assign the result to a variable named f.", "f = float(\"3.14\")"),
    ("Convert the integer 255 to a string and assign the result to a variable named s.", "s = str(255)"),
    ("Convert the float 7.0 to an integer and assign the result to a variable named k.", "k = int(7.0)"),
]


def _build_pool():
    # Keep behavior unchanged: flat combined pool, sampled uniformly later in start_exercises.
    raw = POOL_OUTPUT + POOL_COMMENTS + POOL_VARIABLES + POOL_TYPES_AND_CASTING
    return [_make_exercise(question, expected) for question, expected in raw]


def _pick_batch1_session(pool, count=12):
    """Build one Batch 1 session from a flat pool with fixed size."""
    return random.sample(pool, min(count, len(pool)))


class Batch1Exercises:
    """
    Batch 1: Topics 1–4. Single-line exercises; 12 questions per session.
    """

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def __init__(self):
        self.pool = _build_pool()

    def start_exercises(self):
        """Start the output, comments, variables and types exercises sequence."""
        print_session_header("PYTHON BASICS - OUTPUT, COMMENTS, VARIABLES AND TYPES EXERCISES")
        print("\nYou will get 12 single-line code questions.")
        print("Type one line of Python code per question. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        chosen = _pick_batch1_session(
            self.pool,
            self.EXERCISES_PER_SESSION,
        )
        completed, not_completed = run_simple_exercises(
            chosen,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)