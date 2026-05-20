from __future__ import annotations

import pytest

from gnomon.eval.aggregate import score_ci
from gnomon.eval.runner import EvalRunner
from gnomon.stats import BootstrapResult
from gnomon.types import EvalCase, EvalResult


def _results(*scores: float | None) -> list[EvalResult]:
    return [
        EvalResult(case_id=f"c{i}", agent_name="fake", output="o", score=s)
        for i, s in enumerate(scores)
    ]


def test_returns_bootstrap_result_with_mean_point_estimate() -> None:
    ci = score_ci(_results(1.0, 0.0, 1.0, 0.0), random_state=0)
    assert isinstance(ci, BootstrapResult)
    assert ci.point_estimate == 0.5


def test_all_pass_collapses_interval_to_one() -> None:
    ci = score_ci(_results(1.0, 1.0, 1.0, 1.0), random_state=0)
    assert ci.point_estimate == 1.0
    assert ci.low == 1.0
    assert ci.high == 1.0


def test_interval_brackets_the_point_estimate() -> None:
    ci = score_ci(_results(*([1.0] * 18 + [0.0] * 2)), random_state=0)
    assert ci.point_estimate == 0.9
    assert ci.low <= ci.point_estimate <= ci.high


def test_high_score_ci_excludes_a_low_threshold() -> None:
    ci = score_ci(_results(*([1.0] * 19 + [0.0])), random_state=0)
    assert ci.excludes(0.5)


def test_reproducible_with_random_state() -> None:
    data = _results(1.0, 0.0, 1.0, 1.0, 0.0, 1.0)
    a = score_ci(data, random_state=42)
    b = score_ci(data, random_state=42)
    assert (a.low, a.high) == (b.low, b.high)


def test_raises_on_unscored_result() -> None:
    with pytest.raises(ValueError, match="scored"):
        score_ci(_results(1.0, None, 1.0))


def test_raises_on_too_few_results() -> None:
    with pytest.raises(ValueError, match="at least two"):
        score_ci(_results(1.0))


def test_end_to_end_runner_to_ci() -> None:
    class _Agent:
        name = "echo"

        def run(self, input: str) -> str:
            return input

    class _PassNonEmpty:
        name = "non-empty-judge"

        def score(self, case: EvalCase, output: str) -> float:
            return 1.0 if output else 0.0

    runner = EvalRunner(agent=_Agent(), judge=_PassNonEmpty())
    cases = [EvalCase(input=f"q{i}") for i in range(5)]
    results = runner.run(cases)

    ci = score_ci(results, random_state=0)
    assert ci.point_estimate == 1.0
