"""
Histogram Exercises Module
Handles all histogram exercise generation, verification, and execution.
"""

import random
import re

from hints import (
    HINT_NP_RANDOM_NORMAL,
    HINT_PLT_HIST,
)
from session_common import (
    SESSION_INTRO_LINE,
    print_step_header,
    print_sequence_intro,
)
from engine import (
    SHOW_ANSWER,
    SeriesContext,
    SeriesOutcome,
    format_np_int_array,
    normalize_code,
    run_step,
    verify_step_show,
)
from exercise_session import run_exercise_sequence


class HistogramExercises:
    """Class for handling histogram exercises."""

    def __init__(self):
        self.exercises = []
        self.generate_exercises()

    def generate_exercises(self):
        """Generate 3 histogram exercises."""
        self.exercises = []
        for i in range(3):
            exercise = {
                "number": i + 1,
                "mean": random.randint(100, 300),
                "std": random.randint(50, 100),
                "size": random.randint(100, 300),
            }
            self.exercises.append(exercise)

    def verify_step1(self, user_input, mean, std, size):
        """Verify Step 1: Create data using np.random.normal."""
        normalized_input = normalize_code(user_input)

        if not re.match(r"x\s*=", normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"

        if not re.search(r"\bnp\.random\.normal\s*\(", normalized_input, re.IGNORECASE):
            return False, "Should use np.random.normal()"

        normal_match = re.search(
            r"np\.random\.normal\s*\(\s*([^)]+)\s*\)", normalized_input, re.IGNORECASE
        )
        if not normal_match:
            return False, "Invalid format"

        params = [p.strip() for p in normal_match.group(1).split(",")]
        if len(params) != 3:
            return False, "Invalid format"

        try:
            param1, param2, param3 = int(params[0]), int(params[1]), int(params[2])
            if param1 != mean or param2 != std or param3 != size:
                return False, "Incorrect values or order"
            return True, "Correct!"
        except (ValueError, Exception):
            return False, "Invalid format"

    def verify_step2(self, user_input):
        """Verify Step 2: plt.hist(x)."""
        normalized_input = normalize_code(user_input)
        if normalized_input.lower() != "plt.hist(x)":
            return False, "Invalid format"
        return True, "Correct!"

    def _expected_step1(self, exercise: dict) -> str:
        e = exercise
        return f"x = np.random.normal({e['mean']}, {e['std']}, {e['size']})"

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single histogram series."""
        ctx = SeriesContext()
        print("\n" + "=" * 70)
        print(f"Series {exercise['number']}: Histogram")
        print("=" * 70)
        print("In this series, you will create a basic histogram.")
        print()
        print("Use the following specification:")
        print(
            f"- Use np.random.normal with mean={exercise['mean']}, "
            f"std={exercise['std']}, size={exercise['size']}"
        )
        print("\nYou need to complete the following steps:\n")

        total_steps = 3
        print_step_header(1, total_steps, "Create the data array", first=True)
        print("Variable name must be: x")
        if not run_step(
            ctx,
            lambda ui: self.verify_step1(
                ui, exercise["mean"], exercise["std"], exercise["size"]
            ),
            correct_answer=self._expected_step1(exercise),
            hint=HINT_NP_RANDOM_NORMAL,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Plot the histogram")
        if not run_step(
            ctx,
            self.verify_step2,
            correct_answer="plt.hist(x)",
            hint=HINT_PLT_HIST,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Show the histogram")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED

        return ctx.finish()

    def start_exercises(self):
        """Start the histogram exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Histogram Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)
