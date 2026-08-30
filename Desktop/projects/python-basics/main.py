"""
Python Basics
Interactive practice for fundamental Python topics (output, comments, variables, types, etc.).
"""

import sys
from pathlib import Path

# Ensure the script's directory is on the path so imports work when run from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import PythonBasics


def main():
    """Main entry point."""
    PythonBasics().main_menu()


if __name__ == "__main__":
    main()
