# Gnomon

> From eval numbers to ship decisions.

Statistical rigor for LLM agent evaluation. Bootstrapped confidence intervals, power analysis, and judge calibration as first-class features — so an eval result becomes a decision, not just a number.

## Status

Pre-alpha. Building toward v1.0 (Q1 2027). Not ready for production use.

## Why

Most LLM eval tools report point estimates without uncertainty. Teams ship changes based on differences within noise. Power analysis is absent. Judge calibration is ignored. Gnomon is the missing statistical decision layer.

## Where Gnomon fits

**Discover → Quantify → Decide**

| Layer | Tools | Question |
|-------|-------|----------|
| Discover | Anthropic [Petri](https://github.com/safety-research/petri), audit tools | What concerning behaviors does this model exhibit? |
| Quantify | Anthropic [Bloom](https://github.com/safety-research/bloom), benchmark suites | How often does behavior X occur, and at what severity? |
| **Decide** | **Gnomon** | Is v2 significantly better than v1? Am I powered to detect a meaningful effect? |

Gnomon ingests eval results from any of the above (or runs its own) and produces a calibrated **ship / don't ship / underpowered** recommendation.

## Roadmap (V1)

1. **Eval runner** — agent + cases → scored results
2. **Bootstrapped CIs** on aggregate metrics
3. **Power analysis** — sample size recommendations given effect size + α
4. **Judge calibration** — Cohen's κ, Krippendorff's α, bucketed agreement
5. **A/B harness** — paired comparison with sequential testing
6. **Storage + reports** — SQLite + HTML/markdown executive summary

V2: distribution shift, Bloom/Petri/Inspect ingestion, Bayesian A/B, agent-trace eval primitives.

See [docs/PRD.md](docs/PRD.md) for the full product requirements document.

## Foundation

Gnomon operationalizes the methodology of:
- Hashimoto et al., ["A statistical approach to model evaluations"](https://www.anthropic.com/news/statistical-approach-to-model-evals) (Anthropic, Nov 2024)

## Audience

AI engineers shipping agents to production who need calibrated decisions, not just point estimates.

## License

MIT. © 2026 Ashwath.
