"""
Plot Exercises
Exercises for practicing basic matplotlib.pyplot plotting.
"""

import random
import re

from hints import (
    HINT_NP_ARRAY,
    HINT_PLT_PLOT,
    HINT_TITLE_LABEL,
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
    normalize_code,
    run_step,
    verify_step_show,
)
from exercise_session import run_exercise_sequence



class PlotExercises:
    """Exercises for practicing basic pyplot line plotting."""
    
    def __init__(self):
        self.colors_list = DEFAULT_COLORS
        self.linestyles = ["solid", "dotted", "dashed", "dashdot"]
        self.markers = ["o", "*", ".", "x", "+", "s", "D", "H"]
        self.fmt_lines = ["-", ":", "--", "-."]
        self.fmt_colors = ["r", "g", "b", "c", "m", "y", "k", "w"]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 plot exercises."""
        self.exercises = []
        for i in range(3):
            exercise = {
                'number': i + 1,
            }
            
            if i == 0:  # Exercise 1: 3 lines with different formatting
                # Generate 3 y arrays
                exercise['y1'] = [random.randint(1, 12) for _ in range(4)]
                exercise['y2'] = [random.randint(1, 12) for _ in range(4)]
                exercise['y3'] = [random.randint(1, 12) for _ in range(4)]
                
                # Line 1: linestyle, linewidth, color
                exercise['linestyle'] = random.choice(self.linestyles)
                linewidth_value = random.randint(1, 2000) / 100.0  # Float in (0,20] with 0.01 intervals
                exercise['linewidth'] = round(linewidth_value, 2)
                exercise['color1'] = random.choice(self.colors_list)
                
                # Line 2: marker, ms, mec, mfc
                exercise['marker'] = random.choice(self.markers)
                exercise['marker_size'] = random.randint(5, 25)
                exercise['mec'] = random.choice(self.colors_list)
                exercise['mfc'] = random.choice(self.colors_list)
                
                # Line 3: fmt format
                exercise['fmt_marker'] = random.choice(self.markers)
                exercise['fmt_line'] = random.choice(self.fmt_lines)
                exercise['fmt_color'] = random.choice(self.fmt_colors)
                exercise['fmt'] = exercise['fmt_marker'] + exercise['fmt_line'] + exercise['fmt_color']
                
                self.exercises.append(exercise)
            
            elif i == 1:  # Exercise 2: 2 lines with labels and title
                # Generate monotonically increasing x arrays
                def generate_monotonic_x():
                    values = sorted([random.randint(1, 20) for _ in range(4)])
                    # Ensure they're strictly increasing
                    while len(set(values)) < 4:
                        values = sorted([random.randint(1, 20) for _ in range(4)])
                    return values
                
                exercise['x1'] = generate_monotonic_x()
                exercise['y1'] = [random.randint(1, 20) for _ in range(4)]
                exercise['x2'] = generate_monotonic_x()
                exercise['y2'] = [random.randint(1, 20) for _ in range(4)]
                
                # Title and labels - using exact strings as specified
                exercise['title'] = "coordinates"
                exercise['xlabel'] = "x-axis"
                exercise['ylabel'] = "y-axis"
                
                self.exercises.append(exercise)
            
            elif i == 2:  # Exercise 3: 2 lines with grid
                # Generate monotonically increasing x arrays
                def generate_monotonic_x():
                    values = sorted([random.randint(1, 20) for _ in range(4)])
                    # Ensure they're strictly increasing
                    while len(set(values)) < 4:
                        values = sorted([random.randint(1, 20) for _ in range(4)])
                    return values
                
                exercise['x1'] = generate_monotonic_x()
                exercise['y1'] = [random.randint(1, 20) for _ in range(4)]
                exercise['x2'] = generate_monotonic_x()
                exercise['y2'] = [random.randint(1, 20) for _ in range(4)]
                
                # Grid properties
                exercise['grid_color'] = random.choice(self.colors_list)
                exercise['grid_linestyle'] = random.choice(self.fmt_lines)  # Using fmt_lines for grid: [-, :, --, -.]
                # Linewidth is integer in (0,1], which means only 1 is valid
                exercise['grid_linewidth'] = 1
                
                self.exercises.append(exercise)
    
    
    def verify_y_array(self, user_input, var_name, expected_values):
        """Verify y array: y1/y2/y3 = np.array([n1, n2, n3, n4])."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(rf'{var_name}\s*=', normalized_input, re.IGNORECASE):
            return False, f"Variable name should be '{var_name}'"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(expected_values):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != expected_values:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_x_array(self, user_input, var_name, expected_values):
        """Verify x array: x1/x2 = np.array([m1, m2, m3, m4])."""
        normalized_input = normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(rf'{var_name}\s*=', normalized_input, re.IGNORECASE):
            return False, f"Variable name should be '{var_name}'"
        
        # Extract array values - must be in exact order
        # Use word boundaries to prevent typos like "np.arrays", "np.arrayx", etc.
        array_match = re.search(r'\bnp\.array\s*\(\s*\[(.*?)\]\s*\)', normalized_input)
        if not array_match:
            return False, "Invalid format"
        
        try:
            values_str = array_match.group(1)
            values = [int(x.strip()) for x in values_str.split(',')]
            
            if len(values) != len(expected_values):
                return False, "Invalid format"
            
            # Check exact match in exact order
            if values != expected_values:
                return False, "Invalid format"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step4_line1(self, user_input, linestyle, linewidth, color):
        """Verify Step 4: plt.plot(y1, linestyle='...', linewidth=..., color='...')."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.plot
        if not re.search(r'\bplt\.plot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.plot() call parameters
        plot_match = re.search(r'plt\.plot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not plot_match:
            return False, "Invalid format"
        
        params = plot_match.group(1)
        
        # Check for y1 as first positional argument
        if not re.search(r'\by1\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for linestyle parameter - must be exactly "linestyle"
        linestyle_pattern = rf'\blinestyle\s*=\s*["\']{re.escape(linestyle)}["\']'
        if not re.search(linestyle_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for linewidth parameter - must be exactly "linewidth"
        linewidth_match = re.search(r'\blinewidth\s*=\s*([\d.]+)', params, re.IGNORECASE)
        if not linewidth_match:
            return False, "Invalid format"
        try:
            linewidth_value = float(linewidth_match.group(1))
            if abs(linewidth_value - linewidth) > 0.001:
                return False, "Invalid format"
        except ValueError:
            return False, "Invalid format"
        
        # Check for color parameter - must be exactly "color"
        color_pattern = rf'\bcolor\s*=\s*["\']{re.escape(color)}["\']'
        if not re.search(color_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_step5_line2(self, user_input, marker, marker_size, mec, mfc):
        """Verify Step 5: plt.plot(y2, marker='...', ms=..., mec='...', mfc='...')."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.plot
        if not re.search(r'\bplt\.plot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.plot() call parameters
        plot_match = re.search(r'plt\.plot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not plot_match:
            return False, "Invalid format"
        
        params = plot_match.group(1)
        
        # Check for y2 as first positional argument
        if not re.search(r'\by2\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for marker parameter - must be exactly "marker"
        marker_pattern = rf'\bmarker\s*=\s*["\']{re.escape(marker)}["\']'
        if not re.search(marker_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for ms parameter - must be exactly "ms"
        ms_match = re.search(r'\bms\s*=\s*(\d+)', params, re.IGNORECASE)
        if not ms_match:
            return False, "Invalid format"
        try:
            ms_value = int(ms_match.group(1))
            if ms_value != marker_size:
                return False, "Invalid format"
        except ValueError:
            return False, "Invalid format"
        
        # Check for mec parameter - must be exactly "mec"
        mec_pattern = rf'\bmec\s*=\s*["\']{re.escape(mec)}["\']'
        if not re.search(mec_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for mfc parameter - must be exactly "mfc"
        mfc_pattern = rf'\bmfc\s*=\s*["\']{re.escape(mfc)}["\']'
        if not re.search(mfc_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_step6_line3(self, user_input, fmt):
        """Verify Step 6: plt.plot(y3, 'fmt')."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.plot
        if not re.search(r'\bplt\.plot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.plot() call parameters
        plot_match = re.search(r'plt\.plot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not plot_match:
            return False, "Invalid format"
        
        params = plot_match.group(1)
        
        # Check for y3 as first positional argument
        if not re.search(r'\by3\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for fmt string - must be exactly the fmt value
        fmt_pattern = rf'["\']{re.escape(fmt)}["\']'
        if not re.search(fmt_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_plot_simple(self, user_input, x_var, y_var):
        """Verify simple plot: plt.plot(x_var, y_var)."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.plot
        if not re.search(r'\bplt\.plot\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.plot() call parameters
        plot_match = re.search(r'plt\.plot\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not plot_match:
            return False, "Invalid format"
        
        params = plot_match.group(1)
        
        # Check for x_var as first positional argument
        if not re.search(rf'\b{x_var}\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for y_var as second positional argument
        if not re.search(rf'\b{y_var}\b', params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_title(self, user_input, expected_title):
        """Verify plt.title() call: plt.title("title")."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.title
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
    
    def verify_xlabel(self, user_input, expected_label):
        """Verify plt.xlabel() call: plt.xlabel("label")."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.xlabel
        if not re.search(r'\bplt\.xlabel\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.xlabel() call parameters
        xlabel_match = re.search(r'plt\.xlabel\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not xlabel_match:
            return False, "Invalid format"
        
        params = xlabel_match.group(1)
        
        # Check for exact label string
        label_pattern = rf'["\']{re.escape(expected_label)}["\']'
        if not re.search(label_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_ylabel(self, user_input, expected_label):
        """Verify plt.ylabel() call: plt.ylabel("label")."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.ylabel
        if not re.search(r'\bplt\.ylabel\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.ylabel() call parameters
        ylabel_match = re.search(r'plt\.ylabel\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not ylabel_match:
            return False, "Invalid format"
        
        params = ylabel_match.group(1)
        
        # Check for exact label string
        label_pattern = rf'["\']{re.escape(expected_label)}["\']'
        if not re.search(label_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def verify_grid(self, user_input, color, linestyle, linewidth):
        """Verify plt.grid() call: plt.grid(color='...', linestyle='...', linewidth=...)."""
        normalized_input = normalize_code(user_input)
        
        # Must use exact function name plt.grid
        if not re.search(r'\bplt\.grid\s*\(', normalized_input, re.IGNORECASE):
            return False, "Invalid format"
        
        # Extract the plt.grid() call parameters
        grid_match = re.search(r'plt\.grid\s*\((.*?)\)', normalized_input, re.IGNORECASE)
        if not grid_match:
            return False, "Invalid format"
        
        params = grid_match.group(1)
        
        # Check for color parameter - must be exactly "color"
        color_pattern = rf'\bcolor\s*=\s*["\']{re.escape(color)}["\']'
        if not re.search(color_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for linestyle parameter - must be exactly "linestyle"
        linestyle_pattern = rf'\blinestyle\s*=\s*["\']{re.escape(linestyle)}["\']'
        if not re.search(linestyle_pattern, params, re.IGNORECASE):
            return False, "Invalid format"
        
        # Check for linewidth parameter - must be exactly "linewidth"
        linewidth_match = re.search(r'\blinewidth\s*=\s*(\d+)', params, re.IGNORECASE)
        if not linewidth_match:
            return False, "Invalid format"
        try:
            linewidth_value = int(linewidth_match.group(1))
            if linewidth_value != linewidth:
                return False, "Invalid format"
        except ValueError:
            return False, "Invalid format"
        
        return True, "Correct!"

    def _expected_y(self, var_name: str, values: list[int]) -> str:
        return format_np_int_array(var_name, values)

    def _expected_x(self, var_name: str, values: list[int]) -> str:
        return format_np_int_array(var_name, values)

    def _expected_line1(self, exercise: dict) -> str:
        return (
            f"plt.plot(y1, linestyle='{exercise['linestyle']}', "
            f"linewidth={exercise['linewidth']}, color='{exercise['color1']}')"
        )

    def _expected_line2(self, exercise: dict) -> str:
        return (
            f"plt.plot(y2, marker='{exercise['marker']}', ms={exercise['marker_size']}, "
            f"mec='{exercise['mec']}', mfc='{exercise['mfc']}')"
        )

    def _expected_line3(self, exercise: dict) -> str:
        return f"plt.plot(y3, '{exercise['fmt']}')"

    def _expected_plot_simple(self, x_var: str, y_var: str) -> str:
        return f"plt.plot({x_var}, {y_var})"

    def _expected_title(self, title: str) -> str:
        return f'plt.title("{title}")'

    def _expected_xlabel(self, label: str) -> str:
        return f'plt.xlabel("{label}")'

    def _expected_ylabel(self, label: str) -> str:
        return f'plt.ylabel("{label}")'

    def _expected_grid(self, exercise: dict) -> str:
        return (
            f"plt.grid(color='{exercise['grid_color']}', "
            f"linestyle='{exercise['grid_linestyle']}', "
            f"linewidth={exercise['grid_linewidth']})"
        )

    def _run_exercise1(self, ctx: SeriesContext, exercise: dict) -> SeriesOutcome | None:
        total_steps = 7
        print_step_header(1, total_steps, "Define the y-axis coordinates array for the first line", first=True)
        print("Variable name must be: y1")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y1", exercise["y1"]),
            correct_answer=self._expected_y("y1", exercise["y1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the y-axis coordinates array for the second line")
        print("Variable name must be: y2")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y2", exercise["y2"]),
            correct_answer=self._expected_y("y2", exercise["y2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Define the y-axis coordinates array for the third line")
        print("Variable name must be: y3")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y3", exercise["y3"]),
            correct_answer=self._expected_y("y3", exercise["y3"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(4, total_steps, "Plot the first line")
        if not run_step(
            ctx,
            lambda ui: self.verify_step4_line1(
                ui, exercise["linestyle"], exercise["linewidth"], exercise["color1"]
            ),
            correct_answer=self._expected_line1(exercise),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(5, total_steps, "Plot the second line")
        if not run_step(
            ctx,
            lambda ui: self.verify_step5_line2(
                ui,
                exercise["marker"],
                exercise["marker_size"],
                exercise["mec"],
                exercise["mfc"],
            ),
            correct_answer=self._expected_line2(exercise),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(6, total_steps, "Plot the third line")
        if not run_step(
            ctx,
            lambda ui: self.verify_step6_line3(ui, exercise["fmt"]),
            correct_answer=self._expected_line3(exercise),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(7, total_steps, "Show the plot")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED
        return None

    def _run_exercise2(self, ctx: SeriesContext, exercise: dict) -> SeriesOutcome | None:
        total_steps = 10
        print_step_header(1, total_steps, "Define the x-axis coordinates array for the first line", first=True)
        print("Variable name must be: x1")
        if not run_step(
            ctx,
            lambda ui: self.verify_x_array(ui, "x1", exercise["x1"]),
            correct_answer=self._expected_x("x1", exercise["x1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the y-axis coordinates array for the first line")
        print("Variable name must be: y1")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y1", exercise["y1"]),
            correct_answer=self._expected_y("y1", exercise["y1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Define the x-axis coordinates array for the second line")
        print("Variable name must be: x2")
        if not run_step(
            ctx,
            lambda ui: self.verify_x_array(ui, "x2", exercise["x2"]),
            correct_answer=self._expected_x("x2", exercise["x2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(4, total_steps, "Define the y-axis coordinates array for the second line")
        print("Variable name must be: y2")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y2", exercise["y2"]),
            correct_answer=self._expected_y("y2", exercise["y2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(5, total_steps, "Create a title for the plot")
        if not run_step(
            ctx,
            lambda ui: self.verify_title(ui, exercise["title"]),
            correct_answer=self._expected_title(exercise["title"]),
            hint=HINT_TITLE_LABEL,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(6, total_steps, "Create a label for the x-axis")
        if not run_step(
            ctx,
            lambda ui: self.verify_xlabel(ui, exercise["xlabel"]),
            correct_answer=self._expected_xlabel(exercise["xlabel"]),
            hint=HINT_TITLE_LABEL,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(7, total_steps, "Create a label for the y-axis")
        if not run_step(
            ctx,
            lambda ui: self.verify_ylabel(ui, exercise["ylabel"]),
            correct_answer=self._expected_ylabel(exercise["ylabel"]),
            hint=HINT_TITLE_LABEL,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(8, total_steps, "Plot the first line")
        if not run_step(
            ctx,
            lambda ui: self.verify_plot_simple(ui, "x1", "y1"),
            correct_answer=self._expected_plot_simple("x1", "y1"),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(9, total_steps, "Plot the second line")
        if not run_step(
            ctx,
            lambda ui: self.verify_plot_simple(ui, "x2", "y2"),
            correct_answer=self._expected_plot_simple("x2", "y2"),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(10, total_steps, "Show the plot")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED
        return None

    def _run_exercise3(self, ctx: SeriesContext, exercise: dict) -> SeriesOutcome | None:
        total_steps = 8
        print_step_header(1, total_steps, "Define the x-axis coordinates array for the first line", first=True)
        print("Variable name must be: x1")
        if not run_step(
            ctx,
            lambda ui: self.verify_x_array(ui, "x1", exercise["x1"]),
            correct_answer=self._expected_x("x1", exercise["x1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(2, total_steps, "Define the y-axis coordinates array for the first line")
        print("Variable name must be: y1")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y1", exercise["y1"]),
            correct_answer=self._expected_y("y1", exercise["y1"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(3, total_steps, "Define the x-axis coordinates array for the second line")
        print("Variable name must be: x2")
        if not run_step(
            ctx,
            lambda ui: self.verify_x_array(ui, "x2", exercise["x2"]),
            correct_answer=self._expected_x("x2", exercise["x2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(4, total_steps, "Define the y-axis coordinates array for the second line")
        print("Variable name must be: y2")
        if not run_step(
            ctx,
            lambda ui: self.verify_y_array(ui, "y2", exercise["y2"]),
            correct_answer=self._expected_y("y2", exercise["y2"]),
            hint=HINT_NP_ARRAY,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(5, total_steps, "Plot the first line")
        if not run_step(
            ctx,
            lambda ui: self.verify_plot_simple(ui, "x1", "y1"),
            correct_answer=self._expected_plot_simple("x1", "y1"),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(6, total_steps, "Plot the second line")
        if not run_step(
            ctx,
            lambda ui: self.verify_plot_simple(ui, "x2", "y2"),
            correct_answer=self._expected_plot_simple("x2", "y2"),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(7, total_steps, "Create a grid")
        if not run_step(
            ctx,
            lambda ui: self.verify_grid(
                ui,
                exercise["grid_color"],
                exercise["grid_linestyle"],
                exercise["grid_linewidth"],
            ),
            correct_answer=self._expected_grid(exercise),
            hint=HINT_PLT_PLOT,
        ):
            return SeriesOutcome.NOT_COMPLETED

        print_step_header(8, total_steps, "Show the plot")
        if not run_step(
            ctx,
            verify_step_show,
            correct_answer=SHOW_ANSWER,
            hint=None,
        ):
            return SeriesOutcome.NOT_COMPLETED
        return None

    def run_exercise(self, exercise) -> SeriesOutcome:
        """Run a single plot series."""
        ctx = SeriesContext()
        titles = {
            1: "Series 1: Line plots (styling)",
            2: "Series 2: Line plots (labels)",
            3: "Series 3: Line plots (grid)",
        }
        contexts = {
            1: "In this series, you will create a line plot with 3 lines.",
            2: "In this series, you will create a line plot with 2 lines, a title and labels.",
            3: "In this series, you will create a line plot with 2 lines and a grid.",
        }
        print("\n" + "="*70)
        print(titles[exercise["number"]])
        print("="*70)
        print(contexts[exercise["number"]])
        print()
        print("Use the following specifications:")

        if exercise['number'] == 1:
            y1_str = ', '.join(map(str, exercise['y1']))
            y2_str = ', '.join(map(str, exercise['y2']))
            y3_str = ', '.join(map(str, exercise['y3']))
            print(f"- First line y-values: {y1_str}")
            print(f"- Second line y-values: {y2_str}")
            print(f"- Third line y-values: {y3_str}")
            print(f"- First line: linestyle='{exercise['linestyle']}', linewidth={exercise['linewidth']}, color='{exercise['color1']}'")
            print(f"- Second line: marker='{exercise['marker']}', ms={exercise['marker_size']}, mec='{exercise['mec']}', mfc='{exercise['mfc']}'")
            print(f"- Third line: fmt='{exercise['fmt']}'")
        elif exercise['number'] == 2:
            x1_str = ', '.join(map(str, exercise['x1']))
            y1_str = ', '.join(map(str, exercise['y1']))
            x2_str = ', '.join(map(str, exercise['x2']))
            y2_str = ', '.join(map(str, exercise['y2']))
            print(f"- First line x-values: {x1_str}")
            print(f"- First line y-values: {y1_str}")
            print(f"- Second line x-values: {x2_str}")
            print(f"- Second line y-values: {y2_str}")
            print(f"- Title: \"{exercise['title']}\"")
            print(f"- X-axis label: \"{exercise['xlabel']}\"")
            print(f"- Y-axis label: \"{exercise['ylabel']}\"")
        elif exercise['number'] == 3:
            x1_str = ', '.join(map(str, exercise['x1']))
            y1_str = ', '.join(map(str, exercise['y1']))
            x2_str = ', '.join(map(str, exercise['x2']))
            y2_str = ', '.join(map(str, exercise['y2']))
            print(f"- First line x-values: {x1_str}")
            print(f"- First line y-values: {y1_str}")
            print(f"- Second line x-values: {x2_str}")
            print(f"- Second line y-values: {y2_str}")
            print(f"- Grid: color='{exercise['grid_color']}', linestyle='{exercise['grid_linestyle']}', linewidth={exercise['grid_linewidth']}")

        print("\nYou need to complete the following steps:\n")

        if exercise['number'] == 1:
            early = self._run_exercise1(ctx, exercise)
        elif exercise['number'] == 2:
            early = self._run_exercise2(ctx, exercise)
        else:
            early = self._run_exercise3(ctx, exercise)

        if early is not None:
            return early

        return ctx.finish()
    
    def start_exercises(self):
        """Start the plot exercises sequence."""
        self.generate_exercises()
        print_sequence_intro(
            "Line Plot Exercise",
            SESSION_INTRO_LINE,
        )
        run_exercise_sequence(self.exercises, self.run_exercise)
