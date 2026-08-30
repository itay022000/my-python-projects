"""Puzzle Rush application shell (B015)."""

from games.array_blitz import play_game as play_array_blitz
from games.matrix_challenge import play_game as play_matrix_challenge
from games.ufunc_arena import play_game as play_ufunc_arena
from games.vector_battle import play_game as play_vector_battle
from session_common import SESSION_BANNER_WIDTH

_GOODBYE = "\nWe'll talk later! 👋"


class PuzzleRush:
    """Main menu and game dispatch for puzzle-rush-game."""

    def show_menu(self) -> None:
        bar = "=" * SESSION_BANNER_WIDTH
        print("\n" + bar)
        print("Puzzle Rush - NumPy Practice")
        print(bar)
        print("1. Array Blitz")
        print("2. Vector Battle")
        print("3. Matrix Challenge")
        print("4. Ufunc Arena")
        print("5. Exit (or type 'exit'/'Exit')")
        print(bar)

    def run(self) -> None:
        games = {
            "1": play_array_blitz,
            "2": play_vector_battle,
            "3": play_matrix_challenge,
            "4": play_ufunc_arena,
        }

        while True:
            self.show_menu()
            prompt = "Select an option (1-5 or 'exit'/'Exit'): "
            while True:
                choice = input(prompt).strip()
                if choice != "":
                    break

            if choice in games:
                games[choice]()
            elif choice == "5" or choice in ("exit", "Exit"):
                print(_GOODBYE)
                break
            else:
                print("\n❌ Invalid choice. Please select 1-5, or type 'exit'/'Exit'.")
