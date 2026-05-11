"""Generate ANSWERS.md from Question definitions in exercises.py.

This keeps the answer key tied to the same prompts and reference answers used by
the interactive exercises.
"""

import argparse
import ast
from pathlib import Path
from typing import List, NamedTuple, Optional


ROOT = Path(__file__).resolve().parent
EXERCISES_PATH = ROOT / "exercises.py"
ANSWERS_PATH = ROOT / "ANSWERS.md"

EXERCISE_TITLES = {
    "exercise_constants": "1. Constants Exercise",
    "exercise_optimize": "2. Optimization Exercise",
    "exercise_sparse": "3. Sparse Matrices Exercise",
    "exercise_csgraph": "4. CSGraph Exercise",
    "exercise_spatial": "5. Spatial Data Exercise",
    "exercise_interpolate": "6. Interpolation Exercise",
}


class AnswerQuestion(NamedTuple):
    text: str
    reference_answer: str


class ExerciseAnswers(NamedTuple):
    title: str
    questions: List[AnswerQuestion]


def string_value(node: Optional[ast.AST]) -> Optional[str]:
    """Return a string literal value from an AST node, if it is one."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def question_call_name(call: ast.Call) -> Optional[str]:
    """Return the called function name for Question(...) calls."""
    if isinstance(call.func, ast.Name):
        return call.func.id
    return None


def get_keyword(call: ast.Call, name: str) -> Optional[ast.AST]:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def extract_question(call: ast.Call) -> Optional[AnswerQuestion]:
    """Extract prompt and reference answer from a Question(...) AST call."""
    if question_call_name(call) != "Question":
        return None

    text_node = get_keyword(call, "text")
    if text_node is None and call.args:
        text_node = call.args[0]

    reference_node = get_keyword(call, "reference_answer")

    text = string_value(text_node)
    reference_answer = string_value(reference_node)
    if text is None or reference_answer is None:
        return None
    return AnswerQuestion(text=text, reference_answer=reference_answer)


def extract_answers(source: str) -> List[ExerciseAnswers]:
    """Extract ordered exercise question/answer data from exercises.py source."""
    tree = ast.parse(source)
    sections = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name not in EXERCISE_TITLES:
            continue

        questions = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                question = extract_question(child)
                if question is not None:
                    questions.append(question)

        sections.append(ExerciseAnswers(title=EXERCISE_TITLES[node.name], questions=questions))

    return sections


def build_answers_markdown(sections: List[ExerciseAnswers]) -> str:
    """Build the full ANSWERS.md contents."""
    lines = [
        "# Practice Questions and Answers",
        "",
        "> Generated from `exercises.py` by `generate_answers.py`.",
        "> Run `python generate_answers.py --check` to verify this file is in sync.",
        "",
    ]

    for section in sections:
        lines.append(f"## {section.title}")
        lines.append("")

        for index, question in enumerate(section.questions, start=1):
            lines.append(f"### Question {index}")
            lines.append(f"**Question:** {question.text}  ")
            lines.append(f"**Reference answer:** `{question.reference_answer}`")
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def generate_answers() -> str:
    return build_answers_markdown(extract_answers(EXERCISES_PATH.read_text()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or verify ANSWERS.md.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if ANSWERS.md is not in sync with exercises.py.",
    )
    args = parser.parse_args()

    expected = generate_answers()
    if args.check:
        actual = ANSWERS_PATH.read_text()
        if actual != expected:
            print("ANSWERS.md is out of sync. Run: python generate_answers.py")
            return 1
        print("ANSWERS.md is in sync.")
        return 0

    ANSWERS_PATH.write_text(expected)
    print("Wrote ANSWERS.md from exercises.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
