"""Main and explore menus mixin (B011)."""

import sys
import termios
import tty

import session_common


class MenusMixin:
    """Mixin for PandasPractice."""

    def wait_for_esc(self):
        """Wait for ESC key press to return to menu."""
        print("\n" + "-" * session_common.SESSION_BANNER_WIDTH)
        print("Press ESC to return to menu...")

        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    char = sys.stdin.read(1)
                    if ord(char) == 27:
                        break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            input("Press Enter to return to menu...")

    _EXIT_WORDS = frozenset({"Exit", "exit", "Quit", "quit"})
    _EXIT_HINT = "or type 'exit'/'quit' to return"

    def _prompt_row_count(self, max_rows: int):
        """Prompt for an integer row count in [1, max_rows]; empty re-prompts."""
        prompt = f"How many rows? (1-{max_rows}; {self._EXIT_HINT}): "
        while True:
            raw = input(prompt).strip()
            if raw == "":
                continue
            if raw in self._EXIT_WORDS:
                return None
            if raw.isdigit() and 1 <= int(raw) <= max_rows:
                return int(raw)
            print(f"Please enter a whole number between 1 and {max_rows}.")

    def _prompt_existing_column(self, df, prompt: str):
        """Prompt for a column in df; empty re-prompts; Exit/exit/Quit/quit → menu."""
        base = prompt.rstrip().rstrip(":").rstrip()
        full_prompt = f"{base} ({self._EXIT_HINT}): "
        while True:
            col = input(full_prompt).strip()
            if col == "":
                continue
            if col in self._EXIT_WORDS:
                return None
            if col in df.columns:
                return col
            print(f"Column '{col}' not found! Enter an existing column name.")

    def _prompt_filter_value(self, df, col: str):
        """Prompt for a filter value; empty re-prompts; Exit/exit/Quit/quit → menu."""
        is_numeric = df[col].dtype in ["int64", "float64"]
        suffix = " (numeric)" if is_numeric else ""
        prompt = f"Enter value to filter by{suffix} ({self._EXIT_HINT}): "
        while True:
            raw = input(prompt).strip()
            if raw == "":
                continue
            if raw in self._EXIT_WORDS:
                return None
            if not is_numeric:
                return raw
            try:
                return float(raw)
            except ValueError:
                print("Please enter a numeric value.")

    def _prompt_sort_ascending(self):
        """Prompt for sort direction (lowercase 'a' or 'd' only); empty re-prompts."""
        prompt = (
            f"Sort order? (a = ascending, d = descending; {self._EXIT_HINT}): "
        )
        while True:
            raw = input(prompt).strip()
            if raw == "":
                continue
            if raw in self._EXIT_WORDS:
                return None
            if raw == "a":
                return True
            if raw == "d":
                return False
            print("Please enter 'a' for ascending or 'd' for descending.")

    def _repeat_or_return(self) -> bool:
        """After an option runs, return True to run it again or False to go back to the menu.

        Interactive: press Enter to repeat, ESC to return. Non-interactive: return to menu.
        """
        print("\n" + "-" * session_common.SESSION_BANNER_WIDTH)
        print("Press Enter to run this option again, or ESC to return to the menu...")

        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    char = sys.stdin.read(1)
                    if ord(char) == 27:  # ESC
                        return False
                    if char in ("\r", "\n"):  # Enter
                        return True
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return False

    def _dtype_display_name(self, dtype) -> str:
        """Map dtypes to stable learner-facing labels (string-like → object)."""
        name = str(dtype)
        if name in ("object", "str") or name.startswith("string"):
            return "object"
        return name

    def _print_dataset_info(self, df) -> None:
        """Dataset info table with PM-locked formatting (Explore option 3)."""
        n_rows = len(df)
        n_cols = len(df.columns)
        idx = df.index
        try:
            lo, hi = idx.min(), idx.max()
            print(f"Index range: {n_rows} entries ({lo}-{hi})")
        except TypeError:
            print(f"Index range: {n_rows} entries")
        print(f"Data columns (total {n_cols} columns):")
        print()

        name_w = max((len(str(c)) for c in df.columns), default=5)
        name_w = max(name_w, len("Column"))
        null_header = "Non-Null Count"
        type_header = "Data type"
        null_w = max(len(null_header), len(f"{n_rows} (out of {n_rows})"))
        type_w = max(
            len(type_header),
            max(
                (len(self._dtype_display_name(df[c].dtype)) for c in df.columns),
                default=0,
            ),
        )

        print(f" #   {'Column':<{name_w}}  {null_header:<{null_w}}  {type_header}")
        print(f"---  {'-' * name_w}  {'-' * null_w}  {'-' * type_w}")

        dtype_counts: dict[str, int] = {}
        for i, col in enumerate(df.columns):
            non_null = int(df[col].notna().sum())
            dtype_str = self._dtype_display_name(df[col].dtype)
            dtype_counts[dtype_str] = dtype_counts.get(dtype_str, 0) + 1
            null_label = f"{non_null} (out of {n_rows})"
            print(f" {i:<3} {str(col):<{name_w}}  {null_label:<{null_w}}  {dtype_str}")

        print()
        # e.g. float64 (2), int64 (3), object (4) — alpha sort of type names
        summary_parts = [
            f"{dtype} ({count})"
            for dtype, count in sorted(dtype_counts.items(), key=lambda x: x[0])
        ]
        print(f"Data types: {', '.join(summary_parts)}")
        try:
            mem = df.memory_usage(deep=True).sum()
            if mem < 1024:
                mem_s = f"{mem} bytes"
            elif mem < 1024 ** 2:
                mem_s = f"{mem / 1024:.1f} KB"
            else:
                mem_s = f"{mem / (1024 ** 2):.1f} MB"
            print(f"Memory usage: {mem_s}")
        except Exception:
            pass

    def explore_dataset(self, df=None):
        """Interactive dataset exploration."""
        if df is None:
            df = self.current_dataset

        max_rows = len(df)
        bar = "=" * session_common.SESSION_BANNER_WIDTH
        while True:
            print("\n" + bar)
            print("DATASET EXPLORATION MENU")
            print(bar)
            print("1. View first few rows (head)")
            print("2. View last few rows (tail)")
            print("3. View dataset info")
            print("4. View basic statistics")
            print("5. View unique values in a column")
            print("6. Filter data by condition")
            print("7. Sort data")
            print("8. Return to main menu")

            prompt = "\nSelect an option (1-8): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break
                prompt = "Select an option (1-8): "

            if choice == "1":
                while True:
                    n = self._prompt_row_count(max_rows)
                    if n is None:
                        break
                    print(f"\nFirst {n} rows:")
                    print(df.head(n))
                    if not self._repeat_or_return():
                        break

            elif choice == "2":
                while True:
                    n = self._prompt_row_count(max_rows)
                    if n is None:
                        break
                    print(f"\nLast {n} rows:")
                    print(df.tail(n))
                    if not self._repeat_or_return():
                        break

            elif choice == "3":
                print("\nDataset Info:")
                self._print_dataset_info(df)
                self.wait_for_esc()

            elif choice == "4":
                print("\nBasic Statistics:")
                print(df.describe())
                self.wait_for_esc()

            elif choice == "5":
                while True:
                    col = self._prompt_existing_column(df, "Enter column name: ")
                    if col is None:
                        break
                    print(f"\nUnique values in '{col}':")
                    print(df[col].unique())
                    print(f"\nCount: {df[col].nunique()} unique values")
                    if not self._repeat_or_return():
                        break

            elif choice == "6":
                while True:
                    col = self._prompt_existing_column(df, "Enter column name to filter: ")
                    if col is None:
                        break
                    print(f"\nSample values in '{col}': {df[col].unique()[:5]}")
                    value = self._prompt_filter_value(df, col)
                    if value is None:
                        break
                    filtered = df[df[col] == value]
                    print(f"\nFiltered results ({len(filtered)} rows):")
                    print(filtered)
                    if not self._repeat_or_return():
                        break

            elif choice == "7":
                while True:
                    col = self._prompt_existing_column(df, "Enter column to sort by: ")
                    if col is None:
                        break
                    ascending = self._prompt_sort_ascending()
                    if ascending is None:
                        break
                    sorted_df = df.sort_values(by=col, ascending=ascending)
                    print("\nSorted data:")
                    print(sorted_df)
                    if not self._repeat_or_return():
                        break

            elif choice == "8":
                break
            else:
                print("Invalid choice! Please select an option from 1 to 8.")

    def main_menu(self):
        """Display and handle main menu."""
        bar = "=" * session_common.SESSION_BANNER_WIDTH
        while True:
            print("\n" + bar)
            print("Pandas Practice")
            print(bar)
            print("1. Basic Operations Exercise")
            print("2. Filtering Data Exercise")
            print("3. Sorting and Column Selection Exercise")
            print("4. Data Manipulation Exercise")
            print("5. Data Cleaning Exercise")
            print("6. Explore Dataset")
            print("7. Exit (or type 'exit'/'Exit')")
            print(bar)

            prompt = "Select an option (1-7 or 'exit'/'Exit'): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break

            if choice == "1":
                self.run_exercise(1)
            elif choice == "2":
                self.run_exercise(2)
            elif choice == "3":
                self.run_exercise(3)
            elif choice == "4":
                self.run_exercise(4)
            elif choice == "5":
                self.run_exercise(5)
            elif choice == "6":
                self.explore_dataset()
            elif choice == "7" or choice in ("exit", "Exit"):
                print("\nWe'll talk later! 👋")
                break
            else:
                print("\n❌ Invalid choice. Please select 1-7, or type 'exit'/'Exit'.")
