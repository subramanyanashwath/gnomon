# ADR-0003: Steering response to first-party enterprise test harnesses (Power CAT Copilot Studio Kit)

**Status:** Accepted
**Date:** 2026-07-02
**Author:** ashwath s

## Context

Reviewed the [Power CAT Copilot Studio Kit](https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit)
(Microsoft first-party, open source): a batch test harness for Copilot Studio agents —
response/topic/attachment match, multi-turn tests, LLM-rubric grading via AI Builder — plus
compliance, governance, and telemetry tooling. Its results analysis computes success-rate
percentages and average latency. Checked explicitly against its README and
`ANALYZE_TEST_RESULTS.md`: **no** confidence intervals, statistical significance, sample-size
guidance, power analysis, judge/rubric reliability measurement, run-to-run comparison, or
uncertainty quantification of any kind. Generative-answer results ship as *"AI-generated
assessment of the response. Please review."*

The question: does a mature first-party harness in the maintainer's future employer's
ecosystem change Gnomon's steering?

## Decision

**No rescope.** The Kit occupies the runner/judging layers and stops exactly where Gnomon
begins; it is evidence for the PRD §1 thesis (point estimates without uncertainty, shipped
as results), not competition for the decision layer. Steering sharpens in four ways:

1. **The runner is plumbing, not product.** First-party harnesses (this Kit, Inspect,
   promptfoo, commercial SaaS) win the runner category everywhere. V1 feature 1 gets no
   investment beyond what ingestion requires.
2. **Generic ingest is the enterprise on-ramp.** Kits like this are upstream data sources:
   they emit case-level pass/fail results; Gnomon ingests and decides. Within feature 1,
   prioritize and document the generic path — case-level results as JSONL/CSV with a minimal
   column mapping. Platform-neutral, per the hard rule; no vendor named in the codebase.
3. **Judge calibration is the killer feature for the rubric-harness world.** The Kit ships a
   rubric-refinement loop with no measurement of rubric-judge reliability. Gnomon's M3
   calibration output ("your judge agrees κ=X; insufficient for ship decisions on deltas
   < Y") is the missing piece of the entire category. The M3 methodology post critiques the
   *pattern* ("match tests + LLM rubrics + a success percentage"), and must not name the
   Kit or any vendor product — the maintainer is onboarding into Microsoft (PRD §11:
   use, don't pitch).
4. **The real novelty risk is upstream, not first-party kits.** Inspect already reports
   standard errors; Hashimoto et al. is Anthropic's own methods paper — either could
   productize the decision layer. Mitigation: speed (v0.1.0 on schedule or earlier) and
   depth (calibration, power, sequential testing go far past aggregate stderr). Extend the
   PRD §10 overlap audit beyond Bloom to Inspect's statistics features at each milestone.

## What must not change

- No Copilot Studio / Power Platform integrations, no governance/compliance/telemetry
  features. Employer's commercial surface (see also ADR-0002); also dilutes the one layer
  nobody else ships.
- No runner feature-matching against harness products.

## Consequences

Execution queue unchanged. Adds two small, non-scope items: a documented generic-ingest
example (within existing feature 1) and the no-vendor-naming constraint on the M3
methodology post.

---

**Related:** [`0002-scope-response-satya-mfc.md`](0002-scope-response-satya-mfc.md) ·
[`PRD.md`](../PRD.md) §1 (problem) · §5.1 (ingestor) · §10 (overlap risk) · §11 (guardrails)
