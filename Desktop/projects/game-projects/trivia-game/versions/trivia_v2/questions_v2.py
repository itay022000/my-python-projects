import sys
import os

# Add parent directory to path to import from v1
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from trivia_v1.questions_v1 import (
    open_ended_questions,
    multiple_choice_questions,
    true_or_false_questions,
)