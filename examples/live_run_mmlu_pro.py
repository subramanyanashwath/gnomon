"""M2 live run: evaluate a Claude model on an MMLU-Pro subset, end to end.

The first real eval through the full Gnomon pipeline: public benchmark
questions -> AnthropicAgent (real API) -> LLMJudge (real API) -> score_ci ->
a ship / don't-ship / underpowered verdict, persisted to SQLite.

Usage::

    export ANTHROPIC_API_KEY=sk-ant-...
    python examples/live_run_mmlu_pro.py [--n 50] [--threshold 0.5]

Questions are fetched once from the Hugging Face datasets server (TIGER-Lab/
MMLU-Pro, test split) and cached at ``examples/data/mmlu_pro_subset.json`` so
reruns are reproducible and offline.
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
import urllib.request
from pathlib import Path

from gnomon import bootstrap_ci  # noqa: F401  (re-exported API smoke check)
from gnomon.agents.anthropic_agent import AnthropicAgent
from gnomon.eval.aggregate import score_ci
from gnomon.eval.judge import LLMJudge
from gnomon.eval.runner import EvalRunner
from gnomon.storage.db import connect, init_db, insert_cases, insert_results, insert_run
from gnomon.types import EvalCase

HF_ROWS_URL = (
    "https://datasets-server.huggingface.co/rows"
    "?dataset=TIGER-Lab%2FMMLU-Pro&config=default&split=test&offset={offset}&length={length}"
)
# Spread offsets across the ~12k-row test split so the sample isn't one category.
FETCH_OFFSETS = [0, 2000, 4000, 6000, 8000]
SEED = 42

AGENT_SYSTEM = (
    "You are answering a multiple-choice question. Reason step by step, then "
    "give your final answer on its own last line in exactly the form "
    "'Answer: <letter>'."
)


def fetch_subset(cache_path: Path, n: int) -> list[dict]:
    """Return ``n`` MMLU-Pro test rows, fetching and caching on first use."""
    if cache_path.exists():
        rows = json.loads(cache_path.read_text())
        if len(rows) >= n:
            return rows[:n]

    pool: list[dict] = []
    per_offset = max(n // len(FETCH_OFFSETS) * 2, 20)
    for offset in FETCH_OFFSETS:
        url = HF_ROWS_URL.format(offset=offset, length=per_offset)
        with urllib.request.urlopen(url, timeout=30) as resp:
            payload = json.load(resp)
        pool.extend(item["row"] for item in payload["rows"])

    rows = random.Random(SEED).sample(pool, n)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(rows, indent=2))
    return rows


def to_case(row: dict) -> EvalCase:
    letters = string.ascii_uppercase
    options = "\n".join(f"{letters[i]}. {opt}" for i, opt in enumerate(row["options"]))
    answer_letter = row["answer"]
    answer_text = row["options"][row["answer_index"]]
    return EvalCase(
        input=f"{row['question']}\n\n{options}",
        expected=f"{answer_letter}. {answer_text}",
        metadata={"category": row.get("category", "unknown"), "benchmark": "mmlu-pro"},
    )


def verdict(ci, threshold: float) -> str:
    if ci.low > threshold:
        return "SHIP"
    if ci.high < threshold:
        return "DON'T SHIP"
    return "UNDERPOWERED"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=50, help="number of questions")
    parser.add_argument("--agent-model", default="claude-haiku-4-5")
    parser.add_argument("--judge-model", default="claude-sonnet-4-6")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="pass-rate bar the CI is tested against",
    )
    parser.add_argument("--db", default="examples/runs.db")
    args = parser.parse_args()

    here = Path(__file__).parent
    rows = fetch_subset(here / "data" / "mmlu_pro_subset.json", args.n)
    cases = [to_case(r) for r in rows]
    print(f"{len(cases)} MMLU-Pro cases ready", flush=True)

    agent = AnthropicAgent(args.agent_model, system=AGENT_SYSTEM)
    judge = LLMJudge(args.judge_model)
    runner = EvalRunner(agent, judge=judge, name=f"m2-live-mmlu-pro-{args.agent_model}")

    results = []
    for i, case in enumerate(cases, 1):
        results.extend(runner.run([case]))
        print(f"  [{i}/{len(cases)}] score={results[-1].score}", flush=True)

    ci = score_ci(results, random_state=SEED)
    call = verdict(ci, args.threshold)

    conn = connect(args.db)
    init_db(conn)
    runner.run_meta.metadata.update(
        {
            "benchmark": "mmlu-pro",
            "n": len(results),
            "threshold": args.threshold,
            "pass_rate": ci.point_estimate,
            "ci_low": ci.low,
            "ci_high": ci.high,
            "confidence_level": ci.confidence_level,
            "verdict": call,
        }
    )
    insert_run(conn, runner.run_meta)
    insert_cases(conn, runner.run_meta.id, cases)
    insert_results(conn, runner.run_meta.id, results)

    print()
    print(f"agent      : {args.agent_model}")
    print(f"judge      : {args.judge_model}")
    print(f"n          : {len(results)}")
    print(f"pass rate  : {ci.point_estimate:.3f}")
    print(f"95% CI     : [{ci.low:.3f}, {ci.high:.3f}]")
    print(f"threshold  : {args.threshold}")
    print(f"VERDICT    : {call}")
    print(f"persisted  : run {runner.run_meta.id} -> {args.db}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
