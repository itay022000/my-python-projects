"""
Batch 8: Topic 12 (Functions).
Mixed session: 12 answer lines across 11 questions (equal weight ~9.09% each; session intro states this for the user).
Only the exact expected answer is accepted for each line.

Rules for all questions (apply to new questions unless stated otherwise):
  - Space normalization is applied to every answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_mixed_functions
from session_runner import print_session_footer, print_session_header, run_mixed_units_session

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_mixed_functions.normalize
_make_exact_check = checker_mixed_functions.make_exact_check
_make_simple = checker_mixed_functions.make_simple
_make_compound = checker_mixed_functions.make_compound


# ---------------------------------------------------------------------------
# 1–2: pick 1
# ---------------------------------------------------------------------------
POOL_1_PRINT_STRING_AND_PARAM = [
    (
        "Write one line that defines the function greet with one parameter name, and prints \"Hello\" and name.",
        "def greet(name): print(\"Hello\", name)",
    ),
    (
        "Write one line that defines the function show with one parameter item, and prints \"Value\" and item.",
        "def show(item): print(\"Value\", item)",
    ),
]

POOL_2_PRINT_TWO_PARAMS = [
    (
        "Write one line that defines the function pair with parameters a and b, and prints both values.",
        "def pair(a, b): print(a, b)",
    ),
    (
        "Write one line that defines the function show2 with parameters x and y, and prints both values.",
        "def show2(x, y): print(x, y)",
    ),
]


# ---------------------------------------------------------------------------
# 3–7: all selected every session
# ---------------------------------------------------------------------------
POOL_3_KWARGS_REVERSED = [
    (
        "Assume the function person(first, last) already exists. Write only the call that passes first=\"Ada\" and last=\"Lovelace\" as keyword arguments in reversed order.",
        "person(last=\"Lovelace\", first=\"Ada\")",
    ),
    (
        "Assume the function pair(a, b) already exists. Write only the call that passes a=1 and b=2 as keyword arguments in reversed order.",
        "pair(b=2, a=1)",
    ),
]

POOL_4_POSITIONAL_AND_KEYWORD = [
    (
        "Assume the function paint(color, item) already exists. Write only the call with color=\"red\" as positional and item=\"car\" as keyword.",
        "paint(\"red\", item=\"car\")",
    ),
    (
        "Assume the function move(direction, steps) already exists. Write only the call with direction=\"left\" as positional and steps=3 as keyword.",
        "move(\"left\", steps=3)",
    ),
]

POOL_5_POSITIONAL_ONLY = [
    (
        "Write one line that defines the function add with positional-only parameters a and b, and returns their sum.",
        "def add(a, b, /): return a + b",
    ),
    (
        "Write one line that defines the function diff with positional-only parameters x and y, and returns x - y.",
        "def diff(x, y, /): return x - y",
    ),
]

POOL_6_KEYWORD_ONLY = [
    (
        "Write one line that defines the function area with keyword-only parameters w and h, and returns w * h.",
        "def area(*, w, h): return w * h",
    ),
    (
        "Write one line that defines the function total with keyword-only parameters x and y, and returns x + y.",
        "def total(*, x, y): return x + y",
    ),
]

POOL_7_POS_ONLY_AND_KW_ONLY = [
    (
        "Write one line that defines the function mix with x as positional-only and y as keyword-only, and returns x + y.",
        "def mix(x, /, *, y): return x + y",
    ),
    (
        "Write one line that defines the function combine with a as positional-only and b as keyword-only, and returns a * b.",
        "def combine(a, /, *, b): return a * b",
    ),
]


# ---------------------------------------------------------------------------
# 8–11: pick exactly one ordered pair: (8,9) or (10,11)
# ---------------------------------------------------------------------------
POOL_8_ARGS = [
    (
        "Write one line that defines the function collect to accept any number of positional arguments and print the collected tuple.",
        "def collect(*args): print(args)",
    ),
    (
        "Write one line that defines the function show_all to accept any number of positional arguments and print the collected tuple.",
        "def show_all(*args): print(args)",
    ),
]

POOL_9_ARGS_AND_REGULAR = [
    (
        "Write one line that defines the function tag with regular parameter label plus any extra positional arguments, and prints label and the extras tuple.",
        "def tag(label, *args): print(label, args)",
    ),
    (
        "Write one line that defines the function wrap with regular parameter head plus any extra positional arguments, and prints head and the extras tuple.",
        "def wrap(head, *args): print(head, args)",
    ),
]

POOL_10_KWARGS = [
    (
        "Write one line that defines the function show_map to accept any keyword arguments and print the collected dictionary.",
        "def show_map(**kwargs): print(kwargs)",
    ),
    (
        "Write one line that defines the function dump to accept any keyword arguments and print the collected dictionary.",
        "def dump(**kwargs): print(kwargs)",
    ),
]

POOL_11_KWARGS_AND_REGULAR = [
    (
        "Write one line that defines the function mark with regular parameter title plus any keyword arguments, and prints title and the collected dictionary.",
        "def mark(title, **kwargs): print(title, kwargs)",
    ),
    (
        "Write one line that defines the function log with regular parameter prefix plus any keyword arguments, and prints prefix and the collected dictionary.",
        "def log(prefix, **kwargs): print(prefix, kwargs)",
    ),
]


# ---------------------------------------------------------------------------
# 12–14: all selected; 13 is two lines
# ---------------------------------------------------------------------------
POOL_12_REGULAR_ARGS_KWARGS = [
    (
        "Write one line that defines the function combo with regular parameter x, extra positional arguments, and keyword arguments; print x, the extras tuple, and the collected dictionary.",
        "def combo(x, *args, **kwargs): print(x, args, kwargs)",
    ),
    (
        "Write one line that defines the function all_in with regular parameter first, extra positional arguments, and keyword arguments; print first, the extras tuple, and the collected dictionary.",
        "def all_in(first, *args, **kwargs): print(first, args, kwargs)",
    ),
]

DECORATOR_VARIANTS = [
    _make_compound(
        "Basic decorator in 2 lines (in order)",
        [
            (
                "Assume the function work() already exists. Step 1: write one line that defines decorator deco, which receives f and returns f.",
                "def deco(f): return f",
            ),
            (
                "Step 2: write only the decorator line that applies deco to work.",
                "@deco",
            ),
        ],
    ),
    _make_compound(
        "Basic decorator in 2 lines (in order)",
        [
            (
                "Assume the function task() already exists. Step 1: write one line that defines decorator wrap, which receives fn and returns fn.",
                "def wrap(fn): return fn",
            ),
            (
                "Step 2: write only the decorator line that applies wrap to task.",
                "@wrap",
            ),
        ],
    ),
]

POOL_14_LAMBDA = [
    (
        "Write one line that stores in f a lambda receiving a and b and returning their sum.",
        "f = lambda a, b: a + b",
    ),
    (
        "Write one line that stores in f a lambda receiving a and b and returning their product.",
        "f = lambda a, b: a * b",
    ),
]


def _pick_batch8_units():
    """
    Build 11 scored questions in session order:
      1) one of (q1, q2)
      2-6) q3..q7 all included
      7-8) one full ordered pair: (q8, q9) or (q10, q11)
      9) q12
      10) q13 compound (2 lines)
      11) q14
    """
    units = []

    if random.choice([True, False]):
        units.append(_make_simple(*random.choice(POOL_1_PRINT_STRING_AND_PARAM)))
    else:
        units.append(_make_simple(*random.choice(POOL_2_PRINT_TWO_PARAMS)))

    units.append(_make_simple(*random.choice(POOL_3_KWARGS_REVERSED)))
    units.append(_make_simple(*random.choice(POOL_4_POSITIONAL_AND_KEYWORD)))
    units.append(_make_simple(*random.choice(POOL_5_POSITIONAL_ONLY)))
    units.append(_make_simple(*random.choice(POOL_6_KEYWORD_ONLY)))
    units.append(_make_simple(*random.choice(POOL_7_POS_ONLY_AND_KW_ONLY)))

    if random.choice([True, False]):
        units.append(_make_simple(*random.choice(POOL_8_ARGS)))
        units.append(_make_simple(*random.choice(POOL_9_ARGS_AND_REGULAR)))
    else:
        units.append(_make_simple(*random.choice(POOL_10_KWARGS)))
        units.append(_make_simple(*random.choice(POOL_11_KWARGS_AND_REGULAR)))

    units.append(_make_simple(*random.choice(POOL_12_REGULAR_ARGS_KWARGS)))
    units.append(random.choice(DECORATOR_VARIANTS))
    units.append(_make_simple(*random.choice(POOL_14_LAMBDA)))

    return units


class Batch8Exercises:
    """
    Batch 8: Topic 12 (Functions). 11 questions per session; 12 lines of code total.
    """

    EXERCISES_PER_SESSION_UNITS = 11
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        """Start the functions exercises sequence."""
        print_session_header("PYTHON BASICS - FUNCTIONS EXERCISES")
        print("\nYou will get 11 questions. Each counts the same toward your session score (~9.09% per question).")
        print("One question asks for two lines of code; the other ten ask for one line each.")
        print("Type one line when prompted. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        units = _pick_batch8_units()
        units_passed, units_failed = run_mixed_units_session(
            units,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(units_passed, units_failed)
