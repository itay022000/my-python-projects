"""
Engine behavior verification for puzzle-rush-game.

Exercises correct / wrong / empty / skip / exit paths across all 20 question
slots for each of the four games (mocked challenges; generators unchanged).

Run from this directory:
  python3 verify_answer_behavior.py
"""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from exercise_session import run_game_session
from session_common import ROUND_TOTAL, classify_special_input, make_code_validator

GAME_PROFILES = {
    "array_blitz": "default",
    "vector_battle": "vector",
    "matrix_challenge": "matrix",
    "ufunc_arena": "default",
}

TOTAL = ROUND_TOTAL


def _assert_code_attempt_messaging(text: str, label: str) -> None:
    if "Incorrect answer (attempt 1/3)." not in text:
        raise AssertionError(f"{label}: missing code wrong-attempt message")
    if "Try again..." not in text:
        raise AssertionError(f"{label}: missing Try again after wrong code answer")
    if "Incorrect answer (attempt 3/3)." not in text:
        raise AssertionError(f"{label}: missing third-strike attempt message")


def _mock_code() -> dict:
    return {
        "type": "create",
        "question": "Write the code answer `ok`",
        "answer": "ok",
        "hint": "type ok",
    }


def _mock_tf() -> dict:
    return {
        "type": "true_false",
        "question": "True or False: sample statement",
        "answer": "True",
        "hint": "",
    }


def _code_factories() -> list:
    return [lambda: _mock_code() for _ in range(TOTAL)]


def _tf_factories() -> list:
    return [lambda: _mock_tf() for _ in range(TOTAL)]


def _run(inputs: list[str], *, profile: str, factories: list) -> str:
    out = StringIO()
    validator = make_code_validator(profile)
    with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
        run_game_session(
            teach_title="TEST",
            teach_body_lines=["line"],
            code_validator=validator,
            sequence_builder=lambda *a: factories,
            challenge_factories=factories,
        )
    return out.getvalue()


def _prefix_correct(qi: int) -> list[str]:
    return [""] + ["ok"] * qi


def test_special_commands() -> None:
    assert classify_special_input("skip") == "skip"
    assert classify_special_input("Skip") == "skip"
    assert classify_special_input("exit") == "exit"
    assert classify_special_input("Exit") == "exit"
    assert classify_special_input("quit") == "exit"
    assert classify_special_input("Quit") == "exit"
    assert classify_special_input("SKIP") is None
    assert classify_special_input("EXIT") is None


def test_skip_at_slot(game: str, qi: int) -> None:
    inputs = _prefix_correct(qi) + ["skip"]
    if qi < TOTAL - 1:
        inputs.append("exit")
    text = _run(inputs, profile=GAME_PROFILES[game], factories=_code_factories())
    label = f"{game} Q{qi + 1}"
    if "Skipping question." not in text:
        raise AssertionError(f"{label}: skip did not fire")
    if "Correct answer:" not in text:
        raise AssertionError(f"{label}: skip did not show answer")
    if qi < TOTAL - 1:
        if "Session exited." not in text:
            raise AssertionError(f"{label}: expected early exit after skip probe")
    elif "Session Statistics" not in text or "Returning to main menu" not in text:
        raise AssertionError(f"{label}: skip on last question must finish batch")


def test_exit_at_slot(game: str, qi: int) -> None:
    text = _run(_prefix_correct(qi) + ["exit"], profile=GAME_PROFILES[game], factories=_code_factories())
    label = f"{game} Q{qi + 1}"
    if "Session exited." not in text:
        raise AssertionError(f"{label}: exit did not end round")
    if "Returning to main menu" not in text:
        raise AssertionError(f"{label}: exit missing menu return")
    if "play again" in text.lower():
        raise AssertionError(f"{label}: replay prompt must not appear")


def test_empty_at_slot(game: str, qi: int) -> None:
    inputs = _prefix_correct(qi) + ["", "", "ok"]
    if qi < TOTAL - 1:
        inputs.append("exit")
    text = _run(inputs, profile=GAME_PROFILES[game], factories=_code_factories())
    label = f"{game} Q{qi + 1}"
    if text.count("Hint:") > 0:
        raise AssertionError(f"{label}: empty input must not trigger hint")
    if qi < TOTAL - 1:
        if "Session exited." not in text:
            raise AssertionError(f"{label}: expected to survive empty lines and exit later")
    elif "Session Statistics" not in text:
        raise AssertionError(f"{label}: empty lines on last question must still complete batch")


def test_code_three_strikes_at_slot(game: str, qi: int) -> None:
    text = _run(
        _prefix_correct(qi) + ["bad", "bad", "bad", "exit"],
        profile=GAME_PROFILES[game],
        factories=_code_factories(),
    )
    label = f"{game} Q{qi + 1}"
    if text.count("Hint:") != 1:
        raise AssertionError(f"{label}: expected exactly one hint after first strike, got {text.count('Hint:')}")
    if "Correct answer:" not in text:
        raise AssertionError(f"{label}: third strike must reveal answer")
    _assert_code_attempt_messaging(text, label)


def test_tf_one_strike_at_slot(game: str, qi: int) -> None:
    text = _run(
        _prefix_correct(qi) + ["false", "exit"],
        profile=GAME_PROFILES[game],
        factories=_tf_factories(),
    )
    label = f"{game} Q{qi + 1} T/F"
    if "Hint:" in text:
        raise AssertionError(f"{label}: T/F wrong must not show hint")
    if "Correct answer: True" not in text:
        raise AssertionError(f"{label}: T/F wrong must reveal answer")
    if "Incorrect answer (attempt 1/1)." not in text:
        raise AssertionError(f"{label}: missing T/F wrong-attempt message")


def test_late_round_partial_exit(game: str) -> None:
    text = _run(
        [""] + ["ok"] * 13 + ["exit"],
        profile=GAME_PROFILES[game],
        factories=_code_factories(),
    )
    label = f"{game} Q14"
    if "Completed successfully: 13" not in text:
        raise AssertionError(f"{label}: expected 13 completed before exit")


def test_correct_completes_batch(game: str) -> None:
    text = _run([""] + ["ok"] * TOTAL, profile=GAME_PROFILES[game], factories=_code_factories())
    if "Session Statistics" not in text or "Completed successfully: 20" not in text:
        raise AssertionError(f"{game}: full correct run failed")
    if "Returning to main menu" not in text:
        raise AssertionError(f"{game}: batch end must return to menu")


def test_shared_ux_helpers() -> None:
    from session_common import (
        MAX_ATTEMPTS,
        ROUND_TOTAL,
        TF_MAX_ATTEMPTS,
        build_teach_body_lines,
        code_prompt,
        true_false_prompt,
    )

    body = build_teach_body_lines("Intro")
    assert len(body) == 2
    assert body[1].startswith("After three wrong attempts (one for True/False questions)")
    assert code_prompt(0).endswith(f"(attempt 1/{MAX_ATTEMPTS}): ")
    assert code_prompt(2).endswith(f"(attempt 3/{MAX_ATTEMPTS}): ")
    assert true_false_prompt() == f"Your answer (attempt 1/{TF_MAX_ATTEMPTS}): "
    assert ROUND_TOTAL == 20


def main() -> None:
    test_special_commands()
    test_shared_ux_helpers()

    for game in GAME_PROFILES:
        test_correct_completes_batch(game)
        test_late_round_partial_exit(game)
        for qi in range(TOTAL):
            test_skip_at_slot(game, qi)
            test_exit_at_slot(game, qi)
            test_empty_at_slot(game, qi)
            test_code_three_strikes_at_slot(game, qi)
            test_tf_one_strike_at_slot(game, qi)

    print(
        f"verify_answer_behavior: OK "
        f"({TOTAL} slots × {len(GAME_PROFILES)} games × skip/exit/empty/strikes/T-F checks)."
    )


if __name__ == "__main__":
    main()
