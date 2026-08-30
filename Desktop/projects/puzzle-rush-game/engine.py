"""Shared gameplay engine for puzzle-rush-game sessions."""

from __future__ import annotations

from typing import Callable

from session_common import (
    MAX_ATTEMPTS,
    ROUND_TIP,
    TF_MAX_ATTEMPTS,
    ChallengeFactory,
    QuestionOutcome,
    build_challenge_sequence,
    classify_special_input,
    code_prompt,
    get_challenge_counts,
    make_code_validator,
    print_correct_answer,
    print_partial_exit_score,
    print_question_header,
    print_session_footer,
    print_skip_answer,
    print_teach_intro,
    print_wrong_attempt,
    true_false_prompt,
)


Challenge = dict
SequenceBuilder = Callable[[int, int, set[str]], list[ChallengeFactory]]

_MAX_UNIQUE_GENERATION_ATTEMPTS = 500
CodeValidator = Callable[[str, str], bool]
Checker = Callable[[str], bool]


def _question_text(challenge: Challenge) -> str:
    text = challenge["question"]
    return text[:-1] if text.endswith(".") else text


def record_outcome(
    outcome: QuestionOutcome,
    completed: int,
    not_completed: int,
) -> tuple[int, int] | None:
    """2-bucket score update. Returns None after handling EXIT (partial printed)."""
    if outcome == QuestionOutcome.EXIT:
        not_completed += 1
        print_partial_exit_score(completed, not_completed)
        return None
    if outcome == QuestionOutcome.COMPLETED:
        return completed + 1, not_completed
    return completed, not_completed + 1


def _default_on_skip(correct_answer: str) -> QuestionOutcome:
    print_skip_answer(correct_answer)
    return QuestionOutcome.NOT_COMPLETED


def ask_code_question(
    *,
    check: Checker,
    correct_answer: str,
    hint: str | None = None,
    max_attempts: int = MAX_ATTEMPTS,
    on_skip: Callable[[], QuestionOutcome] | None = None,
) -> QuestionOutcome:
    """Shared strike-loop body. Does not update scores."""
    skip_fn = on_skip or (lambda: _default_on_skip(correct_answer))
    print()
    strikes = 0
    while True:
        raw = input(code_prompt(strikes, max_attempts)).strip()
        if raw == "":
            continue

        special = classify_special_input(raw)
        if special == "exit":
            return QuestionOutcome.EXIT
        if special == "skip":
            return skip_fn()

        if check(raw):
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        print_wrong_attempt(strikes, max_attempts)
        if strikes == 1 and hint:
            print(f"Hint: {hint}")
            print()
        if strikes >= max_attempts:
            print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED


def ask_true_false_question(
    *,
    check: Checker,
    correct_answer: str,
    max_attempts: int = TF_MAX_ATTEMPTS,
    on_skip: Callable[[], QuestionOutcome] | None = None,
) -> QuestionOutcome:
    """One-attempt T/F loop. Does not update scores."""
    skip_fn = on_skip or (lambda: _default_on_skip(correct_answer))
    print()
    strikes = 0
    while True:
        raw = input(true_false_prompt()).strip()
        if raw == "":
            continue

        special = classify_special_input(raw)
        if special == "exit":
            return QuestionOutcome.EXIT
        if special == "skip":
            return skip_fn()

        if check(raw):
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        print_wrong_attempt(strikes, max_attempts)
        if strikes >= max_attempts:
            print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED


def run_game_session(
    *,
    teach_title: str,
    teach_body_lines: list[str],
    code_validator: CodeValidator,
    sequence_builder: SequenceBuilder,
    challenge_factories: list[ChallengeFactory] | None = None,
    background: str | None = None,
) -> None:
    """Run one full game round and return to the caller (main menu)."""
    print_teach_intro(teach_title, teach_body_lines)
    print(ROUND_TIP)
    if background:
        print(background)
        print()

    total_challenges, code_count, tf_count = get_challenge_counts()
    seen_questions: set[str] = set()

    if challenge_factories is not None:
        factories = challenge_factories
    else:
        factories = sequence_builder(code_count, tf_count, seen_questions)

    assert len(factories) == total_challenges, (
        f"expected {total_challenges} challenges, got {len(factories)}"
    )

    completed = 0
    not_completed = 0
    for i in range(total_challenges):
        if challenge_factories is not None:
            challenge = factories[i]()
        else:
            challenge_func = factories[i]
            challenge = None
            for _ in range(_MAX_UNIQUE_GENERATION_ATTEMPTS):
                candidate = challenge_func()
                if candidate["question"] not in seen_questions:
                    challenge = candidate
                    break
            if challenge is None:
                challenge = challenge_func()
            seen_questions.add(challenge["question"])

        print_question_header(
            i + 1,
            total_challenges,
            _question_text(challenge),
            first=(i == 0),
        )
        correct_answer = challenge["answer"]
        if challenge["type"] == "true_false":
            outcome = ask_true_false_question(
                check=lambda raw, expected=correct_answer: raw == expected,
                correct_answer=correct_answer,
            )
        else:
            outcome = ask_code_question(
                check=lambda raw, expected=correct_answer: code_validator(raw, expected),
                correct_answer=correct_answer,
                hint=challenge.get("hint") or None,
            )

        result = record_outcome(outcome, completed, not_completed)
        if result is None:
            return
        completed, not_completed = result

    print_session_footer(completed, not_completed)


def run_standard_game(
    *,
    teach_title: str,
    teach_body_lines: list[str],
    validator_profile: str,
    code_generators: list[ChallengeFactory],
    true_false_factory: ChallengeFactory,
    background: str | None = None,
) -> None:
    """Run one session using shared sequence wiring and validator profile."""

    def build_sequence(code_count: int, tf_count: int, used_questions: set[str]):
        return build_challenge_sequence(
            code_generators,
            true_false_factory,
            code_count=code_count,
            tf_count=tf_count,
            used_questions=used_questions,
        )

    run_game_session(
        teach_title=teach_title,
        teach_body_lines=teach_body_lines,
        code_validator=make_code_validator(validator_profile),
        sequence_builder=build_sequence,
        background=background,
    )
