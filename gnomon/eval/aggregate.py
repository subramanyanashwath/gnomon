"""Aggregate scored eval results into a bootstrapped confidence interval.

This is the bridge from a raw eval run to a *decision*: instead of reporting a
bare mean score, :func:`score_ci` reports the mean with a confidence interval,
so you can ask whether the interval excludes a threshold you care about.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from gnomon.stats import BootstrapResult, bootstrap_ci
from gnomon.types import EvalResult


def score_ci(
    results: Sequence[EvalResult],
    *,
    confidence_level: float = 0.95,
    n_resamples: int = 10_000,
    random_state: int | None = None,
) -> BootstrapResult:
    """Bootstrap a confidence interval for the mean score of ``results``.

    Parameters
    ----------
    results
        Scored eval results. Every result must have a non-``None`` ``score``
        (i.e. the run was executed with a judge).
    confidence_level
        Nominal coverage probability. Default: 0.95.
    n_resamples
        Number of bootstrap resamples. Default: 10,000.
    random_state
        Seed for reproducibility.

    Returns
    -------
    BootstrapResult
        ``point_estimate`` is the observed mean score.

    Raises
    ------
    ValueError
        If any result is unscored, or there are fewer than two results.
    """
    scores: list[float] = []
    for r in results:
        if r.score is None:
            raise ValueError(
                "score_ci requires every result to be scored; "
                "run the eval with a judge"
            )
        scores.append(r.score)

    if len(scores) < 2:
        raise ValueError("score_ci needs at least two scored results to bootstrap a CI")

    return bootstrap_ci(
        scores,
        statistic=lambda a: float(np.mean(a)),
        confidence_level=confidence_level,
        n_resamples=n_resamples,
        random_state=random_state,
    )
