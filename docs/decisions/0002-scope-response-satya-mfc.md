# ADR-0002: Scope response to Satya's "frontier ecosystem" memo and the Microsoft Frontier Company announcement

**Status:** Accepted
**Date:** 2026-07-02
**Author:** ashwath s

## Context

Two Microsoft announcements landed in early July 2026:

1. **Satya Nadella's "A frontier without an ecosystem is not stable"** — a memo on human capital
   and token capital compounding inside a firm-owned learning loop. The load-bearing sentence
   for this project: *"Private evals should capture whether a model is actually improving
   against outcomes that matter to the business (not just external benchmarks!)."*
2. **Microsoft Frontier Company (Jul 2, 2026)** — a $2.5B operating business, 6,000 embedded
   industry and engineering experts, explicitly outcome-driven, built on a "model-diverse,
   open, heterogeneous AI platform."

The maintainer is onboarding into Microsoft (date immigration-gated, likely post-v0.1.0).
The question: does Gnomon need rescoping in light of these?

## Decision

**No rescope. V1 stays frozen at the six features in PRD §5.** What changes is narrative
framing, two V2 backlog entries, and urgency — not scope.

Three reasons:

1. **The memo validates the thesis; it does not change it.** Gnomon's §2 thesis — most tools
   give you a number, Gnomon gives you a decision — is exactly the statistical layer that
   "private evals against outcomes that matter" requires. A point estimate on a private eval
   is no more decision-grade than a point estimate on MMLU. The market just got named by the
   CEO of the company the maintainer is joining. The correct response to validation is to
   ship sooner, not to redesign.

2. **The existing guardrails were built for this exact world.** PRD §11 (platform neutrality,
   no Microsoft-specific code paths, HTTPAgent as the universal escape hatch, publish before
   onboarding) reads, in hindsight, like it was written with MFC in mind. MFC's own platform
   pitch is "model-diverse, open, heterogeneous" — a neutral OSS statistical layer fits that
   ethos; a Microsoft-flavored one would be redundant with Microsoft's own trust/observability
   platform and would poison the pre-existing-IP claim.

3. **Scope creep is the documented top risk (PRD §10), and a CEO memo naming your market is
   precisely the stimulus that triggers it.** The temptation is to bolt on "business outcome
   tracking" or "learning loop integration." Both belong to the employer's commercial surface
   (FinOps, observability, the trust platform), not to a statistics library. The PRD freeze
   is the mechanism; this ADR is the mechanism being used.

## What changes

**Narrative (docs only, zero code):**
- README and positioning language gain the *private evals* vocabulary: Gnomon is the
  statistical rigor layer for private evals — the thing that tells you whether "improving
  against outcomes that matter" is signal or noise. Cite the memo directly (voice rule:
  cite the lineage).
- One of the four planned methodology posts becomes the timely piece: private evals need
  confidence intervals, power analysis, and judge calibration, or they are vibes with a
  dashboard. Written to land near the v0.1.0 announcement while the memo is current.

**V2 backlog (PRD §6 — discuss, do not build):**
- *Longitudinal improvement tracking* — "is the model actually improving" is a
  repeated-measures question across runs, not a single-run question. Regression detection
  over a run series.
- *Outcome-metric ingestion* — joining eval scores against business outcome metrics the
  team already tracks, so the decision layer can be powered against the metric that matters
  rather than a proxy.

**Urgency:**
- Publish-before-onboard upgrades from goal to hard requirement. MFC makes enterprise AI
  evaluation commercially adjacent to the employer. The pre-existing-IP position is
  strongest with a public, tagged, pip-installable release predating day one. v0.1.0 target
  (~2026-08-10) stands; earlier is better.

## What must not change

- **No Microsoft-specific code paths** — now with more force, not less. No named Foundry or
  Copilot Studio adapters; `HTTPAgent` already covers any HTTP-reachable target anonymously.
- **No drift toward outcomes observability.** Gnomon consumes metrics and returns decisions.
  It does not collect, host, or dashboard production telemetry (explicit non-goal, PRD §4).

## Consequences

Execution queue is unchanged and unblocked, in order: (1) execute the M2 live run and record
the verdict; (2) M3 — power analysis + judge calibration, due 2026-07-31, now the critical
path; (3) v0.1.0 packaging + README with the private-evals framing; (4) methodology posts,
including the memo-reaction piece, at launch.

---

**Related:** [`PRD.md`](../PRD.md) §2 (thesis) · §6 (V2 backlog, updated by this ADR) ·
§10 (scope-creep risk) · §11 (IP / employment guardrails) ·
[`0001-naming.md`](0001-naming.md) (the previous "letting go" decision)
