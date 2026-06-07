"""
Pandas Practice - entry point (B003 thin main).
"""

import warnings

# Keep conda/base installs quiet when optional pandas deps (e.g. bottleneck) are stale.
warnings.filterwarnings(
    "ignore",
    message=r"Pandas requires version .* of 'bottleneck'",
    category=UserWarning,
)

from app import PandasPractice


def main():
    """Main entry point."""
    app = PandasPractice()
    app.main_menu()


if __name__ == "__main__":
    main()
