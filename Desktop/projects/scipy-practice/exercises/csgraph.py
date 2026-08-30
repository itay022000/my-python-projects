"""SciPy exercise: csgraph."""

import numpy as np
from scipy import sparse
from scipy.sparse import csgraph

from engine import Question
from exercise_session import run_exercise_questions
from hints import (
    HINT_CSGRAPH_COMPONENTS,
    HINT_CSGRAPH_CONNECTED,
    HINT_CSGRAPH_DIRECTED,
    HINT_CSGRAPH_SHORTEST,
    HINT_CSGRAPH_UNDIRECTED,
)
from session_common import EXERCISE_BACKGROUNDS, SESSION_BANNER_WIDTH

def _build_csgraph_practice():
    graph2 = np.array(
        [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )
    graph2_sparse = sparse.csr_matrix(graph2)

    chain_graph = np.array(
        [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
        ]
    )
    chain_sparse = sparse.csr_matrix(chain_graph)

    namespace = {
        "csgraph": csgraph,
        "chain_sparse": chain_sparse,
        "graph2_sparse": graph2_sparse,
        "sparse": sparse,
        "np": np,
    }

    def check1(result):
        correct = csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)
        if int(result) == correct:
            return True, f"Number of components: {result}"
        return False, f"Expected {correct} components"

    def check2(result):
        n_comp = csgraph.connected_components(chain_sparse, directed=False, return_labels=False)
        correct = n_comp == 1
        if bool(result) == correct:
            return True, f"Graph is {'connected' if correct else 'disconnected'}"
        return False, f"Expected {correct} (graph has {n_comp} component(s))"

    def check3(result):
        dist = csgraph.shortest_path(chain_sparse, directed=False)
        if np.allclose(result, dist):
            return True, "Distance matrix computed correctly"
        return False, "Expected the shortest path distance matrix"

    def check4(result):
        graph3 = np.array(
            [
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 0],
            ]
        )
        graph3_sparse = sparse.csr_matrix(graph3)
        dist = csgraph.shortest_path(graph3_sparse, directed=False)
        if np.allclose(result, dist):
            return True, "Distance matrix computed correctly"
        return False, "Expected the shortest path distance matrix"

    def check5(result):
        directed_graph = np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [0, 0, 0],
            ]
        )
        directed_sparse = sparse.csr_matrix(directed_graph)
        dist = csgraph.shortest_path(directed_sparse, directed=True)
        if np.allclose(result, dist):
            return True, "Distance matrix for directed graph computed"
        return False, "Expected the shortest path distance matrix"

    questions = [
        Question(
            "Find the number of connected components in graph2_sparse",
            check1,
            HINT_CSGRAPH_COMPONENTS,
            correct_answer="csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)",
        ),
        Question(
            "Check if chain_sparse is connected (has exactly 1 component)",
            check2,
            HINT_CSGRAPH_CONNECTED,
            correct_answer="csgraph.connected_components(chain_sparse, directed=False, return_labels=False) == 1",
        ),
        Question(
            "Find the shortest path distance matrix for chain_sparse",
            check3,
            HINT_CSGRAPH_SHORTEST,
            correct_answer="csgraph.shortest_path(chain_sparse, directed=False)",
        ),
        Question(
            "Find the shortest path distance matrix for a 3-node fully connected graph (use sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])))",
            check4,
            HINT_CSGRAPH_UNDIRECTED,
            correct_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])), directed=False)",
        ),
        Question(
            "Find the shortest path distance matrix for a directed graph (use sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]]))) with directed=True",
            check5,
            HINT_CSGRAPH_DIRECTED,
            correct_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]])), directed=True)",
        ),
    ]
    return namespace, questions




def exercise_csgraph():
    """Practice with scipy.sparse.csgraph algorithms."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("CSGraph (Graph Algorithms) Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    namespace, questions = _build_csgraph_practice()
    run_exercise_questions(
        namespace,
        questions,
        background=EXERCISE_BACKGROUNDS['csgraph'],
    )

