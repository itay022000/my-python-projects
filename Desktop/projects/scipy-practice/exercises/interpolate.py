"""SciPy exercise: interpolate."""

import numpy as np
from scipy import interpolate

from engine import Question
from exercise_session import run_exercise_questions
from hints import (
    HINT_INTERPOLATE_CUBIC,
    HINT_INTERPOLATE_LINEAR,
    HINT_INTERPOLATE_NEAREST,
    HINT_INTERPOLATE_QUADRATIC,
)
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_interpolate_practice():
    x_points = np.array([0, 1, 2])
    y_points = np.array([0, 1, 4])
    x_points2 = np.array([0, 1, 2, 3, 4])
    y_points2 = np.array([0, 1, 4, 9, 16])

    namespace = {
        "interpolate": interpolate,
        "x_points": x_points,
        "y_points": y_points,
        "x_points2": x_points2,
        "y_points2": y_points2,
        "np": np,
    }

    def check1(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind="linear")
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Linear interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check2(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind="quadratic")
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Quadratic interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check3(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind="cubic")
        if callable(result):
            test_val = 2.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Cubic interpolation function created"
            return False, f"Expected value at x=2.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check4(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind="nearest")
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Nearest interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    questions = [
        Question(
            "Create a linear interpolation function for x_points and y_points",
            check1,
            HINT_INTERPOLATE_LINEAR,
            correct_answer="interpolate.interp1d(x_points, y_points, kind='linear')",
        ),
        Question(
            "Create a quadratic interpolation function for x_points2 and y_points2",
            check2,
            HINT_INTERPOLATE_QUADRATIC,
            correct_answer="interpolate.interp1d(x_points2, y_points2, kind='quadratic')",
        ),
        Question(
            "Create a cubic interpolation function for x_points2 and y_points2",
            check3,
            HINT_INTERPOLATE_CUBIC,
            correct_answer="interpolate.interp1d(x_points2, y_points2, kind='cubic')",
        ),
        Question(
            "Create a nearest interpolation function for x_points and y_points",
            check4,
            HINT_INTERPOLATE_NEAREST,
            correct_answer="interpolate.interp1d(x_points, y_points, kind='nearest')",
        ),
    ]
    return namespace, questions




def exercise_interpolate():
    """Practice with scipy.interpolate."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Interpolation Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_interpolate_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['interpolate'],
    )

