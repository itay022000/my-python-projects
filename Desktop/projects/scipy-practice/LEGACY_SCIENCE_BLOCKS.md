# Legacy SciPy science blocks (removed 2026-08-08)
Exact source excerpts of pre-question science/demo bodies. Not imported by the app.
Constants acceptance note remains in product.

## constants.py

```python
def exercise_constants():
    """Practice with scipy.constants."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Constants Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("1. Metric constants:")
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
    # ... then build practice + run_exercise_questions
```

## optimize.py

```python
def exercise_optimize():
    """Practice with scipy.optimize - root finding and minimization."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Optimization Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("1. Root Finding:")
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
    # ... then build practice + run_exercise_questions
```

## sparse.py

```python
def exercise_sparse():
    """Practice with sparse matrices (CSR and CSC formats)."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Sparse Matrices (CSR and CSC) Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("1. Why sparse matrices? Memory efficiency:")
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
    dense_matrix = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    sparse_from_dense = sparse.csr_matrix(dense_matrix)
    print("   Dense matrix (3×3 = 9 elements):\n", dense_matrix)
    print("   Sparse matrix (CSR format) - stored as sparse object:")
    print("   ", sparse_from_dense)
    print("   When converted back to array (for display):\n", sparse_from_dense.toarray())
    print("   Sparse representation stores only:", sparse_from_dense.nnz, "non-zero elements")
    print("   Memory saved:", f"{(1 - sparse_from_dense.nnz / 9) * 100:.1f}%", "for this small example")
    print("   For larger matrices, savings become substantial")
    # ... then build practice + run_exercise_questions
```

## csgraph.py

```python
def exercise_csgraph():
    """Practice with scipy.sparse.csgraph algorithms."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("CSGraph (Graph Algorithms) Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("1. Creating a graph as a sparse matrix:")
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
    # ... then build practice + run_exercise_questions
```

## spatial.py

```python
def exercise_spatial():
    """Practice with scipy.spatial (excluding cosine distance)."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Spatial Data Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("1. Euclidean distance:")
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
    # ... then build practice + run_exercise_questions
```

## interpolate.py

```python
def exercise_interpolate():
    """Practice with scipy.interpolate."""
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Interpolation Exercise")
    print("=" * SESSION_BANNER_WIDTH)

    print("What is interpolation?")
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
    print("   Linear: connects points with straight lines (simplest, fastest)")
    print("   Quadratic: uses quadratic curves to create smooth transitions (needs ≥3 points)")
    print("   Cubic: uses cubic curves for smoother, more natural curves (needs ≥4 points)")
    print("   Nearest: uses the value of the nearest data point (step-like function)")

    print("\n3. Using different data:")
    x2 = np.array([0, 1, 2, 3, 4])
    y2 = np.array([0, 1, 4, 9, 16])
    f2 = interpolate.interp1d(x2, y2, kind="linear")
    print(f"   Different dataset: x={x2}, y={y2}")
    print(f"   Relationship: y = x² (squared)")
    print(f"   Interpolate at x=2.5: y={f2(2.5):.1f}")
    print("   (Note: Linear interpolation draws a STRAIGHT LINE between (2,4) and (3,9),")
    print("    so at x=2.5 (halfway), y is halfway: (4+9)/2 = 6.5")
    print("    The actual curve y=x² would give 2.5² = 6.25, but linear uses lines, not curves)")
    # ... then build practice + run_exercise_questions
```
