# Trivia Game

A simple, interactive command-line trivia game built with Python.

## Getting Started

Run the game:
```bash
python trivia.py
```

## Project Structure

```
trivia-game/
├── trivia.py          # Main game file
├── questions.py       # (Optional) Store questions separately
└── README.md          # This file
```

## Features to Build

- [ ] Question bank (list of questions and answers)
- [ ] Interactive question asking
- [ ] Answer validation
- [ ] Score tracking
- [ ] Final score display
- [ ] (Optional) Multiple choice questions
- [ ] (Optional) Categories
- [ ] (Optional) Difficulty levels

## Tips

- Start simple: get one question working first
- Use dictionaries to store questions: `{"question": "...", "answer": "..."}`
- Use lists to store multiple questions
- Use loops to go through questions
- Use f-strings for nice output formatting
- Track score with a variable

## Example Question Structure

```python
question = {
    "question": "What is the capital of France?",
    "answer": "Paris"
}
```

Or for multiple choice:
```python
question = {
    "question": "What is 2+2?",
    "options": ["2", "3", "4", "5"],
    "correct": 2  # index of correct answer
}
```

Happy coding! 🎮

