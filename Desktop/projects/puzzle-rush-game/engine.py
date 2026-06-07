"""Shared gameplay engine for puzzle-rush-game sessions."""

from __future__ import annotations

from typing import Callable

from game_common import (
    EXIT_ROUND_KEYWORDS,
    REPLAY_EXIT,
    REPLAY_KEEP,
    ChallengeFactory,
    build_challenge_sequence,
    get_challenge_counts,
    make_code_validator,
    normalize_true_false_answer,
    prompt_difficulty,
    show_hint,
)


Challenge = dict
ChallengeFactory = Callable[[str], Challenge]
SequenceBuilder = Callable[[str, int, int, set[str]], list[ChallengeFactory]]

_MAX_UNIQUE_GENERATION_ATTEMPTS = 500
CodeValidator = Callable[[str, str], bool]
HintPrinter = Callable[[Challenge], None]

def run_game_session(
    *,
    game_name: str,
    subtitle: str,
    perfect_message: str,
    thank_you_message: str,
    code_validator: CodeValidator,
    sequence_builder: SequenceBuilder,
    show_hint: HintPrinter,
) -> None:
    """Run one full game session with shared I/O, scoring and feedback."""
    print(f"Welcome to {game_name}!")
    print(f"{subtitle}\n")

    difficulty = prompt_difficulty()

    print(f"\nYou selected {difficulty.upper()} difficulty. Good luck!")
    print("(Tip: Type 'exit' at any time to quit the current round)\n")

    total_challenges, code_count, tf_count = get_challenge_counts(difficulty)
    seen_questions: set[str] = set()
    challenge_sequence = sequence_builder(difficulty, code_count, tf_count, seen_questions)
    score = 0

    for i in range(total_challenges):
        print(f"--- Challenge {i + 1} of {total_challenges} ---")

        challenge_func = challenge_sequence[i]
        challenge = None
        # After _MAX_UNIQUE_GENERATION_ATTEMPTS, accept a duplicate question rather than abort.
        for _ in range(_MAX_UNIQUE_GENERATION_ATTEMPTS):
            candidate = challenge_func(difficulty)
            if candidate["question"] not in seen_questions:
                challenge = candidate
                break
        if challenge is None:
            challenge = challenge_func(difficulty)
        seen_questions.add(challenge["question"])
        print(f"\n{challenge['question']}\n")

        if challenge["type"] == "true_false":
            user_answer = normalize_true_false_answer(input("Your answer: "))
            if user_answer == "exit":
                print("\nRound ended. Returning to menu...")
                return
            is_correct = user_answer == challenge["answer"]
        else:
            user_answer = input("Your answer (write the code): ").strip()
            if user_answer in EXIT_ROUND_KEYWORDS:
                print("\nRound ended. Returning to menu...")
                return
            is_correct = code_validator(user_answer, challenge["answer"])

        if is_correct:
            print("✓ Correct! Well done!")
            score += 1
        else:
            if challenge["type"] == "true_false":
                shown = challenge["answer"].capitalize()
                print(f"✗ Incorrect. The correct answer is {shown}")
            else:
                print(f"✗ Incorrect. The correct answer is: {challenge['answer']}")
            show_hint(challenge)

        print(f"Current score: {score}/{i + 1}\n")

    percentage = (score / total_challenges) * 100
    print("=" * 50)
    print(f"Final Score: {score} out of {total_challenges}")
    print(f"Percentage: {percentage:.1f}%")

    if percentage == 100:
        print(perfect_message)
    elif percentage >= 80:
        print("Excellent work! You're getting really good! 🌟")
    elif percentage >= 60:
        print("Good job! Keep practicing! 👍")
    else:
        print("Keep practicing! You'll get better! 💪")

    print(f"\n{thank_you_message}")


def run_standard_game(
    *,
    game_name: str,
    subtitle: str,
    perfect_message: str,
    thank_you_message: str,
    validator_profile: str,
    code_generators: list[ChallengeFactory],
    true_false_factory: ChallengeFactory,
    mandatory_first: ChallengeFactory | None = None,
) -> None:
    """Run one session using shared sequence wiring and validator profile."""

    def build_sequence(_difficulty: str, code_count: int, tf_count: int, used_questions: set[str]):
        return build_challenge_sequence(
            code_generators,
            true_false_factory,
            code_count=code_count,
            tf_count=tf_count,
            used_questions=used_questions,
            mandatory_first=mandatory_first,
        )

    run_game_session(
        game_name=game_name,
        subtitle=subtitle,
        perfect_message=perfect_message,
        thank_you_message=thank_you_message,
        code_validator=make_code_validator(validator_profile),
        sequence_builder=build_sequence,
        show_hint=show_hint,
    )


def run_with_replay(play_once: Callable[[], None]) -> None:
    """Run play_once() and handle the standard replay prompt loop.

    Uses ``REPLAY_KEEP`` / ``REPLAY_EXIT`` from ``game_common`` — same for every game.
    """
    while True:
        play_once()

        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").strip()
            if play_again in REPLAY_KEEP or play_again in REPLAY_EXIT:
                break
            print("Invalid choice. Please enter 'yes' or 'no'.")

        if play_again in REPLAY_EXIT:
            print("\nWe'll talk later! 👋")
            break
        print("\n" + "=" * 50 + "\n")
