"""Shared low-risk gameplay helpers for puzzle-rush-game."""

from __future__ import annotations
import random


# Exact spellings accepted for difficulty (case-sensitive on words; see prompt_difficulty).
_DIFFICULTY_TO_CANONICAL = {
    "1": "easy",
    "easy": "easy",
    "Easy": "easy",
    "2": "medium",
    "medium": "medium",
    "Medium": "medium",
    "3": "hard",
    "hard": "hard",
    "Hard": "hard",
}


def parse_difficulty_choice(raw: str) -> str | None:
    """Map allowed difficulty strings to canonical 'easy' | 'medium' | 'hard', or None if invalid."""
    s = raw.strip()
    return _DIFFICULTY_TO_CANONICAL.get(s)


def prompt_difficulty() -> str:
    """Prompt until a valid difficulty is chosen."""
    while True:
        difficulty = parse_difficulty_choice(
            input("Select difficulty (easy/medium/hard or 1/2/3): ")
        )
        if difficulty is not None:
            return difficulty
        print("Invalid choice. Please enter difficulty level.")


def get_challenge_counts(difficulty: str) -> tuple[int, int, int]:
    """Return (total_challenges, code_count, tf_count) for a difficulty."""
    if difficulty == "easy":
        return 6, 5, 1
    if difficulty == "medium":
        return 13, 10, 3
    return 20, 15, 5


# Quit mid-round from engine (code + true_false paths); EXIT / eXiT etc. rejected.
EXIT_ROUND_KEYWORDS = frozenset({"exit", "Exit"})

# Play-again prompt — shared by all games via engine.run_with_replay (YES/NO etc. rejected).
REPLAY_KEEP = frozenset({"y", "yes", "Y", "Yes"})
REPLAY_EXIT = frozenset({"n", "no", "N", "No"})

# Exact spellings accepted for true/false questions (case-sensitive; mixed case like TRUE rejected).
_TRUE_FALSE_ACCEPT_TRUE = frozenset({"t", "true", "T", "True"})
_TRUE_FALSE_ACCEPT_FALSE = frozenset({"f", "false", "F", "False"})


def normalize_true_false_answer(raw: str) -> str:
    """
    Map allowed true/false spellings to canonical 'true' / 'false'.

    Mid-round quit (engine): only ``exit`` and ``Exit`` — see ``EXIT_ROUND_KEYWORDS``.

    Only these exact strings (after stripping surrounding whitespace) are accepted:
      True:  t, true, T, True
      False: f, false, F, False

    Any other spelling is returned unchanged so grading compares false.
    """
    s = raw.strip()
    if s in EXIT_ROUND_KEYWORDS:
        return "exit"
    if s in _TRUE_FALSE_ACCEPT_TRUE:
        return "true"
    if s in _TRUE_FALSE_ACCEPT_FALSE:
        return "false"
    return s


def pick_true_false_statement(
    difficulty: str,
    statements_by_difficulty: dict[str, list[tuple[str, str]]],
    hints_by_difficulty: dict[str, str],
    *,
    used_questions: set[str] | None = None,
) -> tuple[str, str, str]:
    """
    Pick a (question, answer, hint) tuple from data tables.

    When ``used_questions`` is provided, only statements whose question text is not
    already in that set are eligible (no duplicate T/F prompts in one session).

    This keeps true/false generators data-driven instead of large if/elif chains.
    """
    statements = statements_by_difficulty.get(difficulty, statements_by_difficulty["hard"])
    if used_questions is not None:
        candidates = [s for s in statements if s[0] not in used_questions]
        if not candidates:
            raise ValueError(
                f"No unused true/false statement left for difficulty {difficulty!r}; "
                "add more entries to the bank or lower tf_count for this tier."
            )
        question, answer = random.choice(candidates)
    else:
        question, answer = random.choice(statements)
    hint = hints_by_difficulty.get(difficulty, hints_by_difficulty["hard"])
    return question, answer, hint
