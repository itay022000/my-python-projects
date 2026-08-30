"""Shared grading helpers for scipy-practice (B015)."""

from __future__ import annotations

import re


def normalize_code(code: str) -> str:
    """Normalize code string for comparison (remove extra spaces)."""
    return re.sub(r"\s+", "", code)
