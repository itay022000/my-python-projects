# Matplotlib Pyplot Practice - Pie Chart Exercises

An interactive learning tool for practicing matplotlib.pyplot pie charts in Python.

## Description

This program provides 10 consecutive exercises for practicing pie chart creation using matplotlib.pyplot. Each exercise walks you through creating a pie chart step by step, with random attributes selected from predefined lists.

## Features

- **10 Pie Chart Exercises**: Each exercise creates a pie chart with 5 wedges
- **Step-by-Step Learning**: Exercises are broken down into clear steps:
  1. Define proportions array using `np.array`
  2. Define colors array using `np.array` (color names as strings)
  3. Define labels array using `np.array`
  4. Create the pie chart using `plt.pie()`
  5. Add legend (when required) using `plt.legend()`
- **Random Attributes**: Each exercise has randomly generated:
  - Proportions (5 values that sum to 100%)
  - Colors (from a predefined list of color names)
  - Labels (LabelA, LabelB, etc.)
- **Special Requirements**:
  - At least 2 exercises require `shadow=True`
  - At least 2 exercises require `plt.legend()`
- **Exact Verification**: Only the exact correct answer is accepted for each step

## Requirements

- Python 3.6+
- numpy >= 1.20.0
- matplotlib >= 3.3.0

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python main.py
```

The program will:
1. Display 10 consecutive exercises
2. For each exercise, present the requirements (proportions, colors, labels, and special attributes)
3. Guide you through each step
4. Verify your code input for each step
5. Only accept the exact correct answer before proceeding

## Example Exercise Flow

```
EXERCISE 1: Pie Chart
======================================================================

Create a pie chart with the following specifications:
- 5 wedges with proportions: [30, 10, 15, 40, 5]%
- Colors for each wedge: ['red', 'blue', 'green', 'yellow', 'orange']
- Labels for each wedge: ['LabelA', 'LabelB', 'LabelC', 'LabelD', 'LabelE']
- The pie chart must have a shadow effect

You need to complete the following steps:

STEP 1: Define the proportions array
   Example: proportions = np.array([30, 10, 15, 40, 5])
   Your code: ...
```

## Notes

- Colors must be specified as words (e.g., "red", "blue", "magenta") - no shorthand letters or RGB codes
- Each step must match the exact format expected
- The program uses exact matching for verification to ensure correct learning

