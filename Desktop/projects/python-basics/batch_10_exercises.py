"""
Batch 10: Topics 17–21 (Arrays, Dates, JSON, Try/Except, Input).
Mixed session: 24 answer lines across 19 questions (equal weight ~5.26% each; intro states this).
Only the exact expected answer is accepted for each line.

Rules for all questions (apply to new questions unless stated otherwise):
  - Space normalization is applied to every answer (no exceptions).
  - Do not give overly explicit hints in question text.
"""

import random

from exercise_checks import checker_mixed_dicts
from session_runner import print_session_footer, print_session_header, run_mixed_units_session

# Shared exact-answer verification (same behavior as before; see exercise_checks.py).
_normalize_code = checker_mixed_dicts.normalize
_make_exact_check = checker_mixed_dicts.make_exact_check
_make_simple = checker_mixed_dicts.make_simple
_make_compound = checker_mixed_dicts.make_compound


# ---------------------------------------------------------------------------
# Arrays (Q1-Q6)
# ---------------------------------------------------------------------------
POOL_1_ACCESS_ARRAY = [
    ("Suppose arr = [10, 20, 30]. Store in x the element at index 1.", "x = arr[1]"),
    ("Suppose arr = [5, 6, 7]. Store in val the element at index 2.", "val = arr[2]"),
]

POOL_2_ACCESS_MODIFY_ARRAY = [
    ("Suppose arr = [10, 20, 30]. Change the element at index 0 to 99.", "arr[0] = 99"),
    ("Suppose arr = [1, 2, 3]. Change the element at index 2 to 8.", "arr[2] = 8"),
]

POOL_3_ARRAY_LEN = [
    ("Suppose arr = [10, 20, 30]. Store the number of elements in n.", "n = len(arr)"),
    ("Suppose arr = [1, 2, 3, 4]. Store the number of elements in size.", "size = len(arr)"),
]

POOL_4_ARRAY_ADD = [
    ("Suppose arr = [10, 20]. Add 30 to the end of arr.", "arr.append(30)"),
    ("Suppose arr = [1]. Add 2 to the end of arr.", "arr.append(2)"),
]

POOL_5_ARRAY_POP = [
    ("Suppose arr = [10, 20, 30]. Remove and store the last element in last.", "last = arr.pop()"),
    ("Suppose arr = [1, 2]. Remove and store the last element in x.", "x = arr.pop()"),
]

POOL_6_ARRAY_REMOVE = [
    ("Suppose arr = [10, 20, 30]. Remove the value 20 from arr.", "arr.remove(20)"),
    ("Suppose arr = [1, 2, 3]. Remove the value 1 from arr.", "arr.remove(1)"),
]


# ---------------------------------------------------------------------------
# Dates (Q7-Q14). Assume import datetime already exists.
# ---------------------------------------------------------------------------
POOL_7_CURRENT_TIME = [
    ("Assume import datetime was already done. Display the current date-time value.", "print(datetime.datetime.now())"),
]

POOL_8_CURRENT_YEAR = [
    ("Assume import datetime was already done. Display the current year number.", "print(datetime.datetime.now().year)"),
]

POOL_9_CURRENT_MONTH = [
    ("Assume import datetime was already done. Display the current month number.", "print(datetime.datetime.now().month)"),
]

POOL_10_CURRENT_DAY = [
    ("Assume import datetime was already done. Display the current day of the month.", "print(datetime.datetime.now().day)"),
]

POOL_11_CREATE_DATE = [
    ("Assume import datetime was already done. Create a date-time object for 2024-01-15 and store it in d.", "d = datetime.datetime(2024, 1, 15)"),
    ("Assume import datetime was already done. Create a date-time object for 2023-12-31 and store it in d.", "d = datetime.datetime(2023, 12, 31)"),
]

POOL_12_STRFTIME_WEEKDAY = [
    ("Suppose d is a datetime object. Store the weekday name of d in txt (full name).", "txt = d.strftime(\"%A\")"),
    ("Suppose d is a datetime object. Store in out the full weekday name of d.", "out = d.strftime(\"%A\")"),
]

POOL_13_STRFTIME_MONTH_NAME = [
    ("Suppose d is a datetime object. Store the month name of d in txt (full name).", "txt = d.strftime(\"%B\")"),
    ("Suppose d is a datetime object. Store in out the full month name of d.", "out = d.strftime(\"%B\")"),
]

POOL_14_STRFTIME_HOUR = [
    ("Suppose d is a datetime object. Store the hour (24h) of d in hh using formatting.", "hh = d.strftime(\"%H\")"),
    ("Suppose d is a datetime object. Store in out the hour of d as two digits (24h).", "out = d.strftime(\"%H\")"),
]


# ---------------------------------------------------------------------------
# JSON (Q15-Q18). Assume import json already exists.
# ---------------------------------------------------------------------------
POOL_15_JSON_LOADS = [
    ("Assume import json was already done. Convert s = \"{\\\"x\\\": 1}\" from JSON text to a Python object and store in obj.", "obj = json.loads(s)"),
    ("Assume import json was already done. Convert txt = \"{\\\"name\\\": \\\"Ada\\\"}\" from JSON text to a Python object and store in data.", "data = json.loads(txt)"),
]

POOL_16_JSON_DUMPS = [
    ("Assume import json was already done. Convert d to a JSON string and store it in txt.", "txt = json.dumps(d)"),
    ("Assume import json was already done. Convert obj to a JSON string and store it in s.", "s = json.dumps(obj)"),
]

POOL_17_JSON_FORMATTED = [
    ("Assume import json was already done. Convert d to formatted JSON using indentation of 4 spaces and store in txt.", "txt = json.dumps(d, indent=4)"),
    ("Assume import json was already done. Convert obj to formatted JSON using indentation of 2 spaces and store in s.", "s = json.dumps(obj, indent=2)"),
]

POOL_18_JSON_FORMATTED_SORTED = [
    ("Assume import json was already done. Convert d to formatted JSON with indentation 4 and sorted keys; store in txt.", "txt = json.dumps(d, indent=4, sort_keys=True)"),
    ("Assume import json was already done. Convert obj to formatted JSON with indentation 2 and sorted keys; store in s.", "s = json.dumps(obj, indent=2, sort_keys=True)"),
]


# ---------------------------------------------------------------------------
# Try/Except and Input (Q19-Q25)
# ---------------------------------------------------------------------------
POOL_19_TRY_EXCEPT = [
    _make_compound(
        "Try... except in 2 lines (in order)",
        [
            ("Step 1: write a try line that attempts 1 / 0 and stores it in x.", "try: x = 1 / 0"),
            ("Step 2: write a broad except line that prints \"error\".", "except: print(\"error\")"),
        ],
    ),
    _make_compound(
        "Try... except in 2 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(\"a\") and stores it in n.", "try: n = int(\"a\")"),
            ("Step 2: write a broad except line that prints \"bad\".", "except: print(\"bad\")"),
        ],
    ),
]

POOL_20_TRY_EXCEPT_EXCEPT = [
    _make_compound(
        "Try... except... except in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(\"a\") and stores it in x.", "try: x = int(\"a\")"),
            ("Step 2: catch ValueError and print \"value\".", "except ValueError: print(\"value\")"),
            ("Step 3: catch TypeError and print \"type\".", "except TypeError: print(\"type\")"),
        ],
    ),
    _make_compound(
        "Try... except... except in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(None) and stores it in x.", "try: x = int(None)"),
            ("Step 2: catch TypeError and print \"type\".", "except TypeError: print(\"type\")"),
            ("Step 3: catch ValueError and print \"value\".", "except ValueError: print(\"value\")"),
        ],
    ),
]

POOL_21_TRY_EXCEPT_ELSE = [
    _make_compound(
        "Try... except... else in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(\"7\") and stores it in x.", "try: x = int(\"7\")"),
            ("Step 2: catch ValueError and print \"bad\".", "except ValueError: print(\"bad\")"),
            ("Step 3: write the else line that prints \"ok\".", "else: print(\"ok\")"),
        ],
    ),
    _make_compound(
        "Try... except... else in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(\"12\") and stores it in n.", "try: n = int(\"12\")"),
            ("Step 2: catch ValueError and print \"bad\".", "except ValueError: print(\"bad\")"),
            ("Step 3: write the else line that prints \"good\".", "else: print(\"good\")"),
        ],
    ),
]

POOL_22_TRY_EXCEPT_FINALLY = [
    _make_compound(
        "Try... except... finally in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts 1 / 0 and stores it in x.", "try: x = 1 / 0"),
            ("Step 2: catch ZeroDivisionError and print \"div0\".", "except ZeroDivisionError: print(\"div0\")"),
            ("Step 3: write the finally line that prints \"done\".", "finally: print(\"done\")"),
        ],
    ),
    _make_compound(
        "Try... except... finally in 3 lines (in order)",
        [
            ("Step 1: write a try line that attempts int(\"a\") and stores it in n.", "try: n = int(\"a\")"),
            ("Step 2: catch ValueError and print \"bad\".", "except ValueError: print(\"bad\")"),
            ("Step 3: write the finally line that prints \"end\".", "finally: print(\"end\")"),
        ],
    ),
]

POOL_23_RAISE = [
    ("Raise a generic exception with the message \"stop\".", "raise Exception(\"stop\")"),
    ("Raise a ValueError with the message \"bad value\".", "raise ValueError(\"bad value\")"),
]

POOL_24_INPUT_NO_PROMPT = [
    ("Read user input without a prompt and store it in text.", "text = input()"),
    ("Read user input without a prompt and store it in value.", "value = input()"),
]

POOL_25_INPUT_WITH_PROMPT = [
    ("Read user input with the prompt \"Enter value: \" and store it in text.", "text = input(\"Enter value: \")"),
    ("Read user input with the prompt \"Type your name: \" and store it in name.", "name = input(\"Type your name: \")"),
]


def _pick_batch10_units():
    """
    Build 19 scored questions in session order:
      Q1-Q2: both
      Q3-Q4: pick 1
      Q5-Q6: pick 1
      Q7-Q10: pick 2
      Q11: fixed
      Q12-Q14: pick 2
      Q15-Q18: all 4
      Q19: fixed compound (2 lines)
      Q20-Q22: pick 2 compounds (3 lines each)
      Q23-Q25: all 3
    """
    units = []

    units.append(_make_simple(*random.choice(POOL_1_ACCESS_ARRAY)))
    units.append(_make_simple(*random.choice(POOL_2_ACCESS_MODIFY_ARRAY)))

    units.append(_make_simple(*random.choice(random.choice([POOL_3_ARRAY_LEN, POOL_4_ARRAY_ADD]))))
    units.append(_make_simple(*random.choice(random.choice([POOL_5_ARRAY_POP, POOL_6_ARRAY_REMOVE]))))

    for pool in random.sample([POOL_7_CURRENT_TIME, POOL_8_CURRENT_YEAR, POOL_9_CURRENT_MONTH, POOL_10_CURRENT_DAY], 2):
        units.append(_make_simple(*random.choice(pool)))

    units.append(_make_simple(*random.choice(POOL_11_CREATE_DATE)))

    for pool in random.sample([POOL_12_STRFTIME_WEEKDAY, POOL_13_STRFTIME_MONTH_NAME, POOL_14_STRFTIME_HOUR], 2):
        units.append(_make_simple(*random.choice(pool)))

    units.append(_make_simple(*random.choice(POOL_15_JSON_LOADS)))
    units.append(_make_simple(*random.choice(POOL_16_JSON_DUMPS)))
    units.append(_make_simple(*random.choice(POOL_17_JSON_FORMATTED)))
    units.append(_make_simple(*random.choice(POOL_18_JSON_FORMATTED_SORTED)))

    units.append(random.choice(POOL_19_TRY_EXCEPT))

    for pool in random.sample([POOL_20_TRY_EXCEPT_EXCEPT, POOL_21_TRY_EXCEPT_ELSE, POOL_22_TRY_EXCEPT_FINALLY], 2):
        units.append(random.choice(pool))

    units.append(_make_simple(*random.choice(POOL_23_RAISE)))
    units.append(_make_simple(*random.choice(POOL_24_INPUT_NO_PROMPT)))
    units.append(_make_simple(*random.choice(POOL_25_INPUT_WITH_PROMPT)))

    return units


class Batch10Exercises:
    """
    Batch 10: Topics 17-21. 19 questions per session; 24 lines of code total.
    """

    EXERCISES_PER_SESSION_UNITS = 19
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        """Start the advanced mixed exercises sequence."""
        print_session_header("PYTHON BASICS - ADVANCED TOPICS EXERCISES")
        print("\nYou will get 19 questions. Each counts the same toward your session score (~5.26% per question).")
        print("Three questions are multi-line, so you will type 24 lines of code total.")
        print("Type one line when prompted. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        units = _pick_batch10_units()
        units_passed, units_failed = run_mixed_units_session(
            units,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(units_passed, units_failed)
