"""SciPy exercise sessions: constants, optimize, sparse, csgraph, spatial, interpolate."""

from exercises.constants import _build_constants_practice, exercise_constants
from exercises.csgraph import _build_csgraph_practice, exercise_csgraph
from exercises.interpolate import _build_interpolate_practice, exercise_interpolate
from exercises.optimize import _build_optimize_practice, exercise_optimize
from exercises.sparse import _build_sparse_practice, exercise_sparse
from exercises.spatial import _build_spatial_practice, exercise_spatial

PRACTICE_BUILDERS = {
    "constants": _build_constants_practice,
    "optimize": _build_optimize_practice,
    "sparse": _build_sparse_practice,
    "csgraph": _build_csgraph_practice,
    "spatial": _build_spatial_practice,
    "interpolate": _build_interpolate_practice,
}

__all__ = [
    "PRACTICE_BUILDERS",
    "exercise_constants",
    "exercise_optimize",
    "exercise_sparse",
    "exercise_csgraph",
    "exercise_spatial",
    "exercise_interpolate",
]
