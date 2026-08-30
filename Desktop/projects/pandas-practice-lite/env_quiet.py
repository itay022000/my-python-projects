"""
Quiet known environment warnings before pandas / matplotlib import.

Anaconda base often ships an older bottleneck than pandas expects; the app
still runs, but learners should not see dependency noise on startup.

Also pins MPLCONFIGDIR to a writable temp dir so matplotlib never prints
cache-path warnings into the learner CLI.
"""

from __future__ import annotations

import os
import tempfile
import warnings

# Must run before the first matplotlib import in this process.
if not os.environ.get("MPLCONFIGDIR"):
    _mpl_dir = os.path.join(tempfile.gettempdir(), "pandas-practice-lite-mpl")
    os.makedirs(_mpl_dir, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = _mpl_dir

warnings.filterwarnings(
    "ignore",
    message=r"Pandas requires version .+ of 'bottleneck'",
    category=UserWarning,
)

warnings.filterwarnings(
    "ignore",
    message=r".*Matplotlib.*",
    category=UserWarning,
)
