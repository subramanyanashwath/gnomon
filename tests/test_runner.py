from gnomon.eval.runner import EvalRunner
from gnomon.types import EvalCase, EvalResult


class _EchoAgent:
    name = "echo"

    def run(self, input: str) -> str:
        return f"echo: {input}"


class _LengthJudge:
    """Judge that scores 1.0 when the output is non-empty, 0.0 otherwise."""

    name = "length-judge"

    def __init__(self) -> None:
        self.seen: list[tuple[str, str]] = []

    def score(self, case: EvalCase, output: str) -> float:
        self.seen.append((case.input, output))
        return 1.0 if output else 0.0


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


def test_runner_without_judge_leaves_score_unset() -> None:
    runner = EvalRunner(agent=_EchoAgent())
    results = runner.run([EvalCase(input="hello")])
    assert results[0].score is None
    assert runner.run_meta.judge_name is None


def test_runner_with_judge_scores_each_result() -> None:
    judge = _LengthJudge()
    runner = EvalRunner(agent=_EchoAgent(), judge=judge)
    results = runner.run([EvalCase(input="a"), EvalCase(input="b")])

    assert [r.score for r in results] == [1.0, 1.0]
    assert runner.run_meta.judge_name == "length-judge"


def test_runner_passes_case_and_output_to_judge() -> None:
    judge = _LengthJudge()
    runner = EvalRunner(agent=_EchoAgent(), judge=judge)
    runner.run([EvalCase(input="hello")])

    assert judge.seen == [("hello", "echo: hello")]


def test_runner_results_are_eval_results() -> None:
    runner = EvalRunner(agent=_EchoAgent(), judge=_LengthJudge())
    results = runner.run([EvalCase(input="x")])
    assert isinstance(results[0], EvalResult)
