# Python basics — interactive practice

A small **terminal menu** of graded single-line (and some multi-line) Python exercises, grouped by topic. Answers are checked with **shared normalization rules** per topic; sessions track mistakes and print statistics at the end.

**Requirements:** Python **3.10+** recommended (uses modern typing syntax). **No third-party packages** — standard library only.

## Run

From this directory:

```bash
python3 main.py
```

Choose menu options **1–10** for exercise batches, **11** or `exit` to quit.

## Verify (developers)

Regression scripts live next to `main.py`. Run them from this directory; each exits **0** only if all internal checks pass.

```bash
python3 verify_exercise_checks_parity.py
python3 verify_project_smoke.py
python3 verify_answer_behavior.py
```

They exercise graders, pool wiring, and session behavior; they are **not** a full replacement for trying the menu yourself.

## Project layout (short)

| Piece | Role |
|--------|------|
| `main.py` | Menu and batch wiring |
| `session_runner.py` | Shared interactive loop, banners, statistics |
| `exercise_checks.py` | Normalizers and exact-answer checks |
| `batch_*_exercises.py` | Topic pools and session builders |
| `verify_*.py` | Automated checks |

More detail: **`PROJECT_STRUCTURE_AND_REQUIREMENTS.md`**.

## License

Add a `LICENSE` file in your repo if you want an explicit license for GitHub.
