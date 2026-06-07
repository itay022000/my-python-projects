# SciPy Practice - Focused Learning Tool

A simple, maintainable project to practice key SciPy modules through hands-on exercises.

## What You'll Learn

This project focuses on practical SciPy modules:

- **Constants** - Metric, binary, length, and time constants
- **Optimization** - Root finding and minimization
- **Sparse Matrices** - CSR and CSC formats
- **CSGraph** - Graph algorithms and shortest paths
- **Spatial Data** - Distance calculations (excluding cosine distance)
- **Interpolation** - 1D interpolation (`interp1d`: linear, quadratic, cubic, nearest)

## Getting Started

### Prerequisites

- Python **3.10.9** recommended (3.8+ may work)
- pip (Python package installer)

### Installation

A virtual environment is recommended. On Anaconda base, NumPy 2.x with older SciPy wheels can fail to import — use a venv:

```bash
cd scipy-practice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Tested with:** Python 3.10.9, NumPy 1.26.x, SciPy 1.11.x in a venv.  
`requirements.txt` keeps flexible lower bounds (`numpy>=1.20`, `scipy>=1.7`).

### Run

```bash
python main.py
```

## Usage

The program provides an interactive menu where you can:

- Choose a module to practice (options **1–6**), show revision info (**0**), or exit (**7**)
- Learn through examples and explanations
- Answer practice questions to test your understanding
- Track progress with question counters like **Question 2/5** (interpolation has **4** questions)
- Skip a practice question by typing **skip**
- Leave an exercise early by typing **exit** or **quit** at a practice prompt

## Project Structure

```
scipy-practice/
├── main.py                    # Entry point: menu, LAST_UPDATED, CLI loop
├── engine.py                  # Question specs + run_exercise_questions()
├── practice.py                # normalize_code(), ask_question(), ExerciseAbort
├── exercises.py               # Six exercise_* sessions + PRACTICE_BUILDERS
├── verify_smoke.py            # Menu 0 + exit smoke
├── verify_answer_behavior.py  # All 29 questions: correct/wrong grading matrix
├── verify_skip_exit_behavior.py  # All 29 questions: skip + exit at each prompt
├── generate_answers.py        # Regenerates/checks ANSWERS.md
├── tests/                     # Unittest coverage for helpers
├── requirements.txt
├── ANSWERS.md
└── README.md
```

## Verification

Run from this directory (venv active, SciPy installed):

```bash
python3 -m unittest discover -s tests -v
python3 verify_smoke.py
python3 generate_answers.py --check
python3 verify_answer_behavior.py
python3 verify_skip_exit_behavior.py
```

All five must exit **0** before release.

### Release timestamp

`main.py` defines **`LAST_UPDATED`** (menu option **0**). **Update it whenever you change project behavior or content** — it is the learner-visible “last updated” stamp for this repo.

## Exercises

| # | Module | Questions |
|---|--------|-----------|
| 1 | Constants | 5 (`N * const.x` and `const.x * N` both accepted) |
| 2 | Optimization | 5 (full `optimize.root` / `minimize` result objects) |
| 3 | Sparse Matrices | 5 |
| 4 | CSGraph | 5 |
| 5 | Spatial Data | 5 |
| 6 | Interpolation | 4 |

## Safety note

Practice answers are evaluated locally with Python's `eval()`. Only run with code you trust; not for untrusted users or unsandboxed server use.

## Additional Resources

- [SciPy Documentation](https://docs.scipy.org/doc/scipy/)
