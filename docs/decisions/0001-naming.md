# ADR-0001: Naming — Aletheia → Gnomon

**Status:** Accepted
**Date:** 2026-05-09
**Author:** ashwath s

## Context

The project needed a name before going public. The internal codename throughout the strategic phase was **Gnomon**. During PRD drafting I briefly renamed it to **Aletheia** — Greek ἀλήθεια, *truth* or *disclosure* — because the philosophical framing (truth in evaluation) felt unusually clean.

Pre-publish due diligence on the Aletheia name surfaced four problems:

1. **DeepMind launched their own Aletheia in February 2026** as a flagship Gemini Deep Think math research agent. It autonomously solved four open Erdős conjectures and scored ~91.9% on IMO-ProofBench. Public repo at `google-deepmind/superhuman/tree/main/aletheia`. DeepMind explicitly framed the name as "a homage to the Greek goddess of Truth" — *exactly* the etymological framing I had in mind.
2. **Aletheia Framework™** (Rolls-Royce, OECD-cataloged) is a trademarked ethical AI governance framework.
3. **arXiv 2601.01532** — *"Aletheia: Quantifying Cognitive Conviction in Reasoning Models"* (Jan 2026) — a paper on judge calibration in reasoning models. Uncomfortably adjacent to Gnomon's V1 judge-calibration feature.
4. **`Youcef3939/aletheia`** on GitHub — an XAI explainability framework.

Four AI/ML projects with the same name, one of them a flagship Google effort and one of them on Gnomon's exact methodological territory. SEO and conversational disambiguation were already lost before the project had its first commit.

## Decision

Revert to **Gnomon**.

A gnomon is the upright piece of a sundial that casts the shadow used to measure time. It is also a Euclidean geometric figure: the L-shaped piece that, when added to a smaller square, completes a larger one. The Greek root γνώμων means *indicator* or *that which knows*.

Three semantic layers, all on-thesis for a statistical decision layer:

1. **Indicator.** A statistical metric is an indicator. A ship/no-ship recommendation is an indicator. The project's job is to be the indicator.
2. **Measurement through indirection.** A sundial does not measure the sun directly; it measures the shadow. LLM evaluation does not measure model behavior directly; it measures projections of it (outputs, traces, judge scores). Same epistemic shape.
3. **The completing piece.** In Euclidean geometry a gnomon is what you add to a square to make it larger. In the three-layer eval stack — Discover (Petri) → Quantify (Bloom) → Decide — Gnomon is the piece that completes the figure.

The naming triad becomes coherent: Petri (laboratory dish), Bloom (botanical growth), Gnomon (scientific instrument). Three different metaphor families, each tied to its layer's verb, all under the umbrella of scientific instruments.

## Verification

Before committing to the rename, the following were checked:

- **GitHub repo path** `github.com/subramanyanashwath/gnomon` — clear (HTTP 404, available)
- **GitHub Python repos named gnomon** — 22 total, all unrelated and small (max 12 stars: a sundial generator, a Flask time tracker, geographic projections, attribute metadata). Zero AI/ML/eval overlap.
- **AI/ML namespace search** — zero prominent project named Gnomon in AI, eval, or agents
- **PyPI `gnomon`** — technically taken by an abandoned 2012 placeholder (author `tunnell`, version 0.2, summary literally `"desc"`, linked to a 14-year-dormant 1-star GitHub repo at `nuSTORM/gnomon` last pushed 2012-10-30). PyPI's project-reclamation policy applies; reclaim filed in parallel. Until then the pip distribution name is **`gnomon-eval`**; brand and import name remain `gnomon`. The pattern matches `scikit-learn` → `import sklearn` and `opencv-python` → `import cv2`.

## Consequences

| Surface | Name |
|---------|------|
| Brand | Gnomon (everywhere — README, docs, talks, posts) |
| GitHub repo | `github.com/subramanyanashwath/gnomon` |
| Python import | `import gnomon` |
| pip install (initial) | `pip install gnomon-eval` |
| pip install (after PyPI reclaim succeeds) | `pip install gnomon` |
| Tagline | *From eval numbers to ship decisions.* (unchanged) |

The brief Aletheia detour cost roughly thirty minutes of review-and-rename. The cost of catching the name collision *after* a public release would have been larger by orders of magnitude: stars, forks, blog posts, search-engine indexing, conference references all attached to a name we would then have had to abandon.

## Honest acknowledgment

Aletheia is a more poetic name. Gnomon is a stronger one. The poetic name lost its meaning the moment Google attached it to a flagship product with the same etymological framing. The stronger name was always there, was the original codename, and rewards a five-second explanation with a memorable mental image. Letting go of the prettier name and keeping the more durable one is, recursively, the kind of decision Gnomon itself is designed to support.

---

**Related:** [`PRD.md`](../PRD.md) §3 (positioning) · [`README.md`](../../README.md) (top-level branding) · `project_gnomon.md` in Claude memory (full strategic context)
