"""
Scatter Plot Exercises Module
Handles all scatter plot exercise generation, verification, and execution.
"""

import random
import re

class ScatterPlotExercises:
    """
    Class for handling scatter plot exercises.
    """
    
    def __init__(self):
        self.colors_list = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink",
            "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
            "navy", "coral", "teal", "gold", "silver", "indigo", "violet"
        ]
        self.colormaps = [
            "Reds", "Greens", "Blues", "hot", "ocean",
            "spring", "summer", "winter", "viridis", "nipy_spectral"
        ]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 scatter plot exercises."""
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
    
    def verify_step1(self, user_input, x_coords):
        """Verify Step 1: x coordinates array."""
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
    
    def verify_step_show(self, user_input):
        """Verify final step: plt.show()."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.show() - no parameters
        if normalized_input.lower() != 'plt.show()':
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def run_exercise(self, exercise, is_last):
        """Run a single scatter plot exercise. Returns True if completed, False if skipped."""
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: Scatter Plot")
        print("="*70)
        print(f"\nCreate a scatter plot with the following specifications:")
        
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
        
        mistake_count = 0
        
        # Step 1: X coordinates
        print("STEP 1: Define the x-axis coordinates array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step1(user_input, exercise['x_coords'])
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
        
        # Step 2: Y coordinates
        print("STEP 2: Define the y-axis coordinates array")
        print("   Variable name must be: y")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step2(user_input, exercise['y_coords'])
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
        
        # Step 3: Exercise-specific additional arrays
        step_num = 3
        if exercise['number'] == 1:
            # Exercise 1: No additional arrays, skip to plot
            step_num = 3
        elif exercise['number'] == 2:
            # Exercise 2: Colors array
            print("STEP 3: Define the colors array")
            print("   Variable name must be: colors")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step3_colors_array(user_input, exercise['colors_array'])
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
            
            # Step 4: Sizes array
            print("STEP 4: Define the sizes array")
            print("   Variable name must be: sizes")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step4_sizes(user_input, exercise['sizes_array'])
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
            step_num = 5
        elif exercise['number'] == 3:
            # Exercise 3: Colors array (numeric)
            print("STEP 3: Define the colors array")
            print("   Variable name must be: colors")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step3_colors_numeric(user_input, exercise['colors_array'])
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
            
            # Step 4: Sizes array
            print("STEP 4: Define the sizes array")
            print("   Variable name must be: sizes")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step4_sizes(user_input, exercise['sizes_array'])
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
            step_num = 5
        
        # Plot step
        print(f"STEP {step_num}: Plot the scatter plot")
        if exercise['number'] == 1:
            print(f"   Remember to include color=\"{exercise['color']}\"")
        elif exercise['number'] == 2:
            print("   Remember to include c=colors and s=sizes")
        elif exercise['number'] == 3:
            print(f"   Remember to include c=colors, s=sizes, alpha={exercise['alpha']}, and cmap=\"{exercise['cmap']}\"")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step_plot(user_input, exercise)
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
        
        # Show step
        show_step = step_num + 1
        print(f"STEP {show_step}: Show the plot")
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
        """Start the scatter plot exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - SCATTER PLOT EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive exercises for practicing")
        print("matplotlib.pyplot scatter plots. Complete each exercise step by step.\n")
        
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
        completed_pct = (completed_count / total * 100) if total > 0 else 0
        not_completed_pct = (not_completed_count / total * 100) if total > 0 else 0
        
        # Display statistics
        print("\n" + "="*70)
        print("EXERCISE SEQUENCE STATISTICS")
        print("="*70)
        print(f"\nCompleted successfully: {completed_count} ({completed_pct:.1f}%)")
        print(f"Not completed: {not_completed_count} ({not_completed_pct:.1f}%)")
        print(f"Total exercises: {total}")
        print("\n" + "="*70)