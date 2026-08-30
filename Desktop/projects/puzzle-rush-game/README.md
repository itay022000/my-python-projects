# Puzzle Rush Game — NumPy Challenge Collection

Interactive terminal games for practicing NumPy topics through short code and True/False challenges.

## Run

From this directory:

```bash
python3 main.py
```

**Main menu:** **1–4** = games · **5** = exit · `Select an option (1-5):`

Legacy per-game scripts (`array_blitz.py`, etc.) only print a note to use `main.py` — they do not start a round.

## Games

| # | Menu | Module | Topic |
|---|------|--------|--------|
| 1 | Array Blitz | `array_blitz.py` | Arrays (creation, indexing, slicing, reshape, join/split, search/sort/filter) |
| 2 | Vector Battle | `vector_battle.py` | Random ops (permutation, shuffle, distributions, choice) |
| 3 | Matrix Challenge | `matrix_challenge.py` | Matrix math, transpose, reshape, properties |
| 4 | Ufunc Arena | `ufunc_arena.py` | Universal functions (arithmetic, rounding, logs, sums, set ops) |

## During a round

Each game runs one batch of **20** questions: **15** code (shuffled, questions 1–15) then **5** True/False (questions 16–20). There is no difficulty picker — one question pool per game.

1. **Teach intro** — short rules (python-basics style), then **Press Enter to start...**
2. **Tip** — `skip` moves on; `exit` / `quit` ends the round and returns to the main menu
3. **Questions** — `--- Challenge n of 20 ---` with a running score **`Current score: x/20`** (always out of **20**, not the current question number)

### Prompts and feedback

| Type | Prompt | On wrong |
|------|--------|----------|
| **Code** | `Your answer (write the code) (attempt n/3):` | `Incorrect answer (attempt n/3).` · attempt 1 → hint + `Try again...` · attempt 2 → `Try again...` only · attempt 3 → correct answer |
| **True/False** | `Your answer (attempt 1/1):` | `Incorrect answer (attempt 1/1).` → correct answer |

Accepted T/F answers (exact, after strip): **`True`** · **`False`** only (same as python-basics Batch 2).

Partial exit and final score also use the batch total (**20**): e.g. `Round ended early. Score: 12/20 (60.0%)` and `Final Score: 12 out of 20`.

### Special commands (any question)

Accepted spellings: **`skip` / `Skip`**, **`exit` / `Exit`**, **`quit` / `Quit`**

| Input | Effect |
|--------|--------|
| **`skip`** | Show correct answer; count as **wrong**; next question |
| **`exit`** or **`quit`** | End round early; show **partial score**; return to main menu |
| **Empty line** | Re-prompt; **no strike**; no hint |

### Strikes

| Type | Attempts | On wrong |
|------|----------|----------|
| **Code** | 3 | Attempt 1 → hint only · Attempt 2 → no new hint · Attempt 3 → correct answer, next question |
| **True/False** | 1 | Correct answer, next question |

Empty lines do not consume an attempt (prompt is re-shown with the same attempt number).

After the last question (or early exit), you return to the **main menu** — there is no “play again?” prompt.

## Requirements

**Tested with:** Python **3.10.9** and NumPy **1.26.x** in a venv.

A virtual environment is recommended. If your base Anaconda install shows NumPy binary mismatch warnings, create a venv and install there:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` keeps a flexible lower bound (`numpy>=1.20.0`); use the tested stack above for QA parity.

## Verification

Run from this directory:

```bash
python3 verify_phase0_smoke.py
python3 verify_answer_behavior.py
```

Both must exit **0** before release.

**POSIX only:** `verify_phase0_smoke.py` uses `signal.SIGALRM` for generator timeouts (macOS / Linux).

| Script | Covers |
|--------|--------|
| `verify_phase0_smoke.py` | Imports; generator shape; main menu exit; per-game `play_game()` entry; T/F scheduling guard; Array Blitz slice regression |
| `verify_answer_behavior.py` | Correct / wrong / empty / skip / exit across all **20** question slots × **4** games; attempt messaging; running score always **x/20** |

## Project architecture

```
puzzle-rush-game/
├── main.py                    # Thin entry → PuzzleRush().run()
├── app.py                     # Main menu + game dispatch
├── engine.py                  # run_game_session, run_standard_game
├── session_common.py          # Teach intro, counts, T/F banks helper, sequence builder
├── validators.py              # Code-answer profiles (default, vector, matrix)
├── hints.py                   # Strike-1 hint strings (HINT_*)
├── games/
│   ├── array_blitz.py         # Generators + play_game()
│   ├── vector_battle.py
│   ├── matrix_challenge.py
│   └── ufunc_arena.py
├── verify_phase0_smoke.py
├── verify_answer_behavior.py
└── README.md
```

Maintainers: **`README.md` and on-disk code are authoritative.** `IMPLEMENTATION_GUIDE.md` is archived historical notes.

## Notes

- Type-checker warnings about unresolved `numpy` usually mean your IDE interpreter differs from the environment where NumPy is installed.
