"""LLM-as-judge scoring for eval outputs.

Defines the :class:`Judge` protocol and :class:`LLMJudge`, a minimal judge that
asks a Claude model to grade an output. Judge *calibration* — Cohen's kappa,
Krippendorff's alpha, agreement matrices — is a separate, later concern; this
is just the scorer.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from gnomon.types import EvalCase

if TYPE_CHECKING:
    from anthropic import Anthropic

DEFAULT_MAX_TOKENS = 1024

_SYSTEM = (
    "You are a strict, fair evaluator of AI assistant outputs. Decide whether "
    "the output correctly and adequately answers the task. Reason briefly "
    "first, then give your verdict."
)

# reasoning before passed: the model fills fields in order, so it reasons
# before committing to a verdict.
_VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string"},
        "passed": {"type": "boolean"},
    },
    "required": ["reasoning", "passed"],
    "additionalProperties": False,
}


@runtime_checkable
class Judge(Protocol):
    """Scores an agent's output for a single eval case.

    The score is a float — by convention in [0.0, 1.0], higher is better. A
    binary judge returns 0.0 or 1.0; the mean of those is a pass rate.
    """

    name: str

    def score(self, case: EvalCase, output: str) -> float: ...


def _build_prompt(case: EvalCase, output: str) -> str:
    parts = [f"# Task\n{case.input}"]
    if case.expected is not None:
        parts.append(f"# Reference answer\n{case.expected}")
    parts.append(f"# Output to evaluate\n{output}")
    return "\n\n".join(parts)


class LLMJudge:
    """A :class:`Judge` that grades outputs with a Claude model.

    Each :meth:`score` call is one stateless ``messages.create`` request using
    structured outputs to force a JSON verdict. Returns ``1.0`` if the model
    judges the output as passing, ``0.0`` otherwise.

    Parameters
    ----------
    model
        Claude model ID to judge with. Structured outputs must be supported.
    name
        Judge name surfaced on ``EvalRun``. Defaults to ``"llm-judge:<model>"``.
    max_tokens
        Output token ceiling per request.
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
        name: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        api_key: str | None = None,
        client: Anthropic | None = None,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.name = name or f"llm-judge:{model}"

        if client is None:
            try:
                from anthropic import Anthropic
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "LLMJudge requires the 'anthropic' package. "
                    "Install it with: pip install gnomon-eval[anthropic]"
                ) from exc
            client = Anthropic(api_key=api_key)
        self._client = client

    def score(self, case: EvalCase, output: str) -> float:
        """Grade ``output`` against ``case`` and return 1.0 (pass) or 0.0 (fail)."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=_SYSTEM,
            messages=[{"role": "user", "content": _build_prompt(case, output)}],
            output_config={
                "format": {"type": "json_schema", "schema": _VERDICT_SCHEMA}
            },
        )
        text = next(block.text for block in response.content if block.type == "text")
        verdict = json.loads(text)
        return 1.0 if verdict["passed"] else 0.0
