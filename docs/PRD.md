# Gnomon — Product Requirements Document

**Version:** 0.3
**Owner:** Ashwath
**Last updated:** 2026-05-09
**Status:** Active — guides V1 build

---

## 1. Problem

LLM eval tooling reports point estimates without uncertainty. Teams ship changes based on differences within noise. Power analysis is absent. Judge calibration is ignored. Result: confident decisions on insufficient evidence.

## 2. Thesis

Most eval tools give you a number. Gnomon gives you a **decision** — with confidence intervals, power analysis, and judge calibration as first-class features.

**Tagline:** *From eval numbers to ship decisions.*

## 3. Positioning — the three-layer stack

| Layer | Role | Examples |
|-------|------|----------|
| Discover | What concerning behaviors does this model exhibit? | Anthropic Petri |
| Quantify | How often does behavior X occur? | Anthropic Bloom, benchmark suites |
| **Decide** | **Is v2 significantly better than v1? Am I powered?** | **Gnomon** |

Gnomon is the statistical decision layer. It runs native evals or ingests results from upstream tools, then produces calibrated **ship / don't ship / underpowered** recommendations.

## 4. Target users (V1)

- **AI engineers shipping agents to production** — primary
- ML teams making ship/no-ship calls on eval deltas
- Researchers who need to know if their result is real

**Explicit non-users for V1:** hyperscale workloads (>1M samples), multi-tenant SaaS, real-time production telemetry.

## 5. V1 scope — FROZEN. Six features.

1. **Eval runner** — `Agent` protocol + native runner + transcript ingestor (Bloom JSONL, Inspect logs, raw JSONL)
2. **Bootstrapped CIs** — on aggregate scores; configurable resamples
3. **Power analysis** — sample size recommendation given effect size + α + power
4. **Judge calibration** — Cohen's κ, Krippendorff's α, Spearman with bootstrapped CIs, bucketed agreement matrix; recommendation: "your judge correlates X — for ship-decisions on differences <Y points, this is insufficient"
5. **A/B harness** — paired comparison with bootstrapped CIs on the *difference*; sequential testing (alpha-spending); pre-run power analysis
6. **Storage + reports** — SQLite + HTML + machine-readable JSON + markdown executive summary leading with **Decision: SHIP / DON'T SHIP / UNDERPOWERED**

## 6. Out of scope for V1 (V2 backlog)

Distribution shift detection · reward model patterns · multi-judge ensembling · Bayesian A/B · multi-arm bandit · Bloom adapter (full) · Petri adapter · Streamlit dashboard · agent-trace eval primitives (tool-use scoring, multi-step) · sabotage / reward-hacking detection patterns.

**If it's not in §5, it does not get built before alpha.**

## 7. Tech

- Python 3.11+, packaged with `pyproject.toml` (hatchling)
- SQLite (stdlib)
- Anthropic SDK (primary provider), OpenAI SDK (secondary), HTTPAgent (universal — covers Foundry, Copilot Studio published agents, any HTTP-reachable target)
- pytest, ruff, mypy
- GitHub Actions CI

**Agent abstraction (V1):**
- `Agent` Protocol — `name: str`, `run(input: str) -> str`
- Adapters: `AnthropicAgent`, `OpenAIAgent`, `HTTPAgent`

**Storage schema (V1):** `runs`, `cases`, `results` tables — every record carries a `source` field (`native | bloom | petri | inspect | custom`) for lineage.

**Dataset format:** JSONL, schema-versioned. Generic enough to hold any input/output pairs from any platform.

## 8. Success metrics

- `pip install gnomon-eval` works on macOS + Linux (PyPI namespace `gnomon` is squatted by an abandoned 2012 placeholder; reclaim filed in parallel)
- README quickstart → first eval result in <5 minutes
- 3 real users running real evals before v1.0 tag
- 1 published methodology blog post with case-study numbers
- CI green on every commit to `main`

## 9. Milestones

| ID | Date | Deliverable |
|----|------|-------------|
| M1 | 2026-05-31 | Repo scaffolded, `Agent` protocol, eval-runner skeleton, SQLite schema, CI green |
| M2 | 2026-06-30 | Bootstrapped CIs end-to-end, first working eval against Claude (Anthropic adapter live) |
| M3 | 2026-07-31 | Power analysis + judge calibration shipped |
| M4 | 2026-08-31 | A/B harness + HTML reports → **working alpha** |
| M5 | 2026-09-15 | Docs pass, alpha tag on PyPI, first 3 users identified |
| — | CAPE start (~2026-09) | Maintenance mode |
| v1.0 | 2027-02 | First blog post live, v1 tagged |
| v2.0 | 2027-06 | V2 features |

## 10. Risks & mitigations

- **Scope creep** (documented tendency) → V2 backlog file gets every "wouldn't it be cool if" idea. PRD frozen until alpha.
- **USCIS resolves → CAPE start kills morning hours** → maintenance-mode definition pre-written so transition is mechanical.
- **No users at alpha** → identify first 3 by M3, not at v1.0. Cold-DM AI engineers in network now.
- **Statistical correctness bugs** → every stats feature ships with a property-based test against a known reference (scipy or R).
- **Overlap with Bloom/Petri** → mitigated by clear positioning as decision layer (§3); audit at M2 against Bloom's then-current feature set.

## 11. IP / employment guardrails

- **Public from day one.** All commits on a public GitHub repo under personal handle, MIT-licensed.
- **No customer data, ever.** Synthetic datasets and public benchmarks only.
- **Disclose at MSFT onboarding.** Pre-existing personal IP; preserved under standard pre-existing-IP clause.
- **No proselytizing at work.** Use, don't pitch.
- **No Microsoft-specific code paths.** Platform neutrality is the symbiosis.

## 12. Foundation

Gnomon operationalizes:
- Hashimoto et al., "A statistical approach to model evaluations" (Anthropic, Nov 2024)

Complementary to:
- [Petri](https://github.com/safety-research/petri) — automated auditing
- [Bloom](https://github.com/safety-research/bloom) — automated behavioral evaluation
