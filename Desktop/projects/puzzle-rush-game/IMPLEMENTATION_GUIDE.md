# Puzzle Rush Game - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing each NumPy game. Each game focuses on different NumPy concepts you've learned.

---

## Game 1: Array Blitz

### Concept
A fast-paced game where players manipulate arrays to solve challenges.

### NumPy Topics Covered
- Array creation (`np.array()`, `np.arange()`, `np.zeros()`, `np.ones()`)
- Indexing and slicing
- Shape and reshape
- Joining and splitting arrays
- Searching and sorting
- Filtering arrays

### Implementation Steps

#### Step 1: Setup
```python
import numpy as np
import random
```

#### Step 2: Challenge Types
Create different challenge types:
1. **Create Challenge**: "Create an array of numbers from 5 to 15"
2. **Shape Challenge**: "What is the shape of this array?"
3. **Reshape Challenge**: "Reshape this array to (3, 4)"
4. **Slice Challenge**: "What are elements at indices 2 to 5?"
5. **Filter Challenge**: "Filter elements greater than 10"

#### Step 3: Generate Challenges
- Generate random arrays
- Create questions based on array operations
- Validate user answers

#### Step 4: Scoring
- Track correct/incorrect answers
- Time-based scoring (optional)
- Difficulty levels

### Example Challenge Structure
```python
challenge = {
    "type": "create",
    "question": "Create an array of even numbers from 2 to 20",
    "answer": np.arange(2, 21, 2),
    "hint": "Use np.arange(start, stop, step)"
}
```

---

## Game 2: Vector Battle

### Concept
A game about random operations, permutations, and data distributions.

### NumPy Topics Covered
- `np.random.permutation()`
- `np.random.shuffle()`
- `np.random.choice()`
- `np.random.randint()`
- Data distributions

### Implementation Steps

#### Step 1: Setup
```python
import numpy as np
```

#### Step 2: Challenge Types
1. **Permutation Challenge**: "Shuffle this array using permutation"
2. **Distribution Challenge**: "Generate 10 random numbers between 1 and 100"
3. **Choice Challenge**: "Randomly select 3 items from this array"
4. **Comparison Challenge**: "What's the difference between shuffle and permutation?"

#### Step 3: Generate Random Data
- Create arrays to shuffle
- Generate random numbers
- Create distribution questions

#### Step 4: Interactive Challenges
- Show arrays before/after operations
- Ask users to predict outcomes
- Compare shuffle vs permutation

### Example Challenge
```python
array = np.array([1, 2, 3, 4, 5])
shuffled = np.random.permutation(array)
# Question: "What will the shuffled array look like?"
```

---

## Game 3: Matrix Challenge

### Concept
Solve matrix operations and transformations.

### NumPy Topics Covered
- 2D array creation
- Matrix operations (addition, multiplication)
- Transpose
- Matrix properties
- Reshaping matrices

### Implementation Steps

#### Step 1: Setup
```python
import numpy as np
```

#### Step 2: Challenge Types
1. **Create Matrix**: "Create a 3x3 matrix of zeros"
2. **Matrix Math**: "Add these two matrices"
3. **Transpose**: "What is the transpose of this matrix?"
4. **Shape**: "What is the shape of this matrix?"
5. **Reshape**: "Reshape this matrix to (2, 6)"

#### Step 3: Generate Matrices
- Create random matrices
- Generate matrix operations
- Create visual representations (text-based)

#### Step 4: Validate Answers
- Compare user input with correct answer
- Handle matrix format input
- Provide hints

### Example Challenge
```python
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])
result = matrix_a + matrix_b
# Question: "What is matrix_a + matrix_b?"
```

---

## Game 4: Ufunc Arena

### Concept
Master universal functions through challenges.

### NumPy Topics Covered
- Arithmetic operations (`np.add()`, `np.subtract()`, etc.)
- Rounding (`np.round()`, `np.floor()`, `np.ceil()`)
- Logarithms (`np.log()`, `np.log10()`)
- Summations (`np.sum()`)
- Products (`np.prod()`)
- Differences (`np.diff()`)
- LCM and GCD (`np.lcm()`, `np.gcd()`)
- Set operations (`np.unique()`, `np.intersect1d()`, etc.)

### Implementation Steps

#### Step 1: Setup
```python
import numpy as np
```

#### Step 2: Challenge Categories
1. **Arithmetic**: "What is the sum of this array?"
2. **Rounding**: "Round this array to 2 decimal places"
3. **Logarithms**: "What is log10(100)?"
4. **Aggregations**: "Find the product of this array"
5. **Differences**: "What is the difference array?"
6. **LCM/GCD**: "Find the GCD of 12 and 18"
7. **Sets**: "What are the unique values in this array?"

#### Step 3: Generate Challenges
- Create arrays for operations
- Generate questions for each ufunc type
- Provide multiple choice or open-ended answers

#### Step 4: Progressive Difficulty
- Start with simple operations
- Increase complexity
- Combine multiple operations

### Example Challenges
```python
# Summation challenge
array = np.array([1, 2, 3, 4, 5])
# Question: "What is np.sum(array)?"

# LCM/GCD challenge
# Question: "What is np.gcd(12, 18)?"
```

---

## General Implementation Tips

### 1. User Input Validation
- Validate array format input
- Handle errors gracefully
- Provide helpful error messages

### 2. Answer Formatting
- Accept multiple formats (list, string, etc.)
- Normalize user input
- Compare arrays properly using `np.array_equal()`

### 3. Scoring System
- Track correct/incorrect answers
- Calculate percentage
- Show progress

### 4. Difficulty Levels
- Easy: Simple operations, small arrays
- Medium: Combined operations, medium arrays
- Hard: Complex operations, large arrays

### 5. Hints System
- Provide hints after wrong answers
- Show examples
- Explain NumPy functions

### 6. Code Structure
```python
def generate_challenge(difficulty):
    # Generate challenge based on difficulty
    pass

def validate_answer(user_answer, correct_answer):
    # Validate and compare answers
    pass

def show_hint(challenge):
    # Display helpful hints
    pass
```

---

## Testing Your Games

1. **Test each challenge type** individually
2. **Test edge cases** (empty arrays, single elements, etc.)
3. **Test error handling** (invalid input, etc.)
4. **Test scoring** (verify calculations)
5. **Play through** a full game session

---

## Next Steps After Implementation

1. Add more challenge types
2. Implement difficulty progression
3. Add statistics tracking
4. Create a leaderboard (optional)
5. Add visualizations (if you learn matplotlib)

Happy coding! 🎮

