from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

Source = Literal["native", "bloom", "petri", "inspect", "custom"]


def _new_id() -> str:
    return uuid.uuid4().hex


def _utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass
class EvalCase:
    input: str
    expected: str | None = None
    id: str = field(default_factory=_new_id)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalResult:
    case_id: str
    agent_name: str
    output: str
    score: float | None = None
    id: str = field(default_factory=_new_id)
    source: Source = "native"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utcnow)


@dataclass
class EvalRun:
    name: str
    agent_name: str
    judge_name: str | None = None
    source: Source = "native"
    id: str = field(default_factory=_new_id)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utcnow)
