# Gnomon — context for Claude Code sessions

This file auto-loads when Claude Code opens a session in this repo. Read it before doing anything substantive. The full PRD lives at `docs/PRD.md`; the milestone log at `docs/JOURNAL.md`; decision records at `docs/decisions/`.

## What Gnomon is

Open-source Python library: the **statistical decision layer for LLM agent evaluation**. Bootstrapped CIs, power analysis, and judge calibration as first-class features.

Tagline: *From eval numbers to ship decisions.*

Public at https://github.com/subramanyanashwath/gnomon · MIT · `pip install gnomon-eval` (then `import gnomon`; pip name differs because the PyPI `gnomon` slot is squatted by an abandoned 2012 placeholder — reclaim filed in parallel).

## Three-layer positioning — do not muddy this

**Discover** (Anthropic Petri) → **Quantify** (Anthropic Bloom) → **Decide** (Gnomon).

Gnomon is the decision layer the others don't ship. Don't drift into discovery or quantification — those are upstream tools. Gnomon ingests their output (or runs its own evals) and produces calibrated **ship / don't ship / underpowered** recommendations.

## V1 scope — FROZEN. Six features.

1. Eval runner + Bloom/Inspect ingestor
2. Bootstrapped CIs on aggregate metrics
3. Power analysis (sample size from effect size + α + desired power)
4. Judge calibration (Cohen's κ, Krippendorff's α, bucketed agreement matrix)
5. A/B harness (paired comparison, sequential testing, pre-run power analysis)
6. SQLite storage + HTML executive summary (HTML primary, JSON secondary, markdown optional)

**If a request asks for something not in this list before alpha (M5, due 2026-09-15), push back.** V2 backlog lives in `docs/PRD.md` §6 — discuss freely, do not build.

## Hard rules

- **Platform-neutral.** No Microsoft-specific code paths. `HTTPAgent` is the universal escape hatch (covers Foundry, Copilot Studio, any HTTP-reachable target) without naming any of them in the codebase.
- **No customer data, ever.** Synthetic datasets and public benchmarks only.
- **HTML-first reports.** Per Thariq (May 2026): HTML conveys richer information than markdown and the audience is more likely to actually read it. Source files (PRD, README, this file) stay in markdown for git-diff sanity.
- **Statistical correctness over feature breadth.** Every stats feature ships with a property-based test against a known reference (scipy or R).
- **No scope creep.** This is a documented tendency for the maintainer. The PRD is the contract.

## North-star references

- **Inspect AI** (UK AISI) — API design + log viewer UX
- **Anthropic Bloom blog post** (Dec 2025) — methodology writing structure
- **Anthropic Petri** (Oct 2025) — auditing complement
- **Hashimoto et al., "A statistical approach to model evaluations"** (Anthropic, Nov 2024) — methodological foundation
- **HELM** (Stanford CRFM) — visual results presentation
- **Thariq, "Unreasonable Effectiveness of HTML"** (May 2026) — output format

## Milestones

| ID | Date | Status |
|----|------|--------|
| M1 | 2026-05-31 | ✅ Done (2026-05-09) |
| M2 | 2026-06-30 | Bootstrapped CIs + first real Anthropic eval |
| M3 | 2026-07-31 | Power analysis + judge calibration |
| M4 | 2026-08-31 | A/B harness + HTML reports → working alpha |
| M5 | 2026-09-15 | Docs pass, alpha tag on PyPI, first 3 users identified |
| v1.0 | 2027-02 | First blog post live, v1 tagged |
| v2.0 | 2027-06 | V2 features |

## Voice rules (apply to all writing produced from this repo)

- TL;DR upfront. Lead with the conclusion.
- Honest limitations section is non-negotiable. "Gnomon is bad at: X, Y, Z."
- Cite the lineage. Don't reinvent.
- Precise language: "95% bootstrapped CI" not "pretty confident."
- Calm, curious, specific. Not promotional, not academic-stuffy.

## Repo-local git identity

Committer is set repo-locally to `subramanyanashwath <250072341+subramanyanashwath@users.noreply.github.com>` so commits are properly attributed to the GitHub account without leaking machine hostnames. Do not change this.
