"""Focused tests for pure prompt/runner helpers."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from engine import Question, run_exercise_questions
from practice import ExerciseAbort, QuestionSkip, ask_question, normalize_code


class NormalizeCodeTests(unittest.TestCase):
    def test_normalize_code_removes_all_whitespace(self):
        self.assertEqual(normalize_code("12 * const.inch"), "12*const.inch")
        self.assertEqual(normalize_code("const.hour\n *\t2"), "const.hour*2")


class AskQuestionTests(unittest.TestCase):
    def test_semantic_answer_can_differ_from_reference_answer(self):
        def check(result):
            return result == 24, "value checked"

        output = StringIO()
        with patch("builtins.input", return_value="6 * 4"), redirect_stdout(output):
            ask_question(
                "Compute 24",
                {},
                check,
                "Any expression that evaluates to 24 works.",
                reference_answer="12 * 2",
            )

        self.assertIn("Correct", output.getvalue())

    def test_require_exact_rejects_semantically_equivalent_code(self):
        def check(result):
            return result == 24, "value checked"

        output = StringIO()
        with patch("builtins.input", return_value="6 * 4"), redirect_stdout(output):
            ask_question(
                "Compute 24",
                {},
                check,
                "Use the exact reference form.",
                reference_answer="12 * 2",
                require_exact=True,
            )

        self.assertIn("Incorrect", output.getvalue())

    def test_exit_raises_exercise_abort(self):
        with patch("builtins.input", return_value="exit"), \
                redirect_stdout(StringIO()), \
                self.assertRaises(ExerciseAbort):
            ask_question("Anything", {}, lambda result: (True, ""), "Hint")

    def test_skip_raises_question_skip(self):
        with patch("builtins.input", return_value="skip"), \
                redirect_stdout(StringIO()), \
                self.assertRaises(QuestionSkip):
            ask_question("Anything", {}, lambda result: (True, ""), "Hint")

    def test_question_prompt_does_not_repeat_command_reminder(self):
        output = StringIO()
        with patch("builtins.input", return_value="1"), redirect_stdout(output):
            ask_question("Anything", {}, lambda result: (True, ""), "Hint")

        text = output.getvalue()
        self.assertIn("Enter your code:", text)
        self.assertNotIn("or type skip / exit", text)


class RunExerciseQuestionsTests(unittest.TestCase):
    def test_runner_prints_footer_after_all_questions(self):
        question = Question(
            "Compute 3",
            lambda result: (result == 3, "checked"),
            "Use 1 + 2.",
            reference_answer="1 + 2",
        )

        output = StringIO()
        with patch("builtins.input", return_value="1 + 2"), redirect_stdout(output):
            run_exercise_questions({}, [question])

        self.assertIn("Exercise completed! Returning to main menu", output.getvalue())

    def test_runner_prints_question_progress(self):
        questions = [
            Question("Compute 1", lambda result: (result == 1, ""), "Use 1."),
            Question("Compute 2", lambda result: (result == 2, ""), "Use 2."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(output):
            run_exercise_questions({}, questions)

        text = output.getvalue()
        self.assertIn("Practice Question (1/2):", text)
        self.assertIn("Practice Question (2/2):", text)

    def test_runner_prints_single_command_reminder_per_batch(self):
        questions = [
            Question("Compute 1", lambda result: (result == 1, ""), "Use 1."),
            Question("Compute 2", lambda result: (result == 2, ""), "Use 2."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["1", "2"]), redirect_stdout(output):
            run_exercise_questions({}, questions)

        text = output.getvalue()
        self.assertEqual(text.count("Tip: type skip"), 1)
        self.assertTrue(text.startswith("\nTip: type skip"))
        self.assertIn("main menu.\n\n" + "-" * 60 + "\nPractice Question (1/2):", text)
        self.assertIn("exit/quit to return to the main menu", text)

    def test_runner_skips_footer_when_exercise_aborts(self):
        question = Question("Leave", lambda result: (True, ""), "Type exit.")

        output = StringIO()
        with patch("builtins.input", return_value="quit"), redirect_stdout(output):
            run_exercise_questions({}, [question])

        self.assertIn("Leaving exercise early", output.getvalue())
        self.assertNotIn("Exercise completed! Returning to main menu", output.getvalue())

    def test_runner_continues_after_skip(self):
        questions = [
            Question("Skip this", lambda result: (False, ""), "Type skip."),
            Question("Compute 3", lambda result: (result == 3, ""), "Use 3."),
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=["skip", "3"]), redirect_stdout(output):
            run_exercise_questions({}, questions)

        text = output.getvalue()
        self.assertIn("Skipping question.", text)
        self.assertIn("Practice Question (2/2):", text)
        self.assertIn("Exercise completed! Returning to main menu", text)


if __name__ == "__main__":
    unittest.main()
