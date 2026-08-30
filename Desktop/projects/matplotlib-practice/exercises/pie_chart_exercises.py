"""
Pie Chart Exercises Module
Handles all pie chart exercise generation, verification, and execution.
"""

import random
import re

from hints import (
    HINT_NP_ARRAY,
    HINT_PLT_LEGEND,
    HINT_PLT_PIE,
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


class PieChartExercises:
    """
    Class for handling pie chart exercises.
    """
    
    def __init__(self):
        self.colors_list = DEFAULT_COLORS
        self.fruit_names = [
            "apple", "banana", "cherry", "date", "strawberry",
            "fig", "grape", "honeydew", "kiwi", "lemon"
        ]
        self.exercises = []
        self.generate_exercises()
    
    def generate_proportions(self):
        """Generate 5 proportions that sum to 100. All must be positive integers (>= 1)."""
        # Generate 5 random positive integers that sum to 95
        # Then add 1 to each to ensure all are >= 1 and sum to 100
        
        remaining = 95  # 100 - 5 (minimum of 1 for each of 5 values)
        values = []
        current_sum = 0
        
        # Generate first 4 values
        for i in range(4):
            # Maximum value for this position ensures we can fill remaining positions
            # with at least 0 each (we'll add 1 later)
            max_val = remaining - current_sum - (4 - i)
            if max_val < 0:
                max_val = 0
            # Generate value between 0 and max_val
            value = random.randint(0, max_val)
            values.append(value)
            current_sum += value
        
        # The 5th value is what's left
        fifth_value = remaining - current_sum
        values.append(fifth_value)
        
        # Now add 1 to each value to ensure all are >= 1 and sum to 100
        values = [v + 1 for v in values]
        
        # Shuffle to avoid predictable order
        random.shuffle(values)
        
        # Verify all constraints
        assert all(v >= 1 for v in values), "All proportions must be >= 1"
        assert sum(values) == 100, f"Proportions must sum to 100, got {sum(values)}"
        
        return values
    
    def generate_explode(self):
        """Generate 5 explode rates (floats, 0 or small positive)."""
        return [round(random.choice([0, random.uniform(0.05, 0.15)]), 2) for _ in range(5)]
    
    def generate_exercises(self):
        """Generate 3 pie chart exercises (fixed feature ladder; random data)."""
        self.exercises = []
        # 6.1 explode+legend · 6.2 +shadow · 6.3 +legend title
        for i in range(3):
            proportions = self.generate_proportions()
            colors = random.sample(self.colors_list, 5)
            labels = random.sample(self.fruit_names, 5)

            has_explode = True
            has_legend = True
            has_shadow = i >= 1
            legend_title = "fruits" if i == 2 else None
            explode = self.generate_explode()

            exercise = {
                'number': i + 1,
                'proportions': proportions,
                'colors': colors,
                'labels': labels,
                'has_legend': has_legend,
                'has_shadow': has_shadow,
                'legend_title': legend_title,
                'has_explode': has_explode,
                'explode': explode
            }
            self.exercises.append(exercise)
    
    
    def verify_step1(self, user_input, proportions):
        """Verify Step 1: proportions array."""
        normalized_input = normalize_code(user_input)
        
        # Build exact expected format
        proportions_str = '[' + ', '.join(map(str, proportions)) + ']'
        expected = f"x=np.array({proportions_str})"
        normalized_expected = normalize_code(expected)
        
        # Check variable name exactly
        if not re.match(r'x\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Should use np.array([...]) format"
        
        try:
            # Parse the array values exactly as they appear
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            # Check exact match in exact order
            if values != proportions:
                return False, "Incorrect values or order"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception as e:
            return False, "Invalid format"
    
    def verify_step2(self, user_input, colors):
        """Verify Step 2: colors array."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'c\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'c'"
        
        # Extract array values - colors are strings, must be in exact order
        array_match = re.search(r'np\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Should use np.array([...]) format"
        
        try:
            values_str = array_match.group(1)
            # Extract quoted strings exactly
            # Match 'color' or "color" patterns
            values = re.findall(r"['\"]([^'\"]+)['\"]", values_str)
            
            if len(values) != len(colors):
                return False, "Incorrect number of colors"
            
            # Check exact match in exact order
            if values != colors:
                return False, "Incorrect colors or order"
            
            return True, "Correct!"
        except Exception as e:
            return False, "Invalid format"
    
    def verify_step3(self, user_input, labels):
        """Verify Step 3: labels array."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'lb\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'lb'"
        
        # Extract array values - labels are strings, must be in exact order
        array_match = re.search(r'np\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Should use np.array([...]) format"
        
        try:
            values_str = array_match.group(1)
            # Extract quoted strings exactly
            values = re.findall(r"['\"]([^'\"]+)['\"]", values_str)
            
            if len(values) != len(labels):
                return False, "Incorrect number of labels"
            
            # Check exact match in exact order
            if values != labels:
                return False, "Incorrect labels or order"
            
            return True, "Correct!"
        except Exception as e:
            return False, "Invalid format"
    
    def verify_step_explode(self, user_input, explode):
        """Verify explode array. Variable name must be ex."""
        normalized_input = normalize_code(user_input)
        
        if not re.match(r'ex\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'ex'"
        
        array_match = re.search(r'np\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Should use np.array([...]) format"
        
        try:
            values_str = array_match.group(1)
            values = [float(x.strip()) for x in values_str.split(',')]
            if len(values) != 5:
                return False, "Incorrect number of values"
            # Compare rounded to 2 decimals (explode can be 0, 0.05, 0.1, etc.)
            if [round(v, 2) for v in values] != [round(e, 2) for e in explode]:
                return False, "Incorrect values or order"
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step4(self, user_input, has_shadow, has_explode):
        """Verify plt.pie() call with optional shadow and explode."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.pie (not plt.pies, plt.pied, etc.)
        if not re.search(r'\bplt\.pie\s*\(', normalized_input, re.IGNORECASE):
            return False, "Should call plt.pie()"
        
        # Extract the plt.pie() call parameters
        pie_match = re.search(r'plt\.pie\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not pie_match:
            return False, "Invalid format"
        
        params = pie_match.group(1)
        
        # Check for exact keyword parameter names AND exact variable names
        # Must have exactly "labels=lb" (not "lables=lb" or "labels=labels")
        # Must have exactly "colors=c" (not "color=c" or "colors=colors")
        # Must have exactly "explode=ex" if required (not "explodes=ex")
        
        # Check for "labels=lb" - parameter name must be exactly "labels", variable must be exactly "lb"
        if not re.search(r'\blabels\s*=\s*lb\b', params, re.IGNORECASE):
            return False, "Should use the lb variable"
        
        # Check for "colors=c" - parameter name must be exactly "colors", variable must be exactly "c"
        if not re.search(r'\bcolors\s*=\s*c\b', params, re.IGNORECASE):
            return False, "Should use the c variable"
        
        # Check for "x" as first positional argument or "x="
        # x must be exactly "x" (standalone or as parameter)
        if not re.search(r'(?:^\s*|\W)x(?:\s*[,=]|\s*\Z)', params, re.IGNORECASE):
            return False, "Should use the x variable"
        
        # Check for "explode=ex" if required - parameter name must be exactly "explode", variable must be exactly "ex"
        if has_explode:
            if not re.search(r'\bexplode\s*=\s*ex\b', params, re.IGNORECASE):
                return False, "Should use the ex variable"
        
        # Check for shadow=True if required - Python boolean is case-sensitive, must be "True" not "true"
        if has_shadow and 'shadow=True' not in normalized_input:
            return False, "Should include shadow=True parameter"
        
        return True, "Correct!"
    
    def verify_step5(self, user_input, has_legend, legend_title):
        """Verify plt.legend() - with or without title."""
        if not has_legend:
            return True, "This step is not required for this exercise."
        
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.legend (not plt.legends, plt.legand, etc.)
        if not re.search(r'\bplt\.legend\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        if legend_title:
            # Must have title="fruits" - parameter name must be exactly "title" (not "titles", etc.)
            if not re.search(r'\btitle\s*=\s*["\']fruits["\']', normalized_input, re.IGNORECASE):
                return False, "Invalid format"
        else:
            # No parameters - must be exactly plt.legend()
            if normalized_input.lower() != 'plt.legend()':
                return False, "Invalid format"
        
        return True, "Correct!"

    def _expected_step1(self, exercise: dict) -> str:
        return format_np_int_array("x", exercise["proportions"])

    def _expected_step2(self, exercise: dict) -> str:
        return format_np_str_array("c", exercise["colors"])

    def _expected_step3(self, exercise: dict) -> str:
        return format_np_str_array("lb", exercise["labels"])

    def _expected_explode(self, explode: list) -> str:
        inner = ", ".join(str(v) for v in explode)
        return f"ex = np.array([{inner}])"

    def _expected_step4(self, exercise: dict) -> str:
        parts = ["x", "labels=lb", "colors=c"]
        if exercise.get("has_explode"):
            parts.insert(1, "explode=ex")
        if exercise["has_shadow"]:
            parts.append("shadow=True")
        return f"plt.pie({', '.join(parts)})"

    def _expected_step5(self, exercise: dict) -> str:
        if exercise.get("legend_title"):
            return 'plt.legend(title="fruits")'
        return "plt.legend()"

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single pie chart series."""
        ctx = SeriesContext()
        titles = {
            1: "Series 1: Pie Chart (explode and legend)",
            2: "Series 2: Pie Chart (shadow)",
            3: "Series 3: Pie Chart (title)",
        }
        contexts = {
            1: "In this series, you will create a pie chart with multiple wedges (varied by proportion, color, label and explode rate) and a legend.",
            2: "In this series, you will create a pie chart with multiple wedges (varied by proportion, color, label and explode rate), a shadow and a legend.",
            3: "In this series, you will create a pie chart with multiple wedges (varied by proportion, color, label and explode rate), a shadow and a titled legend.",
        }
        print("\n" + "="*70)
        print(titles[exercise["number"]])
        print("="*70)
        print(contexts[exercise["number"]])
        print()
        print("Use the following specifications:")
        proportions_str = ', '.join([f"{p}%" for p in exercise['proportions']])
        colors_str = ', '.join(exercise['colors'])
        labels_str = ', '.join(exercise['labels'])
        print(f"- 5 wedges with proportions: {proportions_str}")
        print(f"- Colors for each wedge: {colors_str}")
        print(f"- Labels for each wedge: {labels_str}")

        if exercise.get('has_explode') and exercise.get('explode'):
            explode_str = ', '.join([str(e) for e in exercise['explode']])
            print(f"- Explode rates for each wedge: {explode_str}")
        if exercise['has_shadow']:
            print(f"- The pie chart must have a shadow effect")
        if exercise['has_legend']:
            if exercise.get('legend_title'):
                print(f"- The pie chart must include a legend with title \"fruits\"")
            else:
                print(f"- The pie chart must include a legend")

        print("\nYou need to complete the following steps:\n")

        total_steps = 5
        if exercise.get('has_explode') and exercise.get('explode'):
            total_steps += 1
        if exercise['has_legend']:
            total_steps += 1

        print_step_header(1, total_steps, "Define the proportions array", first=True)
        print("Variable name must be: x")
        if not run_step(
            ctx,
            lambda ui: self.verify_step1(ui, exercise["proportions"]),
            correct_answer=self._expected_step1(exercise),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the colors array")
        print("Variable name must be: c")
        if not run_step(
            ctx,
            lambda ui: self.verify_step2(ui, exercise["colors"]),
            correct_answer=self._expected_step2(exercise),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Define the labels array")
        print("Variable name must be: lb")
        if not run_step(
            ctx,
            lambda ui: self.verify_step3(ui, exercise["labels"]),
            correct_answer=self._expected_step3(exercise),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        step_num = 4
        if exercise.get('has_explode') and exercise.get('explode'):
            print_step_header(4, total_steps, "Define the explode array")
            print("Variable name must be: ex")
            if not run_step(
                ctx,
                lambda ui: self.verify_step_explode(ui, exercise["explode"]),
                correct_answer=self._expected_explode(exercise["explode"]),
                hint=HINT_NP_ARRAY,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num = 5

        print_step_header(step_num, total_steps, "Create the pie chart using plt.pie()")
        if exercise.get('has_explode'):
            print("Remember to include the ex (explode) variable")
        if exercise['has_shadow']:
            print("Remember to include shadow=True")
        if not run_step(
            ctx,
            lambda ui: self.verify_step4(
                ui, exercise["has_shadow"], exercise.get("has_explode", False)
            ),
            correct_answer=self._expected_step4(exercise),
            hint=HINT_PLT_PIE,
        ):
            return SeriesOutcome.NOT_COMPLETED

        if exercise['has_legend']:
            legend_step = step_num + 1
            print_step_header(legend_step, total_steps, "Add a legend to the pie chart")
            if exercise.get('legend_title'):
                print("The legend must have a title, as specified in the exercise")
            if not run_step(
                ctx,
                lambda ui: self.verify_step5(
                    ui, exercise["has_legend"], exercise.get("legend_title")
                ),
                correct_answer=self._expected_step5(exercise),
                hint=HINT_PLT_LEGEND,
            ):
                return SeriesOutcome.NOT_COMPLETED

        if exercise['has_legend']:
            show_step = step_num + 2
        else:
            show_step = step_num + 1
        print_step_header(show_step, total_steps, "Show the chart")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED

        return ctx.finish()
    
    def start_exercises(self):
        """Start the pie chart exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Pie Chart Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)