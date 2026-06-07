# Puzzle Rush Game - NumPy Challenge Collection

Interactive terminal games for practicing NumPy topics through short code and true/false challenges.

## Games

- `array_blitz.py` - Arrays (creation, indexing, slicing, reshape, join/split, search/sort/filter)
- `vector_battle.py` - Random operations (permutation vs shuffle, distributions, choice/randint/random)
- `matrix_challenge.py` - Matrix operations (2D arrays, matrix math, transpose, reshape, properties)
- `ufunc_arena.py` - Universal functions (arithmetic, rounding, logs, sums/products/diffs, set ops)

## Requirements

**Tested with:** Python **3.10.9** and NumPy **1.26.x** in a venv.

A virtual environment is recommended. If your base Anaconda install shows NumPy binary mismatch warnings, create a venv and install there:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` keeps a flexible lower bound (`numpy>=1.20.0`); use the tested stack above for QA parity.

## Run a game

From this directory:

```bash
python3 array_blitz.py
python3 vector_battle.py
python3 matrix_challenge.py
python3 ufunc_arena.py
```

## Verification

Run the smoke verifier from this directory:

```bash
python3 verify_phase0_smoke.py
```

**POSIX only:** the verifier uses `signal.SIGALRM` / `setitimer` for generator timeouts. Run on macOS or Linux (not Windows) unless the smoke script is ported.

It checks:

- module import smoke
- challenge generator output shape across difficulties
- quick CLI entry smoke for each game
- guard that `play_game()` schedules true/false challenges
- Array Blitz hard-mode negative slice edge case (regression probe)

## Project architecture

- `engine.py` - Shared session engine (`run_game_session`, `run_standard_game`, replay loop)
- `game_common.py` - Shared helpers (difficulty, counts, T/F normalization, sequence builder, hints)
- `code_validators.py` - Shared code-answer validation profiles (`default`, `vector`, `matrix`)
- `array_blitz.py`, `vector_battle.py`, `matrix_challenge.py`, `ufunc_arena.py` - Game-specific challenge generators
- `verify_phase0_smoke.py` - Regression/smoke guard

Maintainers: **`README.md` and on-disk code are authoritative.** `IMPLEMENTATION_GUIDE.md` is archived historical notes from pre-ship development.

## Notes

- Type-checker warnings about unresolved `numpy` usually mean your IDE interpreter differs from the environment where NumPy is installed.
