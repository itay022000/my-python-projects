# Python Basics — Project Structure & Requirements

> Reference doc: on-disk layout, topic coverage, and automated verification for the Python basics teaching project.

---

## 1. Project layout (current)

All paths are relative to the `python-basics/` directory.

| File / module | Role |
|---------------|------|
| **`main.py`** | Thin entry → `PythonBasics().main_menu()` |
| **`app.py`** | Menu shell; options 1–10 launch batch sessions, 11 exits |
| **`batch_1_exercises.py` … `batch_10_exercises.py`** | Exercise pools, session pickers, and `BatchNExercises.start_exercises()` |
| **`validators.py`** | Five normalizer profiles (`normalize_code_*`) and checker bundles (`checker_basic`, `checker_lists`, `checker_sets`, `checker_dicts`, `checker_functions`, plus mixed helpers for batches 5, 8, 10) |
| **`engine.py`** | Shared session loops (`run_simple_exercises`, `run_mixed_units_session`), banners/footers, attempt counting |
| **`verify_exercise_checks_parity.py`** | Normalizer parity vs independent reference implementations |
| **`verify_project_smoke.py`** | Stochastic smoke across all batches (300 sessions × 10) |
| **`verify_answer_behavior.py`** | Grading behavior, three-strike logic, pool enumeration |
| **`README.md`** | User-facing run and verify instructions |
| **`PROJECT_STRUCTURE_AND_REQUIREMENTS.md`** | This file |

**Dependencies:** CPython stdlib only (no `requirements.txt`).

---

## 2. Content (topics covered)

**Exercise question rules (apply to all batches and new question types unless stated otherwise):**
- **Space normalization:** Apply to every question’s answer (no exceptions).
- **No overly explicit hints:** Do not name the exact function, keyword, or syntax the user must type (e.g. avoid “using complex(1, 2)” or “use end=” in the question text).  
  *Footnote:* Batch 1 includes a few teaching prompts that reference `end=` or casting by design; those predate this doc rule and are not rewritten in housekeeping passes.

**Batch numbering (menu order):**

| Batch | Topics | Session shape |
|-------|--------|---------------|
| 1 | Output, comments, variables, data types & casting | 12 random single lines |
| 2 | Strings, booleans | 12 random single lines |
| 3 | Operators | 12 random single lines |
| 4 | Lists | 12 random single lines (segment pools) |
| 5 | Tuples | 12 mixed units (simple + compound) |
| 6 | Sets | 19 random single lines |
| 7 | Dictionaries | 11 random single lines |
| 8 | Functions | 8 mixed units |
| 9 | Shorthand if, match, range, math | 12 fixed-order single lines |
| 10 | Arrays, dates, JSON, try/except, user input | 25 mixed units |

Topic checklist (implemented in batches above):

1. Python output (printing text and/or numbers)
2. Comments
3. Variables (assigning multiple values)
4. Basic data types (bool, int, float, complex, str) and casting
5. Strings (slicing, modification, concatenation, format strings)
6. Booleans (evaluations of values and variables)
7. Operators (arithmetic, assignment, comparison, logical, identity, membership, bitwise)
8. Lists (accessing items, changing items, adding items, removing items, list comprehension, sorting, copying, joining lists)
9. Tuples (accessing, updating, unpacking, joining)
10. Sets (accessing items, adding items, removing items, joining, frozensets)
11. Dictionaries (accessing items, changing items, adding items, removing items, copying)
12. Functions (arguments, *args, **kwargs, decorators, lambda)
13. Shorthand if
14. Match
15. Range
16. Math (min, max, abs, pow)
17. Arrays
18. Dates
19. JSON
20. Try… except
21. User input

---

## 3. Automated verification scripts

Run from the `python-basics/` directory (for example `python3 verify_project_smoke.py`). These scripts exit with status 0 only if every internal **`assert`** passes; they do **not** replace manual play-testing of `main.py`, but they catch regressions in grading and pool wiring.

| Script | What it checks |
|--------|----------------|
| **`verify_exercise_checks_parity.py`** | Shared **`validators`** normalizers match independent reference implementations on thousands of random inputs; each batch’s **`_normalize_code`** is wired to the correct profile; one Batch 1 exact-check smoke test. |
| **`verify_project_smoke.py`** | **`app.PythonBasics`** imports and builds all batches; **`check(expected)`** succeeds for every exercise in **300** stochastic sessions per batch (plus Batch 1’s **full** flat pool); mixed batches (5, 8, 10) validate simple units and every compound **part**; session sizes match the documented constants. |
| **`verify_answer_behavior.py`** | Wrong answers are rejected; spacing variants that normalize the same as **`expected`** are accepted (where applicable); three-strike logic matches **`engine`**’s simple-exercise loop; scoring percentage uses the same **`completed / (completed + not_completed)`** formula as the printed stats; static pools are enumerated exhaustively where defined; batches 5 / 8 / 10 also deep-walk module globals for every compound line plus **400** extra stochastic rounds; **`engine._run_one_simple_exercise`** is exercised twice with mocked **`input`** on a Batch 1 item (three failures vs. wrong-then-right). |

Together they confirm graders, pools, and control-flow helpers behave consistently; they do **not** prove the full interactive menu experience for every batch without running **`main.py`** yourself.
