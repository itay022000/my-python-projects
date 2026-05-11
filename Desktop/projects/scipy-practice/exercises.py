"""SciPy exercise sessions: constants, optimize, sparse, csgraph, spatial, interpolate."""

import numpy as np
import scipy.constants as const
from scipy import interpolate, optimize, sparse
from scipy.sparse import csgraph
from scipy.spatial import distance

from engine import Question, run_exercise_questions


def exercise_constants():
    """Practice with scipy.constants."""
    print("\n" + "-" * 60)
    print("Exercise: SciPy Constants")
    print("-" * 60)

    print("\n1. Metric constants:")
    print(f"   Speed of light: {const.c} m/s")
    print(f"   Gravitational constant: {const.G} m³/(kg·s²)")
    print(f"   Planck constant: {const.h} J·s")

    print("\n2. Binary prefixes:")
    print(f"   kilo: {const.kilo}")
    print(f"   mega: {const.mega}")
    print(f"   giga: {const.giga}")

    print("\n3. Length conversions:")
    print(f"   inch to meter: {const.inch} m")
    print(f"   foot to meter: {const.foot} m")
    print(f"   mile to meter: {const.mile} m")

    print("\n4. Time conversions:")
    print(f"   minute to second: {const.minute} s")
    print(f"   hour to second: {const.hour} s")
    print(f"   day to second: {const.day} s")

    print("\nNote: For all questions, both '(number) * (constant)' and '(constant) * (number)' are accepted.")

    namespace = {"const": const, "np": np}

    def check1(result):
        correct = 12 * const.inch
        if abs(float(result) - correct) < 0.01:
            return True, f"12 inches = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check2(result):
        correct = 5 * const.mile
        if abs(float(result) - correct) < 0.01:
            return True, f"5 miles = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check3(result):
        correct = 10 * const.foot
        if abs(float(result) - correct) < 0.01:
            return True, f"10 feet = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"

    def check4(result):
        correct = 3 * const.minute
        if abs(float(result) - correct) < 0.01:
            return True, f"3 minutes = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"

    def check5(result):
        correct = 2 * const.hour
        if abs(float(result) - correct) < 0.01:
            return True, f"2 hours = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"

    run_exercise_questions(
        namespace,
        [
            Question(
                "Convert 12 inches to meters",
                check1,
                "What constant converts inches to meters?",
                reference_answer="12 * const.inch",
            ),
            Question(
                "Convert 5 miles to meters",
                check2,
                "What constant converts miles to meters?",
                reference_answer="5 * const.mile",
            ),
            Question(
                "Convert 10 feet to meters",
                check3,
                "What constant converts feet to meters?",
                reference_answer="10 * const.foot",
            ),
            Question(
                "Convert 3 minutes to seconds",
                check4,
                "What constant converts minutes to seconds?",
                reference_answer="3 * const.minute",
            ),
            Question(
                "Convert 2 hours to seconds",
                check5,
                "What constant converts hours to seconds?",
                reference_answer="2 * const.hour",
            ),
        ],
    )

def exercise_optimize():
    """Practice with scipy.optimize - root finding and minimization."""
    print("\n" + "-" * 60)
    print("Exercise: SciPy Optimization")
    print("-" * 60)

    print("\n1. Root Finding:")
    print("   Finding root of f(x) = x² - 4")

    def f(x):
        return x**2 - 4

    root_result = optimize.root(f, x0=1.0)
    print(f"   Root found: x = {root_result.x[0]:.6f}")
    print(f"   Function value at root: {f(root_result.x[0]):.2e}")

    root_result2 = optimize.root(f, x0=-3.0)
    print(f"   Another root found: x = {root_result2.x[0]:.6f}")

    print("\n2. Minimization:")
    print("   Finding minimum of f(x) = x² + 2x + 1")

    def g(x):
        return x**2 + 2 * x + 1

    minimize_result = optimize.minimize(g, x0=0.0)
    print(f"   Minimum at: x = {minimize_result.x[0]:.6f}")
    print(f"   Minimum value: {minimize_result.fun:.6f}")

    def h(x):
        return x**2 - 9

    def linear(x):
        return x - 5

    def quad(x):
        return x**2 - 4 * x + 3

    def cubic(x):
        return x**3 - 2 * x - 5

    namespace = {
        "optimize": optimize,
        "h": h,
        "linear": linear,
        "quad": quad,
        "cubic": cubic,
        "g": g,
        "np": np,
    }

    def check1(result):
        if not hasattr(result, "x"):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"

    def check2(result):
        if not hasattr(result, "x"):
            return False, "Expected a result object from optimize.minimize(), not just a number"
        min_value = float(result.x[0])
        return True, f"Minimum at: {min_value:.2f}"

    def check3(result):
        if not hasattr(result, "x"):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"

    def check4(result):
        if not hasattr(result, "x"):
            return False, "Expected a result object from optimize.minimize(), not just a number"
        min_value = float(result.x[0])
        return True, f"Minimum at: {min_value:.2f}"

    def check5(result):
        if not hasattr(result, "x"):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"

    run_exercise_questions(
        namespace,
        [
            Question(
                "For linear(x) = x - 5, find the root near x0=0",
                check1,
                "What function finds where a function equals zero?",
                reference_answer="optimize.root(linear, x0=0.0)",
            ),
            Question(
                "For quad(x) = x² - 4x + 3, find the minimum near x0=0",
                check2,
                "What function finds the minimum value of a function?",
                reference_answer="optimize.minimize(quad, x0=0.0)",
            ),
            Question(
                "For h(x) = x² - 9, find the root near x0=3",
                check3,
                "How do you find where a function crosses zero?",
                reference_answer="optimize.root(h, x0=3.0)",
            ),
            Question(
                "For g(x) = x² + 2x + 1, find the minimum near x0=0",
                check4,
                "What function finds the minimum value of a function?",
                reference_answer="optimize.minimize(g, x0=0.0)",
            ),
            Question(
                "For cubic(x) = x³ - 2x - 5, find the root near x0=2",
                check5,
                "How do you find where a function equals zero starting from a guess?",
                reference_answer="optimize.root(cubic, x0=2.0)",
            ),
        ],
    )

def exercise_sparse():
    """Practice with sparse matrices (CSR and CSC formats)."""
    print("\n" + "-" * 60)
    print("Exercise: Sparse Matrices (CSR and CSC)")
    print("-" * 60)

    print("\n1. Why sparse matrices? Memory efficiency:")
    print("   Consider a 1000x1000 matrix with only 50 non-zero values.")
    print("   Dense storage: 1,000,000 elements × 8 bytes = 8 MB")
    print("   Sparse storage: ~50 elements × 8 bytes + indices = ~2 KB")
    print("   Sparse matrices are essential for large, mostly-empty matrices")
    print("   (e.g., graph adjacency matrices, finite element methods, network analysis)")

    print("\n2. Creating a sparse matrix in CSR format (Compressed Sparse Row):")
    print("   CSR is efficient for row-based operations and matrix-vector products")
    network_dense = np.array(
        [
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ]
    )
    csr_matrix = sparse.csr_matrix(network_dense)
    print("   Directed network adjacency matrix (5 nodes, 5 directed connections):")
    print("   Dense representation:\n", network_dense)
    print("   CSR matrix shape:", csr_matrix.shape)
    print(
        "   Non-zero elements:",
        csr_matrix.nnz,
        "(out of",
        csr_matrix.shape[0] * csr_matrix.shape[1],
        "total)",
    )
    print(
        "   Sparsity:",
        f"{(1 - csr_matrix.nnz / (csr_matrix.shape[0] * csr_matrix.shape[1])) * 100:.1f}% zeros",
    )
    print("   CSR format stores only:", csr_matrix.nnz, "values + row/column indices")

    print("\n3. Converting to CSC format (Compressed Sparse Column):")
    print("   CSC is efficient for column-based operations and column slicing")
    csc_matrix = csr_matrix.tocsc()
    print("   CSC matrix shape:", csc_matrix.shape)
    print("   Non-zero elements:", csc_matrix.nnz, "(same data, different storage)")
    print("   Original matrix:\n", csr_matrix.toarray())
    print("   Transpose (different from original, since matrix is asymmetric):\n", csr_matrix.T.toarray())
    print("   Use CSR for row operations, CSC for column operations")

    print("\n4. Sparse matrix operations:")
    network_dense2 = np.array(
        [
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    csr_matrix2 = sparse.csr_matrix(network_dense2)
    print("   Adding two sparse matrices (combining network connections):")
    print("   Matrix 1:\n", network_dense)
    print("   Matrix 2:\n", network_dense2)
    result = csr_matrix + csr_matrix2
    print("   Sum (Matrix 1 + Matrix 2):\n", result.toarray())
    print("   Matrix 1 (CSR):", csr_matrix.nnz, "non-zeros")
    print("   Matrix 2 (CSR):", csr_matrix2.nnz, "non-zeros")
    print("   Result (CSR):", result.nnz, "non-zeros")
    print("   Note: Operations preserve sparsity when possible")

    print("\n5. Converting dense to sparse:")
    dense = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    sparse_from_dense = sparse.csr_matrix(dense)
    print("   Dense matrix (3×3 = 9 elements):\n", dense)
    print("   Sparse matrix (CSR format) - stored as sparse object:")
    print("   ", sparse_from_dense)
    print("   When converted back to array (for display):\n", sparse_from_dense.toarray())
    print("   Sparse representation stores only:", sparse_from_dense.nnz, "non-zero elements")
    print("   Memory saved:", f"{(1 - sparse_from_dense.nnz / 9) * 100:.1f}%", "for this small example")
    print("   For larger matrices, savings become substantial")

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

    run_exercise_questions(
        namespace,
        [
            Question(
                "Convert dense_matrix to a CSR sparse matrix",
                check1,
                "How do you create a CSR matrix from a dense array?",
                reference_answer="sparse.csr_matrix(dense_matrix)",
            ),
            Question(
                "Get the number of non-zero elements in csr_example",
                check2,
                "What attribute tells you how many non-zero elements a sparse matrix has?",
                reference_answer="csr_example.nnz",
            ),
            Question(
                "Convert csr_example to CSC format",
                check3,
                "What method converts a CSR matrix to CSC format?",
                reference_answer="csr_example.tocsc()",
            ),
            Question(
                "Get the shape of csr_example",
                check4,
                "What attribute contains the dimensions of a matrix?",
                reference_answer="csr_example.shape",
            ),
            Question(
                "Add sparse.csr_matrix(dense_matrix) and sparse.csr_matrix(dense_matrix2)",
                check5,
                "How do you add two sparse matrices together?",
                reference_answer="sparse.csr_matrix(dense_matrix) + sparse.csr_matrix(dense_matrix2)",
            ),
        ],
    )

def exercise_csgraph():
    """Practice with scipy.sparse.csgraph algorithms."""
    print("\n" + "-" * 60)
    print("Exercise: CSGraph (Graph Algorithms)")
    print("-" * 60)

    print("\n1. Creating a graph as a sparse matrix:")
    graph = np.array(
        [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]
    )
    print("   Dense adjacency matrix:\n", graph)
    print("   Converting to sparse CSR format...")
    graph_sparse = sparse.csr_matrix(graph)
    print("   Sparse matrix (CSR format):", graph_sparse)
    print("   Non-zero elements:", graph_sparse.nnz, "out of", graph.shape[0] * graph.shape[1], "total")
    print("   When converted back to array (for display):\n", graph_sparse.toarray())

    print("\n2. Shortest paths:")
    dist_matrix = csgraph.shortest_path(graph_sparse, directed=False)
    print("   Shortest path distances:")
    print(dist_matrix)

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

    run_exercise_questions(
        namespace,
        [
            Question(
                "Find the number of connected components in graph2_sparse",
                check1,
                "What function counts how many separate groups of connected nodes exist?",
                reference_answer="csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)",
            ),
            Question(
                "Check if chain_sparse is connected (has exactly 1 component)",
                check2,
                "How can you determine if all nodes are reachable from each other?",
                reference_answer="csgraph.connected_components(chain_sparse, directed=False, return_labels=False) == 1",
            ),
            Question(
                "Find the shortest path distance matrix for chain_sparse",
                check3,
                "What function computes the shortest distances between all pairs of nodes?",
                reference_answer="csgraph.shortest_path(chain_sparse, directed=False)",
            ),
            Question(
                "Find the shortest path distance matrix for a 3-node fully connected graph (use sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])))",
                check4,
                "How do you find distances in an undirected graph?",
                reference_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])), directed=False)",
            ),
            Question(
                "Find the shortest path distance matrix for a directed graph (use sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]]))) with directed=True",
                check5,
                "How do you compute distances when edges have direction?",
                reference_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]])), directed=True)",
            ),
        ],
    )

def exercise_spatial():
    """Practice with scipy.spatial (excluding cosine distance)."""
    print("\n" + "-" * 60)
    print("Exercise: Spatial Data")
    print("-" * 60)

    print("\n1. Euclidean distance:")
    print("   Straight-line distance between two points (Pythagorean theorem)")
    point1 = np.array([0, 0])
    point2 = np.array([3, 4])
    euclidean_dist = distance.euclidean(point1, point2)
    print(f"   Distance between {point1} and {point2}: {euclidean_dist}")

    print("\n2. Manhattan distance (also called cityblock distance):")
    print("   Sum of absolute differences along each dimension (L1 norm)")
    manhattan_dist = distance.cityblock(point1, point2)
    print(f"   Manhattan distance between {point1} and {point2}: {manhattan_dist}")

    print("\n3. Distance matrix:")
    points = np.array([[0, 0], [1, 1], [4, 5]])
    dist_matrix = distance.pdist(points, metric="euclidean")
    print(f"   Points: {points}")
    print(f"   Pairwise distances: {dist_matrix}")

    square_dist = distance.squareform(dist_matrix)
    print(f"   Distance matrix:\n{square_dist}")

    print("\n4. Multiple distance metrics:")
    p1, p2 = np.array([1, 2]), np.array([4, 6])
    print(f"   Points: {p1}, {p2}")
    print(f"   Euclidean: {distance.euclidean(p1, p2):.2f} (straight-line distance)")
    print(f"   Manhattan (cityblock): {distance.cityblock(p1, p2):.2f} (sum of absolute differences)")
    print(f"   Chebyshev: {distance.chebyshev(p1, p2):.2f} (maximum absolute difference)")

    print("\n5. Minkowski distance:")
    print("   Generalized distance metric: distance = (Σ|xi - yi|^p)^(1/p)")
    print("   Parameter p controls the distance type:")
    print("   - p=1: Manhattan distance")
    print("   - p=2: Euclidean distance")
    print("   - p=∞: Chebyshev distance (approximated with large p)")
    minkowski_dist = distance.minkowski(p1, p2, p=3)
    print(f"   Minkowski distance (p=3) between {p1} and {p2}: {minkowski_dist:.2f}")

    p1 = np.array([0, 0])
    p2 = np.array([5, 12])
    p3 = np.array([1, 2])
    p4 = np.array([4, 6])
    p5 = np.array([2, 3])
    p6 = np.array([5, 7])
    p7 = np.array([1, 1])
    p8 = np.array([4, 5])
    points_array = np.array([[0, 0], [1, 1], [4, 5]])

    namespace = {
        "distance": distance,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "p5": p5,
        "p6": p6,
        "p7": p7,
        "p8": p8,
        "points_array": points_array,
        "np": np,
    }

    def check1(result):
        correct = distance.euclidean(p1, p2)
        if abs(float(result) - correct) < 0.01:
            return True, f"Euclidean distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check2(result):
        correct = distance.cityblock(p3, p4)
        if abs(float(result) - correct) < 0.01:
            return True, f"Manhattan distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check3(result):
        correct = distance.chebyshev(p5, p6)
        if abs(float(result) - correct) < 0.01:
            return True, f"Chebyshev distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    def check4(result):
        correct = distance.pdist(points_array, metric="euclidean")
        if np.allclose(result, correct):
            return True, f"Pairwise distances computed for {len(points_array)} points"
        return False, "Expected pairwise distance array"

    def check5(result):
        correct = distance.minkowski(p7, p8, p=3)
        if abs(float(result) - correct) < 0.01:
            return True, f"Minkowski distance (p=3): {result:.2f}"
        return False, f"Expected distance {correct:.2f}"

    run_exercise_questions(
        namespace,
        [
            Question(
                "Calculate the Euclidean distance between p1 (0, 0) and p2 (5, 12)",
                check1,
                "What function calculates straight-line distance between two points?",
                reference_answer="distance.euclidean(p1, p2)",
            ),
            Question(
                "Calculate the Manhattan distance between p3 (1, 2) and p4 (4, 6)",
                check2,
                "What function calculates distance as sum of absolute differences?",
                reference_answer="distance.cityblock(p3, p4)",
            ),
            Question(
                "Calculate the Chebyshev distance between p5 (2, 3) and p6 (5, 7)",
                check3,
                "What function calculates distance as maximum absolute difference?",
                reference_answer="distance.chebyshev(p5, p6)",
            ),
            Question(
                "Calculate pairwise Euclidean distances for points_array [[0, 0], [1, 1], [4, 5]]",
                check4,
                "What function computes distances between all pairs of points?",
                reference_answer="distance.pdist(points_array, metric='euclidean')",
            ),
            Question(
                "Calculate the Minkowski distance between p7 (1, 1) and p8 (4, 5) with p=3",
                check5,
                "What function calculates a generalized distance with a power parameter?",
                reference_answer="distance.minkowski(p7, p8, p=3)",
            ),
        ],
    )

def exercise_interpolate():
    """Practice with scipy.interpolate."""
    print("\n" + "-" * 60)
    print("Exercise: Interpolation")
    print("-" * 60)

    print("\nWhat is interpolation?")
    print("   Estimating values between known data points")
    print("   Given: x = [0, 1, 2, 3, 4, 5], y = [1, 2, 3, 4, 5, 6]")
    print("   Find: y value at x = 2.5 (between x=2 and x=3)")

    print("\n1. 1D Interpolation (one variable):")
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([0, 2, 4, 6, 8, 10])
    f_linear = interpolate.interp1d(x, y, kind="linear")
    x_new = 1.5
    y_new = f_linear(x_new)
    print(f"   Known points: x={x}, y={y}")
    print(f"   Relationship: y = 2x (multiplication by 2)")
    print(f"   Interpolate at x={x_new}: y={y_new:.1f}")
    print(f"   (Linear: draws straight lines between points)")

    print("\n2. Interpolation kinds (the 'kind' parameter):")
    print(f"   Linear: connects points with straight lines (simplest, fastest)")
    print(f"   Quadratic: uses quadratic curves to create smooth transitions (needs ≥3 points)")
    print(f"   Cubic: uses cubic curves for smoother, more natural curves (needs ≥4 points)")
    print(f"   Nearest: uses the value of the nearest data point (step-like function)")

    print("\n3. Using different data:")
    x2 = np.array([0, 1, 2, 3, 4])
    y2 = np.array([0, 1, 4, 9, 16])
    f2 = interpolate.interp1d(x2, y2, kind="linear")
    print(f"   Different dataset: x={x2}, y={y2}")
    print(f"   Relationship: y = x² (squared)")
    print(f"   Interpolate at x=2.5: y={f2(2.5):.1f}")
    print(f"   (Note: Linear interpolation draws a STRAIGHT LINE between (2,4) and (3,9),")
    print(f"    so at x=2.5 (halfway), y is halfway: (4+9)/2 = 6.5")
    print(f"    The actual curve y=x² would give 2.5² = 6.25, but linear uses lines, not curves)")

    x_points = np.array([0, 1, 2])
    y_points = np.array([0, 1, 4])
    x_points2 = np.array([0, 1, 2, 3, 4])
    y_points2 = np.array([0, 1, 4, 9, 16])

    namespace = {
        "interpolate": interpolate,
        "x_points": x_points,
        "y_points": y_points,
        "x_points2": x_points2,
        "y_points2": y_points2,
        "np": np,
    }

    def check1(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind="linear")
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Linear interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check2(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind="quadratic")
        if callable(result):
            test_val = 2.0
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Quadratic interpolation function created"
            return False, f"Expected value at x=2.0: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check3(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind="cubic")
        if callable(result):
            test_val = 2.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Cubic interpolation function created"
            return False, f"Expected value at x=2.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    def check4(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind="nearest")
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Nearest interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"

    run_exercise_questions(
        namespace,
        [
            Question(
                "Create a linear interpolation function for x_points and y_points",
                check1,
                "What function creates an interpolation function from x and y data points?",
                reference_answer="interpolate.interp1d(x_points, y_points, kind='linear')",
            ),
            Question(
                "Create a quadratic interpolation function for x_points2 and y_points2",
                check2,
                "How do you create a smooth curve using quadratic polynomials?",
                reference_answer="interpolate.interp1d(x_points2, y_points2, kind='quadratic')",
            ),
            Question(
                "Create a cubic interpolation function for x_points2 and y_points2",
                check3,
                "How do you create a smooth curve using cubic polynomials?",
                reference_answer="interpolate.interp1d(x_points2, y_points2, kind='cubic')",
            ),
            Question(
                "Create a nearest interpolation function for x_points and y_points",
                check4,
                "How do you create an interpolation that uses the nearest data point?",
                reference_answer="interpolate.interp1d(x_points, y_points, kind='nearest')",
            ),
        ],
    )
