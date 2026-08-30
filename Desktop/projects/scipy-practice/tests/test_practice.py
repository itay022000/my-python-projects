"""Focused tests for pure prompt/runner helpers."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from engine import Question, QuestionOutcome, ask_question
from exercise_session import run_exercise_questions
from session_common import TEACH_RULE_LINE
from validators import normalize_code


class NormalizeCodeTests(unittest.TestCase):
    def test_normalize_code_removes_all_whitespace(self):
        self.assertEqual(normalize_code("12 * const.inch"), "12*const.inch")
        self.assertEqual(normalize_code("const.hour\n *\t2"), "const.hour*2")


class AskQuestionTests(unittest.TestCase):
    def test_semantic_answer_can_differ_from_correct_answer(self):
        def check(result):
            return result == 24, "value checked"

        output = StringIO()
        with patch("builtins.input", return_value="6 * 4"), redirect_stdout(output):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Compute 24",
                hint="Any expression that evaluates to 24 works.",
                namespace={},
                check_func=check,
                first=True,
                correct_answer="12 * 2",
            )

        self.assertEqual(outcome, QuestionOutcome.COMPLETED)
        self.assertIn("✓ Correct!", output.getvalue())

    def test_require_exact_rejects_semantically_equivalent_code(self):
        def check(result):
            return result == 24, "value checked"

        output = StringIO()
        with patch("builtins.input", side_effect=["6 * 4", "12 * 2"]), redirect_stdout(output):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Compute 24",
                hint="Use the exact reference form.",
                namespace={},
                check_func=check,
                first=True,
                correct_answer="12 * 2",
                require_exact=True,
            )

        self.assertEqual(outcome, QuestionOutcome.COMPLETED)
        self.assertIn("Incorrect answer (attempt 1/3)", output.getvalue())

    def test_exit_returns_exit_outcome(self):
        with patch("builtins.input", return_value="exit"), redirect_stdout(StringIO()):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Anything",
                hint="Hint",
                namespace={},
                check_func=lambda result: (True, ""),
                first=True,
            )
        self.assertEqual(outcome, QuestionOutcome.EXIT)

    def test_skip_returns_not_completed(self):
        output = StringIO()
        with patch("builtins.input", return_value="skip"), redirect_stdout(output):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Anything",
                hint="Hint",
                namespace={},
                check_func=lambda result: (True, ""),
                first=True,
                correct_answer="1",
            )
        self.assertEqual(outcome, QuestionOutcome.NOT_COMPLETED)
        self.assertIn("Skipping question.", output.getvalue())

    def test_prompt_uses_your_code_attempt(self):
        with patch("builtins.input", return_value="1") as mock_input:
            ask_question(
                question_num=1,
                total=1,
                title="Anything",
                hint="Hint",
                namespace={},
                check_func=lambda result: (result == 1, ""),
                first=True,
            )

        mock_input.assert_called_with("Your code (attempt 1/3): ")


class RunExerciseQuestionsTests(unittest.TestCase):
    def test_runner_prints_footer_after_all_questions(self):
        question = Question(
            "Compute 3",
            lambda result: (result == 3, "checked"),
            "Use 1 + 2.",
            correct_answer="1 + 2",
        )

        output = StringIO()
        with patch("builtins.input", side_effect=["", "1 + 2"]), redirect_stdout(output):
            run_exercise_questions({}, [question], background='test')

        self.assertIn("Session Statistics", output.getvalue())

    def test_runner_prints_question_progress(self):
        questions = [
            Question("Compute 1", lambda result: (result == 1, ""), "Use 1."),
            Question("Compute 2", lambda result: (result == 2, ""), "Use 2."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["", "", "1", "2"]), redirect_stdout(output):
            run_exercise_questions({}, questions, background='test')

        text = output.getvalue()
        self.assertIn("--- Question 1/2 ---", text)
        self.assertIn("--- Question 2/2 ---", text)

    def test_runner_prints_teach_block_once(self):
        questions = [
            Question("Compute 1", lambda result: (result == 1, ""), "Use 1."),
            Question("Compute 2", lambda result: (result == 2, ""), "Use 2."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["", "", "1", "2"]), redirect_stdout(output):
            run_exercise_questions({}, questions, background='test')

        text = output.getvalue()
        self.assertEqual(text.count(TEACH_RULE_LINE), 1)
        self.assertEqual(text.count("Tip: type 'skip'"), 1)

    def test_runner_partial_exit_on_quit(self):
        question = Question("Leave", lambda result: (True, ""), "Type exit.")

        output = StringIO()
        with patch("builtins.input", side_effect=["", "quit"]), redirect_stdout(output):
            run_exercise_questions({}, [question], background='test')

        text = output.getvalue()
        self.assertIn("Session exited.", text)
        self.assertNotIn("Session Statistics", text)

    def test_runner_continues_after_skip(self):
        questions = [
            Question("Skip this", lambda result: (False, ""), "Type skip.", correct_answer="9"),
            Question("Compute 3", lambda result: (result == 3, ""), "Use 3."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["", "skip", "3"]), redirect_stdout(output):
            run_exercise_questions({}, questions, background='test')

        text = output.getvalue()
        self.assertIn("Skipping question.", text)
        self.assertIn("--- Question 2/2 ---", text)
        self.assertIn("Session Statistics", text)


if __name__ == "__main__":
    unittest.main()
