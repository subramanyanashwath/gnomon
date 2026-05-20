from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from gnomon.agents import AnthropicAgent
from gnomon.agents.base import Agent


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


def _client(*blocks: _Block) -> _FakeClient:
    return _FakeClient(_Response(list(blocks)))


def test_run_returns_concatenated_text() -> None:
    agent = AnthropicAgent("claude-opus-4-7", client=_client(_Block("text", "hello")))
    assert agent.run("hi") == "hello"


def test_run_joins_multiple_text_blocks_and_skips_non_text() -> None:
    client = _client(
        _Block("thinking", "internal reasoning"),
        _Block("text", "part one "),
        _Block("text", "part two"),
    )
    agent = AnthropicAgent("claude-opus-4-7", client=client)
    assert agent.run("hi") == "part one part two"


def test_satisfies_agent_protocol() -> None:
    agent = AnthropicAgent("claude-opus-4-7", client=_client(_Block("text", "x")))
    assert isinstance(agent, Agent)


def test_input_becomes_a_single_user_message() -> None:
    client = _client(_Block("text", "ok"))
    agent = AnthropicAgent("claude-sonnet-4-6", client=client)
    agent.run("what is 2+2?")

    call = client.messages.calls[0]
    assert call["model"] == "claude-sonnet-4-6"
    assert call["messages"] == [{"role": "user", "content": "what is 2+2?"}]
    assert call["max_tokens"] > 0


def test_system_prompt_omitted_when_unset() -> None:
    client = _client(_Block("text", "ok"))
    AnthropicAgent("claude-opus-4-7", client=client).run("hi")
    assert "system" not in client.messages.calls[0]


def test_system_prompt_sent_with_cache_control() -> None:
    client = _client(_Block("text", "ok"))
    agent = AnthropicAgent(
        "claude-opus-4-7", system="You are a math tutor.", client=client
    )
    agent.run("hi")

    system = client.messages.calls[0]["system"]
    assert system == [
        {
            "type": "text",
            "text": "You are a math tutor.",
            "cache_control": {"type": "ephemeral"},
        }
    ]


def test_name_defaults_to_model() -> None:
    agent = AnthropicAgent("claude-opus-4-7", client=_client(_Block("text", "x")))
    assert agent.name == "anthropic:claude-opus-4-7"


def test_name_can_be_overridden() -> None:
    agent = AnthropicAgent(
        "claude-opus-4-7", name="baseline", client=_client(_Block("text", "x"))
    )
    assert agent.name == "baseline"
