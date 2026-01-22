"""
Matplotlib Pyplot Practice
Interactive practice program for learning matplotlib.pyplot with pie charts and histograms.
"""

from subplot_exercises import SubplotExercises
from scatter_plot_exercises import ScatterPlotExercises
from histogram_exercises import HistogramExercises
from pie_chart_exercises import PieChartExercises
from bar_plot_exercises import BarPlotExercises
from plot_exercises import PlotExercises

class MatplotlibPractice:
    """
    Main class for matplotlib pyplot practice exercises.
    Handles the main menu and links between exercise types.
    """
    
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
            print("\n" + "="*70)
            print("MATPLOTLIB PYPLOT PRACTICE")
            print("="*70)
            print("\n1. Start plot exercises sequence")
            print("2. Start subplot exercises sequence")
            print("3. Start scatter plot exercises sequence")
            print("4. Start bar plot exercises sequence")
            print("5. Start histogram exercises sequence")
            print("6. Start pie chart exercises sequence")
            print("7. Exit (or type 'exit')")
            
            choice = input("\nSelect an option (1-7 or 'exit'): ").strip().lower()
            
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
            elif choice == "7" or choice == "exit":
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice! Please select 1, 2, 3, 4, 5, 6, 7, or type 'exit'.")

if __name__ == "__main__":
    practice = MatplotlibPractice()
    practice.main_menu()