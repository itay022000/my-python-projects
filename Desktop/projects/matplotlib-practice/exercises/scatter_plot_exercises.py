"""
Scatter Plot Exercises Module
Handles all scatter plot exercise generation, verification, and execution.
"""

import random
import re

from hints import (
    HINT_NP_ARRAY,
    HINT_SCATTER_PLOT,
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


class ScatterPlotExercises:
    """
    Class for handling scatter plot exercises.
    """
    
    def __init__(self):
        self.colors_list = DEFAULT_COLORS
        self.colormaps = [
            "Reds", "Greens", "Blues", "hot", "ocean",
            "spring", "summer", "winter", "viridis", "nipy_spectral"
        ]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 scatter plot exercises."""
        self.exercises = []
        for i in range(3):
            # Step 1 & 2: x and y coordinates (all exercises)
            x_coords = [random.randint(0, 100) for _ in range(10)]
            y_coords = [random.randint(0, 100) for _ in range(10)]
            
            if i == 0:
                # Exercise 1: Simple scatter plot with color
                color = random.choice(self.colors_list)
                
                exercise = {
                    'number': i + 1,
                    'x_coords': x_coords,
                    'y_coords': y_coords,
                    'color': color,
                    'has_colors_array': False,
                    'has_sizes_array': False,
                    'has_alpha': False,
                    'has_cmap': False
                }
            elif i == 1:
                # Exercise 2: Scatter plot with colors array and sizes array
                colors_array = random.sample(self.colors_list, 10)
                sizes_array = [random.randint(50, 500) for _ in range(10)]
                
                exercise = {
                    'number': i + 1,
                    'x_coords': x_coords,
                    'y_coords': y_coords,
                    'colors_array': colors_array,
                    'sizes_array': sizes_array,
                    'has_colors_array': True,
                    'has_sizes_array': True,
                    'has_alpha': False,
                    'has_cmap': False
                }
            else:
                # Exercise 3: Scatter plot with numeric colors, sizes, alpha, and cmap
                colors_array = [random.randint(0, 100) for _ in range(10)]
                sizes_array = [random.randint(50, 500) for _ in range(10)]
                # Alpha in (0, 1] with 0.01 steps
                alpha_value = random.randint(1, 100) / 100.0
                alpha = round(alpha_value, 2)
                cmap = random.choice(self.colormaps)
                
                exercise = {
                    'number': i + 1,
                    'x_coords': x_coords,
                    'y_coords': y_coords,
                    'colors_array': colors_array,
                    'sizes_array': sizes_array,
                    'alpha': alpha,
                    'cmap': cmap,
                    'has_colors_array': True,
                    'has_sizes_array': True,
                    'has_alpha': True,
                    'has_cmap': True
                }
            
            self.exercises.append(exercise)
    
    
    def verify_step1(self, user_input, x_coords):
        """Verify Step 1: x coordinates array."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'x\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(x_coords):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != x_coords:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step2(self, user_input, y_coords):
        """Verify Step 2: y coordinates array."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'y\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'y'"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(y_coords):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != y_coords:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step3_colors_array(self, user_input, colors_array):
        """Verify Step 3 (Exercise 2): colors array with color names."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'colors\s*=', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract array values - colors are strings, must be in exact order
        array_match = re.search(r'np\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            # Extract quoted strings exactly
            values = re.findall(r"['\"]([^'\"]+)['\"]", values_str)
            
            if len(values) != len(colors_array):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != colors_array:
                return False, "Invalid format"
            
            return True, "Correct!"
        except Exception:
            return False, "Invalid format"
    
    def verify_step3_colors_numeric(self, user_input, colors_array):
        """Verify Step 3 (Exercise 3): colors array with numeric values."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'colors\s*=', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(colors_array):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != colors_array:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step4_sizes(self, user_input, sizes_array):
        """Verify Step 4: sizes array."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'sizes\s*=', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(sizes_array):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != sizes_array:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step_plot(self, user_input, exercise):
        """Verify plotting step: plt.scatter() call with various parameters."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.scatter (not plt.scatters, etc.)
        if not re.search(r'\bplt\.scatter\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.scatter() call parameters
        scatter_match = re.search(r'plt\.scatter\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not scatter_match:
            return False, "Invalid format"
        
        params = scatter_match.group(1)
        
        # Check for "x" as first positional argument - must be exactly "x"
        if not re.search(r'(?:^\s*|\W)x(?:\s*[,=]|\s*\Z)', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for "y" as second positional argument - must be exactly "y"
        if not re.search(r'\by\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Exercise 1: color parameter
        if exercise['number'] == 1:
            color_value = exercise['color']
            color_pattern = rf'\bcolor\s*=\s*["\']{re.escape(color_value)}["\']'
            if not re.search(color_pattern, params, re.IGNORECASE):
                return False, "Invalid format"
        
        # Exercise 2: c=colors and s=sizes
        elif exercise['number'] == 2:
            # Check for c=colors
            if not re.search(r'\bc\s*=\s*colors\b', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for s=sizes
            if not re.search(r'\bs\s*=\s*sizes\b', params, re.IGNORECASE):
                return False, "Invalid format"
        
        # Exercise 3: c=colors, s=sizes, alpha=a, cmap='chosen'
        elif exercise['number'] == 3:
            # Check for c=colors
            if not re.search(r'\bc\s*=\s*colors\b', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for s=sizes
            if not re.search(r'\bs\s*=\s*sizes\b', params, re.IGNORECASE):
                return False, "Invalid format"
            
            # Check for alpha parameter
            alpha_match = re.search(r'\balpha\s*=\s*([\d.]+)', params, re.IGNORECASE)
            if not alpha_match:
                return False, "Invalid format"
            
            try:
                alpha_value = float(alpha_match.group(1))
                # Compare with tolerance for floating point precision
                if abs(alpha_value - exercise['alpha']) > 0.001:
                    return False, "Invalid format"
            except ValueError:
                return False, "Invalid format"
            
            # Check for cmap parameter
            cmap_value = exercise['cmap']
            cmap_pattern = rf'\bcmap\s*=\s*["\']{re.escape(cmap_value)}["\']'
            if not re.search(cmap_pattern, params, re.IGNORECASE):
                return False, "Invalid format"
        
        return True, "Correct!"

    def _expected_step1(self, exercise: dict) -> str:
        return format_np_int_array("x", exercise["x_coords"])

    def _expected_step2(self, exercise: dict) -> str:
        return format_np_int_array("y", exercise["y_coords"])

    def _expected_colors_array(self, colors: list[str]) -> str:
        return format_np_str_array("colors", colors)

    def _expected_colors_numeric(self, colors: list[int]) -> str:
        return format_np_int_array("colors", colors)

    def _expected_sizes(self, sizes: list[int]) -> str:
        return format_np_int_array("sizes", sizes)

    def _expected_plot(self, exercise: dict) -> str:
        if exercise["number"] == 1:
            return f'plt.scatter(x, y, color="{exercise["color"]}")'
        if exercise["number"] == 2:
            return "plt.scatter(x, y, c=colors, s=sizes)"
        return (
            f'plt.scatter(x, y, c=colors, s=sizes, alpha={exercise["alpha"]}, '
            f'cmap="{exercise["cmap"]}")'
        )

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single scatter plot series."""
        ctx = SeriesContext()
        titles = {
            1: "Series 1: Scatter Plot (color)",
            2: "Series 2: Scatter Plot (sizes)",
            3: "Series 3: Scatter Plot (color map)",
        }
        contexts = {
            1: "In this series, you will create a scatter plot with points in one color.",
            2: "In this series, you will create a scatter plot with points in different colors and sizes.",
            3: "In this series, you will create a scatter plot with points in different colors and sizes.",
        }
        print("\n" + "="*70)
        print(titles[exercise["number"]])
        print("="*70)
        print(contexts[exercise["number"]])
        print()
        print("Use the following specifications:")

        x_str = ', '.join(map(str, exercise['x_coords']))
        y_str = ', '.join(map(str, exercise['y_coords']))
        print(f"- X-axis coordinates: {x_str}")
        print(f"- Y-axis coordinates: {y_str}")

        if exercise['number'] == 1:
            print(f"- Color: {exercise['color']}")
        elif exercise['number'] == 2:
            colors_str = ', '.join(exercise['colors_array'])
            sizes_str = ', '.join(map(str, exercise['sizes_array']))
            print(f"- Colors: {colors_str}")
            print(f"- Sizes: {sizes_str}")
        elif exercise['number'] == 3:
            colors_str = ', '.join(map(str, exercise['colors_array']))
            sizes_str = ', '.join(map(str, exercise['sizes_array']))
            print(f"- Colors (numeric): {colors_str}")
            print(f"- Sizes: {sizes_str}")
            print(f"- Alpha: {exercise['alpha']}")
            print(f"- Color map: {exercise['cmap']}")

        print("\nYou need to complete the following steps:\n")

        total_steps = 4 if exercise["number"] == 1 else 6
        print_step_header(1, total_steps, "Define the x-axis coordinates array", first=True)
        print("Variable name must be: x")
        if not run_step(
            ctx,
            lambda ui: self.verify_step1(ui, exercise["x_coords"]),
            correct_answer=self._expected_step1(exercise),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the y-axis coordinates array")
        print("Variable name must be: y")
        if not run_step(
            ctx,
            lambda ui: self.verify_step2(ui, exercise["y_coords"]),
            correct_answer=self._expected_step2(exercise),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        step_num = 3
        if exercise['number'] == 2:
            print_step_header(3, total_steps, "Define the colors array")
            print("Variable name must be: colors")
            if not run_step(
                ctx,
                lambda ui: self.verify_step3_colors_array(
                    ui, exercise["colors_array"]
                ),
                correct_answer=self._expected_colors_array(exercise["colors_array"]),
                hint=HINT_NP_ARRAY,
            ):
                return SeriesOutcome.NOT_COMPLETED

            print_step_header(4, total_steps, "Define the sizes array")
            print("Variable name must be: sizes")
            if not run_step(
                ctx,
                lambda ui: self.verify_step4_sizes(ui, exercise["sizes_array"]),
                correct_answer=self._expected_sizes(exercise["sizes_array"]),
                hint=HINT_NP_ARRAY,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num = 5
        elif exercise['number'] == 3:
            print_step_header(3, total_steps, "Define the colors array")
            print("Variable name must be: colors")
            if not run_step(
                ctx,
                lambda ui: self.verify_step3_colors_numeric(
                    ui, exercise["colors_array"]
                ),
                correct_answer=self._expected_colors_numeric(exercise["colors_array"]),
                hint=HINT_NP_ARRAY,
            ):
                return SeriesOutcome.NOT_COMPLETED

            print_step_header(4, total_steps, "Define the sizes array")
            print("Variable name must be: sizes")
            if not run_step(
                ctx,
                lambda ui: self.verify_step4_sizes(ui, exercise["sizes_array"]),
                correct_answer=self._expected_sizes(exercise["sizes_array"]),
                hint=HINT_NP_ARRAY,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num = 5

        print_step_header(step_num, total_steps, "Plot the scatter plot")
        if exercise['number'] == 1:
            print(f"   Remember to include color=\"{exercise['color']}\"")
        elif exercise['number'] == 2:
            print("Remember to include c=colors and s=sizes")
        elif exercise['number'] == 3:
            print(
                f"   Remember to include c=colors, s=sizes, alpha={exercise['alpha']}, "
                f"and cmap=\"{exercise['cmap']}\""
            )
        if not run_step(
            ctx,
            lambda ui: self.verify_step_plot(ui, exercise),
            correct_answer=self._expected_plot(exercise),
            hint=HINT_SCATTER_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        show_step = step_num + 1
        print_step_header(show_step, total_steps, "Show the plot")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED

        return ctx.finish()
    
    def start_exercises(self):
        """Start the scatter plot exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Scatter Plot Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)