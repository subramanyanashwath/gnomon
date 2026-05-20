from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from gnomon.eval.judge import Judge, LLMJudge
from gnomon.types import EvalCase


@dataclass
class _Block:
    type: str
    text: str = ""


@dataclass
class _Response:
    content: list[_Block]


class _FakeMessages:
    def __init__(self, response: _Response) -> None:
        self._response = response
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> _Response:
        self.calls.append(kwargs)
        return self._response


@dataclass
class _FakeClient:
    response: _Response
    messages: _FakeMessages = field(init=False)

    def __post_init__(self) -> None:
        self.messages = _FakeMessages(self.response)


def _verdict_client(*, passed: bool, reasoning: str = "because") -> _FakeClient:
    payload = json.dumps({"reasoning": reasoning, "passed": passed})
    return _FakeClient(_Response([_Block("text", payload)]))


def test_score_returns_one_when_passed() -> None:
    judge = LLMJudge("claude-opus-4-7", client=_verdict_client(passed=True))
    assert judge.score(EvalCase(input="2+2?"), "4") == 1.0


def test_score_returns_zero_when_failed() -> None:
    judge = LLMJudge("claude-opus-4-7", client=_verdict_client(passed=False))
    assert judge.score(EvalCase(input="2+2?"), "5") == 0.0


def test_satisfies_judge_protocol() -> None:
    judge = LLMJudge("claude-opus-4-7", client=_verdict_client(passed=True))
    assert isinstance(judge, Judge)


def test_prompt_includes_task_and_output() -> None:
    client = _verdict_client(passed=True)
    judge = LLMJudge("claude-opus-4-7", client=client)
    judge.score(EvalCase(input="What is the capital of France?"), "Paris")

    content = client.messages.calls[0]["messages"][0]["content"]
    assert "What is the capital of France?" in content
    assert "Paris" in content


def test_prompt_includes_reference_when_expected_set() -> None:
    client = _verdict_client(passed=True)
    judge = LLMJudge("claude-opus-4-7", client=client)
    judge.score(EvalCase(input="2+2?", expected="4"), "4")

    content = client.messages.calls[0]["messages"][0]["content"]
    assert "Reference answer" in content
    assert "4" in content


def test_prompt_omits_reference_when_no_expected() -> None:
    client = _verdict_client(passed=True)
    judge = LLMJudge("claude-opus-4-7", client=client)
    judge.score(EvalCase(input="Write a haiku."), "An old silent pond...")

    content = client.messages.calls[0]["messages"][0]["content"]
    assert "Reference answer" not in content


def test_uses_structured_output_schema() -> None:
    client = _verdict_client(passed=True)
    judge = LLMJudge("claude-opus-4-7", client=client)
    judge.score(EvalCase(input="2+2?"), "4")

    fmt = client.messages.calls[0]["output_config"]["format"]
    assert fmt["type"] == "json_schema"
    assert fmt["schema"]["properties"].keys() == {"reasoning", "passed"}


def test_name_defaults_to_model() -> None:
    judge = LLMJudge("claude-opus-4-7", client=_verdict_client(passed=True))
    assert judge.name == "llm-judge:claude-opus-4-7"


def test_name_can_be_overridden() -> None:
    judge = LLMJudge(
        "claude-opus-4-7", name="reference-judge", client=_verdict_client(passed=True)
    )
    assert judge.name == "reference-judge"
