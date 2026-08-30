"""Strike-1 hint strings for scipy-practice exercises (B015)."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Constants — no strike-1 hints (empty strings)
# ---------------------------------------------------------------------------

HINT_CONSTANTS_1 = ""
HINT_CONSTANTS_2 = ""
HINT_CONSTANTS_3 = ""
HINT_CONSTANTS_4 = ""
HINT_CONSTANTS_5 = ""

# ---------------------------------------------------------------------------
# Optimize
# ---------------------------------------------------------------------------

HINT_OPTIMIZE_ROOT = "What function finds where a function equals zero?"
HINT_OPTIMIZE_MINIMIZE = "What function finds the minimum value of a function?"

# ---------------------------------------------------------------------------
# Sparse
# ---------------------------------------------------------------------------

HINT_SPARSE_CSR = "How do you create a CSR matrix from a dense array?"
HINT_SPARSE_NNZ = "What attribute tells you how many non-zero elements a sparse matrix has?"
HINT_SPARSE_CSC = "What method converts a CSR matrix to CSC format?"
HINT_SPARSE_SHAPE = "What attribute contains the dimensions of a matrix?"
HINT_SPARSE_ADD = "How do you add two sparse matrices together?"

# ---------------------------------------------------------------------------
# CSGraph
# ---------------------------------------------------------------------------

HINT_CSGRAPH_COMPONENTS = (
    "What function counts how many separate groups of connected nodes exist?"
)
HINT_CSGRAPH_CONNECTED = "How can you determine if all nodes are reachable from each other?"
HINT_CSGRAPH_SHORTEST = (
    "What function computes the shortest distances between all pairs of nodes?"
)
HINT_CSGRAPH_UNDIRECTED = "How do you find distances in an undirected graph?"
HINT_CSGRAPH_DIRECTED = "How do you find distances in a directed graph?"

# ---------------------------------------------------------------------------
# Spatial
# ---------------------------------------------------------------------------

HINT_SPATIAL_EUCLIDEAN = "What function calculates straight-line distance between two points?"
HINT_SPATIAL_CITYBLOCK = "What function calculates distance as sum of absolute differences?"
HINT_SPATIAL_CHEBYSHEV = "What function calculates distance as maximum absolute difference?"
HINT_SPATIAL_PDIST = "What function computes distances between all pairs of points?"
HINT_SPATIAL_MINKOWSKI = "What function calculates a generalized distance with a power parameter?"

# ---------------------------------------------------------------------------
# Interpolate
# ---------------------------------------------------------------------------

HINT_INTERPOLATE_LINEAR = (
    "What function creates an interpolation function from x and y data points?"
)
HINT_INTERPOLATE_QUADRATIC = "How do you create a smooth curve using quadratic polynomials?"
HINT_INTERPOLATE_CUBIC = "How do you create a smooth curve using cubic polynomials?"
HINT_INTERPOLATE_NEAREST = "How do you create an interpolation that uses the nearest data point?"
