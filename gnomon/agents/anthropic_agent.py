"""Anthropic SDK adapter implementing the :class:`~gnomon.agents.base.Agent` protocol.

Lets a Claude model be used as an eval target. The ``anthropic`` package is an
optional dependency — install it with ``pip install gnomon-eval[anthropic]``.
The import is deferred to construction time so ``import gnomon`` works without it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from anthropic import Anthropic

DEFAULT_MAX_TOKENS = 4096


class AnthropicAgent:
    """An :class:`~gnomon.agents.base.Agent` backed by a Claude model.

    Each :meth:`run` call is one stateless ``messages.create`` request: the case
    input becomes a single user message and the model's text reply is returned.

    Parameters
    ----------
    model
        Claude model ID to evaluate (e.g. ``"claude-opus-4-7"``). Required — the
        whole point of the adapter is to pin the target under test.
    system
        Optional system prompt sent on every request. It is marked for prompt
        caching, since an eval reuses one system prompt across many cases.
    max_tokens
        Output token ceiling per request.
    name
        Agent name surfaced on ``EvalResult``. Defaults to ``"anthropic:<model>"``.
    api_key
        Anthropic API key. If omitted, the SDK reads ``ANTHROPIC_API_KEY``.
    client
        A pre-built ``anthropic.Anthropic`` client. Supplying one skips SDK
        construction entirely — used by tests to inject a fake.
    """

    def __init__(
        self,
        model: str,
        *,
        system: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        name: str | None = None,
        api_key: str | None = None,
        client: Anthropic | None = None,
    ) -> None:
        self.model = model
        self.system = system
        self.max_tokens = max_tokens
        self.name = name or f"anthropic:{model}"

        if client is None:
            try:
                from anthropic import Anthropic
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "AnthropicAgent requires the 'anthropic' package. "
                    "Install it with: pip install gnomon-eval[anthropic]"
                ) from exc
            client = Anthropic(api_key=api_key)
        self._client = client

    def run(self, input: str) -> str:
        """Send ``input`` as a user message and return the model's text reply."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": input}],
        }
        if self.system is not None:
            kwargs["system"] = [
                {
                    "type": "text",
                    "text": self.system,
                    "cache_control": {"type": "ephemeral"},
                }
            ]

        response = self._client.messages.create(**kwargs)

        return "".join(
            block.text for block in response.content if block.type == "text"
        )
