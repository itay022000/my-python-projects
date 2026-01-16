# NumPy-Enhanced Trivia Game v2

A command-line trivia game enhanced with NumPy for efficient array operations and statistical analysis.

## What's New in v2?

This version incorporates NumPy to:
- ✅ Use `np.random.permutation()` for efficient question shuffling
- ✅ Track scores using NumPy arrays instead of simple variables
- ✅ Calculate statistics (totals, percentages, standard deviation) using NumPy functions
- ✅ Combine results from different question types using `np.concatenate()`
- ✅ Enable advanced analysis and performance tracking

## Getting Started

### Prerequisites

Install NumPy:
```bash
pip install numpy
```

### Project Structure

```
trivia_v2/
├── trivia_v2.py          # Main game file (skeleton with TODOs)
├── questions_v2.py        # Questions (imports from v1)
├── GAME_STRUCTURE_v2.md   # Detailed implementation guide
└── README_v2.md          # This file
```

### Running the Game

```bash
# From the trivia-game directory
cd versions/trivia_v2
python trivia_v2.py
```

**Note:** The game is currently a skeleton. Follow the instructions in `GAME_STRUCTURE_v2.md` to implement the NumPy features.

---

## NumPy Topics Used

### Arrays
- **Creation**: `np.array()`, `np.arange()`
- **Operations**: `np.append()`, `np.concatenate()`
- **Indexing**: Using arrays as indices for shuffling

### Random
- **Permutation**: `np.random.permutation()` for shuffling question order
- **Data distribution**: Understanding how permutation works vs shuffle

### Ufunc (Universal Functions)
- **Summations**: `np.sum()` for calculating total scores
- **Products**: `np.mean()` for calculating percentages
- **Statistics**: `np.std()` for consistency metrics

---

## Implementation Status

### To Implement:
- [ ] Replace `random.shuffle()` with `np.random.permutation()`
- [ ] Create NumPy arrays for score tracking
- [ ] Implement result tracking (1 for correct, 0 for incorrect)
- [ ] Calculate statistics using NumPy functions
- [ ] Combine results from all question types
- [ ] Add conditional feedback using NumPy (optional)

### Features:
- [x] Project structure created
- [x] Skeleton code with TODOs
- [x] Implementation guide
- [ ] NumPy shuffling
- [ ] NumPy score tracking
- [ ] NumPy statistics

---

## Learning Objectives

By implementing this version, you'll practice:

1. **Array Operations**
   - Creating NumPy arrays
   - Appending to arrays
   - Concatenating arrays
   - Using arrays for indexing

2. **Random Operations**
   - Using `np.random.permutation()` instead of `random.shuffle()`
   - Understanding the difference between permutation and shuffle

3. **Statistical Functions**
   - Calculating sums with `np.sum()`
   - Calculating means with `np.mean()`
   - Calculating standard deviation with `np.std()`

4. **Practical Application**
   - Applying NumPy to a real project
   - Seeing the benefits of NumPy over basic Python operations
   - Building on existing code

---

## Comparison: v1 vs v2

| Feature | v1 (Basic Python) | v2 (NumPy-Enhanced) |
|---------|-------------------|---------------------|
| Shuffling | `random.shuffle()` | `np.random.permutation()` |
| Score Tracking | Simple variables | NumPy arrays |
| Statistics | Manual calculation | `np.sum()`, `np.mean()`, etc. |
| Result Storage | Not stored | Array of 1s and 0s |
| Analysis | Limited | Advanced (with NumPy) |

---

## Next Steps

1. **Read** `GAME_STRUCTURE_v2.md` for detailed implementation instructions
2. **Implement** NumPy features step by step
3. **Test** each feature as you add it
4. **Experiment** with additional NumPy functions

---

## Tips

- Start with shuffling - it's the easiest NumPy feature to add
- Use `print()` to inspect your arrays while debugging
- Read NumPy error messages carefully - they're usually helpful
- Test incrementally - don't try to implement everything at once

---

## Resources

- [NumPy Documentation](https://numpy.org/doc/stable/)
- [NumPy Array Creation](https://numpy.org/doc/stable/user/basics.creation.html)
- [NumPy Random](https://numpy.org/doc/stable/reference/random/index.html)
- [NumPy Statistics](https://numpy.org/doc/stable/reference/routines.statistics.html)

Happy coding! 🎮📊

