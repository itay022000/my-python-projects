"""Ensure the committed answer key stays in sync with exercises.py."""

import unittest

from generate_answers import ANSWERS_PATH, generate_answers


class AnswersMarkdownTests(unittest.TestCase):
    def test_answers_markdown_is_generated_from_exercises(self):
        self.assertEqual(ANSWERS_PATH.read_text(), generate_answers())


if __name__ == "__main__":
    unittest.main()
