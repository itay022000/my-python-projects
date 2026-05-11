# SciPy Practice - Focused Learning Tool

A simple, maintainable project to practice key SciPy modules through hands-on exercises.

## 📚 What You'll Learn

This project focuses on practical SciPy modules:

- **Constants** - Metric, binary, length, and time constants
- **Optimization** - Root finding and minimization
- **Sparse Matrices** - CSR and CSC formats
- **CSGraph** - Graph algorithms and shortest paths
- **Spatial Data** - Distance calculations (excluding cosine distance)
- **Interpolation** - 1D interpolation (`interp1d`: linear, quadratic, cubic, nearest)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd scipy-practice
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 📖 Usage

The program provides an interactive menu where you can:
- Choose a module to practice (options **1–6**), show revision info (**0**), or exit (**7**)
- Learn through examples and explanations
- Answer practice questions to test your understanding
- Navigate between different exercises easily
- Track progress with question counters like **Question 2/5**
- Skip a practice question by typing **skip**
- Leave an exercise early by typing **exit** or **quit** at a practice prompt

## 📁 Project Structure

```
scipy-practice/
├── main.py              # Entry point: menu, LAST_UPDATED, and CLI loop
├── engine.py            # Question specs + run_exercise_questions() shared runner
├── practice.py          # normalize_code(), ask_question(), ExerciseAbort
├── exercises.py         # All six exercise_* sessions (SciPy topics)
├── verify_smoke.py      # Quick import/menu smoke check
├── generate_answers.py  # Regenerates/checks ANSWERS.md from exercises.py
├── tests/               # Focused unittest coverage for helper behavior
├── requirements.txt     # Python dependencies
├── ANSWERS.md           # Generated reference answers for practice questions
└── README.md            # This file
```

## ✅ Verification

Run the smoke check:
```bash
python verify_smoke.py
```

Run the helper tests:
```bash
python -m unittest discover -s tests
```

Verify the answer key is synced with `exercises.py`:
```bash
python generate_answers.py --check
```

## 🎯 Exercises

### 1. Constants
Practice using physical and mathematical constants, unit conversions for length and time, and binary prefixes.

### 2. Optimization
Learn to find roots of functions and minimize functions using SciPy's optimization tools.

### 3. Sparse Matrices
Work with Compressed Sparse Row (CSR) and Compressed Sparse Column (CSC) matrix formats, including creation, conversion, and operations.

### 4. CSGraph
Use graph algorithms including shortest path calculations and connected component analysis.

### 5. Spatial Data
Calculate various distance metrics (Euclidean, Manhattan, Chebyshev) and work with distance matrices.

### 6. Interpolation
Perform **1D** interpolation using `interp1d` (linear, quadratic, cubic, nearest and other kinds supported by the exercise).

## 💡 Learning Tips

1. **Start with Constants** - Get familiar with SciPy's constant values and conversions
2. **Practice Optimization** - Understanding root finding and minimization is crucial for many applications
3. **Master Sparse Matrices** - Essential for working with large, sparse datasets
4. **Explore Graph Algorithms** - Useful for network analysis and pathfinding problems
5. **Understand Spatial Distances** - Important for clustering, classification, and similarity calculations
6. **Learn Interpolation** - Key for data smoothing and estimating values between known points

## 📚 Additional Resources

- [SciPy Documentation](https://docs.scipy.org/doc/scipy/)
- [SciPy Constants](https://docs.scipy.org/doc/scipy/reference/constants.html)
- [SciPy Optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [SciPy Sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html)

## 📝 Notes

This project is intentionally simpler and more focused than comprehensive pandas practice projects. It emphasizes:
- Clean, maintainable code structure
- Practical, hands-on exercises
- Focused learning on specific SciPy modules
- Easy to extend with additional exercises

### Safety note

Practice answers are evaluated locally with Python's `eval()` so the tool can check live SciPy expressions. Only run this project with code you trust; it is not designed for untrusted users, a shared public service, or browser/server execution without sandboxing.

---

**Happy Learning! 🔬📊**
