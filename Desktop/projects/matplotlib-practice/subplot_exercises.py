"""
Subplot Exercises Module
Handles all subplot exercise generation, verification, and execution.
"""

import random
import re

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
    
    def verify_x_array(self, user_input):
        """Verify x array: x = np.array([0, 1, 2, 3])."""
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
    
    def verify_step_show(self, user_input):
        """Verify final step: plt.show()."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.show() - no parameters
        if normalized_input.lower() != 'plt.show()':
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def run_exercise(self, exercise, is_last):
        """Run a single subplot exercise. Returns True if completed, False if skipped."""
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: Subplot")
        print("="*70)
        print(f"\nCreate a subplot with the following specifications:")
        
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
        
        mistake_count = 0
        step_num = 1
        
        # Step 1: First x array
        print(f"STEP {step_num}: Define the first x-axis coordinates array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_x_array(user_input)
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
        step_num += 1
        
        # Step 2: First y array
        print(f"STEP {step_num}: Define the first y-axis coordinates array")
        print("   Variable name must be: y")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_y_array(user_input, exercise['y1'])
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
        step_num += 1
        
        # Step 3: First subplot
        print(f"STEP {step_num}: Create the first subplot")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_subplot(user_input, exercise['subplot1'])
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
        step_num += 1
        
        # Step 4: First plot
        print(f"STEP {step_num}: Plot the first line")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_plot(user_input)
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
        step_num += 1
        
        # Step 5: Title for first plot (if applicable)
        if exercise['has_titles']:
            print(f"STEP {step_num}: Add a title to the first plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_title(user_input, exercise['title1'])
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
            step_num += 1
        
        # Step 6: Second x array
        print(f"STEP {step_num}: Define the second x-axis coordinates array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_x_array(user_input)
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
        step_num += 1
        
        # Step 7: Second y array
        print(f"STEP {step_num}: Define the second y-axis coordinates array")
        print("   Variable name must be: y")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_y_array(user_input, exercise['y2'])
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
        step_num += 1
        
        # Step 8: Second subplot
        print(f"STEP {step_num}: Create the second subplot")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_subplot(user_input, exercise['subplot2'])
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
        step_num += 1
        
        # Step 9: Second plot
        print(f"STEP {step_num}: Plot the second line")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_plot(user_input)
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
        step_num += 1
        
        # Step 10: Title for second plot (if applicable)
        if exercise['has_titles']:
            print(f"STEP {step_num}: Add a title to the second plot")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_title(user_input, exercise['title2'])
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
            step_num += 1
        
        # Step 11: Super title (if applicable)
        if exercise['has_suptitle']:
            print(f"STEP {step_num}: Add a super title to the figure")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_suptitle(user_input, exercise['suptitle'])
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
            step_num += 1
        
        # Final step: Show
        print(f"STEP {step_num}: Show the plot")
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
        """Start the subplot exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - SUBPLOT EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive exercises for practicing")
        print("matplotlib.pyplot subplots. Complete each exercise step by step.\n")
        
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

