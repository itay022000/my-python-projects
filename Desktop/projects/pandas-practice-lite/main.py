"""
Pandas Practice - entry point (B003 thin main).
"""

import env_quiet  # noqa: F401 — before pandas (via app)

from app import PandasPractice


def main():
    """Main entry point."""
    app = PandasPractice()
    app.main_menu()


if __name__ == "__main__":
    main()
