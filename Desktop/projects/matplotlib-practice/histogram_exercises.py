"""
Histogram Exercises Module
Handles all histogram exercise generation, verification, and execution.
"""

import random
import re

class HistogramExercises:
    """
    Class for handling histogram exercises.
    """
    
    def __init__(self):
        self.exercises = []
        self.generate_exercises()
    
    def generate_exercises(self):
        """Generate 3 histogram exercises."""
        for i in range(3):
            n1 = random.randint(100, 300)  # mean
            n2 = random.randint(50, 100)   # std
            n3 = random.randint(100, 300)  # size
            
            exercise = {
                'number': i + 1,
                'mean': n1,
                'std': n2,
                'size': n3
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
    
    def verify_step1(self, user_input, mean, std, size):
        """Verify Step 1: Create data using np.random.normal."""
        normalized_input = self.normalize_code(user_input)
        
        # Check variable name exactly
        if not re.match(r'x\s*=', normalized_input, re.IGNORECASE):
            return False, "Variable name should be 'x'"
        
        # Check for np.random.normal - must be exact function name (not np.random.normals, etc.)
        if not re.search(r'\bnp\.random\.normal\s*\(', normalized_input, re.IGNORECASE):
            return False, "Should use np.random.normal()"
        
        # Extract the three parameters
        normal_match = re.search(r'np\.random\.normal\s*\(\s*([^)]+)\s*\)', normalized_input, re.IGNORECASE)
        if not normal_match:
            return False, "Invalid format"
        
        params_str = normal_match.group(1)
        params = [p.strip() for p in params_str.split(',')]
        
        if len(params) != 3:
            return False, "Invalid format"
        
        try:
            # Parse the three parameters (should be integers in this case)
            param1 = int(params[0])
            param2 = int(params[1])
            param3 = int(params[2])
            
            # Check exact match (order matters: mean, std, size)
            if param1 != mean or param2 != std or param3 != size:
                return False, "Incorrect values or order"
            
            return True, "Correct!"
        except ValueError:
            return False, "Invalid format"
        except Exception:
            return False, "Invalid format"
    
    def verify_step2(self, user_input):
        """Verify Step 2: plt.hist(x)."""
        normalized_input = self.normalize_code(user_input)
        
        # Must be exactly plt.hist(x)
        if normalized_input.lower() != 'plt.hist(x)':
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
        """Run a single histogram exercise. Returns True if completed, False if skipped."""
        print("\n" + "="*70)
        print(f"EXERCISE {exercise['number']}: Histogram")
        print("="*70)
        print(f"\nCreate a histogram with the following specifications:")
        print(f"- Use np.random.normal with mean={exercise['mean']}, std={exercise['std']}, size={exercise['size']}")
        
        print("\nYou need to complete the following steps:\n")
        
        mistake_count = 0
        
        # Step 1: Create data
        print("STEP 1: Create the data array")
        print("   Variable name must be: x")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step1(user_input, exercise['mean'], exercise['std'], exercise['size'])
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
        
        # Step 2: Plot histogram
        print("STEP 2: Plot the histogram")
        while True:
            user_input = input("   Your code: ").strip()
            correct, message = self.verify_step2(user_input)
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
        
        # Step 3: Show histogram
        print("STEP 3: Show the histogram")
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
        """Start the histogram exercises sequence."""
        print("="*70)
        print("MATPLOTLIB PYPLOT PRACTICE - HISTOGRAM EXERCISES")
        print("="*70)
        print("\nThis program contains 3 consecutive exercises for practicing")
        print("matplotlib.pyplot histograms. Complete each exercise step by step.\n")
        
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