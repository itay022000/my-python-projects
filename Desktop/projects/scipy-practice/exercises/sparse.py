"""SciPy exercise: sparse."""

import numpy as np
from scipy import sparse

from engine import Question
from exercise_session import run_exercise_questions
from hints import (
    HINT_SPARSE_ADD,
    HINT_SPARSE_CSC,
    HINT_SPARSE_CSR,
    HINT_SPARSE_NNZ,
    HINT_SPARSE_SHAPE,
)
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_sparse_practice():
    dense_matrix = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    csr_example = sparse.csr_matrix(dense_matrix)
    dense_matrix2 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

    namespace = {
        "sparse": sparse,
        "dense_matrix": dense_matrix,
        "csr_example": csr_example,
        "dense_matrix2": dense_matrix2,
        "np": np,
    }

    def check1(result):
        correct_matrix = sparse.csr_matrix(dense_matrix)
        if (
            hasattr(result, "shape")
            and result.shape == (3, 3)
            and result.nnz == 3
            and np.allclose(result.toarray(), correct_matrix.toarray())
        ):
            return True, f"Matrix has {result.nnz} non-zero elements"
        return False, "Expected: 3x3 CSR matrix with 3 non-zero elements"

    def check2(result):
        correct = csr_example.nnz
        if int(result) == correct:
            return True, f"Number of non-zero elements: {result}"
        return False, f"Expected {correct} non-zero elements"

    def check3(result):
        correct_matrix = csr_example.tocsc()
        if (
            hasattr(result, "shape")
            and result.shape == (3, 3)
            and result.nnz == 3
            and np.allclose(result.toarray(), correct_matrix.toarray())
        ):
            return True, "Successfully converted to CSC format"
        return False, "Expected: 3x3 CSC matrix with 3 non-zero elements"

    def check4(result):
        correct = csr_example.shape
        if result == correct:
            return True, f"Matrix shape: {result}"
        return False, f"Expected shape {correct}"

    def check5(result):
        csr1 = sparse.csr_matrix(dense_matrix)
        csr2 = sparse.csr_matrix(dense_matrix2)
        correct_matrix = csr1 + csr2
        if hasattr(result, "shape") and result.shape == (3, 3) and np.allclose(
            result.toarray(), correct_matrix.toarray()
        ):
            return True, "Matrices added successfully"
        return False, "Expected: sum of the two sparse matrices"

    questions = [
        Question(
            "Convert dense_matrix to a CSR sparse matrix",
            check1,
            HINT_SPARSE_CSR,
            correct_answer="sparse.csr_matrix(dense_matrix)",
        ),
        Question(
            "Get the number of non-zero elements in csr_example",
            check2,
            HINT_SPARSE_NNZ,
            correct_answer="csr_example.nnz",
        ),
        Question(
            "Convert csr_example to CSC format",
            check3,
            HINT_SPARSE_CSC,
            correct_answer="csr_example.tocsc()",
        ),
        Question(
            "Get the shape of csr_example",
            check4,
            HINT_SPARSE_SHAPE,
            correct_answer="csr_example.shape",
        ),
        Question(
            "Add sparse.csr_matrix(dense_matrix) and sparse.csr_matrix(dense_matrix2)",
            check5,
            HINT_SPARSE_ADD,
            correct_answer="sparse.csr_matrix(dense_matrix) + sparse.csr_matrix(dense_matrix2)",
        ),
    ]
    return namespace, questions




def exercise_sparse():
    """Practice with sparse matrices (CSR and CSC formats)."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Sparse Matrices (CSR and CSC) Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_sparse_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['sparse'],
    )

