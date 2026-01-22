"""
Pie Chart Exercises Module
Handles all pie chart exercise generation, verification, and execution.
"""

import random
import re

class PieChartExercises:
    """
    Class for handling pie chart exercises.
    """
    
    def __init__(self):
        self.colors_list = [
            "red", "blue", "green", "yellow", "orange", "purple", "pink",
            "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
            "navy", "coral", "teal", "gold", "silver", "indigo", "violet"
        ]
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
        """Generate 3 pie chart exercises with random attributes."""
        # Exercise 3 (index 2): always has shadow, legend with title "fruits"
        # 1-2 exercises have explode
        explode_indices = random.sample(range(3), random.randint(1, 2))
        
        for i in range(3):
            proportions = self.generate_proportions()
            colors = random.sample(self.colors_list, 5)
            labels = random.sample(self.fruit_names, 5)  # Random 5 fruits from 10
            
            # Exercise 3 (index 2): always shadow + legend with title "fruits"
            if i == 2:
                has_legend = True
                has_shadow = True
                legend_title = "fruits"
            else:
                has_legend = random.choice([True, False])
                has_shadow = random.choice([True, False])
                legend_title = None
            
            has_explode = i in explode_indices
            explode = self.generate_explode() if has_explode else None
            
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
    
    def verify_step1(self, user_input, proportions):
        """Verify Step 1: proportions array."""
        normalized_input = self.normalize_code(user_input)
        
        # Build exact expected format
        proportions_str = '[' + ', '.join(map(str, proportions)) + ']'
        expected = f"x=np.array({proportions_str})"
        normalized_expected = self.normalize_code(expected)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        normalized_input = self.normalize_code(user_input)
        
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
        
        normalized_input = self.normalize_code(user_input)
        
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
    
    def verify_step_show(self, user_input):
        """Verify final step: plt.show()."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.show() - no parameters
        if normalized_input.lower() != 'plt.show()':
            return False, "Invalid format"
        
        return True, "Correct!"
    
    def run_exercise(self, exercise, is_last):
        """Run a single pie chart exercise. Returns True if completed, False if skipped."""
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: Pie Chart")
        print("="*70)
        print(f"\nCreate a pie chart with the following specifications:")
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
        
        mistake_count = 0
        
        # Step 1: Proportions
        print("STEP 1: Define the proportions array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step1(user_input, exercise['proportions'])
            if correct:
                print(f"   ✓ {message}\n")
                break
            else:
                mistake_count += 1
                print(f"   ✗ {message}")
                if mistake_count >= 3:
                    print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                    return False
                print("   Try again...\n")
        
        # Step 2: Colors
        print("STEP 2: Define the colors array")
        print("   Variable name must be: c")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step2(user_input, exercise['colors'])
            if correct:
                print(f"   ✓ {message}\n")
                break
            else:
                mistake_count += 1
                print(f"   ✗ {message}")
                if mistake_count >= 3:
                    print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                    return False
                print("   Try again...\n")
        
        # Step 3: Labels
        print("STEP 3: Define the labels array")
        print("   Variable name must be: lb")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step3(user_input, exercise['labels'])
            if correct:
                print(f"   ✓ {message}\n")
                break
            else:
                mistake_count += 1
                print(f"   ✗ {message}")
                if mistake_count >= 3:
                    print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                    return False
                print("   Try again...\n")
        
        # Step 4 (or 4a): Explode array, if required
        step_num = 4
        if exercise.get('has_explode') and exercise.get('explode'):
            print("STEP 4: Define the explode array")
            print("   Variable name must be: ex")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step_explode(user_input, exercise['explode'])
                if correct:
                    print(f"   ✓ {message}\n")
                    break
                else:
                    mistake_count += 1
                    print(f"   ✗ {message}")
                    if mistake_count >= 3:
                        print(f"\n⚠️  You have made 3 mistakes in this exercise. Skipping to the next exercise...\n")
                        return False
                    print("   Try again...\n")
            step_num = 5
        
        # Step 4 or 5: plt.pie() call
        print(f"STEP {step_num}: Create the pie chart using plt.pie()")
        if exercise.get('has_explode'):
            print("   Remember to include the ex (explode) variable")
        if exercise['has_shadow']:
            print("   Remember to include shadow=True")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step4(user_input, exercise['has_shadow'], exercise.get('has_explode', False))
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
        
        # Step: plt.legend() if required
        if exercise['has_legend']:
            legend_step = step_num + 1
            print(f"STEP {legend_step}: Add a legend to the pie chart")
            if exercise.get('legend_title'):
                print("   The legend must have a title, as specified in the exercise")
            while True:
                user_input = input("   Your code: ").strip()
                correct, message = self.verify_step5(user_input, exercise['has_legend'], exercise.get('legend_title'))
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
        
        # Final step: plt.show()
        if exercise['has_legend']:
            show_step = legend_step + 1
        else:
            show_step = step_num + 1
        print(f"STEP {show_step}: Show the chart")
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
        """Start the pie chart exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - PIE CHART EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive pie chart exercises for practicing")
        print("matplotlib.pyplot pie charts. Complete each exercise step by step.\n")
        
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