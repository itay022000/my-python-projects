"""
Grading behavior verification for scipy-practice.

For each exercise module, every practice question is checked with:
  - reference answer(s) that must pass check_func(eval(...))
  - wrong answer(s) that must fail (eval error or check_func returns False)

Run from this directory:
  python3 verify_answer_behavior.py
"""

from __future__ import annotations

from exercises import PRACTICE_BUILDERS


# Extra accepted forms beyond reference_answer (constants commutativity).
CONSTANTS_CORRECT_ALTERNATES: dict[int, list[str]] = {
    0: ["const.inch * 12"],
    1: ["const.mile * 5"],
    2: ["const.foot * 10"],
    3: ["const.minute * 3"],
    4: ["const.hour * 2"],
}

# Wrong submissions per (exercise_id, question_index).
WRONG_ANSWERS: dict[str, list[list[str]]] = {
    "constants": [
        ["1 + 1", "12 * const.mile"],
        ["0", "5 * const.foot"],
        ["1", "10 * const.inch"],
        ["999", "3 * const.hour"],
        ["1", "2 * const.minute"],
    ],
    "optimize": [
        ["0.0", "42"],
        ["1.0", "optimize.root(linear, x0=0.0).x[0]"],
        ["0.0", "3.0"],
        ["-1.0", "optimize.minimize(g, x0=0.0).fun"],
        ["0.0", "99"],
    ],
    "sparse": [
        ["0", "np.zeros((3, 3))"],
        ["999", "2"],
        ["1", "csr_example.toarray()"],
        ["(1, 1)", "csr_example.nnz"],
        ["csr_example", "dense_matrix"],
    ],
    "csgraph": [
        ["0", "99"],
        ["False", "True == False"],
        ["np.zeros((2, 2))", "chain_sparse"],
        ["0", "np.eye(3)"],
        ["np.eye(3)", "chain_sparse"],
    ],
    "spatial": [
        ["0", "1 + 1"],
        ["1", "distance.euclidean(p3, p4)"],
        ["0", "distance.cityblock(p1, p2)"],
        ["np.array([0])", "points_array[0]"],
        ["0", "distance.euclidean(p7, p8)"],
    ],
    "interpolate": [
        ["1 + 1", "lambda x: x"],
        ["1 + 1", "interpolate.interp1d(x_points2, y_points2, kind='linear')"],
        ["1 + 1", "interpolate.interp1d(x_points2, y_points2, kind='linear')"],
        ["1 + 1", "interpolate.interp1d(x_points, y_points, kind='linear')"],
    ],
}


def _eval_and_check(user_code: str, namespace: dict, check) -> tuple[bool, str]:
    result = eval(user_code, namespace)
    ok, msg = check(result)
    return ok, msg


def _assert_correct(exercise_id: str, qi: int, code: str, namespace: dict, check) -> None:
    label = f"{exercise_id} Q{qi + 1}"
    try:
        ok, msg = _eval_and_check(code, namespace, check)
    except Exception as exc:
        raise AssertionError(f"{label}: correct code {code!r} raised {exc}") from exc
    if not ok:
        raise AssertionError(f"{label}: correct code {code!r} rejected: {msg!r}")


def _assert_wrong(exercise_id: str, qi: int, code: str, namespace: dict, check) -> None:
    label = f"{exercise_id} Q{qi + 1}"
    try:
        ok, _msg = _eval_and_check(code, namespace, check)
    except Exception:
        return
    if ok:
        raise AssertionError(f"{label}: wrong code {code!r} was accepted")


def main() -> None:
    total_questions = 0
    order = ["constants", "optimize", "sparse", "csgraph", "spatial", "interpolate"]

    for exercise_id in order:
        build = PRACTICE_BUILDERS[exercise_id]
        namespace, questions = build()
        wrong_lists = WRONG_ANSWERS[exercise_id]
        assert len(wrong_lists) == len(questions), (
            f"{exercise_id}: wrong-answer table size mismatch"
        )

        for qi, question in enumerate(questions):
            total_questions += 1
            ref = question.reference_answer
            assert ref, f"{exercise_id} Q{qi + 1}: missing reference_answer"

            codes = [ref]
            if exercise_id == "constants":
                codes.extend(CONSTANTS_CORRECT_ALTERNATES.get(qi, []))

            for code in codes:
                _assert_correct(exercise_id, qi, code, namespace, question.check)

            for code in wrong_lists[qi]:
                _assert_wrong(exercise_id, qi, code, namespace, question.check)

    print(
        f"verify_answer_behavior: OK ({total_questions} questions × correct/wrong checks, "
        f"constants alternates included)."
    )


if __name__ == "__main__":
    main()
