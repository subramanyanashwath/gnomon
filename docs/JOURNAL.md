# Gnomon Journal

Build log. One entry per milestone or significant event. Brief, honest, dated. New entries go on top.

---

## 2026-05-09 — M1 shipped

Scaffolded the repository from scratch in a single working session. Decided the brand, structure, and PRD before writing a line of production code — an inversion of the more common "code first, document later" pattern that I expect to pay back across M2–M5.

**Shipped**
- Public repo at github.com/subramanyanashwath/gnomon, MIT-licensed, CI green on first push (21 seconds)
- PRD v0.3 with V1 scope frozen at six features (`docs/PRD.md`)
- `Agent` Protocol, `EvalRunner` skeleton, SQLite schema with a `source` field for ingest lineage (native / bloom / petri / inspect / custom)
- 19 files, 641 insertions, 6 passing tests, ruff clean
- Profile + repo polish: 8 topics, 4 README badges, bio + name + company

**Decided**
- Named the project Gnomon, after a brief Aletheia detour. See [`decisions/0001-naming.md`](decisions/0001-naming.md).
- pip distribution name is `gnomon-eval` (the PyPI `gnomon` slot is squatted by an abandoned 2012 placeholder; reclaim filed in parallel). Brand and import name remain `gnomon`. Pattern matches `scikit-learn` → `import sklearn`.

**Studied for inspiration** (folded into the PRD as north-star references)
- Anthropic's Bloom blog post — TL;DR-led structure, comparative plots up front, honest limitations section as non-negotiable
- Inspect AI (UK AISI) — clean Python API design, interactive log viewer (the precedent for our M4 HTML report)
- HELM (Stanford CRFM) — multidimensional results presentation
- Thariq, "Unreasonable Effectiveness of HTML" — promoted HTML to primary report format in V1 §6, demoted markdown to optional

**Next (M2, due 2026-06-30):** bootstrapped confidence intervals end-to-end, plus the first real eval against Claude through the Anthropic adapter. Every statistical primitive must ship with a property-based test against a scipy or R reference. The point of M2 is not throughput; it is correctness.

**Reflection.** The temptation to jump into M2 features during M1 was real and present throughout. The PRD scope-freeze held — partly because it was written down, partly because the M1 deliverable was small enough to hold the whole boundary of in one head. A useful pattern: a milestone you can mentally hold the whole boundary of is a milestone whose scope you tend to keep.
