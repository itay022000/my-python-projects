"""
Python Basics
Interactive practice for fundamental Python topics (output, comments, variables, types, etc.).
"""

import sys
from pathlib import Path

# Ensure the script's directory is on the path so imports work when run from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_1_exercises import Batch1Exercises
from batch_2_exercises import Batch2Exercises
from batch_3_exercises import Batch3Exercises
from batch_4_exercises import Batch4Exercises
from batch_5_exercises import Batch5Exercises
from batch_6_exercises import Batch6Exercises
from batch_7_exercises import Batch7Exercises
from batch_8_exercises import Batch8Exercises
from batch_9_exercises import Batch9Exercises
from batch_10_exercises import Batch10Exercises


class PythonBasics:
    """
    Main entry: menu and links to exercise batches.
    """

    def __init__(self):
        self.batch_1 = Batch1Exercises()
        self.batch_2 = Batch2Exercises()
        self.batch_3 = Batch3Exercises()
        self.batch_4 = Batch4Exercises()
        self.batch_5 = Batch5Exercises()
        self.batch_6 = Batch6Exercises()
        self.batch_7 = Batch7Exercises()
        self.batch_8 = Batch8Exercises()
        self.batch_9 = Batch9Exercises()
        self.batch_10 = Batch10Exercises()

    def main_menu(self):
        """Display main menu and handle choices."""
        while True:
            print("\n" + "=" * 70)
            print("PYTHON BASICS")
            print("=" * 70)
            print("\n1.  Basic topics")
            print("2.  Strings and booleans")
            print("3.  Operators")
            print("4.  Lists")
            print("5.  Tuples")
            print("6.  Sets")
            print("7.  Dictionaries")
            print("8.  Functions")
            print("9.  Additional topics")
            print("10. Advanced topics")
            print("11. Exit (or type 'exit')")

            choice = input("\nSelect an option (1–11 or 'exit'): ").strip().lower()

            if choice == "1":
                self.batch_1.start_exercises()
            elif choice == "2":
                self.batch_2.start_exercises()
            elif choice == "3":
                self.batch_3.start_exercises()
            elif choice == "4":
                self.batch_4.start_exercises()
            elif choice == "5":
                self.batch_5.start_exercises()
            elif choice == "6":
                self.batch_6.start_exercises()
            elif choice == "7":
                self.batch_7.start_exercises()
            elif choice == "8":
                self.batch_8.start_exercises()
            elif choice == "9":
                self.batch_9.start_exercises()
            elif choice == "10":
                self.batch_10.start_exercises()
            elif choice == "11" or choice == "exit":
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice. Please select 1–11, or type 'exit'.")


if __name__ == "__main__":
    app = PythonBasics()
    app.main_menu()
