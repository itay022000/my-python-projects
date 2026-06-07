"""Main, explore, and statistics menus mixin."""

import sys
import termios
import tty


class MenusMixin:
    """Mixin for PandasPractice."""

    def wait_for_esc(self):
        """Wait for ESC key press to return to menu."""
        print("\n" + "-"*60)
        print("Press ESC to return to menu...")
        
        # Save terminal settings
        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    char = sys.stdin.read(1)
                    # ESC key is ASCII 27
                    if ord(char) == 27:
                        break
            finally:
                # Restore terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            # Fallback if not in a terminal
            input("Press Enter to return to menu...")
    def explore_dataset(self, df=None):
        """Interactive dataset exploration."""
        if df is None:
            df = self.current_dataset
        
        if df is None:
            print("❌ No dataset loaded! The dataset should be automatically loaded. Please restart the program.")
            return
        
        
        while True:
            print("\n" + "="*60)
            print("📊 DATASET EXPLORATION MENU")
            print("="*60)
            print("1. View first few rows (head)")
            print("2. View last few rows (tail)")
            print("3. View dataset info")
            print("4. View basic statistics")
            print("5. View column names and data types")
            print("6. View unique values in a column")
            print("7. Filter data by condition")
            print("8. Sort data")
            print("9. Return to main menu")
            
            choice = input("\nSelect an option (1-9): ").strip()
            
            if choice == "1":
                rows = input("How many rows? (default 5): ").strip()
                n = int(rows) if rows.isdigit() else 5
                print(f"\n📋 First {n} rows:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.head(n))
                self.wait_for_esc()
                
            elif choice == "2":
                rows = input("How many rows? (default 5): ").strip()
                n = int(rows) if rows.isdigit() else 5
                print(f"\n📋 Last {n} rows:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.tail(n))
                self.wait_for_esc()
                
            elif choice == "3":
                print("\n📋 Dataset Info:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.info())
                self.wait_for_esc()
                
            elif choice == "4":
                print("\n📊 Basic Statistics:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.describe())
                self.wait_for_esc()
                
            elif choice == "5":
                print("\n📋 Columns and Data Types:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.dtypes)
                self.wait_for_esc()
                
            elif choice == "6":
                col = input("Enter column name: ").strip()
                if col in df.columns:
                    print(f"\n📋 Unique values in '{col}':")
                    print(f"Dataset: {self.current_dataset_name}")
                    print(df[col].unique())
                    print(f"\nCount: {df[col].nunique()} unique values")
                    self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "7":
                col = input("Enter column name to filter: ").strip()
                if col in df.columns:
                    print(f"\nSample values in '{col}': {df[col].unique()[:5]}")
                    value = input(f"Enter value to filter by: ").strip()
                    try:
                        # Try numeric comparison
                        if df[col].dtype in ['int64', 'float64']:
                            value = float(value)
                            filtered = df[df[col] == value]
                        else:
                            filtered = df[df[col] == value]
                        print(f"\n📊 Filtered results ({len(filtered)} rows):")
                        print(f"Dataset: {self.current_dataset_name}")
                        print(filtered)
                        self.wait_for_esc()
                    except:
                        print("❌ Error filtering data. Check your input.")
                        self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "8":
                col = input("Enter column to sort by: ").strip()
                if col in df.columns:
                    order = input("Sort ascending? (yes/no, default yes): ").strip().lower()
                    ascending = order != 'no'
                    sorted_df = df.sort_values(by=col, ascending=ascending)
                    print(f"\n📊 Sorted data:")
                    print(f"Dataset: {self.current_dataset_name}")
                    print(sorted_df)
                    self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "9":
                break
            else:
                print("❌ Invalid choice!")
    def show_statistics(self):
        """Display learning statistics."""
        while True:
            print("\n" + "="*60)
            print("📊 YOUR LEARNING STATISTICS")
            print("="*60)
            
            exercise_names = {
                "exercise_1": "Exercise 1: Basic Operations",
                "exercise_2": "Exercise 2: Filtering Data",
                "exercise_3": "Exercise 3: Sorting and Selection",
                "exercise_4": "Exercise 4: Data Manipulation",
                "exercise_5": "Exercise 5: Data Cleaning"
            }
            
            stats = self.progress.get("exercise_stats", {})
            if not stats:
                print("No exercises completed yet.")
            else:
                print("\nExercise Statistics:")
                print("-" * 60)
                for ex_key, ex_name in exercise_names.items():
                    if ex_key in stats:
                        ex_stat = stats[ex_key]
                        count = ex_stat.get("count", 0)
                        total_grade = ex_stat.get("total_grade", 0.0)
                        avg_grade = total_grade / count if count > 0 else 0.0
                        print(f"\n{ex_name}:")
                        print(f"  Times Completed: {count}")
                        print(f"  Average Grade: {avg_grade:.2f}%")
                    else:
                        print(f"\n{ex_name}:")
                        print(f"  Times Completed: 0")
                        print(f"  Average Grade: N/A")
            
            if self.progress.get('last_session'):
                print(f"📅 Last Session: {self.progress['last_session']}")
            
            # Check if stats are already empty
            stats_empty = (
                not self.progress.get("exercise_stats", {}) and 
                not self.progress.get("last_session")
            )
            
            print("\n" + "="*60)
            print("Options:")
            if stats_empty:
                print("1. Back to Main Menu")
                choice = input("\nSelect option (1): ").strip()
                if choice == "1":
                    return
                else:
                    print("❌ Invalid choice! Please try again.")
                    continue
            else:
                print("1. Reset Statistics")
                print("2. Back to Main Menu")
                choice = input("\nSelect option (1-2): ").strip()
                if choice == "1":
                    was_reset = self.reset_statistics()
                    if was_reset:
                        # Reset was successful, go back to main menu
                        return
                    else:
                        # Reset was cancelled, show stats again (loop continues)
                        continue
                elif choice == "2":
                    return
                else:
                    print("❌ Invalid choice! Please try again.")
                    continue
    def main_menu(self):
        """Display and handle main menu."""
        while True:
            print("\n" + "="*60)
            print("🐼 PANDAS PRACTICE - Interactive Learning Tool")
            print("="*60)
            print("1. Explore Dataset")
            print("2. Run Exercise")
            print("3. View Learning Statistics")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                self.explore_dataset()
            elif choice == "2":
                self.show_exercises()
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice!")
    def show_exercises(self):
        """Show available exercises."""
        print("\n📝 Available Exercises:")
        print("1. Basic Operations")
        print("2. Filtering Data")
        print("3. Sorting and Column Selection")
        print("4. Data Manipulation")
        print("5. Data Cleaning")
        
        choice = input("\nSelect exercise (1-5): ").strip()
        try:
            self.run_exercise(int(choice))
        except:
            print("❌ Invalid choice!")
