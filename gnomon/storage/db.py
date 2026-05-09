from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path

from gnomon.storage.schema import ALL_TABLES, CREATE_INDEXES
from gnomon.types import EvalCase, EvalResult, EvalRun


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    for stmt in ALL_TABLES:
        conn.execute(stmt)
    for stmt in CREATE_INDEXES:
        conn.execute(stmt)
    conn.commit()


def insert_run(conn: sqlite3.Connection, run: EvalRun) -> None:
    conn.execute(
        """
        INSERT INTO runs (id, name, agent_name, judge_name, source, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run.id,
            run.name,
            run.agent_name,
            run.judge_name,
            run.source,
            json.dumps(run.metadata) if run.metadata else None,
            run.created_at.isoformat(),
        ),
    )
    conn.commit()


def insert_cases(
    conn: sqlite3.Connection,
    run_id: str,
    cases: Iterable[EvalCase],
) -> int:
    rows = [
        (
            c.id,
            run_id,
            c.input,
            c.expected,
            json.dumps(c.metadata) if c.metadata else None,
        )
        for c in cases
    ]
    conn.executemany(
        "INSERT INTO cases (id, run_id, input, expected, metadata) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    return len(rows)


def insert_results(
    conn: sqlite3.Connection,
    run_id: str,
    results: Iterable[EvalResult],
) -> int:
    rows = [
        (
            r.id,
            run_id,
            r.case_id,
            r.agent_name,
            r.output,
            r.score,
            r.source,
            json.dumps(r.metadata) if r.metadata else None,
            r.created_at.isoformat(),
        )
        for r in results
    ]
    conn.executemany(
        """
        INSERT INTO results
            (id, run_id, case_id, agent_name, output, score, source, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)
