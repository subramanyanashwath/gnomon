from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Agent(Protocol):
    """Generic agent interface: input string -> output string.

    V1 adapters: AnthropicAgent, OpenAIAgent, HTTPAgent.
    HTTPAgent is the universal escape hatch — anything reachable
    over HTTP (including Microsoft Foundry endpoints and Copilot Studio
    published agents) can be wrapped in it.
    """

    name: str

    def run(self, input: str) -> str: ...
