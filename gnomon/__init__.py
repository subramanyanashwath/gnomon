"""Gnomon — statistical decision layer for LLM agent evaluation."""

__version__ = "0.0.1"

from gnomon.stats import BootstrapResult, bootstrap_ci
from gnomon.types import EvalCase, EvalResult, EvalRun

__all__ = [
    "BootstrapResult",
    "EvalCase",
    "EvalResult",
    "EvalRun",
    "__version__",
    "bootstrap_ci",
]
