"""
SciPy Practice - Focused Learning Tool
A simple project to practice key SciPy modules: constants, optimize, sparse, csgraph, spatial, and interpolation.

Release timestamp: LAST_UPDATED below (single source of truth).
"""

from exercises import (
    exercise_constants,
    exercise_csgraph,
    exercise_interpolate,
    exercise_optimize,
    exercise_sparse,
    exercise_spatial,
)

# Shown when user selects menu option 0
LAST_UPDATED = "2026-05-12 00:05:54"


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("SciPy Practice - Main Menu")
    print("=" * 60)
    print("0. Show last updated info")
    print("1. Constants exercise")
    print("2. Optimization (root finding and minimize) exercise")
    print("3. Sparse Matrices (CSR and CSC) exercise")
    print("4. CSGraph (graph algorithms) exercise")
    print("5. Spatial Data exercise")
    print("6. Interpolation exercise")
    print("7. Exit")
    print("=" * 60)


def main():
    """Main program loop."""
    while True:
        show_menu()
        choice = input("Select an option: ").strip()

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
        elif choice == "0":
            print("\n" + "=" * 60)
            print(f"Last Updated: {LAST_UPDATED}")
            print("=" * 60)
            print()
        elif choice == "7":
            print("\nWe'll talk later! 👋")
            break
        else:
            print("\n❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
