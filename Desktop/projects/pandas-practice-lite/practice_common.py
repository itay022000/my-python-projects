"""
Shared helpers for pandas-practice-lite (B002).
Behavior-preserving utilities for code comparison and special task commands.
"""


def normalize_code(code: str) -> str:
    """Collapse whitespace for exact-match comparison (same as inline main.py logic)."""
    return " ".join(code.strip().split())


def codes_match(user_code: str, correct_answer: str) -> bool:
    """True when user code matches the expected answer after whitespace normalization."""
    return normalize_code(user_code) == normalize_code(correct_answer)


def handle_special_commands(code, correct_answer, explanation):
    """
    Handle special commands 'skip' and 'exit'.
    Returns: (is_skip, is_exit, should_continue)
    """
    code_lower = code.lower().strip()

    if code_lower == "skip":
        print("\n" + "=" * 60)
        print("⏭️  Task skipped")
        print("=" * 60)
        print("📖 CORRECT ANSWER:")
        print("=" * 60)
        print(correct_answer)
        if explanation:
            print(f"\n💡 Explanation: {explanation}")
        return True, False, True

    if code_lower == "exit":
        return False, True, False

    return False, False, True


def print_correct_answer(correct_answer: str, explanation: str = "") -> None:
    """Show the canonical answer block after max failed attempts."""
    print("\n" + "=" * 60)
    print("📖 CORRECT ANSWER:")
    print("=" * 60)
    print(correct_answer)
    if explanation:
        print(f"\n💡 Explanation: {explanation}")
