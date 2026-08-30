"""SciPy exercise: constants."""

import numpy as np
import scipy.constants as const

from engine import Question
from exercise_session import run_exercise_questions
from hints import (
    HINT_CONSTANTS_1,
    HINT_CONSTANTS_2,
    HINT_CONSTANTS_3,
    HINT_CONSTANTS_4,
    HINT_CONSTANTS_5,
)
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_constants_practice():
    namespace = {"const": const, "np": np}

    def check1(result):
        correct = 12 * const.inch
        if abs(float(result) - correct) < 0.01:
            return True, f"12 inches = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check2(result):
        correct = 5 * const.mile
        if abs(float(result) - correct) < 0.01:
            return True, f"5 miles = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check3(result):
        correct = 10 * const.foot
        if abs(float(result) - correct) < 0.01:
            return True, f"10 feet = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check4(result):
        correct = 3 * const.minute
        if abs(float(result) - correct) < 0.01:
            return True, f"3 minutes = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"

    def check5(result):
        correct = 2 * const.hour
        if abs(float(result) - correct) < 0.01:
            return True, f"2 hours = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"

    questions = [
        Question(
            "Convert 12 inches to meters",
            check1,
            HINT_CONSTANTS_1,
            correct_answer="12 * const.inch",
        ),
        Question(
            "Convert 5 miles to meters",
            check2,
            HINT_CONSTANTS_2,
            correct_answer="5 * const.mile",
        ),
        Question(
            "Convert 10 feet to meters",
            check3,
            HINT_CONSTANTS_3,
            correct_answer="10 * const.foot",
        ),
        Question(
            "Convert 3 minutes to seconds",
            check4,
            HINT_CONSTANTS_4,
            correct_answer="3 * const.minute",
        ),
        Question(
            "Convert 2 hours to seconds",
            check5,
            HINT_CONSTANTS_5,
            correct_answer="2 * const.hour",
        ),
    ]
    return namespace, questions


def exercise_constants():
    """Practice with scipy.constants."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Constants Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_constants_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['constants'],
        after_background=(
            "Note: For all questions, both '(number) * (constant)' and "
            "'(constant) * (number)' are accepted."
        ),
    )

