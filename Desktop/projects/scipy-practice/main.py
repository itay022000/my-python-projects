"""
SciPy Practice - Focused Learning Tool
A simple project to practice key SciPy modules: constants, optimize, sparse, csgraph, spatial, and interpolation.

Last Updated: 2026-01-03 22:08:49
"""

import scipy.constants as const
from scipy import optimize
from scipy import sparse
from scipy.sparse import csgraph
from scipy.spatial import distance
from scipy import interpolate
import numpy as np
import re

# Last updated timestamp (keep in sync with docstring)
LAST_UPDATED = "2026-01-03 22:08:49"


def show_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("SciPy Practice - Main Menu")
    print("="*60)
    print("1. Constants exercise")
    print("2. Optimization (root finding and minimize) exercise")
    print("3. Sparse Matrices (CSR and CSC) exercise")
    print("4. CSGraph (graph algorithms) exercise")
    print("5. Spatial Data exercise")
    print("6. Interpolation exercise")
    print("7. Exit")
    print("="*60)


def normalize_code(code):
    """Normalize code string for comparison (remove extra spaces)."""
    # Remove all whitespace
    return re.sub(r'\s+', '', code)

def ask_question(question_text, namespace, check_func, hint_text, check_code=None, exact_answer=None):
    """Helper function to ask a question and check the answer."""
    print("\n" + "-"*60)
    print("Practice Question:")
    print(question_text)
    print("Enter your code: ", end="")
    try:
        user_code = input().strip()
        # If exact_answer is provided, check for exact match first
        if exact_answer:
            normalized_user = normalize_code(user_code)
            normalized_exact = normalize_code(exact_answer)
            if normalized_user != normalized_exact:
                print(f"❌ Incorrect.")
                print(f"   Hint: {hint_text}")
                return
        user_result = eval(user_code, namespace)
        # If check_code function is provided, verify the code string first
        if check_code:
            code_check, code_feedback = check_code(user_code)
            if not code_check:
                print(f"❌ Incorrect.")
                if code_feedback:
                    print(f"   {code_feedback}")
                print(f"   Hint: {hint_text}")
                return
        is_correct, feedback = check_func(user_result)
        if is_correct:
            print("✅ Correct!")
            if feedback:
                print(f"   {feedback}")
        else:
            print(f"❌ Incorrect.")
            if feedback:
                print(f"   {feedback}")
            print(f"   Hint: {hint_text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Hint: {hint_text}")


def exercise_constants():
    """Practice with scipy.constants."""
    print("\n" + "-"*60)
    print("Exercise: SciPy Constants")
    print("-"*60)
    
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
    
    print("\n" + "-"*60)
    print("Note: For all questions, use the format '(number) * (constant expression)'")
    print("-"*60)
    
    namespace = {'const': const, 'np': np}
    
    # Question 1: Easy - Convert inches to meters
    def check1(result):
        correct = 12 * const.inch
        if abs(float(result) - correct) < 0.01:
            return True, f"12 inches = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"
    ask_question("Convert 12 inches to meters", namespace, check1, "What constant converts inches to meters?",
                 exact_answer="12 * const.inch")
    
    # Question 2: Easy - Convert miles to meters
    def check2(result):
        correct = 5 * const.mile
        if abs(float(result) - correct) < 0.01:
            return True, f"5 miles = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"
    ask_question("Convert 5 miles to meters", namespace, check2, "What constant converts miles to meters?",
                 exact_answer="5 * const.mile")
    
    # Question 3: Easy - Convert feet to meters
    def check3(result):
        correct = 10 * const.foot
        if abs(float(result) - correct) < 0.01:
            return True, f"10 feet = {result:.2f} meters"
        return False, f"Expected approximately {correct:.2f} meters"
    ask_question("Convert 10 feet to meters", namespace, check3, "What constant converts feet to meters?",
                 exact_answer="10 * const.foot")
    
    # Question 4: Easy - Convert minutes to seconds
    def check4(result):
        correct = 3 * const.minute
        if abs(float(result) - correct) < 0.01:
            return True, f"3 minutes = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"
    ask_question("Convert 3 minutes to seconds", namespace, check4, "What constant converts minutes to seconds?",
                 exact_answer="3 * const.minute")
    
    # Question 5: Medium - Convert hours to seconds
    def check5(result):
        correct = 2 * const.hour
        if abs(float(result) - correct) < 0.01:
            return True, f"2 hours = {result:.0f} seconds"
        return False, f"Expected approximately {correct:.0f} seconds"
    ask_question("Convert 2 hours to seconds", namespace, check5, "What constant converts hours to seconds?",
                 exact_answer="2 * const.hour")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def exercise_optimize():
    """Practice with scipy.optimize - root finding and minimization."""
    print("\n" + "-"*60)
    print("Exercise: SciPy Optimization")
    print("-"*60)
    
    print("\n1. Root Finding:")
    print("   Finding root of f(x) = x² - 4")
    
    def f(x):
        return x**2 - 4
    
    # Find root near x=1
    root_result = optimize.root(f, x0=1.0)
    print(f"   Root found: x = {root_result.x[0]:.6f}")
    print(f"   Function value at root: {f(root_result.x[0]):.2e}")
    
    # Find root near x=-3
    root_result2 = optimize.root(f, x0=-3.0)
    print(f"   Another root found: x = {root_result2.x[0]:.6f}")
    
    print("\n2. Minimization:")
    print("   Finding minimum of f(x) = x² + 2x + 1")
    
    def g(x):
        return x**2 + 2*x + 1
    
    # Find minimum
    minimize_result = optimize.minimize(g, x0=0.0)
    print(f"   Minimum at: x = {minimize_result.x[0]:.6f}")
    print(f"   Minimum value: {minimize_result.fun:.6f}")
    
    # Define functions for questions
    def h(x):
        return x**2 - 9
    
    def linear(x):
        return x - 5
    
    def quad(x):
        return x**2 - 4*x + 3
    
    def cubic(x):
        return x**3 - 2*x - 5
    
    def g(x):
        return x**2 + 2*x + 1
    
    namespace = {'optimize': optimize, 'h': h, 'linear': linear, 
                 'quad': quad, 'cubic': cubic, 'g': g, 'np': np}
    
    # Question 1: Easy - Find root of linear function
    def check1(result):
        if not hasattr(result, 'x'):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"
    ask_question("For linear(x) = x - 5, find the root near x0=0", namespace, check1, 
                 "What function finds where a function equals zero?", 
                 exact_answer="optimize.root(linear, x0=0.0)")
    
    # Question 2: Easy - Find minimum of quadratic
    def check2(result):
        if not hasattr(result, 'x'):
            return False, "Expected a result object from optimize.minimize(), not just a number"
        min_value = float(result.x[0])
        return True, f"Minimum at: {min_value:.2f}"
    ask_question("For quad(x) = x² - 4x + 3, find the minimum near x0=0", namespace, check2,
                 "What function finds the minimum value of a function?",
                 exact_answer="optimize.minimize(quad, x0=0.0)")
    
    # Question 3: Medium - Find root of quadratic
    def check3(result):
        if not hasattr(result, 'x'):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"
    ask_question("For h(x) = x² - 9, find the root near x0=3", namespace, check3,
                 "How do you find where a function crosses zero?",
                 exact_answer="optimize.root(h, x0=3.0)")
    
    # Question 4: Medium - Find minimum of different function
    def check4(result):
        if not hasattr(result, 'x'):
            return False, "Expected a result object from optimize.minimize(), not just a number"
        min_value = float(result.x[0])
        return True, f"Minimum at: {min_value:.2f}"
    ask_question("For g(x) = x² + 2x + 1, find the minimum near x0=0", namespace, check4,
                 "What function finds the minimum value of a function?",
                 exact_answer="optimize.minimize(g, x0=0.0)")
    
    # Question 5: Medium-Hard - Find root of cubic
    def check5(result):
        if not hasattr(result, 'x'):
            return False, "Expected a result object from optimize.root(), not just a number"
        root_value = float(result.x[0])
        return True, f"Root found: {root_value:.2f}"
    ask_question("For cubic(x) = x³ - 2x - 5, find the root near x0=2", namespace, check5,
                 "How do you find where a function equals zero starting from a guess?",
                 exact_answer="optimize.root(cubic, x0=2.0)")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def exercise_sparse():
    """Practice with sparse matrices (CSR and CSC formats)."""
    print("\n" + "-"*60)
    print("Exercise: Sparse Matrices (CSR and CSC)")
    print("-"*60)
    
    print("\n1. Why sparse matrices? Memory efficiency:")
    print("   Consider a 1000x1000 matrix with only 50 non-zero values.")
    print("   Dense storage: 1,000,000 elements × 8 bytes = 8 MB")
    print("   Sparse storage: ~50 elements × 8 bytes + indices = ~2 KB")
    print("   Sparse matrices are essential for large, mostly-empty matrices")
    print("   (e.g., graph adjacency matrices, finite element methods, network analysis)")
    
    print("\n2. Creating a sparse matrix in CSR format (Compressed Sparse Row):")
    print("   CSR is efficient for row-based operations and matrix-vector products")
    # Create a realistic example: adjacency matrix of a directed network (asymmetric)
    network_dense = np.array([
        [0, 1, 1, 0, 0],  # Node 0 -> nodes 1 and 2 (directed edges)
        [0, 0, 0, 1, 0],  # Node 1 -> node 3
        [0, 0, 0, 0, 1],  # Node 2 -> node 4
        [0, 0, 0, 0, 1],  # Node 3 -> node 4
        [0, 0, 0, 0, 0]   # Node 4 -> (no outgoing edges)
    ])
    csr_matrix = sparse.csr_matrix(network_dense)
    print("   Directed network adjacency matrix (5 nodes, 5 directed connections):")
    print("   Dense representation:\n", network_dense)
    print("   CSR matrix shape:", csr_matrix.shape)
    print("   Non-zero elements:", csr_matrix.nnz, "(out of", csr_matrix.shape[0] * csr_matrix.shape[1], "total)")
    print("   Sparsity:", f"{(1 - csr_matrix.nnz / (csr_matrix.shape[0] * csr_matrix.shape[1])) * 100:.1f}% zeros")
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
    # Create another sparse matrix representing a different network state
    network_dense2 = np.array([
        [0, 0, 0, 1, 1],  # Different directed connection pattern
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
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
    
    # Setup for questions
    dense_matrix = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    csr_example = sparse.csr_matrix(dense_matrix)
    dense_matrix2 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    
    namespace = {'sparse': sparse, 'dense_matrix': dense_matrix, 
                 'csr_example': csr_example, 'dense_matrix2': dense_matrix2, 'np': np}
    
    # Question 1: Easy - Convert dense to CSR
    def check1(result):
        correct_matrix = sparse.csr_matrix(dense_matrix)
        if (hasattr(result, 'shape') and result.shape == (3, 3) and
            result.nnz == 3 and
            np.allclose(result.toarray(), correct_matrix.toarray())):
            return True, f"Matrix has {result.nnz} non-zero elements"
        return False, "Expected: 3x3 CSR matrix with 3 non-zero elements"
    ask_question("Convert dense_matrix to a CSR sparse matrix", namespace, check1,
                 "How do you create a CSR matrix from a dense array?",
                 exact_answer="sparse.csr_matrix(dense_matrix)")
    
    # Question 2: Easy - Get number of non-zero elements
    def check2(result):
        correct = csr_example.nnz
        if int(result) == correct:
            return True, f"Number of non-zero elements: {result}"
        return False, f"Expected {correct} non-zero elements"
    ask_question("Get the number of non-zero elements in csr_example", namespace, check2,
                 "What attribute tells you how many non-zero elements a sparse matrix has?",
                 exact_answer="csr_example.nnz")
    
    # Question 3: Easy - Convert CSR to CSC
    def check3(result):
        correct_matrix = csr_example.tocsc()
        if (hasattr(result, 'shape') and result.shape == (3, 3) and
            result.nnz == 3 and
            np.allclose(result.toarray(), correct_matrix.toarray())):
            return True, "Successfully converted to CSC format"
        return False, "Expected: 3x3 CSC matrix with 3 non-zero elements"
    ask_question("Convert csr_example to CSC format", namespace, check3,
                 "What method converts a CSR matrix to CSC format?",
                 exact_answer="csr_example.tocsc()")
    
    # Question 4: Easy - Get matrix shape
    def check4(result):
        correct = csr_example.shape
        if result == correct:
            return True, f"Matrix shape: {result}"
        return False, f"Expected shape {correct}"
    ask_question("Get the shape of csr_example", namespace, check4,
                 "What attribute contains the dimensions of a matrix?",
                 exact_answer="csr_example.shape")
    
    # Question 5: Medium - Add two sparse matrices
    def check5(result):
        csr1 = sparse.csr_matrix(dense_matrix)
        csr2 = sparse.csr_matrix(dense_matrix2)
        correct_matrix = csr1 + csr2
        if (hasattr(result, 'shape') and result.shape == (3, 3) and
            np.allclose(result.toarray(), correct_matrix.toarray())):
            return True, "Matrices added successfully"
        return False, "Expected: sum of the two sparse matrices"
    ask_question("Add sparse.csr_matrix(dense_matrix) and sparse.csr_matrix(dense_matrix2)", namespace, check5,
                 "How do you add two sparse matrices together?",
                 exact_answer="sparse.csr_matrix(dense_matrix) + sparse.csr_matrix(dense_matrix2)")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def exercise_csgraph():
    """Practice with scipy.sparse.csgraph algorithms."""
    print("\n" + "-"*60)
    print("Exercise: CSGraph (Graph Algorithms)")
    print("-"*60)
    
    print("\n1. Creating a graph as a sparse matrix:")
    # Create a simple graph: 0-1-2 (linear graph)
    # Adjacency matrix: 0 connected to 1, 1 connected to 2
    graph = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ])
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
    
    # Create a disconnected graph for questions
    graph2 = np.array([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    graph2_sparse = sparse.csr_matrix(graph2)
    
    # Setup for questions
    chain_graph = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ])
    chain_sparse = sparse.csr_matrix(chain_graph)
    
    namespace = {'csgraph': csgraph, 'chain_sparse': chain_sparse, 
                 'graph2_sparse': graph2_sparse, 'sparse': sparse, 'np': np}
    
    # Question 1: Easy - Find number of connected components
    def check1(result):
        correct = csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)
        if int(result) == correct:
            return True, f"Number of components: {result}"
        return False, f"Expected {correct} components"
    ask_question("Find the number of connected components in graph2_sparse", namespace, check1,
                 "What function counts how many separate groups of connected nodes exist?",
                 exact_answer="csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)")
    
    # Question 2: Easy - Check if graph is connected (1 component)
    def check2(result):
        n_comp = csgraph.connected_components(chain_sparse, directed=False, return_labels=False)
        correct = (n_comp == 1)
        if bool(result) == correct:
            return True, f"Graph is {'connected' if correct else 'disconnected'}"
        return False, f"Expected {correct} (graph has {n_comp} component(s))"
    ask_question("Check if chain_sparse is connected (has exactly 1 component)", namespace, check2,
                 "How can you determine if all nodes are reachable from each other?",
                 exact_answer="csgraph.connected_components(chain_sparse, directed=False, return_labels=False) == 1")
    
    # Question 3: Medium - Find shortest path distance matrix
    def check3(result):
        dist = csgraph.shortest_path(chain_sparse, directed=False)
        if np.allclose(result, dist):
            return True, "Distance matrix computed correctly"
        return False, "Expected the shortest path distance matrix"
    ask_question("Find the shortest path distance matrix for chain_sparse", namespace, check3,
                 "What function computes the shortest distances between all pairs of nodes?",
                 exact_answer="csgraph.shortest_path(chain_sparse, directed=False)")
    
    # Question 4: Medium - Find shortest path for different graph
    def check4(result):
        graph3 = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ])
        graph3_sparse = sparse.csr_matrix(graph3)
        dist = csgraph.shortest_path(graph3_sparse, directed=False)
        if np.allclose(result, dist):
            return True, "Distance matrix computed correctly"
        return False, "Expected the shortest path distance matrix"
    ask_question("Find the shortest path distance matrix for a 3-node fully connected graph (use sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])))", namespace, check4,
                 "How do you find distances in an undirected graph?",
                 exact_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])), directed=False)")
    
    # Question 5: Medium - Find shortest path for directed graph
    def check5(result):
        directed_graph = np.array([
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ])
        directed_sparse = sparse.csr_matrix(directed_graph)
        dist = csgraph.shortest_path(directed_sparse, directed=True)
        if np.allclose(result, dist):
            return True, "Distance matrix for directed graph computed"
        return False, "Expected the shortest path distance matrix"
    ask_question("Find the shortest path distance matrix for a directed graph (use sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]]))) with directed=True", namespace, check5,
                 "How do you compute distances when edges have direction?",
                 exact_answer="csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]])), directed=True)")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def exercise_spatial():
    """Practice with scipy.spatial (excluding cosine distance)."""
    print("\n" + "-"*60)
    print("Exercise: Spatial Data")
    print("-"*60)
    
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
    dist_matrix = distance.pdist(points, metric='euclidean')
    print(f"   Points: {points}")
    print(f"   Pairwise distances: {dist_matrix}")
    
    # Convert to square form
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
    
    # Setup for questions
    p1 = np.array([0, 0])
    p2 = np.array([5, 12])
    p3 = np.array([1, 2])
    p4 = np.array([4, 6])
    p5 = np.array([2, 3])
    p6 = np.array([5, 7])
    p7 = np.array([1, 1])
    p8 = np.array([4, 5])
    points_array = np.array([[0, 0], [1, 1], [4, 5]])
    
    namespace = {'distance': distance, 'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4,
                 'p5': p5, 'p6': p6, 'p7': p7, 'p8': p8,
                 'points_array': points_array, 'np': np}
    
    # Question 1: Easy - Euclidean distance
    def check1(result):
        correct = distance.euclidean(p1, p2)
        if abs(float(result) - correct) < 0.01:
            return True, f"Euclidean distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"
    ask_question("Calculate the Euclidean distance between p1 (0, 0) and p2 (5, 12)", namespace, check1,
                 "What function calculates straight-line distance between two points?",
                 exact_answer="distance.euclidean(p1, p2)")
    
    # Question 2: Easy - Manhattan distance
    def check2(result):
        correct = distance.cityblock(p3, p4)
        if abs(float(result) - correct) < 0.01:
            return True, f"Manhattan distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"
    ask_question("Calculate the Manhattan distance between p3 (1, 2) and p4 (4, 6)", namespace, check2,
                 "What function calculates distance as sum of absolute differences?",
                 exact_answer="distance.cityblock(p3, p4)")
    
    # Question 3: Easy - Chebyshev distance
    def check3(result):
        correct = distance.chebyshev(p5, p6)
        if abs(float(result) - correct) < 0.01:
            return True, f"Chebyshev distance: {result:.2f}"
        return False, f"Expected distance {correct:.2f}"
    ask_question("Calculate the Chebyshev distance between p5 (2, 3) and p6 (5, 7)", namespace, check3,
                 "What function calculates distance as maximum absolute difference?",
                 exact_answer="distance.chebyshev(p5, p6)")
    
    # Question 4: Medium - Pairwise distances
    def check4(result):
        correct = distance.pdist(points_array, metric='euclidean')
        if np.allclose(result, correct):
            return True, f"Pairwise distances computed for {len(points_array)} points"
        return False, "Expected pairwise distance array"
    ask_question("Calculate pairwise Euclidean distances for points_array [[0, 0], [1, 1], [4, 5]]", namespace, check4,
                 "What function computes distances between all pairs of points?",
                 exact_answer="distance.pdist(points_array, metric='euclidean')")
    
    # Question 5: Medium - Minkowski distance
    def check5(result):
        correct = distance.minkowski(p7, p8, p=3)
        if abs(float(result) - correct) < 0.01:
            return True, f"Minkowski distance (p=3): {result:.2f}"
        return False, f"Expected distance {correct:.2f}"
    ask_question("Calculate the Minkowski distance between p7 (1, 1) and p8 (4, 5) with p=3", namespace, check5,
                 "What function calculates a generalized distance with a power parameter?",
                 exact_answer="distance.minkowski(p7, p8, p=3)")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def exercise_interpolate():
    """Practice with scipy.interpolate."""
    print("\n" + "-"*60)
    print("Exercise: Interpolation")
    print("-"*60)
    
    print("\nWhat is interpolation?")
    print("   Estimating values between known data points")
    print("   Given: x = [0, 1, 2, 3, 4, 5], y = [1, 2, 3, 4, 5, 6]")
    print("   Find: y value at x = 2.5 (between x=2 and x=3)")
    
    print("\n1. 1D Interpolation (one variable):")
    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([0, 2, 4, 6, 8, 10])
    f_linear = interpolate.interp1d(x, y, kind='linear')
    x_new = 1.5
    y_new = f_linear(x_new)
    print(f"   Known points: x={x}, y={y}")
    print(f"   Relationship: y = 2x (multiplication by 2)")
    print(f"   Interpolate at x={x_new}: y={y_new:.1f}")
    print(f"   (Linear: draws straight lines between points)")
    
    print("\n2. Interpolation kinds (the 'kind' parameter):")
    f_cubic = interpolate.interp1d(x, y, kind='cubic')
    print(f"   Linear: connects points with straight lines (simplest, fastest)")
    print(f"   Quadratic: uses quadratic curves to create smooth transitions (needs ≥3 points)")
    print(f"   Cubic: uses cubic curves for smoother, more natural curves (needs ≥4 points)")
    print(f"   Nearest: uses the value of the nearest data point (step-like function)")
    
    print("\n3. Using different data:")
    x2 = np.array([0, 1, 2, 3, 4])
    y2 = np.array([0, 1, 4, 9, 16])
    f2 = interpolate.interp1d(x2, y2, kind='linear')
    print(f"   Different dataset: x={x2}, y={y2}")
    print(f"   Relationship: y = x² (squared)")
    print(f"   Interpolate at x=2.5: y={f2(2.5):.1f}")
    print(f"   (Note: Linear interpolation draws a STRAIGHT LINE between (2,4) and (3,9),")
    print(f"    so at x=2.5 (halfway), y is halfway: (4+9)/2 = 6.5")
    print(f"    The actual curve y=x² would give 2.5² = 6.25, but linear uses lines, not curves)")
    
    # Setup for questions
    x_points = np.array([0, 1, 2])
    y_points = np.array([0, 1, 4])
    x_points2 = np.array([0, 1, 2, 3, 4])
    y_points2 = np.array([0, 1, 4, 9, 16])
    
    namespace = {'interpolate': interpolate, 'x_points': x_points, 'y_points': y_points,
                 'x_points2': x_points2, 'y_points2': y_points2, 'np': np}
    
    # Question 1: Easy - Create linear interpolation function
    def check1(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind='linear')
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Linear interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"
    ask_question("Create a linear interpolation function for x_points and y_points", namespace, check1,
                 "What function creates an interpolation function from x and y data points?",
                 exact_answer="interpolate.interp1d(x_points, y_points, kind='linear')")
    
    # Question 2: Easy - Create quadratic interpolation
    def check2(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind='quadratic')
        if callable(result):
            test_val = 2.0
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Quadratic interpolation function created"
            return False, f"Expected value at x=2.0: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"
    ask_question("Create a quadratic interpolation function for x_points2 and y_points2", namespace, check2,
                 "How do you create a smooth curve using quadratic polynomials?",
                 exact_answer="interpolate.interp1d(x_points2, y_points2, kind='quadratic')")
    
    # Question 3: Medium - Create cubic interpolation
    def check3(result):
        correct_func = interpolate.interp1d(x_points2, y_points2, kind='cubic')
        if callable(result):
            test_val = 2.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.1:
                return True, "Cubic interpolation function created"
            return False, f"Expected value at x=2.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"
    ask_question("Create a cubic interpolation function for x_points2 and y_points2", namespace, check3,
                 "How do you create a smooth curve using cubic polynomials?",
                 exact_answer="interpolate.interp1d(x_points2, y_points2, kind='cubic')")
    
    # Question 4: Medium - Create nearest interpolation
    def check4(result):
        correct_func = interpolate.interp1d(x_points, y_points, kind='nearest')
        if callable(result):
            test_val = 1.5
            user_val = float(result(test_val))
            correct_val = float(correct_func(test_val))
            if abs(user_val - correct_val) < 0.01:
                return True, "Nearest interpolation function created"
            return False, f"Expected value at x=1.5: {correct_val:.2f}"
        return False, "Expected a callable interpolation function"
    ask_question("Create a nearest interpolation function for x_points and y_points", namespace, check4,
                 "How do you create an interpolation that uses the nearest data point?",
                 exact_answer="interpolate.interp1d(x_points, y_points, kind='nearest')")
    
    print("\n" + "="*60)
    print("Exercise completed! Returning to main menu...")
    print("="*60)
    print()


def main():
    """Main program loop."""
    while True:
        show_menu()
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            exercise_constants()
        elif choice == "2":
            exercise_optimize()
        elif choice == "3":
            exercise_sparse()
        elif choice == "4":
            exercise_csgraph()
        elif choice == "5":
            exercise_spatial()
        elif choice == "6":
            exercise_interpolate()
        elif choice == "0":
            print("\n" + "="*60)
            print(f"Last Updated: {LAST_UPDATED}")
            print("="*60)
            print()
        elif choice == "7":
            print("\nWe'll talk later! 👋")
            break
        else:
            print("\n❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()