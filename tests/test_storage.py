from pathlib import Path

from gnomon.storage.db import connect, init_db, insert_cases, insert_results, insert_run
from gnomon.types import EvalCase, EvalResult, EvalRun


def test_init_db_creates_tables(tmp_path: Path) -> None:
    conn = connect(tmp_path / "test.db")
    init_db(conn)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row["name"] for row in cursor.fetchall()}
    assert {"runs", "cases", "results"}.issubset(tables)


def test_insert_run_and_results_roundtrip(tmp_path: Path) -> None:
    conn = connect(tmp_path / "test.db")
    init_db(conn)

    run = EvalRun(name="smoke", agent_name="fake")
    insert_run(conn, run)

    cases = [EvalCase(input="hello"), EvalCase(input="world")]
    n_cases = insert_cases(conn, run.id, cases)
    assert n_cases == 2

    results = [
        EvalResult(case_id=cases[0].id, agent_name="fake", output="o1", score=0.8),
        EvalResult(case_id=cases[1].id, agent_name="fake", output="o2", score=0.6),
    ]
    n = insert_results(conn, run.id, results)
    assert n == 2

    row = conn.execute("SELECT COUNT(*) AS n FROM results WHERE run_id = ?", (run.id,)).fetchone()
    assert row["n"] == 2

    row = conn.execute("SELECT name, source FROM runs WHERE id = ?", (run.id,)).fetchone()
    assert row["name"] == "smoke"
    assert row["source"] == "native"
