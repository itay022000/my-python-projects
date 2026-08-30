# Archived tests (pandas-practice-lite)

## Canonical QA (active — run these)

From project root. All four must exit **0** (B011 gate; unchanged by B015 Phase 0 archive pass):

```bash
python3 scripts/qa_regression_b002.py
python3 scripts/qa_flow_b002.py
python3 scripts/qa_menus_b002.py
python3 verify_all_tasks.py
```

Optional structural check after module moves: `python3 scripts/verify_b003_method_map.py`

## Pre-B002 / pre-B011 legacy (archived)

Root-level `test_*.py` and `comprehensive_test.py` were the **pre-B002** subprocess QA surface. As of **B002**, canonical automated coverage moved to `scripts/qa_*_b002.py`. **B011** added `verify_all_tasks.py` as the fourth official gate.

Those legacy files targeted old menus, footers, and pre-B003 monolith layout. They are **not** release gates and many **fail** on the current program.

**Archived 2026-07-09** (B015 Phase 0, PM decision **#4b**): moved from project root into this folder. Do not delete without PM acknowledgment.

| File | Notes |
|------|--------|
| `test_all_tasks.py` | Subprocess pattern tests (first task per exercise) |
| `test_every_task.py` | Exhaustive subprocess case tests |
| `test_all_tasks_comprehensive.py` | Alternative comprehensive subprocess suite |
| `test_all_correct_answers.py` | Correct-answer subprocess checks |
| `test_verify_all_correct_answers.py` | Variant correct-answer verifier |
| `test_verify_correct_answers.py` | Variant correct-answer verifier |
| `test_correct_answers_all_datasets.py` | Historical name; sales-data era |
| `test_all_120_cases.py` | Large subprocess matrix |
| `test_simulation.py` | Early simulation harness |
| `comprehensive_test.py` | Full-program subprocess suite |

Stale root docs (`TEST_FILES_STATUS.md`, `HOW_TO_RUN_TESTS.md`, etc.) may still mention these paths — **ignore**; a future brief will unify suite-wide QA/test plans.
