from __future__ import annotations

from collections.abc import Iterable

from gnomon.agents.base import Agent
from gnomon.eval.judge import Judge
from gnomon.types import EvalCase, EvalResult, EvalRun


class EvalRunner:
    """Run an agent against a set of eval cases.

    Synchronous and stateless per case. If a ``judge`` is supplied, every
    output is scored and the score lands on the :class:`~gnomon.types.EvalResult`;
    without one, results carry only the raw output (``score`` stays ``None``).
    """

    def __init__(
        self,
        agent: Agent,
        *,
        judge: Judge | None = None,
        name: str | None = None,
    ) -> None:
        self.agent = agent
        self.judge = judge
        self.run_meta = EvalRun(
            name=name or f"run-{agent.name}",
            agent_name=agent.name,
            judge_name=judge.name if judge is not None else None,
        )

    def run(self, cases: Iterable[EvalCase]) -> list[EvalResult]:
        results: list[EvalResult] = []
        for case in cases:
            output = self.agent.run(case.input)
            score = self.judge.score(case, output) if self.judge is not None else None
            results.append(
                EvalResult(
                    case_id=case.id,
                    agent_name=self.agent.name,
                    output=output,
                    score=score,
                )
            )
        return results
