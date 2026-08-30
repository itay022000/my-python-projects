"""
Subplot Exercises Module
Handles all subplot exercise generation, verification, and execution.
"""

import random
import re

from hints import (
    HINT_NP_ARRAY,
    HINT_PLT_PLOT,
    HINT_PLT_SUBPLOT,
    HINT_TITLE_LABEL,
)
from session_common import (
    SESSION_INTRO_LINE,
    print_sequence_intro,
    print_step_header,
)
from engine import (
    DEFAULT_COLORS,
    SHOW_ANSWER,
    SeriesContext,
    SeriesOutcome,
    format_np_int_array,
    normalize_code,
    run_step,
    verify_step_show,
)
from exercise_session import run_exercise_sequence


class SubplotExercises:
    """
    Class for handling subplot exercises.
    """
    
    def __init__(self):
        self.car_companies = [
            "mercedes", "bmw", "audi", "jaguar", "toyota", "honda",
            "ford", "chevrolet", "volkswagen", "porsche", "ferrari",
            "lamborghini", "tesla", "nissan", "lexus", "mazda"
        ]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 subplot exercises."""
        self.exercises = []
        for i in range(3):
            # All exercises use x = np.array([0, 1, 2, 3])
            x_array = [0, 1, 2, 3]
            
            # First y array (for first subplot)
            y1 = [random.randint(0, 20) for _ in range(4)]
            # Second y array (for second subplot)
            y2 = [random.randint(0, 20) for _ in range(4)]
            
            if i == 0:
                # Exercise 1: Simple 1x2 subplot with two plots
                exercise = {
                    'number': i + 1,
                    'x_array': x_array,
                    'y1': y1,
                    'y2': y2,
                    'subplot1': (1, 2, 1),
                    'subplot2': (1, 2, 2),
                    'has_titles': False,
                    'has_suptitle': False
                }
            elif i == 1:
                # Exercise 2: 2x1 subplot with titles
                title1 = random.choice(self.car_companies)
                title2 = random.choice([c for c in self.car_companies if c != title1])
                
                exercise = {
                    'number': i + 1,
                    'x_array': x_array,
                    'y1': y1,
                    'y2': y2,
                    'subplot1': (2, 1, 1),
                    'subplot2': (2, 1, 2),
                    'has_titles': True,
                    'title1': title1,
                    'title2': title2,
                    'has_suptitle': False
                }
            else:
                # Exercise 3: 1x2 subplot with titles and supertitle
                title1 = random.choice(self.car_companies)
                title2 = random.choice([c for c in self.car_companies if c != title1])
                
                exercise = {
                    'number': i + 1,
                    'x_array': x_array,
                    'y1': y1,
                    'y2': y2,
                    'subplot1': (1, 2, 1),
                    'subplot2': (1, 2, 2),
                    'has_titles': True,
                    'title1': title1,
                    'title2': title2,
                    'has_suptitle': True,
                    'suptitle': "Car Companies"
                }
            
            self.exercises.append(exercise)
    
    
    def verify_x_array(self, user_input):
        """Verify x array: x = np.array([0, 1, 2, 3])."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'x\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"
        
        # Extract array values - must be exactly [0, 1, 2, 3]
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            expected = [0, 1, 2, 3]
            if values != expected:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_y_array(self, user_input, expected_y):
        """Verify y array: y = np.array([n1, n2, n3, n4])."""
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
            
            if len(values) != len(expected_y):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != expected_y:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_subplot(self, user_input, expected_params):
        """Verify plt.subplot() call: plt.subplot(rows, cols, index)."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.subplot (not plt.subplots, etc.)
        if not re.search(r'\bplt\.subplot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.subplot() call parameters
        subplot_match = re.search(r'plt\.subplot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not subplot_match:
            return False, "Invalid format"
        
        params_str = subplot_match.group(1)
        params = [p.strip() for p in params_str.split(',')]
        
        if len(params) != 3:
            return False, "Invalid format"
        
        try:
            param1 = int(params[0])
            param2 = int(params[1])
            param3 = int(params[2])
            
            if (param1, param2, param3) != expected_params:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_plot(self, user_input):
        """Verify plt.plot(x, y) call."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.plot (not plt.plots, etc.)
        if not re.search(r'\bplt\.plot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.plot() call parameters
        plot_match = re.search(r'plt\.plot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not plot_match:
            return False, "Invalid format"
        
        params = plot_match.group(1)
        
        # Check for "x" as first positional argument
        if not re.search(r'(?:^\s*|\W)x(?:\s*[,=]|\s*\Z)', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for "y" as second positional argument
        if not re.search(r'\by\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_title(self, user_input, expected_title):
        """Verify plt.title() call: plt.title("title")."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.title (not plt.titles, etc.)
        if not re.search(r'\bplt\.title\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.title() call parameters
        title_match = re.search(r'plt\.title\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not title_match:
            return False, "Invalid format"
        
        params = title_match.group(1)
        
        # Check for exact title string
        title_pattern = rf'["\']{re.escape(expected_title)}["\']'
        if not re.search(title_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_suptitle(self, user_input, expected_suptitle):
        """Verify plt.suptitle() call: plt.suptitle("title")."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.suptitle (not plt.suptitles, etc.)
        if not re.search(r'\bplt\.suptitle\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.suptitle() call parameters
        suptitle_match = re.search(r'plt\.suptitle\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not suptitle_match:
            return False, "Invalid format"
        
        params = suptitle_match.group(1)
        
        # Check for exact supertitle string
        suptitle_pattern = rf'["\']{re.escape(expected_suptitle)}["\']'
        if not re.search(suptitle_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"

    def _expected_x(self) -> str:
        return format_np_int_array("x", [0, 1, 2, 3])

    def _expected_y(self, values: list[int]) -> str:
        return format_np_int_array("y", values)

    def _expected_subplot(self, params: tuple[int, int, int]) -> str:
        r, c, i = params
        return f"plt.subplot({r}, {c}, {i})"

    def _expected_plot(self) -> str:
        return "plt.plot(x, y)"

    def _expected_title(self, title: str) -> str:
        return f'plt.title("{title}")'

    def _expected_suptitle(self, title: str) -> str:
        return f'plt.suptitle("{title}")'

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single subplot series."""
        ctx = SeriesContext()
        titles = {
            1: "Series 1: Subplot (basic layout)",
            2: "Series 2: Subplot (titles)",
            3: "Series 3: Subplot (titles extended)",
        }
        contexts = {
            1: "In this series, you will create a plot with 2 subplots (1 row, 2 columns).",
            2: "In this series, you will create a plot with 2 subplots (2 rows, 1 column) and titles.",
            3: "In this series, you will create a plot with 2 subplots (1 row, 2 columns), titles and a super title.",
        }
        print("\n" + "="*70)
        print(titles[exercise["number"]])
        print("="*70)
        print(contexts[exercise["number"]])
        print()
        print("Use the following specifications:")

        if exercise['number'] == 1:
            print(f"- Subplot layout: 1 row, 2 columns")
            y1_str = ', '.join(map(str, exercise['y1']))
            y2_str = ', '.join(map(str, exercise['y2']))
            print(f"- First plot y-values: {y1_str}")
            print(f"- Second plot y-values: {y2_str}")
        elif exercise['number'] == 2:
            print(f"- Subplot layout: 2 rows, 1 column")
            y1_str = ', '.join(map(str, exercise['y1']))
            y2_str = ', '.join(map(str, exercise['y2']))
            print(f"- First plot y-values: {y1_str}")
            print(f"- Second plot y-values: {y2_str}")
            print(f"- First plot title: {exercise['title1']}")
            print(f"- Second plot title: {exercise['title2']}")
        elif exercise['number'] == 3:
            print(f"- Subplot layout: 1 row, 2 columns")
            y1_str = ', '.join(map(str, exercise['y1']))
            y2_str = ', '.join(map(str, exercise['y2']))
            print(f"- First plot y-values: {y1_str}")
            print(f"- Second plot y-values: {y2_str}")
            print(f"- First plot title: {exercise['title1']}")
            print(f"- Second plot title: {exercise['title2']}")
            print(f"- Super title: {exercise['suptitle']}")

        print("\nYou need to complete the following steps:\n")

        total_steps = 9
        if exercise["has_titles"]:
            total_steps += 2
        if exercise["has_suptitle"]:
            total_steps += 1

        step_num = 1

        print_step_header(step_num, total_steps, "Define the first x-axis coordinates array", first=(step_num == 1))
        print("Variable name must be: x")
        if not run_step(
            ctx, self.verify_x_array,
            correct_answer=self._expected_x(),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Define the first y-axis coordinates array", first=(step_num == 1))
        print("Variable name must be: y")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, exercise["y1"]),
            correct_answer=self._expected_y(exercise["y1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Create the first subplot", first=(step_num == 1))
        if not run_step(
            ctx,
            lambda ui: self.verify_subplot(ui, exercise["subplot1"]),
            correct_answer=self._expected_subplot(exercise["subplot1"]),
            hint=HINT_PLT_SUBPLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Plot the first line", first=(step_num == 1))
        if not run_step(
            ctx, self.verify_plot,
            correct_answer=self._expected_plot(),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        if exercise['has_titles']:
            print_step_header(step_num, total_steps, "Add a title to the first plot", first=(step_num == 1))
            if not run_step(
                ctx,
                lambda ui: self.verify_title(ui, exercise["title1"]),
                correct_answer=self._expected_title(exercise["title1"]),
                hint=HINT_TITLE_LABEL,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num += 1

        print_step_header(step_num, total_steps, "Define the second x-axis coordinates array", first=(step_num == 1))
        print("Variable name must be: x")
        if not run_step(
            ctx, self.verify_x_array,
            correct_answer=self._expected_x(),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Define the second y-axis coordinates array", first=(step_num == 1))
        print("Variable name must be: y")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, exercise["y2"]),
            correct_answer=self._expected_y(exercise["y2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Create the second subplot", first=(step_num == 1))
        if not run_step(
            ctx,
            lambda ui: self.verify_subplot(ui, exercise["subplot2"]),
            correct_answer=self._expected_subplot(exercise["subplot2"]),
            hint=HINT_PLT_SUBPLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        print_step_header(step_num, total_steps, "Plot the second line", first=(step_num == 1))
        if not run_step(
            ctx, self.verify_plot,
            correct_answer=self._expected_plot(),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED
        step_num += 1

        if exercise['has_titles']:
            print_step_header(step_num, total_steps, "Add a title to the second plot", first=(step_num == 1))
            if not run_step(
                ctx,
                lambda ui: self.verify_title(ui, exercise["title2"]),
                correct_answer=self._expected_title(exercise["title2"]),
                hint=HINT_TITLE_LABEL,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num += 1

        if exercise['has_suptitle']:
            print_step_header(step_num, total_steps, "Add a super title to the figure", first=(step_num == 1))
            if not run_step(
                ctx,
                lambda ui: self.verify_suptitle(ui, exercise["suptitle"]),
                correct_answer=self._expected_suptitle(exercise["suptitle"]),
                hint=HINT_TITLE_LABEL,
            ):
                return SeriesOutcome.NOT_COMPLETED
            step_num += 1

        print_step_header(step_num, total_steps, "Show the plot", first=(step_num == 1))
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED

        return ctx.finish()
    
    def start_exercises(self):
        """Start the subplot exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Subplot Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)

