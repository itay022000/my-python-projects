"""
Plot Exercises
Exercises for practicing basic matplotlib.pyplot plotting.
"""

import random
import re


class PlotExercises:
    """Exercises for practicing basic pyplot line plotting."""
    
    def __init__(self):
        self.colors_list = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink",
            "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
            "navy", "coral", "teal", "gold", "silver", "indigo", "violet"
        ]
        self.linestyles = ["solid", "dotted", "dashed", "dashdot"]
        self.markers = ["o", "*", ".", "x", "+", "s", "D", "H"]
        self.fmt_lines = ["-", ":", "--", "-."]
        self.fmt_colors = ["r", "g", "b", "c", "m", "y", "k", "w"]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 plot exercises."""
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
    
    def normalize_code(self, code):
        """Normalize code string for comparison (remove extra whitespace)."""
        # Remove leading/trailing whitespace
        code = code.strip()
        # Normalize multiple spaces to single space
        code = re.sub(r'\s+', ' ', code)
        # Normalize spaces around operators and parentheses
        code = re.sub(r'\s*([=\[\]\(\)])\s*', r'\1', code)
        code = re.sub(r'=\s*', '=', code)
        return code.strip()
    
    def verify_y_array(self, user_input, var_name, expected_values):
        """Verify y array: y1/y2/y3 = np.array([n1, n2, n3, n4])."""
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
    
    def verify_step_show(self, user_input):
        """Verify final step: plt.show()."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.show() - no parameters
        if normalized_input.lower() != 'plt.show()':
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def run_exercise(self, exercise, is_last):
        """Run a single plot exercise. Returns True if completed, False if skipped."""
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: Plot")
        print("="*70)
        
        if exercise['number'] == 1:
            print(f"\nCreate 3 different lines with the following specifications:")
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
            print(f"\nCreate 2 lines with labels and title with the following specifications:")
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
            print(f"\nCreate 2 lines with a grid with the following specifications:")
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
        
        mistake_count = 0
        
        if exercise['number'] == 1:
            # Step 1: y1 array
            print("STEP 1: Define the y-axis coordinates array for the first line")
            print("   Variable name must be: y1")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y1', exercise['y1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 2: y2 array
            print("STEP 2: Define the y-axis coordinates array for the second line")
            print("   Variable name must be: y2")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y2', exercise['y2'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 3: y3 array
            print("STEP 3: Define the y-axis coordinates array for the third line")
            print("   Variable name must be: y3")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y3', exercise['y3'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 4: Plot first line
            print("STEP 4: Plot the first line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step4_line1(user_input, exercise['linestyle'], exercise['linewidth'], exercise['color1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 5: Plot second line
            print("STEP 5: Plot the second line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step5_line2(user_input, exercise['marker'], exercise['marker_size'], exercise['mec'], exercise['mfc'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 6: Plot third line
            print("STEP 6: Plot the third line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step6_line3(user_input, exercise['fmt'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 7: Show plot
            print("STEP 7: Show the plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step_show(user_input)
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
        
        elif exercise['number'] == 2:
            # Step 1: x1 array
            print("STEP 1: Define the x-axis coordinates array for the first line")
            print("   Variable name must be: x1")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_x_array(user_input, 'x1', exercise['x1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 2: y1 array
            print("STEP 2: Define the y-axis coordinates array for the first line")
            print("   Variable name must be: y1")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y1', exercise['y1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 3: x2 array
            print("STEP 3: Define the x-axis coordinates array for the second line")
            print("   Variable name must be: x2")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_x_array(user_input, 'x2', exercise['x2'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 4: y2 array
            print("STEP 4: Define the y-axis coordinates array for the second line")
            print("   Variable name must be: y2")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y2', exercise['y2'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 5: Title
            print("STEP 5: Create a title for the plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_title(user_input, exercise['title'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 6: X-axis label
            print("STEP 6: Create a label for the x-axis")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_xlabel(user_input, exercise['xlabel'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 7: Y-axis label
            print("STEP 7: Create a label for the y-axis")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_ylabel(user_input, exercise['ylabel'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 8: Plot both lines
            print("STEP 8: Plot the first line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_plot_simple(user_input, 'x1', 'y1')
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            print("STEP 9: Plot the second line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_plot_simple(user_input, 'x2', 'y2')
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 9 (actually step 10 now): Show plot
            print("STEP 10: Show the plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step_show(user_input)
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
        
        elif exercise['number'] == 3:
            x1_str = ', '.join(map(str, exercise['x1']))
            y1_str = ', '.join(map(str, exercise['y1']))
            x2_str = ', '.join(map(str, exercise['x2']))
            y2_str = ', '.join(map(str, exercise['y2']))
            
            # Step 1: x1 array
            print("STEP 1: Define the x-axis coordinates array for the first line")
            print("   Variable name must be: x1")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_x_array(user_input, 'x1', exercise['x1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 2: y1 array
            print("STEP 2: Define the y-axis coordinates array for the first line")
            print("   Variable name must be: y1")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y1', exercise['y1'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 3: x2 array
            print("STEP 3: Define the x-axis coordinates array for the second line")
            print("   Variable name must be: x2")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_x_array(user_input, 'x2', exercise['x2'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 4: y2 array
            print("STEP 4: Define the y-axis coordinates array for the second line")
            print("   Variable name must be: y2")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_y_array(user_input, 'y2', exercise['y2'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 5: Plot first line
            print("STEP 5: Plot the first line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_plot_simple(user_input, 'x1', 'y1')
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 6: Plot second line
            print("STEP 6: Plot the second line")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_plot_simple(user_input, 'x2', 'y2')
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 7: Grid
            print("STEP 7: Create a grid")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_grid(user_input, exercise['grid_color'], exercise['grid_linestyle'], exercise['grid_linewidth'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            
            # Step 8: Show plot
            print("STEP 8: Show the plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step_show(user_input)
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        if is_last:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Terminating exercises sequence.\n")
                        else:
                            print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
        
        print(f"🎉 Exercise {exercise['number']} completed successfully!")
        return True
    
    def start_exercises(self):
        """Start the plot exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - PLOT EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive exercises for practicing")
        print("matplotlib.pyplot line plotting. Complete each exercise step by step.\n")
        
        input("Press Enter to start...")
        
        # Statistics tracking
        completed_count = 0
        not_completed_count = 0
        
        for i, exercise in enumerate(self.exercises):
            is_last = (i == len(self.exercises) - 1)
            completed = self.run_exercise(exercise, is_last)
            if completed:
                completed_count += 1
            else:
                not_completed_count += 1
                if is_last:
                    # Last exercise was skipped, terminate
                    break
                # Continue to next exercise
                continue
        
        # Calculate statistics
        total = completed_count + not_completed_count
        if total > 0:
            completed_pct = (completed_count / total) * 100
            not_completed_pct = (not_completed_count / total) * 100
            
            print("\n" + "="*70)
            print("EXERCISES SEQUENCE STATISTICS")
            print("="*70)
            print(f"\nTotal exercises: {total}")
            print(f"Successfully completed: {completed_count} ({completed_pct:.1f}%)")
            print(f"Not completed: {not_completed_count} ({not_completed_pct:.1f}%)")
            print("="*70 + "\n")
        else:
            print("\nNo exercises were attempted.\n")