"""Matplotlib Practice application shell (B015)."""

from exercises.bar_plot_exercises import BarPlotExercises
from exercises.histogram_exercises import HistogramExercises
from exercises.pie_chart_exercises import PieChartExercises
from exercises.plot_exercises import PlotExercises
from exercises.scatter_plot_exercises import ScatterPlotExercises
from exercises.subplot_exercises import SubplotExercises
from session_common import SESSION_BANNER_WIDTH


class MatplotlibPractice:
    """Main menu and exercise dispatch for matplotlib-practice."""

    def __init__(self):
        self.subplot_exercises = SubplotExercises()
        self.scatter_plot_exercises = ScatterPlotExercises()
        self.bar_plot_exercises = BarPlotExercises()
        self.histogram_exercises = HistogramExercises()
        self.pie_chart_exercises = PieChartExercises()
        self.plot_exercises = PlotExercises()

    def main_menu(self):
        """Display main menu and handle user choices."""
        while True:
            print("\n" + "=" * SESSION_BANNER_WIDTH)
            print("Matplotlib Practice")
            print("=" * SESSION_BANNER_WIDTH)
            print("1. Line Plot Exercise")
            print("2. Subplot Exercise")
            print("3. Scatter Plot Exercise")
            print("4. Bar Plot Exercise")
            print("5. Histogram Exercise")
            print("6. Pie Chart Exercise")
            print("7. Exit (or type 'exit'/'Exit')")
            print("=" * SESSION_BANNER_WIDTH)
            prompt = "Select an option (1-7 or 'exit'/'Exit'): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break

            if choice == "1":
                self.plot_exercises.start_exercises()
            elif choice == "2":
                self.subplot_exercises.start_exercises()
            elif choice == "3":
                self.scatter_plot_exercises.start_exercises()
            elif choice == "4":
                self.bar_plot_exercises.start_exercises()
            elif choice == "5":
                self.histogram_exercises.start_exercises()
            elif choice == "6":
                self.pie_chart_exercises.start_exercises()
            elif choice == "7" or choice in ("exit", "Exit"):
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice. Please select 1-7, or type 'exit'/'Exit'.")
