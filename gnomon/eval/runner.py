from __future__ import annotations

from collections.abc import Iterable

from gnomon.agents.base import Agent
from gnomon.types import EvalCase, EvalResult, EvalRun


class EvalRunner:
    """Run an agent against a set of eval cases.

    M1 skeleton: synchronous, no judge, no scoring. M2 wires in
    real provider calls and judge scoring.
    """

    def __init__(self, agent: Agent, name: str | None = None) -> None:
        self.agent = agent
        self.run_meta = EvalRun(
            name=name or f"run-{agent.name}",
            agent_name=agent.name,
        )

    def run(self, cases: Iterable[EvalCase]) -> list[EvalResult]:
        results: list[EvalResult] = []
        for case in cases:
            output = self.agent.run(case.input)
            results.append(
                EvalResult(
                    case_id=case.id,
                    agent_name=self.agent.name,
                    output=output,
                )
            )
        return results
