# Puzzle Rush Game - NumPy Challenge Collection

Interactive terminal games for practicing NumPy topics through short code and true/false challenges.

## Games

- `array_blitz.py` - Arrays (creation, indexing, slicing, reshape, join/split, search/sort/filter)
- `vector_battle.py` - Random operations (permutation vs shuffle, distributions, choice/randint/random)
- `matrix_challenge.py` - Matrix operations (2D arrays, matrix math, transpose, reshape, properties)
- `ufunc_arena.py` - Universal functions (arithmetic, rounding, logs, sums/products/diffs, set ops)

## Requirements

```bash
pip install -r requirements.txt
```

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

It checks:
- module import smoke
- challenge generator output shape across difficulties
- quick CLI entry smoke for each game
- guard that `play_game()` includes true/false scheduling

## Project architecture

- `engine.py` - Shared session engine (difficulty flow, challenge loop, scoring, replay prompt)
- `game_common.py` - Shared helpers (difficulty parsing, counts, true/false input normalization, T/F statement picking)
- `code_validators.py` - Shared code-answer validation profiles (`default`, `vector`, `matrix`)
- `array_blitz.py`, `vector_battle.py`, `matrix_challenge.py`, `ufunc_arena.py` - Game-specific challenge generators and sequence building
- `verify_phase0_smoke.py` - Regression/smoke guard

## Notes

- Type-checker warnings about unresolved `numpy` usually mean your IDE interpreter differs from the environment where NumPy is installed.

