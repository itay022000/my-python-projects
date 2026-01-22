"""
Bar Plot Exercises Module
Handles all bar plot exercise generation, verification, and execution.
"""

import random
import re

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
        self.colors_list = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink",
            "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
            "navy", "coral", "teal", "gold", "silver", "indigo", "violet"
        ]
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 bar plot exercises."""
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
    
    def verify_step1(self, user_input, labels):
        """Verify Step 1: labels array with capital letters."""
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
    
    def verify_step_show(self, user_input):
        """Verify final step: plt.show()."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.show() - no parameters
        if normalized_input.lower() != 'plt.show()':
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def run_exercise(self, exercise, is_last):
        """Run a single bar plot exercise. Returns True if completed, False if skipped."""
        plot_type = "Horizontal Bar Plot" if exercise['is_horizontal'] else "Bar Plot"
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: {plot_type}")
        print("="*70)
        print(f"\nCreate a {'horizontal ' if exercise['is_horizontal'] else ''}bar plot with the following specifications:")
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
        
        mistake_count = 0
        
        # Step 1: Labels
        print("STEP 1: Define the bar labels array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step1(user_input, exercise['labels'])
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
        
        # Step 2: Heights
        print("STEP 2: Define the bar heights array")
        print("   Variable name must be: y")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step2(user_input, exercise['heights'])
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
        
        # Step 3: Plot bar
        print("STEP 3: Plot the bar")
        if exercise['has_width']:
            print(f"   Remember to include width={exercise['width']}")
        if exercise['is_horizontal']:
            print(f"   Remember to include color=\"{exercise['color']}\" and height={exercise['height']}")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step3(
                user_input, 
                exercise['has_width'], 
                exercise.get('width'),
                exercise['is_horizontal'],
                exercise.get('color'),
                exercise.get('height')
            )
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
        
        # Step 4: Show plot
        print("STEP 4: Show the plot")
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
        """Start the bar plot exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - BAR PLOT EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive exercises for practicing")
        print("matplotlib.pyplot bar plots. Complete each exercise step by step.\n")
        
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

