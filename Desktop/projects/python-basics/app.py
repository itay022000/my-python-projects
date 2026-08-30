"""
Python Basics — application shell (B015).
"""

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
    """Main entry: menu and links to exercise batches."""

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
            print("Python Basics Practice")
            print("=" * 70)
            print("1.  Basic Topics Exercise")
            print("2.  Strings and Booleans Exercise")
            print("3.  Operators Exercise")
            print("4.  Lists Exercise")
            print("5.  Tuples Exercise")
            print("6.  Sets Exercise")
            print("7.  Dictionaries Exercise")
            print("8.  Functions Exercise")
            print("9.  Additional Topics Exercise")
            print("10. Advanced Topics Exercise")
            print("11. Exit (or type 'exit'/'Exit')")
            print("=" * 70)
            prompt = "Select an option (1-11 or 'exit'/'Exit'): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break

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
            elif choice == "11" or choice in ("exit", "Exit"):
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice. Please select 1-11, or type 'exit'/'Exit'.")
