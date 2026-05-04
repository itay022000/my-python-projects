"""
Batch 4: Lists (topic 8).
12 questions per session: random picks from segment pools (see _pick_batch4_session).
Same rules as other batches: space normalization, 3 attempts, no overly explicit hints.
"""

import random
import re

from session_runner import print_session_footer, print_session_header, run_simple_exercises


# ---------------------------------------------------------------------------
# Exact-answer verification
# ---------------------------------------------------------------------------

def _normalize_code(code):
    """Normalize code string for comparison. Used for every question."""
    if not code:
        return ""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = re.sub(r"\s*([=\[\]\(\):,])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    code = re.sub(r"\s*,\s*", ",", code)
    code = re.sub(r"\s*([*+/])\s*", r"\1", code)
    code = re.sub(r"\s*-\s*", "-", code)
    return code.strip()


def _make_exact_check(expected_code):
    expected_normalized = _normalize_code(expected_code)

    def check(user_code):
        user_normalized = _normalize_code(user_code)
        if user_normalized == expected_normalized:
            return True, "Correct!"
        return False, "That is not the expected answer. Only the exact required line is accepted."

    return check


def _make_exercise(question, expected):
    return {"question": question, "expected": expected, "check": _make_exact_check(expected)}


# ---------------------------------------------------------------------------
# Segments 1–4: access, access range, negative index, negative range (pick 2 types)
# ---------------------------------------------------------------------------
ACCESS_BY_KIND = {
    "access": [
        ("Suppose nums = [7, 8, 9]. Store the value at index 0 in a variable named x.", "x = nums[0]"),
        ("Suppose nums = [4, 5, 6]. Store the value at index 2 in a variable named x.", "x = nums[2]"),
    ],
    "access_range": [
        (
            "Suppose nums = [10, 20, 30, 40]. Store in s the part that starts at index 1 and stops before index 3.",
            "s = nums[1:3]",
        ),
        (
            "Suppose nums = [1, 2, 3, 4, 5]. Store in s the part that starts at index 0 and stops before index 4.",
            "s = nums[0:4]",
        ),
    ],
    "negative": [
        ("Suppose nums = [1, 2, 3]. Store the final element in a variable named u.", "u = nums[-1]"),
        ("Suppose nums = [9, 8, 7]. Store the second-from-last element in a variable named u.", "u = nums[-2]"),
    ],
    "negative_range": [
        (
            "Suppose nums = [1, 2, 3, 4, 5]. Store in seg the slice from index -3 up to but not including index -1.",
            "seg = nums[-3:-1]",
        ),
        (
            "Suppose nums = [10, 20, 30, 40]. Store in seg the slice from index -4 up to but not including index -1.",
            "seg = nums[-4:-1]",
        ),
    ],
}

# ---------------------------------------------------------------------------
# Segments 5–7: change one item, shrink slice assign, enlarge slice assign (pick 2)
# ---------------------------------------------------------------------------
CHANGE_BY_KIND = {
    "change_item": [
        ("Suppose nums = [1, 2, 3]. Replace the element at index 1 with 100.", "nums[1] = 100"),
        ("Suppose nums = [10, 20, 30]. Replace the element at index 0 with 0.", "nums[0] = 0"),
    ],
    "shrink": [
        (
            "Suppose nums = [1, 2, 3, 4]. In one line, replace from index 1 through the end with a list containing only the single value 9.",
            "nums[1:] = [9]",
        ),
        (
            "Suppose nums = [0, 1, 2, 3]. In one line, replace from index 2 through the end with a list containing only 5.",
            "nums[2:] = [5]",
        ),
    ],
    "enlarge": [
        (
            "Suppose nums = [1, 2, 3]. In one line, replace the slice that covers only index 1 with three new values: 5, 6, and 7.",
            "nums[1:2] = [5, 6, 7]",
        ),
        (
            "Suppose nums = [0, 1, 2]. In one line, replace the slice that covers only index 0 with two values: 8 and 9.",
            "nums[0:1] = [8, 9]",
        ),
    ],
}

# ---------------------------------------------------------------------------
# Segments 8–10: insert, extend, append (pick 2)
# ---------------------------------------------------------------------------
ADD_BY_KIND = {
    "insert": [
        (
            "Suppose nums = [1, 2, 3]. Place the value 7 at index 1 without dropping the existing elements; they shift.",
            "nums.insert(1, 7)",
        ),
        (
            "Suppose nums = [0, 1]. Place the value 5 at index 0 without dropping the existing elements.",
            "nums.insert(0, 5)",
        ),
    ],
    "extend": [
        (
            "Suppose nums = [1, 2] and more = [3, 4]. In one line on nums, add every element from more to the end of nums.",
            "nums.extend(more)",
        ),
        (
            "Suppose nums = [10] and more = [20, 30]. In one line on nums, add every element from more to the end of nums.",
            "nums.extend(more)",
        ),
    ],
    "append": [
        ("Suppose nums = [1, 2]. Add 3 as one new item after the current last position.", "nums.append(3)"),
        ("Suppose nums = [0]. Add the value 1 as one new item after the current last position.", "nums.append(1)"),
    ],
}

# ---------------------------------------------------------------------------
# Segments 11–13: remove, pop, clear (pick 1)
# ---------------------------------------------------------------------------
REMOVE_BY_KIND = {
    "remove": [
        ("Suppose nums = [1, 2, 3, 2]. Remove the first occurrence of the value 2.", "nums.remove(2)"),
        ("Suppose nums = [9, 8, 9]. Remove the first occurrence of the value 9.", "nums.remove(9)"),
    ],
    "pop": [
        (
            "Suppose nums = [9, 8, 7]. Remove the last item and assign what was removed to a variable named t.",
            "t = nums.pop()",
        ),
        (
            "Suppose nums = [1, 2, 3]. Remove the item at index 1 and assign what was removed to a variable named t.",
            "t = nums.pop(1)",
        ),
    ],
    "clear": [
        ("Suppose nums = [1, 2, 3]. Remove all items so the list becomes empty.", "nums.clear()"),
        ("Suppose nums = [0]. Remove all items so the list becomes empty.", "nums.clear()"),
    ],
}

# ---------------------------------------------------------------------------
# Segments 14–15: list comprehensions (pick 1)
# ---------------------------------------------------------------------------
COMP_BY_KIND = {
    "comp1": [
        (
            "Suppose nums = [1, 2, 3, 4]. Store in doubles a new list built from nums with each element multiplied by 2. "
            "Name the loop variable over nums n.",
            "doubles = [n * 2 for n in nums]",
        ),
        (
            "Suppose nums = [10, 20, 30]. Store in triples a new list where each element is three times the original. "
            "Name the loop variable over nums n.",
            "triples = [n * 3 for n in nums]",
        ),
    ],
    "comp2": [
        (
            "Suppose nums = [1, 2, 3, 4, 5]. Store in big a new list of every element from nums that is greater than 2. "
            "Name the loop variable over nums n.",
            "big = [n for n in nums if n > 2]",
        ),
        (
            "Suppose nums = [2, 3, 4, 5]. Store in evens a new list of every element from nums that is divisible by 2. "
            "Name the loop variable over nums n.",
            "evens = [n for n in nums if n % 2 == 0]",
        ),
    ],
}

# ---------------------------------------------------------------------------
# Segments 16–18: sort reverse, sort key, reverse (pick 2)
# ---------------------------------------------------------------------------
SORT_BY_KIND = {
    "sort_reversed": [
        (
            "Suppose nums = [3, 1, 2]. Sort nums in place so the order becomes highest to lowest.",
            "nums.sort(reverse=True)",
        ),
        (
            "Suppose nums = [10, 5, 20]. Sort nums in place so the largest values come first.",
            "nums.sort(reverse=True)",
        ),
    ],
    "sort_key": [
        (
            "Suppose words = [\"aaa\", \"bb\", \"c\"]. Sort words in place by increasing length.",
            "words.sort(key=len)",
        ),
        (
            "Suppose scores = [-5, 2, -1, 4]. Sort scores in place by distance from zero (use a built-in as the key).",
            "scores.sort(key=abs)",
        ),
    ],
    "reverse": [
        ("Suppose nums = [1, 2, 3]. Reverse nums in place.", "nums.reverse()"),
        ("Suppose nums = [4, 5, 6]. Reverse nums in place.", "nums.reverse()"),
    ],
}

# ---------------------------------------------------------------------------
# Segments 19–20: copy and join (both every session)
# ---------------------------------------------------------------------------
POOL_COPY = [
    ("Suppose nums = [1, 2, 3]. Store a shallow duplicate in a variable named b.", "b = nums.copy()"),
    ("Suppose nums = [0, 1]. Store a shallow duplicate in a variable named b.", "b = nums.copy()"),
]

POOL_JOIN = [
    ("Suppose a = [1, 2] and b = [3, 4]. Store a new list that is a followed by b in a variable named out.", "out = a + b"),
    ("Suppose a = [0] and b = [1, 2]. Store a new list that is a followed by b in a variable named out.", "out = a + b"),
]


def _pick_batch4_session():
    """
    12 exercises per session:
      2 of 4 kinds from ACCESS_BY_KIND
      2 of 3 kinds from CHANGE_BY_KIND
      2 of 3 kinds from ADD_BY_KIND
      1 of 3 kinds from REMOVE_BY_KIND
      1 of 2 kinds from COMP_BY_KIND
      2 of 3 kinds from SORT_BY_KIND
      both COPY and JOIN (one variant each)
    """
    exercises = []

    access_kinds = random.sample(list(ACCESS_BY_KIND.keys()), 2)
    for k in access_kinds:
        q, e = random.choice(ACCESS_BY_KIND[k])
        exercises.append(_make_exercise(q, e))

    change_kinds = random.sample(list(CHANGE_BY_KIND.keys()), 2)
    for k in change_kinds:
        q, e = random.choice(CHANGE_BY_KIND[k])
        exercises.append(_make_exercise(q, e))

    add_kinds = random.sample(list(ADD_BY_KIND.keys()), 2)
    for k in add_kinds:
        q, e = random.choice(ADD_BY_KIND[k])
        exercises.append(_make_exercise(q, e))

    remove_kind = random.choice(list(REMOVE_BY_KIND.keys()))
    q, e = random.choice(REMOVE_BY_KIND[remove_kind])
    exercises.append(_make_exercise(q, e))

    comp_kind = random.choice(list(COMP_BY_KIND.keys()))
    q, e = random.choice(COMP_BY_KIND[comp_kind])
    exercises.append(_make_exercise(q, e))

    sort_kinds = random.sample(list(SORT_BY_KIND.keys()), 2)
    for k in sort_kinds:
        q, e = random.choice(SORT_BY_KIND[k])
        exercises.append(_make_exercise(q, e))

    q, e = random.choice(POOL_COPY)
    exercises.append(_make_exercise(q, e))
    q, e = random.choice(POOL_JOIN)
    exercises.append(_make_exercise(q, e))

    return exercises


class Batch4Exercises:
    """Batch 4 — Lists. 12 questions per session (segment rules above)."""

    EXERCISES_PER_SESSION = 12
    MAX_MISTAKES_PER_EXERCISE = 3

    def start_exercises(self):
        print_session_header("PYTHON BASICS - LISTS (BATCH 4)")
        print("\nYou will get 12 single-line code questions on lists.")
        print("Each line should be valid Python. Three wrong attempts skip to the next question.\n")

        input("Press Enter to start...")

        exercises = _pick_batch4_session()
        completed, not_completed = run_simple_exercises(
            exercises,
            max_mistakes=self.MAX_MISTAKES_PER_EXERCISE,
        )
        print_session_footer(completed, not_completed)