"""SciPy exercise: optimize."""

from scipy import optimize
import numpy as np

from engine import Question
from exercise_session import run_exercise_questions
from exercises._checks import _minimize_result_ok, _root_result_ok
from hints import HINT_OPTIMIZE_MINIMIZE, HINT_OPTIMIZE_ROOT
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_optimize_practice():
    def h(x):
        return x**2 - 9

    def linear(x):
        return x - 5

    def quad(x):
        return x**2 - 4 * x + 3

    def cubic(x):
        return x**3 - 2 * x - 5

    def g(x):
        return x**2 + 2 * x + 1

    namespace = {
        "optimize": optimize,
        "h": h,
        "linear": linear,
        "quad": quad,
        "cubic": cubic,
        "g": g,
        "np": np,
    }

    questions = [
        Question(
            "For linear(x) = x - 5, find the root near x0=0",
            _root_result_ok,
            HINT_OPTIMIZE_ROOT,
            correct_answer="optimize.root(linear, x0=0.0)",
        ),
        Question(
            "For quad(x) = x² - 4x + 3, find the minimum near x0=0",
            _minimize_result_ok,
            HINT_OPTIMIZE_MINIMIZE,
            correct_answer="optimize.minimize(quad, x0=0.0)",
        ),
        Question(
            "For h(x) = x² - 9, find the root near x0=3",
            _root_result_ok,
            HINT_OPTIMIZE_ROOT,
            correct_answer="optimize.root(h, x0=3.0)",
        ),
        Question(
            "For g(x) = x² + 2x + 1, find the minimum near x0=0",
            _minimize_result_ok,
            HINT_OPTIMIZE_MINIMIZE,
            correct_answer="optimize.minimize(g, x0=0.0)",
        ),
        Question(
            "For cubic(x) = x³ - 2x - 5, find the root near x0=2",
            _root_result_ok,
            HINT_OPTIMIZE_ROOT,
            correct_answer="optimize.root(cubic, x0=2.0)",
        ),
    ]
    return namespace, questions




def exercise_optimize():
    """Practice with scipy.optimize - root finding and minimization."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Optimization Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_optimize_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['optimize'],
    )

