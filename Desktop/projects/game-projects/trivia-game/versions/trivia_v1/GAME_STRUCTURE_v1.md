# Trivia Game Structure Guide

## Step 1: Fix questions.py

You have two variables both named `questions`. Rename them:
- `open_ended_questions` for the first list
- `multiple_choice_questions` for the second list

Or combine them into one list with a "type" field.

---

## Step 2: Import Questions

In `trivia.py`, import your questions:
```python
from questions import open_ended_questions, multiple_choice_questions
```

---

## Step 3: Game Structure

### Main Game Flow:
1. **Welcome message** - Greet the player
2. **Initialize score** - `score = 0`
3. **Combine questions** - Put both question types together (or handle separately)
4. **Loop through questions** - For each question:
   - Display the question
   - Get user input
   - Check if answer is correct
   - Update score
   - Give feedback
5. **Show final results** - Display total score and percentage

---

## Step 4: Handle Two Question Types

You need to detect which type of question you're dealing with:

### For Open-Ended Questions:
- Check if question has "answer" key
- Use `input()` to get text answer
- Compare user answer to correct answer (case-insensitive might be nice)

### For Multiple Choice Questions:
- Check if question has "options" key
- Display all options with numbers (1, 2, 3, 4)
- Get user input (number as string, convert to int)
- Check if user's choice index matches "correct" index

---

## Step 5: Helper Functions (Optional but Recommended)

Consider creating functions:
- `ask_open_ended_question(question_dict)` - handles open-ended
- `ask_multiple_choice_question(question_dict)` - handles multiple choice
- `check_answer(user_answer, correct_answer)` - validates answer
- `display_results(score, total)` - shows final score

---

## Example Logic Flow:

```python
# Pseudocode
score = 0
all_questions = open_ended_questions + multiple_choice_questions

for question in all_questions:
    if "options" in question:
        # Multiple choice
        # Display question and options
        # Get user choice
        # Check if correct
    else:
        # Open-ended
        # Display question
        # Get user answer
        # Check if correct
    
    if correct:
        score += 1
        print("Correct!")
    else:
        print("Wrong!")

print(f"Final score: {score}/{len(all_questions)}")
```

---

## Tips:

1. **Start simple**: Get one question type working first
2. **Test incrementally**: Add one question at a time
3. **Handle errors**: What if user types invalid input for multiple choice?
4. **Format nicely**: Use f-strings and spacing for clean output
5. **Case sensitivity**: Consider `.lower()` for open-ended answers

---

## Quick Fix for questions.py:

Change the variable names:
```python
open_ended_questions = [...]
multiple_choice_questions = [...]
```

Then you can combine them:
```python
all_questions = open_ended_questions + multiple_choice_questions
```

Or keep them separate and loop through both lists.

