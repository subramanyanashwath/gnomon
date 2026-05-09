SCHEMA_VERSION = 1

CREATE_RUNS_TABLE = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    judge_name TEXT,
    source TEXT NOT NULL DEFAULT 'native',
    metadata TEXT,
    created_at TEXT NOT NULL
)
"""

CREATE_CASES_TABLE = """
CREATE TABLE IF NOT EXISTS cases (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    input TEXT NOT NULL,
    expected TEXT,
    metadata TEXT
)
"""

CREATE_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS results (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    output TEXT NOT NULL,
    score REAL,
    source TEXT NOT NULL DEFAULT 'native',
    metadata TEXT,
    created_at TEXT NOT NULL
)
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_results_run_id ON results(run_id)",
    "CREATE INDEX IF NOT EXISTS idx_cases_run_id ON cases(run_id)",
]

ALL_TABLES = [CREATE_RUNS_TABLE, CREATE_CASES_TABLE, CREATE_RESULTS_TABLE]
