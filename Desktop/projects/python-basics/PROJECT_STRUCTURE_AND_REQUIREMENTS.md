# Python Basics — Project Structure & Requirements

> Comment file: structure and demands for the Python basics teaching project.

---

## 1. Proposed structure (high level)

---

## 2. Content (topics to cover — adjust as needed)

**Exercise question rules (apply to all batches and new question types unless stated otherwise):**
- **Space normalization:** Apply to every question’s answer (no exceptions).
- **No overly explicit hints:** Do not name the exact function, keyword, or syntax the user must type (e.g. avoid “using complex(1, 2)” or “use end=” in the question text).

Topics to cover (list may change; exercise batches and structure to be defined later):

**Batch numbering (menu order):**  
- Batch 1: topics 1–4 (output, comments, variables, data types and casting)  
- Batch 2: topics 5–6 (strings, booleans)  
- Batch 3: topic 7 (operators)  
- Batch 4: topic 8 (lists)
- Batch 5: topic 9 (tuples)  
- Batch 6: topic 10 (sets)  
- Batch 7: topic 11 (dictionaries)  
- Batch 8: topic 12 (functions)  
- Batch 9: topics 13–16 (shorthand if, match, range, math)  
- Batch 10: topics 17–21 (arrays, dates, JSON, try… except, user input)  

All planned batches (1-10) are now implemented.

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
| **`verify_exercise_checks_parity.py`** | Shared **`exercise_checks`** normalizers match independent reference implementations on thousands of random inputs; each batch’s **`_normalize_code`** is wired to the correct profile; one Batch 1 exact-check smoke test. |
| **`verify_project_smoke.py`** | **`main.PythonBasics`** imports and builds all batches; **`check(expected)`** succeeds for every exercise in **300** stochastic sessions per batch (plus Batch 1’s **full** flat pool); mixed batches (5, 8, 10) validate simple units and every compound **part**; session sizes match the documented constants. |
| **`verify_answer_behavior.py`** | Wrong answers are rejected; spacing variants that normalize the same as **`expected`** are accepted (where applicable); three-strike logic matches **`session_runner`**’s simple-exercise loop; scoring percentage uses the same **`completed / (completed + not_completed)`** formula as the printed stats; static pools are enumerated exhaustively where defined; batches 5 / 8 / 10 also deep-walk module globals for every compound line plus **400** extra stochastic rounds; **`session_runner._run_one_simple_exercise`** is exercised twice with mocked **`input`** on a Batch 1 item (three failures vs. wrong-then-right). |

Together they confirm graders, pools, and control-flow helpers behave consistently; they do **not** prove the full interactive menu experience for every batch without running **`main.py`** yourself.