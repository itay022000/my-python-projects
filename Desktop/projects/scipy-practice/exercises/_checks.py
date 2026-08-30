"""Shared optimize result checkers."""


def _root_result_ok(result):
    """Shared optimize.root() result check (type-only policy)."""
    if not hasattr(result, "x"):
        return False, "Expected a result object from optimize.root(), not just a number"
    root_value = float(result.x[0])
    return True, f"Root found: {root_value:.2f}"


def _minimize_result_ok(result):
    """Shared optimize.minimize() result check (type-only policy)."""
    if not hasattr(result, "x"):
        return False, "Expected a result object from optimize.minimize(), not just a number"
    min_value = float(result.x[0])
    return True, f"Minimum at: {min_value:.2f}"
