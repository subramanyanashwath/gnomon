"""Statistical primitives for Gnomon.

Each function in this package is a typed wrapper over a well-tested reference
implementation (typically ``scipy.stats``). Gnomon's value-add is decision-
oriented defaults, typed result objects, and integration with the rest of the
eval pipeline — not re-implementing statistics from scratch.

Every primitive ships with a property-based test that compares its output to
the reference implementation directly (see ``tests/test_stats_*.py``).
"""

from gnomon.stats.bootstrap import BootstrapResult, bootstrap_ci

__all__ = ["BootstrapResult", "bootstrap_ci"]
