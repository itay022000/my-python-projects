# Matplotlib Pyplot Practice

An interactive command-line program for practicing **matplotlib.pyplot** across six exercise sequences: line plots, subplots, scatter plots, bar plots, histograms, and pie charts.

## Description

Run `main.py` to open a main menu. Each sequence contains **3 consecutive exercises** (pie chart sequence: 3 exercises). Every exercise guides you step by step; you type Python/matplotlib code for each step. The program uses **exact matching** — only the precisely expected answer is accepted before you move on.

After a sequence, you see completion statistics (wording differs slightly for the plot sequence footer; behavior is the same idea).

## Main menu

| Option | Sequence |
|--------|----------|
| 1 | Plot (line) exercises |
| 2 | Subplot exercises |
| 3 | Scatter plot exercises |
| 4 | Bar plot exercises |
| 5 | Histogram exercises |
| 6 | Pie chart exercises |
| 7 | Exit (or type `exit`) |

## Features (all sequences)

- **Step-by-step prompts** with clear variable-name rules per step
- **Random exercise data** generated when each module loads (counts and rules are fixed per sequence type)
- **Three-strike rule**: three wrong attempts on a step skips the current exercise (or ends the sequence on the last exercise, depending on step and module — pie chart early steps always skip to the next exercise)
- **Exact verification** of code strings (whitespace normalized; no alternate spellings)
- **Shared internals**: common helpers live in `exercise_common.py` (normalization, `plt.show()` check, sequence statistics for most modules)

## Sequence overview

| Module | Topic | Exercises | Notes |
|--------|-------|-----------|--------|
| `plot_exercises.py` | Line plots, labels, grid | 3 | Three variants: multi-line styling, titled axes, grid |
| `subplot_exercises.py` | `plt.subplot`, titles | 3 | 1×2 or 2×1 layouts; optional suptitle |
| `scatter_plot_exercises.py` | `plt.scatter` | 3 | Color arrays, sizes, numeric colors |
| `bar_plot_exercises.py` | `plt.bar` / `plt.barh` | 3 | Vertical bars, width, horizontal bars |
| `histogram_exercises.py` | `plt.hist` | 3 | `np.random.normal` then histogram |
| `pie_chart_exercises.py` | `plt.pie` | 3 | Proportions, colors, labels; optional explode, shadow, legend |

## Requirements

- **Python 3.10+** recommended (verified on 3.10.9 for maintenance brief B001)
- `numpy >= 1.20.0`
- `matplotlib >= 3.3.0`

See `requirements.txt`.

## Installation

```bash
cd matplotlib-practice
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

1. Choose a sequence (1–6) or exit (7 / `exit`).
2. Press Enter at the sequence intro.
3. Complete each exercise step; re-enter code after feedback until correct or three mistakes on that step.
4. View statistics at the end of the sequence (plot sequence uses the heading `EXERCISES SEQUENCE STATISTICS`).

## Verification rules (learners)

- Type answers as instructed (exact variable names: e.g. pie chart uses `x`, `c`, `lb`, `ex` where specified).
- Colors in arrays are **color name strings** (e.g. `"red"`), not RGB tuples, unless the step says otherwise.
- Only the shown correct pattern is accepted; extra spaces are normalized, but wrong names or values are rejected.

## Project layout

```text
main.py                 # Main menu
exercise_common.py      # Shared verification and CLI helpers
plot_exercises.py
subplot_exercises.py
scatter_plot_exercises.py
bar_plot_exercises.py
histogram_exercises.py
pie_chart_exercises.py
requirements.txt
scripts/qa_regression_b001.py   # QA validator regression (228 checks)
```

## Development / QA

Regression check for validators (does not replace learner-facing manual practice):

```bash
python3 scripts/qa_regression_b001.py
python3 scripts/qa_flow_three_strike_b001.py   # 62 checks: 3-strike on all 18 exercises
```

## License / origin

Practice project for learning matplotlib pyplot interactively in the terminal.
