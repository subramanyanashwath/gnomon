from gnomon.eval.runner import EvalRunner
from gnomon.types import EvalCase


class _EchoAgent:
    name = "echo"

    def run(self, input: str) -> str:
        return f"echo: {input}"


def test_runner_smoke() -> None:
    runner = EvalRunner(agent=_EchoAgent())
    cases = [
        EvalCase(input="hello"),
        EvalCase(input="world"),
    ]
    results = runner.run(cases)
    assert len(results) == 2
    assert results[0].output == "echo: hello"
    assert results[1].output == "echo: world"
    assert all(r.agent_name == "echo" for r in results)
    assert all(r.source == "native" for r in results)


def test_runner_preserves_case_ids() -> None:
    runner = EvalRunner(agent=_EchoAgent())
    cases = [EvalCase(input="x"), EvalCase(input="y")]
    results = runner.run(cases)
    assert {r.case_id for r in results} == {c.id for c in cases}
