"""Gnomon — statistical decision layer for LLM agent evaluation."""

__version__ = "0.0.1"

from gnomon.agents import AnthropicAgent
from gnomon.eval import Judge, LLMJudge, score_ci
from gnomon.stats import (
    BootstrapResult,
    PowerResult,
    bootstrap_ci,
    cohens_h,
    power_one_proportion,
    power_two_proportions,
    required_n_one_proportion,
    required_n_two_proportions,
)
from gnomon.types import EvalCase, EvalResult, EvalRun

__all__ = [
    "AnthropicAgent",
    "BootstrapResult",
    "EvalCase",
    "EvalResult",
    "EvalRun",
    "Judge",
    "LLMJudge",
    "PowerResult",
    "__version__",
    "bootstrap_ci",
    "cohens_h",
    "power_one_proportion",
    "power_two_proportions",
    "required_n_one_proportion",
    "required_n_two_proportions",
    "score_ci",
]
