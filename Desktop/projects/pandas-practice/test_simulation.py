#!/usr/bin/env python3
"""
Simulation script to test the pandas practice application.
This script simulates user interactions to verify the application works correctly.
"""

import subprocess
import sys
import time
import re
from io import StringIO

class SimulationRunner:
    def __init__(self):
        self.test_results = []
        self.errors = []
        self.failed_tests_diagnostics = []
        
    def log(self, message, status=""):
        """Log a test message."""
        if status == "PASS":
            print(f"[✓] {message}")
        elif status == "FAIL":
            print(f"[✗] {message}")
        else:
            print(f"[TEST] {message}")
    
    def print_diagnostic(self, test_name, issue, fix_location, fix_instructions):
        """Print diagnostic information for a failed test."""
        print(f"\n{'='*70}")
        print(f"DIAGNOSTIC: {test_name}")
        print(f"{'='*70}")
        print(f"❌ ISSUE: {issue}")
        print(f"\n📍 WHERE TO FIX IN main.py:")
        print(f"   {fix_location}")
        print(f"\n🔧 HOW TO FIX:")
        for i, instruction in enumerate(fix_instructions, 1):
            print(f"   {i}. {instruction}")
        print(f"{'='*70}\n")
        
    def run_simulation(self, inputs, description):
        """Run a simulation with given inputs."""
        self.log(f"Starting: {description}")
        
        try:
            # Create process
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Prepare input string
            input_str = "\n".join(inputs) + "\n"
            
            # Send inputs and get output
            try:
                stdout, stderr = process.communicate(input=input_str, timeout=60)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                self.errors.append(f"{description}: Timeout after 30 seconds")
                return False, stdout, stderr
            
            # Check for errors
            if stderr and "Traceback" in stderr:
                self.errors.append(f"{description}: Error occurred\n{stderr}")
                return False, stdout, stderr
                
            return True, stdout, stderr
            
        except Exception as e:
            self.errors.append(f"{description}: Exception - {str(e)}")
            return False, "", str(e)
    
    def test_dataset_loading_validation(self):
        """Test that invalid dataset choices are handled correctly."""
        test_name = "Dataset loading validation"
        self.log(f"Testing {test_name}...")
        
        # Test: invalid input, then valid input
        # Note: After loading dataset, it goes back to main menu
        inputs = [
            "1",  # Main menu: Load dataset
            "5",  # Invalid dataset number (should prompt again)
            "1",  # Valid dataset number
            "5",  # Main menu: Exit
        ]
        
        success, stdout, stderr = self.run_simulation(
            inputs,
            test_name
        )
        
        if success:
            # Check that invalid input message appears
            if "Invalid" in stdout or "invalid" in stdout.lower():
                self.test_results.append((test_name, "PASS"))
                print(f"[✓] {test_name}: PASS")
            else:
                self.test_results.append((test_name, "FAIL - No invalid message"))
                print(f"[✗] {test_name}: FAIL - No invalid message found")
                self.print_diagnostic(
                    test_name,
                    "Invalid dataset number (5) was accepted or no error message shown",
                    "Method: list_datasets() - around line 200-250",
                    [
                        "Check the while loop in list_datasets() method",
                        "Ensure it validates input: if 0 <= idx < len(datasets)",
                        "Verify it prints error message: '❌ Invalid number! Please enter...'",
                        "Make sure the loop continues until valid input is provided"
                    ]
                )
        else:
            self.test_results.append((test_name, "ERROR"))
            self.log(f"✗ {test_name}: Error occurred", "FAIL")
            if stderr:
                print(f"\nError details:\n{stderr[:500]}")
            
    def test_correct_answer_display(self):
        """Test that correct answer is shown exactly once after 3 failed attempts."""
        test_name = "Correct answer display (3 failed attempts)"
        self.log(f"Testing {test_name}...")
        
        # Provide enough inputs for the first task to fail 3 times, then exit
        inputs = [
            "1",  # Main menu: Load dataset
            "1",  # Select first dataset
            "3",  # Main menu: Run Exercise
            "1",  # Exercise menu: Exercise 1
            "wrong_answer_1",  # Task 1, Attempt 1
            "wrong_answer_2",  # Task 1, Attempt 2
            "wrong_answer_3",  # Task 1, Attempt 3 (should show answer and move to next task)
            "exit",  # Exit exercise after seeing the answer
            "",   # Press Enter to continue (after exercise exits)
            "5",  # Main menu: Exit
        ]
        
        success, stdout, stderr = self.run_simulation(
            inputs,
            test_name
        )
        
        if success:
            # Count occurrences of "CORRECT ANSWER"
            correct_answer_count = stdout.count("CORRECT ANSWER")
            if correct_answer_count == 1:
                self.test_results.append((test_name, "PASS"))
                print(f"[✓] {test_name}: PASS - Answer shown exactly once ({correct_answer_count} times)")
            else:
                self.test_results.append((test_name, f"FAIL - Shown {correct_answer_count} times (expected 1)"))
                print(f"[✗] {test_name}: FAIL - Shown {correct_answer_count} times (expected 1)")
                self.print_diagnostic(
                    test_name,
                    f"Correct answer shown {correct_answer_count} times instead of exactly once",
                    "Method: exercise_1_basic_operations() - Task 1 (around line 700-750)",
                    [
                        "Check the while attempts < max_attempts loop in Task 1",
                        "Ensure 'CORRECT ANSWER' is printed only in ONE place when attempts >= max_attempts",
                        "Look for duplicate print statements or multiple break points",
                        "Verify the answer is shown in the 'else' block when attempts >= max_attempts",
                        "Make sure there's no duplicate answer display after the while loop"
                    ]
                )
        else:
            self.test_results.append((test_name, "ERROR"))
            print(f"[✗] {test_name}: ERROR - Error occurred")
            if stderr:
                print(f"\nError details:\n{stderr[:500]}")
    
    def test_skip_command(self):
        """Test that 'skip' command works correctly."""
        test_name = "Skip command"
        self.log(f"Testing {test_name}...")
        
        inputs = [
            "1",  # Main menu: Load dataset
            "1",  # Select first dataset
            "3",  # Main menu: Run Exercise
            "1",  # Exercise menu: Exercise 1
            "skip",  # Skip first task
            "skip",  # Skip second task (to move through exercise faster)
            "skip",  # Skip third task
            "skip",  # Skip fourth task
            "skip",  # Skip fifth task
            "skip",  # Skip sixth task
            "skip",  # Skip seventh task
            "skip",  # Skip eighth task
            "",   # Press Enter to continue (after exercise completes)
            "5",  # Main menu: Exit
        ]
        
        success, stdout, stderr = self.run_simulation(
            inputs,
            test_name
        )
        
        if success:
            if "Task skipped" in stdout or "skipped" in stdout.lower():
                self.test_results.append((test_name, "PASS"))
                print(f"[✓] {test_name}: PASS - Command worked correctly")
            else:
                self.test_results.append((test_name, "FAIL - Skip not recognized"))
                print(f"[✗] {test_name}: FAIL - Skip not recognized")
                self.print_diagnostic(
                    test_name,
                    "The 'skip' command was not recognized or didn't show 'Task skipped' message",
                    "Method: handle_special_commands() - around line 156-177",
                    [
                        "Check handle_special_commands() method in main.py",
                        "Verify it checks: if code_lower == 'skip':",
                        "Ensure it prints: '⏭️  Task skipped' and '📖 CORRECT ANSWER:'",
                        "Check that all exercise tasks call handle_special_commands() before processing code",
                        "Verify the pattern: is_skip, is_exit, should_continue = self.handle_special_commands(...)",
                        "Make sure tasks check 'if is_skip: break' to skip the task"
                    ]
                )
        else:
            self.test_results.append((test_name, "ERROR"))
            print(f"[✗] {test_name}: ERROR - Error occurred")
            if stderr:
                print(f"\nError details:\n{stderr[:500]}")
    
    def test_exit_command(self):
        """Test that 'exit' command works correctly."""
        test_name = "Exit command"
        self.log(f"Testing {test_name}...")
        
        inputs = [
            "1",  # Main menu: Load dataset
            "1",  # Select first dataset
            "3",  # Main menu: Run Exercise
            "1",  # Exercise menu: Exercise 1
            "df.head(5)",  # Correct answer for task 1 (if it asks for head)
            "exit",  # Exit during task 2
            "5",  # Main menu: Exit
        ]
        
        success, stdout, stderr = self.run_simulation(
            inputs,
            test_name
        )
        
        if success:
            if "Exercise exited" in stdout or "exited" in stdout.lower():
                self.test_results.append((test_name, "PASS"))
                print(f"[✓] {test_name}: PASS - Command worked correctly")
            else:
                self.test_results.append((test_name, "FAIL - Exit not recognized"))
                print(f"[✗] {test_name}: FAIL - Exit not recognized")
                self.print_diagnostic(
                    test_name,
                    "The 'exit' command was not recognized or didn't exit the exercise",
                    "Method: handle_special_commands() and exercise methods - around line 156-177 and exercise_1_basic_operations()",
                    [
                        "Check handle_special_commands() method - verify it returns (False, True, False) for 'exit'",
                        "In exercise methods, check: if is_exit: block",
                        "Verify it calls: self.record_exercise_completion('exercise_X', tasks_completed, total_tasks)",
                        "Ensure it prints: '⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)'",
                        "Make sure it returns immediately: return (not just break)",
                        "Check that all exercise tasks call handle_special_commands() before processing code"
                    ]
                )
        else:
            self.test_results.append((test_name, "ERROR"))
            self.log(f"✗ {test_name}: Error occurred", "FAIL")
            if stderr:
                print(f"\nError details:\n{stderr[:500]}")
    
    def run_all_tests(self):
        """Run all simulation tests."""
        print("\n" + "="*60)
        print("PANDAS PRACTICE - SIMULATION TEST SUITE")
        print("="*60 + "\n")
        
        # Run tests
        self.test_dataset_loading_validation()
        time.sleep(0.5)  # Small delay between tests
        
        self.test_correct_answer_display()
        time.sleep(0.5)
        
        self.test_skip_command()
        time.sleep(0.5)
        
        self.test_exit_command()
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, result in self.test_results if result == "PASS")
        failed_count = len(self.test_results) - passed
        total = len(self.test_results)
        
        print("\n" + "="*60)
        print("SUMMARY OF ALL TESTS:")
        print("="*60)
        for test_name, result in self.test_results:
            if result == "PASS":
                print(f"  [✓] {test_name}: PASS")
            else:
                print(f"  [✗] {test_name}: {result}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if failed_count > 0:
            print(f"\n❌ FAILED TESTS ({failed_count}):")
            for test_name, result in self.test_results:
                if result != "PASS":
                    print(f"   • {test_name}: {result}")
        
        if self.errors:
            print("\n" + "="*60)
            print("ERRORS:")
            print("="*60)
            for error in self.errors:
                print(f"  - {error}")
        
        # Show diagnostics summary
        failed_count = total - passed
        if failed_count > 0:
            print(f"\n⚠️  {failed_count} test(s) failed. See diagnostic messages above for how to fix.")
            print("   Look for 'DIAGNOSTIC:' sections that explain what to fix in main.py")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    runner = SimulationRunner()
    runner.run_all_tests()