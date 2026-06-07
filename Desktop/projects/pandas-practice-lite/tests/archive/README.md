# Archived tests (B002)

Root-level `test_*.py`, `comprehensive_test.py`, and `verify_all_tasks.py` were the pre-B002 QA surface. As part of brief **B002**, canonical automated coverage moved to:

- `scripts/qa_regression_b002.py` — validator & helper regression (no subprocess)
- `scripts/qa_flow_b002.py` — per-task flow: correct, wrong, skip, exit (mocked input)

Those legacy files remain at the project root for reference until PM approves relocation or removal. Do not delete without PM acknowledgment.
