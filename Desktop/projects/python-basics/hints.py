"""
Strike-1 hint resolution for python-basics (B009 hybrid templates).
Batches 1–3: no hints (PM B014). Batches 4–10: enabled. Exercises may set hint or hint_category to override.

Hint wording is grouped by batch (4–10) for B014 review.
"""

from __future__ import annotations

# batch number -> whether strike-1 hints are enabled
BATCH_HINTS_ENABLED: dict[int, bool] = {
    1: False,
    2: False,
    3: False,
    4: True,
    5: True,
    6: True,
    7: True,
    8: True,
    9: True,
    10: True,
}

# ---------------------------------------------------------------------------
# Batch 4 — Lists
# ---------------------------------------------------------------------------

HINT_LIST_INDEX = "Pick one element from the list by position."
HINT_LIST_SLICE = "Take a slice of the list between the indices given."
HINT_LIST_ASSIGN = "Change one position in the list copy."
HINT_LIST_APPEND = "Add a single item at the end of the list."
HINT_LIST_EXTEND = "Merge another sequence into the list in one step."
HINT_LIST_INSERT = "Place a new item at the index named in the question."
HINT_LIST_REMOVE = "Drop a specific value from the list in place."
HINT_LIST_POP = "Remove whatever the list gives you and keep it."
HINT_LIST_CLEAR = "Empty the list without replacing the variable."
HINT_LIST_DEL = "Drop the variable name entirely."
HINT_LIST_SORT = "Reorder the list in place using the criteria in the question."
HINT_LIST_COPY = "Make a separate list with the same items."
HINT_LIST_JOIN = "Join the lists into one new list."
HINT_LIST_COMP = "Build a new list from the expression inside the brackets."

# ---------------------------------------------------------------------------
# Batch 5 — Tuples
# ---------------------------------------------------------------------------

HINT_TUPLE_TO_LIST = "You need a mutable copy before changing anything."
HINT_LIST_TO_TUPLE = "Turn the updated copy back into an immutable sequence."
HINT_TUPLE_NEW_VS_INPLACE = "Check whether you need a new name or to change a in place."
HINT_B5_STARRED = "Capture the middle or rest using a starred name."
HINT_B5_REPEAT = "Repeat the tuple the number of times given."
HINT_B5_TUPLE_CONCAT = "Combine the tuple values into one."
HINT_B5_TUPLE_SLICE = "Use a slice between the indices in the question."
# Inference also returns HINT_LIST_INDEX, HINT_LIST_ASSIGN (batch 4).

# ---------------------------------------------------------------------------
# Batch 6 — Sets
# ---------------------------------------------------------------------------

HINT_SET_MEMBERSHIP = "Store the yes-or-no result of the membership check."
HINT_SET_ADD = "One new element, changed on the set itself."
HINT_SET_UPDATE = "Merge everything from the other set in a single step."
HINT_SET_REMOVE = "Remove a value you name."
HINT_SET_POP = "Remove whatever the set gives you and keep it."
HINT_SET_CLEAR = "Empty the set in place."
HINT_SET_DEL = "Drop the variable name entirely."
HINT_SET_UNION_MANY = "More than two sets can be combined in one call."
HINT_SET_FROZEN = "Build a version that cannot be changed later."
# Inference also returns HINT_TUPLE_NEW_VS_INPLACE (batch 5).

# ---------------------------------------------------------------------------
# Batch 7 — Dictionaries
# ---------------------------------------------------------------------------

HINT_DICT_LOOKUP = "Look up the key named in the question."
HINT_DICT_GET = "The question asks for the safer lookup style."
HINT_DICT_VIEW = "The question tells you which view of the dictionary to store."
HINT_DICT_ASSIGN = "Bracket assignment."
HINT_DICT_UPDATE = "One merge-style call with a small dictionary literal."
HINT_DICT_POP_KEY = "Remove by key."
HINT_DICT_POPITEM = "Remove whatever was inserted last."
HINT_DICT_CLEAR = "Empty the dictionary in place."
HINT_DICT_DEL = "Drop the variable name entirely."
HINT_DICT_COPY_METHOD = "Instance method."
HINT_DICT_COPY_CTOR = "Constructor form — the question says which."

# ---------------------------------------------------------------------------
# Batch 8 — Functions
# ---------------------------------------------------------------------------

HINT_B8_DEF_NAMES = "Spell the function and parameter names exactly as in the question."
HINT_B8_DEF_TWO_PRINT = "Both parameters should show up in what gets printed."
HINT_B8_KWARGS_REVERSED = (
    "Lead with the parameter that comes second in the function header."
)
HINT_B8_POS_KW_CALL = "One argument is plain; the other is named when you pass it."
HINT_B8_POS_ONLY = (
    "Something in the parameter list limits how callers may pass arguments."
)
HINT_B8_KW_ONLY = "The opening of the parameter list is not a normal parameter name."
HINT_B8_MIX_PARAMS = "The parameter list has two special separators, not just commas."
HINT_B8_STAR_ARGS = "Extras are bundled into one tuple parameter."
HINT_B8_STAR_ARGS_REG = "One fixed parameter, then a bundle for the rest."
HINT_B8_STAR_KWARGS = "Named arguments at call time are gathered into one mapping."
HINT_B8_STAR_KWARGS_REG = "One regular parameter, then a mapping for the named extras."
HINT_B8_COMBO = "Three pieces to print: one value, a tuple, and a mapping."
HINT_B8_DECORATOR_DEF = "Whatever you receive, send back unchanged."
HINT_B8_DECORATOR_APPLY = "One short line ties the decorator to the function below it."
HINT_B8_LAMBDA = "One line; the question tells you what to compute from a and b."

# ---------------------------------------------------------------------------
# Batch 9 — Additional topics
# ---------------------------------------------------------------------------

HINT_B9_IF_ONE = "When the flag is true, write the assignment right after the condition."
HINT_B9_IF_ELSE = (
    "Two expressions in the question — the comparison picks which one to store."
)
HINT_B9_IF_CHAIN = "More than one fallback appears in the question."
HINT_B9_MATCH_CASES = "Several values can share one case line."
HINT_B9_MATCH_DEFAULT = "The default case uses a single catch-all pattern."
HINT_B9_RANGE_TWO = "Use both integers from the question, in order."
HINT_B9_RANGE_ONE = "Only one integer appears in the question."
HINT_B9_RANGE_THREE = "Use three integers from the question."
HINT_B9_MINMAX = "Every number in the question goes inside the parentheses."
HINT_B9_ABS = "One value inside the parentheses."
HINT_B9_POW = "Two values from the question."

# ---------------------------------------------------------------------------
# Batch 10 — Advanced topics
# ---------------------------------------------------------------------------

HINT_B10_ARRAY_INDEX = "Pick one element from the array by position."
HINT_B10_ARRAY_ASSIGN = "Change one position in the array."
HINT_B10_ARRAY_LEN = "Store how many items the array holds."
HINT_B10_ARRAY_APPEND = "Add a single item at the end of the array."
HINT_B10_ARRAY_POP = "Remove the last item and keep what you removed."
HINT_B10_ARRAY_REMOVE = "Drop a specific value from the array in place."
HINT_B10_DATETIME_NOW = "Get the current moment from the datetime class."
HINT_B10_DATETIME_PART = "Read one part of the current moment — the question names which."
HINT_B10_DATETIME_CREATE = "Build a date-time from the year, month, and day in the question."
HINT_B10_STRFTIME = "Use formatting on d to produce the text the question describes."
HINT_B10_JSON_LOADS = "Parse the JSON text into a Python object."
HINT_B10_JSON_DUMPS = "Serialize the object to a JSON string."
HINT_B10_JSON_INDENT = "Include the indentation count from the question."
HINT_B10_JSON_SORT = "Formatted JSON with keys sorted — both options appear in the question."
HINT_B10_TRY = "Start with the block that runs the code that might fail."
HINT_B10_EXCEPT_BROAD = "A catch-all branch with no error type named."
HINT_B10_EXCEPT_TYPED = "Name the error type from the question."
HINT_B10_ELSE = "This block runs only when the try finished without raising."
HINT_B10_FINALLY = "This block always runs after try and any except."
HINT_B10_RAISE = "Construct the exception type and message from the question."
HINT_B10_INPUT = "The question asks for input with nothing shown to the user first."
HINT_B10_INPUT_PROMPT = "The question gives you the text the user should see first."


def resolve_hint(batch: int, exercise: dict) -> str | None:
    if not BATCH_HINTS_ENABLED.get(batch, False):
        return None
    if exercise.get("hint") is not None:
        return exercise["hint"]
    category = exercise.get("hint_category")
    if category:
        return _hint_from_category(category)
    return _infer_hint(batch, exercise)


def _hint_from_category(category: str) -> str | None:
    return globals().get(f"HINT_{category.upper()}") or _CATEGORY_MAP.get(category)


_CATEGORY_MAP: dict[str, str] = {
    "list_index": HINT_LIST_INDEX,
    "list_slice": HINT_LIST_SLICE,
    "list_assign": HINT_LIST_ASSIGN,
    "list_append": HINT_LIST_APPEND,
    "tuple_to_list": HINT_TUPLE_TO_LIST,
    "list_to_tuple": HINT_LIST_TO_TUPLE,
    "tuple_new_vs_inplace": HINT_TUPLE_NEW_VS_INPLACE,
    "set_membership": HINT_SET_MEMBERSHIP,
    "set_add": HINT_SET_ADD,
    "set_update": HINT_SET_UPDATE,
    "set_remove": HINT_SET_REMOVE,
    "set_pop": HINT_SET_POP,
    "set_clear": HINT_SET_CLEAR,
    "set_del": HINT_SET_DEL,
    "set_union_many": HINT_SET_UNION_MANY,
    "set_frozen": HINT_SET_FROZEN,
    "dict_lookup": HINT_DICT_LOOKUP,
    "dict_get": HINT_DICT_GET,
    "dict_view": HINT_DICT_VIEW,
    "dict_assign": HINT_DICT_ASSIGN,
    "dict_update": HINT_DICT_UPDATE,
    "dict_pop_key": HINT_DICT_POP_KEY,
    "dict_popitem": HINT_DICT_POPITEM,
    "dict_clear": HINT_DICT_CLEAR,
    "dict_del": HINT_DICT_DEL,
    "dict_copy_method": HINT_DICT_COPY_METHOD,
    "dict_copy_ctor": HINT_DICT_COPY_CTOR,
    "b10_try": HINT_B10_TRY,
    "b10_except_broad": HINT_B10_EXCEPT_BROAD,
    "b10_except_typed": HINT_B10_EXCEPT_TYPED,
    "b10_else": HINT_B10_ELSE,
    "b10_finally": HINT_B10_FINALLY,
}


def _infer_hint(batch: int, exercise: dict) -> str | None:
    q = exercise.get("question", "")
    e = exercise.get("expected", "")
    ql = q.lower()

    if batch == 4:
        return _infer_batch4(q, e, ql)
    if batch == 5:
        return _infer_batch5(q, e, ql)
    if batch == 6:
        return _infer_batch6(q, e, ql)
    if batch == 7:
        return _infer_batch7(q, e, ql)
    if batch == 8:
        return _infer_batch8(q, e, ql)
    if batch == 9:
        return _infer_batch9(q, e, ql)
    if batch == 10:
        return _infer_batch10(q, e, ql)
    return None


def _infer_batch4(q: str, e: str, ql: str) -> str | None:
    if ".append(" in e:
        return HINT_LIST_APPEND
    if ".extend(" in e:
        return HINT_LIST_EXTEND
    if ".insert(" in e:
        return HINT_LIST_INSERT
    if ".remove(" in e:
        return HINT_LIST_REMOVE
    if ".pop(" in e:
        return HINT_LIST_POP
    if ".clear(" in e:
        return HINT_LIST_CLEAR
    if ql.startswith("suppose") and "del " in e:
        return HINT_LIST_DEL
    if ".sort(" in e:
        return HINT_LIST_SORT
    if ".copy(" in e or "list(" in e and "for" not in e:
        return HINT_LIST_COPY
    if " + " in e and "[" in e:
        return HINT_LIST_JOIN
    if e.strip().startswith("[") and "for" in e:
        return HINT_LIST_COMP
    if ":" in e and "[" in e and "=" in e:
        return HINT_LIST_SLICE
    if "[" in e and "=" in e and "]" in e.split("=")[0]:
        return HINT_LIST_ASSIGN
    if "[" in e and "=" in e:
        return HINT_LIST_INDEX
    return HINT_LIST_INDEX


def _infer_batch5(q: str, e: str, ql: str) -> str | None:
    if "list copy" in ql or e.strip().startswith("lst = list("):
        return HINT_TUPLE_TO_LIST
    if e.strip().startswith("t = tuple("):
        return HINT_LIST_TO_TUPLE
    if "lst[" in e and "=" in e:
        return HINT_LIST_ASSIGN
    if "new tuple" in ql or "new set" in ql or "Store in " in q and ".update(" not in e:
        if "update(" in e:
            return HINT_TUPLE_NEW_VS_INPLACE
    if ".update(" in e or ".intersection_update" in e or ".difference_update" in e:
        return HINT_TUPLE_NEW_VS_INPLACE
    if "starred" in ql or "*mid" in e or "*rest" in e:
        return HINT_B5_STARRED
    if ", " in e and "=" in e and "t" in e and "[" not in e:
        return HINT_B5_TUPLE_CONCAT
    if "* " in e or e.strip().endswith("* 3") or e.strip().endswith("* 4"):
        return HINT_B5_REPEAT
    if "[" in e and ":" in e:
        return HINT_B5_TUPLE_SLICE
    if "t[" in e and "=" in e and "lst" not in e:
        return HINT_LIST_INDEX
    return HINT_TUPLE_NEW_VS_INPLACE


def _infer_batch6(q: str, e: str, ql: str) -> str | None:
    if " in s" in e or "not in s" in e:
        return HINT_SET_MEMBERSHIP
    if ".add(" in e:
        return HINT_SET_ADD
    if ".update(" in e:
        return HINT_SET_UPDATE
    if ".remove(" in e:
        return HINT_SET_REMOVE
    if ".pop(" in e:
        return HINT_SET_POP
    if ".clear(" in e:
        return HINT_SET_CLEAR
    if e.strip().startswith("del "):
        return HINT_SET_DEL
    if "frozenset" in e:
        return HINT_SET_FROZEN
    if ".union(" in e and e.count(",") >= 2:
        return HINT_SET_UNION_MANY
    if any(x in e for x in (".union(", ".intersection(", ".difference(", ".symmetric_difference(")):
        return HINT_TUPLE_NEW_VS_INPLACE
    if "_update(" in e:
        return HINT_TUPLE_NEW_VS_INPLACE
    return HINT_SET_MEMBERSHIP


def _infer_batch7(q: str, e: str, ql: str) -> str | None:
    if ".get(" in e:
        return HINT_DICT_GET
    if ".keys()" in e or ".values()" in e or ".items()" in e:
        return HINT_DICT_VIEW
    if ".update(" in e:
        return HINT_DICT_UPDATE
    if ".pop(" in e and "(" in e and '"' in e:
        return HINT_DICT_POP_KEY
    if ".popitem()" in e:
        return HINT_DICT_POPITEM
    if ".clear(" in e:
        return HINT_DICT_CLEAR
    if e.strip().startswith("del d"):
        return HINT_DICT_DEL
    if ".copy()" in e:
        return HINT_DICT_COPY_METHOD
    if e.strip().startswith("d2 = dict(") or "clone = dict(" in e:
        return HINT_DICT_COPY_CTOR
    if '["' in e or "['" in e:
        if "=" in e.split("[", 1)[1]:
            return HINT_DICT_ASSIGN
        return HINT_DICT_LOOKUP
    return HINT_DICT_LOOKUP


def _infer_batch8(q: str, e: str, ql: str) -> str | None:
    if "lambda" in ql:
        return HINT_B8_LAMBDA
    if ql.startswith("step 2:") and "decorator line" in ql:
        return HINT_B8_DECORATOR_APPLY
    if "defines decorator" in ql:
        return HINT_B8_DECORATOR_DEF
    if "reversed order" in ql:
        return HINT_B8_KWARGS_REVERSED
    if "as positional and" in ql and "as keyword" in ql:
        return HINT_B8_POS_KW_CALL
    if "positional-only" in ql and "keyword-only" in ql:
        return HINT_B8_MIX_PARAMS
    if "positional-only" in ql:
        return HINT_B8_POS_ONLY
    if "keyword-only" in ql:
        return HINT_B8_KW_ONLY
    if "**kwargs" in ql:
        if "regular parameter" in ql and "keyword arguments" in ql:
            return HINT_B8_STAR_KWARGS_REG
        return HINT_B8_STAR_KWARGS
    if "*args" in ql and "keyword" in ql:
        return HINT_B8_COMBO
    if "extra positional" in ql or ("*args" in e and "**" not in e):
        if "regular parameter" in ql or "plus any extra" in ql:
            return HINT_B8_STAR_ARGS_REG
        return HINT_B8_STAR_ARGS
    if "defines the function" in ql:
        if "parameters a and b" in ql or "parameters x and y" in ql:
            return HINT_B8_DEF_TWO_PRINT
        return HINT_B8_DEF_NAMES
    return HINT_B8_DEF_NAMES


def _infer_batch9(q: str, e: str, ql: str) -> str | None:
    if ("case line" in ql and "default" in ql) or ql.startswith(
        "write the case line that acts"
    ):
        return HINT_B9_MATCH_DEFAULT
    if "case line" in ql:
        return HINT_B9_MATCH_CASES
    if "when x is true" in ql or "when flag is true" in ql:
        return HINT_B9_IF_ONE
    if "larger" in ql or "smaller" in ql:
        return HINT_B9_IF_ELSE
    if "else 2 when" in ql or "else b when" in ql:
        return HINT_B9_IF_CHAIN
    if "range" in ql:
        if e.count(",") >= 2:
            return HINT_B9_RANGE_THREE
        if e.count(",") == 1:
            return HINT_B9_RANGE_TWO
        return HINT_B9_RANGE_ONE
    if "smallest" in ql or "minimum" in ql or "largest" in ql or "maximum" in ql:
        return HINT_B9_MINMAX
    if "absolute" in ql:
        return HINT_B9_ABS
    if "power" in ql:
        return HINT_B9_POW
    return None


def _infer_batch10(q: str, e: str, ql: str) -> str | None:
    est = e.strip()

    if ql.startswith("step 1:") and "try" in ql:
        return HINT_B10_TRY
    if ql.startswith("step 3:") and "else" in ql:
        return HINT_B10_ELSE
    if ql.startswith("step 3:") and "finally" in ql:
        return HINT_B10_FINALLY
    if ql.startswith("step 2:") and "broad except" in ql:
        return HINT_B10_EXCEPT_BROAD
    if "catch " in ql and ql.startswith("step "):
        return HINT_B10_EXCEPT_TYPED
    if est.startswith("try:"):
        return HINT_B10_TRY
    if est.startswith("except:"):
        return HINT_B10_EXCEPT_BROAD
    if est.startswith("except "):
        return HINT_B10_EXCEPT_TYPED
    if est.startswith("else:"):
        return HINT_B10_ELSE
    if est.startswith("finally:"):
        return HINT_B10_FINALLY

    if ql.startswith("raise "):
        return HINT_B10_RAISE

    if "without a prompt" in ql:
        return HINT_B10_INPUT
    if "with the prompt" in ql:
        return HINT_B10_INPUT_PROMPT

    if "json.loads" in e:
        return HINT_B10_JSON_LOADS
    if "sort_keys" in e:
        return HINT_B10_JSON_SORT
    if "json.dumps" in e and "indent" in e:
        return HINT_B10_JSON_INDENT
    if "json.dumps" in e:
        return HINT_B10_JSON_DUMPS

    if "strftime" in e:
        return HINT_B10_STRFTIME
    if "datetime.datetime(" in e:
        return HINT_B10_DATETIME_CREATE
    if ".year" in e or ".month" in e or ".day" in e:
        return HINT_B10_DATETIME_PART
    if "datetime.datetime.now()" in e:
        return HINT_B10_DATETIME_NOW

    if ".append(" in e:
        return HINT_B10_ARRAY_APPEND
    if ".remove(" in e:
        return HINT_B10_ARRAY_REMOVE
    if ".pop(" in e:
        return HINT_B10_ARRAY_POP
    if "len(arr)" in e:
        return HINT_B10_ARRAY_LEN
    if "arr[" in e and "=" in e.split("arr", 1)[1]:
        return HINT_B10_ARRAY_ASSIGN
    if "arr[" in e:
        return HINT_B10_ARRAY_INDEX

    return None
