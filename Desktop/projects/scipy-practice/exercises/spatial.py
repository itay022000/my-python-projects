"""SciPy exercise: spatial."""

import numpy as np
from scipy.spatial import distance

from engine import Question
from exercise_session import run_exercise_questions
from hints import (
    HINT_SPATIAL_CHEBYSHEV,
    HINT_SPATIAL_CITYBLOCK,
    HINT_SPATIAL_EUCLIDEAN,
    HINT_SPATIAL_MINKOWSKI,
    HINT_SPATIAL_PDIST,
)
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_spatial_practice():
    p1 = np.array([0, 0])
    p2 = np.array([5, 12])
    p3 = np.array([1, 2])
    p4 = np.array([4, 6])
    p5 = np.array([2, 3])
    p6 = np.array([5, 7])
    p7 = np.array([1, 1])
    p8 = np.array([4, 5])
    points_array = np.array([[0, 0], [1, 1], [4, 5]])

    namespace = {
        "distance": distance,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
        "p6": p6,
        "p7": p7,
        "p8": p8,
        "points_array": points_array,
        "np": np,
    }

    def check1(result):
        correct = distance.euclidean(p1, p2)
        if abs(float(result) - correct) < 0.01:
            return True, f"Euclidean distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check2(result):
        correct = distance.cityblock(p3, p4)
        if abs(float(result) - correct) < 0.01:
            return True, f"Manhattan distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check3(result):
        correct = distance.chebyshev(p5, p6)
        if abs(float(result) - correct) < 0.01:
            return True, f"Chebyshev distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check4(result):
        correct = distance.pdist(points_array, metric="euclidean")
        if np.allclose(result, correct):
            return True, f"Pairwise distances computed for {len(points_array)} points"
        return False, "Expected pairwise distance array"

    def check5(result):
        correct = distance.minkowski(p7, p8, p=3)
        if abs(float(result) - correct) < 0.01:
            return True, f"Minkowski distance (p=3): {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    questions = [
        Question(
            "Calculate the Euclidean distance between p1 (0, 0) and p2 (5, 12)",
            check1,
            HINT_SPATIAL_EUCLIDEAN,
            correct_answer="distance.euclidean(p1, p2)",
        ),
        Question(
            "Calculate the Manhattan distance between p3 (1, 2) and p4 (4, 6)",
            check2,
            HINT_SPATIAL_CITYBLOCK,
            correct_answer="distance.cityblock(p3, p4)",
        ),
        Question(
            "Calculate the Chebyshev distance between p5 (2, 3) and p6 (5, 7)",
            check3,
            HINT_SPATIAL_CHEBYSHEV,
            correct_answer="distance.chebyshev(p5, p6)",
        ),
        Question(
            "Calculate pairwise Euclidean distances for points_array [[0, 0], [1, 1], [4, 5]]",
            check4,
            HINT_SPATIAL_PDIST,
            correct_answer="distance.pdist(points_array, metric='euclidean')",
        ),
        Question(
            "Calculate the Minkowski distance between p7 (1, 1) and p8 (4, 5) with p=3",
            check5,
            HINT_SPATIAL_MINKOWSKI,
            correct_answer="distance.minkowski(p7, p8, p=3)",
        ),
    ]
    return namespace, questions




def exercise_spatial():
    """Practice with scipy.spatial (excluding cosine distance)."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Spatial Data Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_spatial_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['spatial'],
    )

