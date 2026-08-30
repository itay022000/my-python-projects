"""
Bar Plot Exercises Module
Handles all bar plot exercise generation, verification, and execution.
"""

import random
import re

from hints import (
    HINT_HEIGHTS_ARRAY,
    HINT_LABELS_ARRAY,
    HINT_PLT_BAR,
)
from session_common import (
    SESSION_INTRO_LINE,
    print_step_header,
    print_sequence_intro,
)
from engine import (
    DEFAULT_COLORS,
    SHOW_ANSWER,
    SeriesContext,
    SeriesOutcome,
    format_np_int_array,
    format_np_str_array,
    normalize_code,
    run_step,
    verify_step_show,
)
from exercise_session import run_exercise_sequence


class BarPlotExercises:
    """
    Class for handling bar plot exercises.
    """
    
    def __init__(self):
        self.car_companies = [
            "mercedes", "bmw", "audi", "jaguar", "toyota", "honda",
            "ford", "chevrolet", "volkswagen", "porsche", "ferrari",
            "lamborghini", "tesla", "nissan", "lexus", "mazda"
        ]
        self.colors_list = DEFAULT_COLORS
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 bar plot exercises."""
        self.exercises = []
        for i in range(3):
            # Step 1: 5 random car company names for labels
            labels = random.sample(self.car_companies, 5)
            
            # Step 2: 5 random integers in range [1, 10] for heights
            heights = [random.randint(1, 10) for _ in range(5)]
            
            # Step 3: 
            # Exercise 1 (index 0): plt.bar(x, y)
            # Exercise 2 (index 1): plt.bar(x, y, width="double")
            # Exercise 3 (index 2): plt.barh(x, y, color="color", height="double")
            
            has_width = (i == 1)  # Exercise 2 has width parameter
            is_horizontal = (i == 2)  # Exercise 3 is horizontal bar
            width = None
            color = None
            height = None
            
            if has_width:
                # Generate a value from 0.01 to 1.00 with 0.01 step
                width_value = random.randint(1, 100) / 100.0  # This gives 0.01, 0.02, ..., 1.00
                width = round(width_value, 2)
            
            if is_horizontal:
                # Generate random color from color list
                color = random.choice(self.colors_list)
                # Generate a value from 0.01 to 1.00 with 0.01 step for height
                height_value = random.randint(1, 100) / 100.0  # This gives 0.01, 0.02, ..., 1.00
                height = round(height_value, 2)
            
            exercise = {
                'number': i + 1,
                'labels': labels,
                'heights': heights,
                'has_width': has_width,
                'width': width,
                'is_horizontal': is_horizontal,
                'color': color,
                'height': height
            }
            self.exercises.append(exercise)
    
    
    def verify_step1(self, user_input, labels):
        """Verify Step 1: labels array with capital letters."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'x\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"
        
        # Extract array values - labels are strings, must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            # Extract quoted strings exactly
            values = re.findall(r"['\"]([^'\"]+)['\"]", values_str)
            
            if len(values) != len(labels):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != labels:
                return False, "Invalid format"
            
            return True, "Correct!"
        except Exception as e:
            return False, "Invalid format"
    
    def verify_step2(self, user_input, heights):
        """Verify Step 2: heights array with integers."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'y\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'y'"
        
        # Extract array values - heights are integers, must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(heights):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != heights:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step3(self, user_input, has_width, width, is_horizontal, color, height):
        """Verify Step 3: plt.bar() or plt.barh() call with optional parameters."""
        normalized_input = normalize_code(user_input)
        
        if is_horizontal:
            # Exercise 3: horizontal bar with color and height
            # Must use exact function name plt.barh (not plt.bar, not plt.barheight, etc.)
            if not re.search(r'\bplt\.barh\s*\(', normalized_input, re.IGNORECASE):
                return False, "Invalid format"
            
            # Ensure it's not plt.bar (must be plt.barh)
            if re.search(r'\bplt\.bar\s*\(', normalized_input, re.IGNORECASE) and not re.search(r'\bplt\.barh\s*\(', normalized_input, re.IGNORECASE):
                return False, "Invalid format"
            
            # Extract the plt.barh() call parameters
            bar_match = re.search(r'plt\.barh\s*\((.*?)\)', normalized_input, re.IGNORECASE)
            if not bar_match:
                return False, "Invalid format"
            
            params = bar_match.group(1)
            
            # Check for "x" as first positional argument - must be exactly "x"
            if not re.search(r'(?:^\s*|\W)x(?:\s*[,=]|\s*\Z)', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for "y" as second positional argument - must be exactly "y"
            if not re.search(r'\by\b', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for color parameter - must be exactly "color" (not "colors", "colours", etc.)
            if color is not None:
                # Must have exactly color="color" or color='color' with exact color name
                color_pattern = rf'\bcolor\s*=\s*["\']{re.escape(color)}["\']'
                if not re.search(color_pattern, params, re.IGNORECASE):
                    return False, "Invalid format"
            
            # Check for height parameter - must be exactly "height" (not "heights", "hight", etc.)
            if height is not None:
                # Extract height value from the parameters - must be exactly "height="
                height_match = re.search(r'\bheight\s*=\s*([\d.]+)', params, re.IGNORECASE)
                if not height_match:
                    return False, "Invalid format"
                
                try:
                    height_value = float(height_match.group(1))
                    # Compare with tolerance for floating point precision
                    if abs(height_value - height) > 0.001:
                        return False, "Invalid format"
                except ValueError:
                    return False, "Invalid format"
        
        else:
            # Exercise 1 or 2: vertical bar
            # Must use exact function name plt.bar (not plt.barh, not plt.bars, etc.)
            if not re.search(r'\bplt\.bar\s*\(', normalized_input, re.IGNORECASE):
                return False, "Invalid format"
            
            # Ensure it's not plt.barh (must be plt.bar)
            if re.search(r'\bplt\.barh\s*\(', normalized_input, re.IGNORECASE):
                return False, "Invalid format"
            
            # Extract the plt.bar() call parameters
            bar_match = re.search(r'plt\.bar\s*\((.*?)\)', normalized_input, re.IGNORECASE)
            if not bar_match:
                return False, "Invalid format"
            
            params = bar_match.group(1)
            
            # Check for "x" as first positional argument - must be exactly "x"
            if not re.search(r'(?:^\s*|\W)x(?:\s*[,=]|\s*\Z)', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for "y" as second positional argument - must be exactly "y"
            if not re.search(r'\by\b', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for width parameter if required - must be exactly "width" (not "widths", "widht", etc.)
            if has_width and width is not None:
                # Extract width value from the parameters - must be exactly "width="
                width_match = re.search(r'\bwidth\s*=\s*([\d.]+)', params, re.IGNORECASE)
                if not width_match:
                    return False, "Invalid format"
                
                try:
                    width_value = float(width_match.group(1))
                    # Compare with tolerance for floating point precision
                    if abs(width_value - width) > 0.001:
                        return False, "Invalid format"
                except ValueError:
                    return False, "Invalid format"
            elif has_width:
                # Should not reach here, but just in case
                return False, "Invalid format"
        
        return True, "Correct!"

    def _expected_step1(self, exercise: dict) -> str:
        return format_np_str_array("x", exercise["labels"])

    def _expected_step2(self, exercise: dict) -> str:
        return format_np_int_array("y", exercise["heights"])

    def _expected_step3(self, exercise: dict) -> str:
        if exercise["is_horizontal"]:
            return (
                f'plt.barh(x, y, color="{exercise["color"]}", '
                f'height={exercise["height"]})'
            )
        if exercise["has_width"]:
            return f'plt.bar(x, y, width={exercise["width"]})'
        return "plt.bar(x, y)"

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single bar plot series."""
        ctx = SeriesContext()
        titles = {
            1: "Series 1: Bar Plot (basic)",
            2: "Series 2: Bar Plot (width)",
            3: "Series 3: Bar Plot (horizontal)",
        }
        contexts = {
            1: "In this series, you will create a basic bar plot.",
            2: "In this series, you will create a basic bar plot with a given bar width.",
            3: "In this series, you will create a horizontal bar plot with given bar color and height (thickness).",
        }
        print("\n" + "="*70)
        print(titles[exercise["number"]])
        print("="*70)
        print(contexts[exercise["number"]])
        print()
        print("Use the following specifications:")
        labels_str = ', '.join(exercise['labels'])
        heights_str = ', '.join(map(str, exercise['heights']))
        print(f"- Bar labels (x-axis): {labels_str}")
        print(f"- Bar heights (y-axis): {heights_str}")

        if exercise['has_width']:
            print(f"- Bar width: {exercise['width']}")

        if exercise['is_horizontal']:
            print(f"- Bar color: {exercise['color']}")
            print(f"- Bar height: {exercise['height']}")

        print("\nYou need to complete the following steps:\n")

        total_steps = 4
        print_step_header(1, total_steps, "Define the bar labels array", first=True)
        print("Variable name must be: x")
        if not run_step(
            ctx,
            lambda ui: self.verify_step1(ui, exercise["labels"]),
            correct_answer=self._expected_step1(exercise),
            hint=HINT_LABELS_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the bar heights array")
        print("Variable name must be: y")
        if not run_step(
            ctx,
            lambda ui: self.verify_step2(ui, exercise["heights"]),
            correct_answer=self._expected_step2(exercise),
            hint=HINT_HEIGHTS_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Plot the bar")
        if exercise['has_width']:
            print(f"   Remember to include width={exercise['width']}")
        if exercise['is_horizontal']:
            print(
                f"   Remember to include color=\"{exercise['color']}\" "
                f"and height={exercise['height']}"
            )
        if not run_step(
            ctx,
            lambda ui: self.verify_step3(
                ui,
                exercise["has_width"],
                exercise.get("width"),
                exercise["is_horizontal"],
                exercise.get("color"),
                exercise.get("height"),
            ),
            correct_answer=self._expected_step3(exercise),
            hint=HINT_PLT_BAR,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(4, total_steps, "Show the plot")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED

        return ctx.finish()
    
    def start_exercises(self):
        """Start the bar plot exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Bar Plot Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)

