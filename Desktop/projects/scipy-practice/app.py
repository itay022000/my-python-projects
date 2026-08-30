"""SciPy Practice application shell (B015)."""

from __future__ import annotations

from exercises import (
    exercise_constants,
    exercise_csgraph,
    exercise_interpolate,
    exercise_optimize,
    exercise_sparse,
    exercise_spatial,
)
from session_common import SESSION_BANNER_WIDTH


class ScipyPractice:
    """Main menu and exercise dispatch for scipy-practice."""

    def show_menu(self) -> None:
        print("\n" + "=" * SESSION_BANNER_WIDTH)
        print("SciPy Practice")
        print("=" * SESSION_BANNER_WIDTH)
        print("1. Constants Exercise")
        print("2. Optimization Exercise")
        print("3. Sparse Matrices (CSR and CSC) Exercise")
        print("4. CSGraph (Graph Algorithms) Exercise")
        print("5. Spatial Data Exercise")
        print("6. Interpolation Exercise")
        print("7. Exit (or type 'exit'/'Exit')")
        print("=" * SESSION_BANNER_WIDTH)

    def run(self) -> None:
        while True:
            self.show_menu()
            prompt = "Select an option (1-7 or 'exit'/'Exit'): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break

            if choice == "1":
                exercise_constants()
            elif choice == "2":
                exercise_optimize()
            elif choice == "3":
                exercise_sparse()
            elif choice == "4":
                exercise_csgraph()
            elif choice == "5":
                exercise_spatial()
            elif choice == "6":
                exercise_interpolate()
            elif choice == "7" or choice in ("exit", "Exit"):
                print("\nWe'll talk later! 👋")
                break
            else:
                print("\n❌ Invalid choice. Please select 1-7, or type 'exit'/'Exit'.")
