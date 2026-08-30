# Suite parity — learner interface standard

> **Authoritative reference** for the five Python practice games after **B009–B015** (plus post-B012 smoke fixes).  
> **Documentation only** — behavior changes require a separate brief.  
> **Hint wording (round 1)** locked in [B014](~/.cursor/skills/briefs/B014-2026-07-05-regular-suite-hint-wording.md) (PM-led iterative review). **Format/indent** for hints locked in B012. **Round 2** hint copy deferred until after [B016](~/.cursor/skills/briefs/B016-2026-08-07-regular-suite-intended-code-convergence.md) (intended code convergence).  
> **Architecture map (B015)** dated 2026-07-10 (suite Accept 2026-07-30) — see § Architecture below.

## Projects

| Short | Project | Launch |
|-------|---------|--------|
| **pybasics** | `python-basics` | `cd python-basics && python3 main.py` |
| **mpl** | `matplotlib-practice` | `cd matplotlib-practice && python3 main.py` |
| **scipy** | `scipy-practice` | `cd scipy-practice && python3 main.py` |
| **ppl** | `pandas-practice-lite` | `cd pandas-practice-lite && python3 main.py` |
| **puzzle** | `puzzle-rush-game` | `cd puzzle-rush-game && python3 main.py` |

## Cross-references

| Brief | Scope | Status |
|-------|-------|--------|
| [B009](~/.cursor/skills/briefs/B009-2026-06-16-regular-python-basics-learner-interface.md) | python-basics: skip/exit/empty, hints, teach, compound skip | done |
| [B010](~/.cursor/skills/briefs/B010-2026-06-18-regular-suite-learner-interface.md) | Suite strikes, scoring, footers, menu exit, scipy core pass | done (retro folded here) |
| [B011](~/.cursor/skills/briefs/B011-2026-06-23-regular-pandas-practice-lite-parity.md) | ppl full parity, Explore, fail-fast dataset | done |
| [B012](~/.cursor/skills/briefs/B012-2026-06-26-regular-suite-learner-interface-close-out.md) | Suite-wide UI close-out (17 feature rows) | done |
| [B013](~/.cursor/skills/briefs/B013-2026-06-27-regular-suite-documentation.md) | This document | done |
| [B014](~/.cursor/skills/briefs/B014-2026-07-05-regular-suite-hint-wording.md) | Suite hint wording — **round 1** (copy only; PM-led review) | done (round 1) |

---

# Part 1 — Parity checklist

Each table row is one locked standard. **Origin** = brief that introduced or finalized it. **Exceptions** call out deliberate per-game differences.

## 1. Main menu

| Element | Standard | pybasics | mpl | scipy | ppl | puzzle | Exceptions | Origin |
|---------|----------|----------|-----|-------|-----|--------|------------|--------|
| App title | TitleCase | Python Basics Practice | Matplotlib Practice | SciPy Practice | Pandas Practice | Puzzle Rush - NumPy Practice | — | B012 |
| Bar width | 70-char `=` | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Title → item 1 | No blank line | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Last item → closing bar | No blank line | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Closing bar → prompt | Bar directly above `Select an option…`; no blank line | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Exercise labels | TitleCase + capital `Exercise` | `Basic Topics Exercise` … (10) | `Line Plot Exercise` … (6) | `Constants Exercise` … (6) | `Basic Operations Exercise` … (5) | gamified names | **puzzle:** `Array Blitz`, `Vector Battle`, `Matrix Challenge`, `Ufunc Arena` (menu ≠ teach title). **mpl:** menu = teach title (B015; was menu `Series` / teach drop-Series until 2026-07-15) | B012/B015 |
| Extra menu options | — | — | — | — | `6. Explore Dataset` | — | ppl only | B011 |
| Exit option | `N. Exit (or type 'exit'/'Exit')` | 11 | 7 | 7 | 7 | 5 | — | B010 |
| Exit input | `exit` or `Exit` (case variants on prompt) | ✓ | ✓ | ✓ | ✓ | ✓ | — | B010 |
| Invalid choice | `❌ Invalid choice…` (non-empty junk only) | ✓ | ✓ | ✓ | ✓ | ✓ | — | B011 |
| Empty input | Silent re-prompt of `Select an option…` (no message, no blank line) | ✓ | ✓ | ✓ | ✓ | ✓ | — | B015 smoke |
| Farewell | `We'll talk later! 👋` then app ends | ✓ | ✓ | ✓ | ✓ | ✓ | — | B010 |
| Removed (ppl) | No Learning Statistics; no Run Exercise submenu; no `Loaded dataset:` banner | — | — | — | ✓ | — | ppl only | B011 |

## 2. Exercise / teach titles

**Suite style:** TitleCase words + capital singular `Exercise`. Short words (`and`, `or`) lowercase.

### pybasics (menu = teach title)

| # | Title |
|---|-------|
| 1 | Basic Topics Exercise |
| 2 | Strings and Booleans Exercise |
| 3 | Operators Exercise |
| 4 | Lists Exercise |
| 5 | Tuples Exercise |
| 6 | Sets Exercise |
| 7 | Dictionaries Exercise |
| 8 | Functions Exercise |
| 9 | Additional Topics Exercise |
| 10 | Advanced Topics Exercise |

### mpl (menu = teach title)

| # | Title |
|---|-------|
| 1 | Line Plot Exercise |
| 2 | Subplot Exercise |
| 3 | Scatter Plot Exercise |
| 4 | Bar Plot Exercise |
| 5 | Histogram Exercise |
| 6 | Pie Chart Exercise |

### scipy (menu = teach title)

Constants Exercise · Optimization Exercise · Sparse Matrices (CSR and CSC) Exercise · CSGraph (Graph Algorithms) Exercise · Spatial Data Exercise · Interpolation Exercise

### ppl (menu = teach title)

Basic Operations Exercise · Filtering Data Exercise · Sorting and Column Selection Exercise · Data Manipulation Exercise · Data Cleaning Exercise

### puzzle (menu ≠ teach title — gamified menu)

| Menu | Teach title |
|------|-------------|
| Array Blitz | Array Blitz - Array Exercise |
| Vector Battle | Vector Battle - Vector Exercise |
| Matrix Challenge | Matrix Challenge - Matrix Exercise |
| Ufunc Arena | Ufunc Arena - Ufunc Exercise |

| Element | Standard | Exceptions | Origin |
|---------|----------|------------|--------|
| Title bar | `====` 70-char bar, title, `====` bar | scipy: was `-` bars → `=` at B012 | B012 |
| Title → teach intro | No blank line after title bar | scipy: science block sits between title bar and teach intro (no blank line between title bar and science block) | B012 |
| mpl series banner → body | No blank line after closing `====` before `Create a…` | mpl only | B015 smoke |


## 3. Teach intro

**Ordering (default):** title bar → session line → teach rule → blank line → `Press Enter to start...` → tip → first question/step.

| Element | Standard | Exceptions | Origin |
|---------|----------|------------|--------|
| Session line | Per-game (see table below) | scipy: N = actual question count per exercise | B012 |
| Teach rule (code) | `After three wrong attempts, the answer for the question is shown, followed by the next question.` | mpl: `After three wrong attempts per step, the answer for the step is shown, followed by the next step.`; puzzle & pybasics batch 2: `…(one for True/False questions)…` + `answer for the question` | B009/B012 |
| Enter prompt | `Press Enter to start...` | — | B009 |
| Tip | `Tip: type 'skip' to skip a question, or 'exit'/'quit' to stop the exercise and return to the main menu.` | mpl: `…skip the current series…`; puzzle/mpl tip spacing (see §9) | B009/B012 |
| Session line → teach rule | No blank line between them | — | B012 |

### Session lines — pybasics (per batch)

| Batch | Session line |
|-------|--------------|
| 1, 3 | `You will get 12 single-line code questions.` |
| 2 | `You will get 12 single-line questions (7 code questions followed by 5 True/False questions).` |
| 4 | `You will get 12 single-line code questions on lists.` |
| 5 | `You will get 8 questions (12.5% each). Two ask for three lines; six ask for one.` |
| 6 | `You will get 12 single-line code questions on sets (topics vary per session).` |
| 7 | `You will get 12 single-line code questions on dictionaries (topics vary per session).` |
| 8 | `You will get 11 questions (~9.09% each). One has two lines; the rest ask for one.` |
| 9 | `You will get 12 single-line code questions.` |
| 10 | `You will get 19 questions (~5.26% each). Three are multi-line (24 lines total).` |

### Session lines — other games

| Game | Session line |
|------|--------------|
| mpl (each exercise) | `You will get 3 <type> series of code steps.` (e.g. `3 line-plot series…`) |
| scipy (per exercise) | `You will get N single-line code questions.` — N=5 (Constants, Optimization, Sparse, CSGraph, Spatial); N=4 (Interpolation) |
| ppl (all exercises) | `You will get 8 single-line code questions.` |
| puzzle (all games) | `You will get 20 single-line questions (15 code questions followed by 5 True/False questions).` |

### scipy science block (exception)

Per-exercise scientific detail prints **immediately after the title bar** (no blank line). One blank line separates the science block from the session line (`You will get N…`). Then teach rule → Enter → tip.

## 4. Question / step presentation

| Element | Standard | pybasics | mpl | scipy | ppl | puzzle | Exceptions | Origin |
|---------|----------|----------|-----|-------|-----|--------|------------|--------|
| Header shape | Two lines: `--- {Label} n/N ---` then text | `Question` | `Step` | `Question` | `Question` | `Question` | mpl uses `Step` | B012 |
| Text line | Question/step text on next line; **no trailing period** | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Header → text | No blank line between header and text | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Text → prompt | One blank line before first prompt | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Inter-question gap | `INTER_ITEM_GAP` = two newlines before next header (not first) | ✓ | ✓ | ✓ | ✓ | ✓ | — | B011 |
| Removed (ppl) | No `TASK`, no `Dataset:`, no upfront `💡` | — | — | — | ✓ | — | ppl only | B011 |

## 5. Strike flow

| Element | Standard | Exceptions | Origin |
|---------|----------|------------|--------|
| Indentation | **Column 0** for every strike-flow line (prompt, `✗`, `Try again…`, `Hint:`, `Correct answer:`, `Skipping…`, `✓`) | — | B012 |
| Max attempts | 3 per code question/line | T/F: **1** (pybasics batch 2, puzzle) | B009 |
| T/F accepted spellings | Exact `True` / `False` only | pybasics batch 2, puzzle (B015) | B009/B015 |
| Prompt label | `Your code (attempt n/3):` | T/F: `Your answer (attempt 1/1):` | B012 |
| Wrong ×1 | `✗ Incorrect answer (attempt 1/3).` then `Try again…` + blank line | T/F: `…(attempt 1/1).` | B009 |
| Wrong ×2 | `✗ Incorrect answer (attempt 2/3).` only (no hint) | — | B009 |
| Wrong ×3 | `Correct answer: <expected>` → next question (no `Try again…`) | — | B009 |
| Hint | Strike 1 only: `Hint: <text>`; blank line before next prompt | **Wording:** B014 round 1 (see §5.1). **No hint:** pybasics batches 1–3; scipy Constants; puzzle T/F wrong path. **Format/indent:** B012 | B009/B012/B014 |
| Empty re-prompt | Re-prompt same attempt; **no strike**; **no extra blank line** on re-prompt | — | B009/B012 |
| Correct | `✓ Correct!` only (no motivational extras) | — | B010 |
| mpl skip wording | — | `Skipping series.` (not `Skipping question.`) | B008 |

### Strike-1 spacing shape (4 games + puzzle)

```text
--- Question 1/8 ---
Display the first 10 rows

Your code (attempt 1/3): <wrong>
✗ Incorrect answer (attempt 1/3).
Try again...

Hint: <hint>

Your code (attempt 2/3):
```

### 5.1 Hint wording (B014 round 1)

**Closed 2026-07-05.** Round 1 was an **iterative, PM-led** pass over hint **strings in source** (not a single batch sign-off). The PM was an active partner: line-by-line review, live rejection of vague/API-leaking copy, and product calls (e.g. puzzle-rush T/F hints removed). **Round 2** deferred until a future **suite architecture unification** brief.

| Principle | Standard |
|-----------|----------|
| Terminology | Use **question**, not **prompt**, in hint copy |
| Style | Question-style nudges (`How do you…?` / `Which…?`); not lectures |
| No giveaways | No API/method names where avoidable; no echoing answer syntax/values |
| Phrasing | Prefer **shown in the question** over **the question describes** |
| Placement | One hint per generator when branches share a task; split when tasks differ |

| Project | Hint locations | Round 1 notes |
|---------|----------------|---------------|
| pybasics | `hints.py` batches **4–10** | Batches **1–3:** no hints |
| mpl | `exercise_common.py` `HINT_*` | Accepted as-is |
| scipy | `exercises.py` `Question(…, hint)` | Exercise **1:** empty hint |
| ppl | `hints.py` (`HINT_E*_…`; wired into exercise specs) | Question-style; no API names |
| puzzle | `hints.py` (`HINT_*`; wired in `games/*.py`) | Code hints; T/F `hint: ''` |

## 6. Input handling

| Input | Effect | All games | Exceptions | Origin |
|-------|--------|-----------|------------|--------|
| **Correct answer** | `✓ Correct!` → next question/step | ✓ | — | B010 |
| **Wrong answer** | Increment strike; see §5 | ✓ | T/F: 1 strike max | B009 |
| **`skip` / `Skip`** | `Skipping question.` → `Correct answer:` → next; counts **not completed** | ✓ | mpl: `Skipping series.` | B009 |
| **Compound skip (pybasics)** | Skip on any line → skip whole unit; reveal all line answers | pybasics only | — | B009 |
| **`exit`/`Exit`/`quit`/`Quit`** | Partial exit score → main menu; current question **not** completed; **no** answer shown | ✓ | Compound mid-unit: no credit for lines done inside | B009 |
| **Empty line** | Re-prompt; no strike | ✓ | — | B009 |
| **Case variants** | `Skip`, `Exit`, `Quit` accepted where listed | ✓ | — | B011 |

### Partial exit message (count-only, no percentages)

```text
⏹️  Session exited. Completed successfully: X · Not completed: Y (of Z questions)
# When Z is 1: … (of 1 question)  [not “questions”]
Returning to main menu...
```

| Game | Denominator label | Buckets |
|------|-------------------|---------|
| pybasics, scipy, ppl, puzzle | `questions` | 2: Completed successfully · Not completed |
| mpl | `series` | 3: Completed successfully · Completed with help · Not completed |

**mpl bucket rules (per series):** Completed successfully = all steps correct (no strike-3 reveal). Completed with help = finished all steps, ≥1 reveal, **and** ≥1 step correct. Not completed = skip, early exit, or finished with **0** correct steps (all revealed).

**Z** = questions/series **attempted** before exit (completed + not completed); unseen items not in denominator.

## 7. Session statistics footer

| Element | Standard | pybasics | mpl | scipy | ppl | puzzle | Exceptions | Origin |
|---------|----------|----------|-----|-------|-----|--------|------------|--------|
| Title | `Session Statistics` (title case) | ✓ | ✓ | ✓ | ✓ | ✓ | was `SESSION STATISTICS` | B012 |
| Bar width | 70-char `=` | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Buckets | See §6 | 2-bucket | 3-bucket | 2-bucket | 2-bucket | 2-bucket | mpl: `Completed with help` | B010/B012 |
| Percentages | Every bucket **except Total** shows `(pct%)` | ✓ | ✓ | ✓ | ✓ | ✓ | Partial exit: count-only | B012 |
| `.0` trim | `25.0%`→`25%`; `37.5%` unchanged | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |
| Total label | `Total questions:` | ✓ | — | ✓ | ✓ | ✓ | mpl: `Total series:` | B012 |
| Closing | `Returning to main menu...` + bar + **one trailing blank line** | ✓ | ✓ | ✓ | ✓ | ✓ | — | B012 |

### mpl 3-bucket footer example

```text
======================================================================
Session Statistics
======================================================================

Completed successfully: 2 (67%)
Completed with help: 0 (0%)
Not completed: 1 (33%)
Total series: 3

======================================================================
Returning to main menu...
======================================================================

```

## 8. Bar width

| Use | Width | Constant |
|-----|-------|----------|
| Main menus, exercise title bars, session footers, explore separators | **70** | `SESSION_BANNER_WIDTH = 70` per project |

## 9. Post-B012 smoke fixes

| Fix | Games | Detail | Origin |
|-----|-------|--------|--------|
| Main menu title | pybasics | `Python basics practice` → `Python Basics Practice` | B012 smoke |
| Batch 2 session line | pybasics | `…12 single-line questions (7 code questions followed by 5 True/False questions).` | B012 smoke |
| Title bar → item 1 | pybasics, mpl | Remove extra blank line | B012 smoke |
| Last item → closing bar | mpl | Remove extra blank line before prompt | B012 smoke |
| Title → science block | scipy | No blank line between title bar and first science line | B012 smoke |
| Tip spacing | mpl | One **fewer** blank line after tip (before first step) | B012 smoke |
| Tip spacing | puzzle | One **more** blank line after tip (before first question) | B012 smoke |
| Empty re-prompt | pybasics | No extra blank line on empty-input re-prompt | B012 smoke |
| Footer total label | pybasics, scipy, ppl, puzzle | `Total:` → `Total questions:` | B012 smoke |

## 10. Game-specific features (not suite-wide)

### ppl — dataset & Explore Dataset (B011)

| Feature | Standard |
|---------|----------|
| Dataset | Single file: `data/sales_data.csv` |
| Fail-fast | Missing/unreadable CSV → plain error, exit, **no menu** |
| Load error (missing) | `Could not load sales_data.csv. Check that data/sales_data.csv exists.` |
| Explore menu | Plain `DATASET EXPLORATION MENU`; options **1–8**; no emoji headers |
| Explore labels | Plain text (`First N rows:`, `Basic Statistics:`, etc.) |
| Column not found | `Column 'name' not found!` (no ❌) |
| ESC / repeat | Options **1–2, 6–8:** Enter to repeat, ESC to return. Options **3–5:** ESC only (no re-run) |
| Empty input | All Explore prompts: silent re-prompt (no message, no blank line). No blank defaults |
| Exit words | Within Explore prompts (1–2, 5–7): only `Exit`, `exit`, `Quit`, `quit` → exploration menu. Prompt text: `or type 'exit'/'quit' to return` |

### mpl — `plt.show()` steps (B008)

| Feature | Standard |
|---------|----------|
| Verification | String match only (`plt.show()`); code is **not** executed |
| Hint | None on these steps |
| Placement | Often the final step of a series |

### pybasics — compound questions (B009)

| Feature | Standard |
|---------|----------|
| Compound unit | Multiple lines = one scored question |
| Skip mid-compound | Reveal all line answers |
| Exit mid-compound | No credit for partial lines in that unit |

### Code answer normalization (ppl, mpl)

Insignificant whitespace ignored via `normalize_code()` — exact semantic match after normalization.

---

# Part 2 — Unified manual smoke procedure

Run **once per game** after automated QA is green. Track **Pass / Fail / Notes** per row.

**Spacing eyeball:** at each step, visually confirm blank-line counts (title→item 1, tip→first question, header→text, etc.). Automated QA cannot assert these.

## Step 1 — Entry / launch

| # | Action | Expected |
|---|--------|----------|
| 1.1 | Launch (see table above) | Main menu renders |
| 1.2 | ppl only | **No** `Loaded dataset:` banner |
| 1.3 | ppl only (optional) | Rename `data/sales_data.csv` → plain error, exit, no menu |

## Step 2 — Main menu

| # | Action | Expected |
|---|--------|----------|
| 2.1 | Glance at menu | TitleCase app title; 70-char bars; exercise labels per §1 |
| 2.2 | Spacing eyeball | No blank line between title bar and item 1; no blank line between last item and closing bar; closing bar directly above prompt |
| 2.3 | Invalid choice (`99`) | `❌ Invalid choice…` |
| 2.3b | Empty input (Enter) | Re-prompt `Select an option…` only — no message, no blank line |
| 2.4 | puzzle only | Gamified menu names (`Array Blitz`, …) — not teach titles |
| 2.5 | *(retired)* | mpl menu = teach title (B015); no Series vs teach mismatch |
| 2.6 | ppl only | Options 1–5 exercises, 6 Explore, 7 Exit; no Learning Statistics |

## Step 3 — Teach intro & exercise initiation

Pick **one exercise** per game (deep check); spot-check others.

| # | Action | Expected |
|---|--------|----------|
| 3.1 | Select exercise → **Enter** on intro | `====` bar → title → session line (per §3) → teach rule → Enter → tip |
| 3.2 | scipy only | Science block after title bar (no blank line after bar); blank line before session line |
| 3.3 | Spacing eyeball | No blank line between title bar and teach intro (except scipy science block); mpl: one blank line after tip; puzzle: two blank lines after tip |
| 3.4 | First question/step appears | Header `--- Question n/N ---` or `--- Step n/N ---` |

## Step 4 — Question presentation

| # | Action | Expected |
|---|--------|----------|
| 4.1 | Read first question | Text on line after header; **no trailing period** |
| 4.2 | Spacing eyeball | No blank line between header and text; one blank line before prompt |
| 4.3 | ppl only | No `TASK`, no `Dataset:`, no upfront `💡` |

## Step 5 — Per-strike behavior

On **one code question** (Q1 or Q2):

| # | Action | Expected |
|---|--------|----------|
| 5.1 | Wrong ×1 | `✗ Incorrect answer (attempt 1/3).` + `Try again…` + `Hint:` (where hints exist) |
| 5.2 | Wrong ×2 | `✗ Incorrect answer (attempt 2/3).` only |
| 5.3 | Wrong ×3 | `Correct answer: <…>` → next question |
| 5.4 | All lines col 0 | No leading spaces on any strike-flow line |

**T/F check** (puzzle any T/F question; pybasics batch 2):

| # | Action | Expected |
|---|--------|----------|
| 5.5 | T/F wrong ×1 | `Your answer (attempt 1/1):` → `Correct answer:` → next (no second attempt). **No `Hint:`** on puzzle T/F wrong path (B014). pybasics batch 2 T/F: also no hint on wrong |

## Step 6 — All input types

On **fresh questions** in the same exercise:

| # | Input | Expected |
|---|-------|----------|
| 6.1 | Empty line | Re-prompt; same attempt number; no extra blank line (pybasics) |
| 6.2 | `skip` | `Skipping question.` (mpl: `Skipping series.`) → `Correct answer:` → next |
| 6.3 | Correct code | `✓ Correct!` → next |
| 6.4 | `exit` or `Quit` | `⏹️ Session exited…` → main menu; current item not completed |
| 6.5 | Case variants | `Skip`, `Exit`, `Quit` accepted |

## Step 7 — Partial exit

| # | Action | Expected |
|---|--------|----------|
| 7.1 | Start exercise; answer 1–2 items; `exit` | Count-only partial message; correct bucket labels; `questions` or `series` denominator |
| 7.2 | mpl only | Three buckets in partial exit |

## Step 8 — Exercise completion

| # | Action | Expected |
|---|--------|----------|
| 8.1 | Finish or skip through all items | `Session Statistics` footer per §7 |
| 8.2 | Percentages | On every bucket except Total; `.0` trimmed |
| 8.3 | Return | Main menu; one trailing blank line after footer |

## Step 9 — Game-specific exceptions

### ppl — Explore Dataset (menu 6)

| # | Action | Expected |
|---|--------|----------|
| 9.1 | Open Explore | Plain `DATASET EXPLORATION MENU` |
| 9.2 | Head (explicit n, e.g. 5) | `First 5 rows:` + table; empty at row prompt re-prompts (no default) |
| 9.3 | Unique — bad column | `Column 'not_a_column' not found!` |
| 9.4 | Invalid option → **8** | Re-prompt; **8** → main menu |

### mpl

| # | Action | Expected |
|---|--------|----------|
| 9.5 | Finish a series with ≥1 strike-3 reveal and ≥1 correct | `Completed with help` increments |
| 9.5b | Finish a series with 0 corrects (all revealed) | Counts as **Not completed**, not with help |
| 9.6 | `plt.show()` step | Exact `plt.show()` → `✓ Correct!`; no strike-1 hint |

### scipy

| # | Action | Expected |
|---|--------|----------|
| 9.7 | Open second exercise | Science block present; session line N matches question count |

### puzzle

| # | Action | Expected |
|---|--------|----------|
| 9.8 | T/F question | `Your answer`; 1 attempt; wrong → `Correct answer:` only (**no hint**, B014) |
| 9.9 | Menu vs teach | Menu `Array Blitz` → teach `Array Blitz - Array Exercise` |

### pybasics batch 2

| # | Action | Expected |
|---|--------|----------|
| 9.10 | Batch 2 T/F section | `Your answer`; 1 attempt; session line mentions 7 code + 5 T/F |

## Step 10 — Exit

| # | Action | Expected |
|---|--------|----------|
| 10.1 | `Exit` or `exit` from main menu | `We'll talk later! 👋` → app ends |

---

## Fast path (~5 min per game)

If short on time: **1.1** → **2.1–2.3** → **3.1, 3.4** → **5.1–5.3** on one code question → **6.2–6.4** → **7.1** → **10.1**. Add game-specific rows from §9 as applicable.

> **When no code changed** (e.g. a docs-only brief like B013): the full dry-run is **redundant** if the suite was already smoke-tested at the prior code brief's acceptance. Verify by **desk-check** (Part 1 vs. what you already confirmed) instead of replaying gameplay.

## Sign-off

Say **"B013 accepted"** when desk-check (Part 1) passes. For docs-only briefs with no code changes, a dry-run (Part 2) is optional if the suite was already smoke-tested at the prior code brief.

**B014 (hint wording round 1):** PM desk-check of hint strings at locations in §5.1; automated QA for hint presence/T/F no-hint where applicable. Round 2 hint copy waits on [B016](~/.cursor/skills/briefs/B016-2026-08-07-regular-suite-intended-code-convergence.md) after intended code convergence.

**B015 (suite code architecture):** Dated **2026-07-10** (Phase 3 START); suite Accept 2026-07-30 — filename/role map across five projects. Follow-on code identity → B016.

---

# Architecture (B015)

> Structural roles after B015. Learner UX unchanged. **Intended code identity** (identical helper bodies + shared strike loop) → [B016](~/.cursor/skills/briefs/B016-2026-08-07-regular-suite-intended-code-convergence.md).

## Canonical roles (every project)

| Role | File | Notes |
|------|------|-------|
| Entry | `main.py` | Thin bootstrap |
| App shell | `app.py` | Menu / `run()` |
| Session UX | `session_common.py` | Skip/exit/empty, strikes, tip, footers |
| Runner | `engine.py` | Question / step / challenge loop |
| Hints authoring | `hints.py` | Hint strings |
| Validators | `validators.py` | Where applicable; **mpl** keeps `verify_fn` in content (approved) |

**Content-shape exceptions (intentional):** pybasics `batch_*_exercises.py`; mpl `exercises/*_exercises.py` (series/steps); puzzle `games/*.py`; scipy `exercises/` package; ppl Explore in `menus.py` (not session loop).

## Canonical release gates

| Project | Scripts (all must exit 0) |
|---------|---------------------------|
| **python-basics** | `verify_exercise_checks_parity.py`, `verify_project_smoke.py`, `verify_answer_behavior.py`, `verify_flow_b009.py` |
| **scipy-practice** | `python3 -m unittest discover -s tests -v`, `verify_smoke.py`, `generate_answers.py --check`, `verify_answer_behavior.py`, `verify_skip_exit_behavior.py`, `verify_flow_b010.py` |
| **matplotlib-practice** | `scripts/qa_regression_b001.py`, `scripts/qa_flow_b008.py` |
| **pandas-practice-lite** | `scripts/qa_regression_b002.py`, `scripts/qa_flow_b002.py`, `scripts/qa_menus_b002.py`, `verify_all_tasks.py` |
| **suite (B016 CORE identity)** | `python3 verify_suite_core_identity.py` (from `projects/`; required when all five cores aligned / B016 complete) |
| **puzzle-rush** | `verify_phase0_smoke.py`, `verify_answer_behavior.py` |
