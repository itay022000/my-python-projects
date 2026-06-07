"""
Histogram Exercises Module
Handles all histogram exercise generation, verification, and execution.
"""

import random
import re

from exercise_common import (
    normalize_code,
    print_sequence_intro,
    prompt_code_step,
    run_exercise_sequence,
    verify_step_show,
)


class HistogramExercises:
    """Class for handling histogram exercises."""

    def __init__(self):
        self.exercises = []
        self.generate_exercises()

    def generate_exercises(self):
        """Generate 3 histogram exercises."""
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

    def run_exercise(self, exercise, is_last):
        """Run a single histogram exercise. Returns True if completed, False if skipped."""
        print("\n" + "=" * 70)
        print(f"EXERCISE {exercise['number']}: Histogram")
        print("=" * 70)
        print("\nCreate a histogram with the following specifications:")
        print(
            f"- Use np.random.normal with mean={exercise['mean']}, "
            f"std={exercise['std']}, size={exercise['size']}"
        )
        print("\nYou need to complete the following steps:\n")

        mistake_count = 0

        print("STEP 1: Create the data array")
        print("   Variable name must be: x")
        ok, mistake_count = prompt_code_step(
            lambda ui: self.verify_step1(
                ui, exercise["mean"], exercise["std"], exercise["size"]
            ),
            mistake_count,
            is_last,
        )
        if not ok:
            return False

        print("STEP 2: Plot the histogram")
        ok, mistake_count = prompt_code_step(
            self.verify_step2, mistake_count, is_last
        )
        if not ok:
            return False

        print("STEP 3: Show the histogram")
        ok, mistake_count = prompt_code_step(
            verify_step_show, mistake_count, is_last
        )
        if not ok:
            return False

        print(f"🎉 Exercise {exercise['number']} completed successfully!")
        return True

    def start_exercises(self):
        """Start the histogram exercises sequence."""
        print_sequence_intro(
            "MATPLOTLIB PYPLOT PRACTICE - HISTOGRAM EXERCISES",
            "This program contains 3 consecutive exercises for practicing\n"
            "matplotlib.pyplot histograms. Complete each exercise step by step.",
        )
        run_exercise_sequence(self.exercises, self.run_exercise)
