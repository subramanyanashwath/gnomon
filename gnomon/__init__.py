"""Gnomon — statistical decision layer for LLM agent evaluation."""

__version__ = "0.0.1"

from gnomon.agents import AnthropicAgent
from gnomon.eval import Judge, LLMJudge, score_ci
from gnomon.stats import BootstrapResult, bootstrap_ci
from gnomon.types import EvalCase, EvalResult, EvalRun

__all__ = [
    "AnthropicAgent",
    "BootstrapResult",
    "EvalCase",
    "EvalResult",
    "EvalRun",
    "Judge",
    "LLMJudge",
    "__version__",
    "bootstrap_ci",
    "score_ci",
]
