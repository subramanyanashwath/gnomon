# ADR-0004: Gnomon joins PeaRL

**Status:** Accepted
**Date:** 2026-09-03
**Author:** Ashwath

## Context

Gnomon established a clear and tested thesis: evaluation numbers become useful
only when uncertainty, experimental design, statistical power, and judge
reliability are connected to a decision. Its existing bootstrap and power
primitives, single-turn evaluation code, provider adapter, and storage layer
are useful work and must retain their provenance.

PeaRL broadens the system around that thesis. It represents workflows as
executable environments, samples reproducible Scenario distributions, executes
Policies, records multi-step Trajectories, evaluates decomposed dimensions,
analyzes conditional Failure Distributions, and improves PolicyConfigs through
bounded search with held-out confirmation.

Maintaining Gnomon and PeaRL as competing flagship products would split the
architecture and obscure where statistical inference belongs in the larger
experimental loop.

## Decision

PeaRL supersedes Gnomon as the flagship technical project.

Gnomon's statistical thesis remains unchanged:

> From eval numbers to ship decisions.

Gnomon becomes PeaRL's statistical inference and experiment-decision subsystem
under the Python namespace:

```python
pearl.gnomon
```

The first migration copies the tested bootstrap and independent-proportion
power primitives into PeaRL without rewriting their frozen result dataclasses
or changing their API semantics. Later PeaRL milestones add design-aware paired
comparison, judge calibration, Hard Gate handling, and structured Verdicts.

Legacy Gnomon `Agent`, `EvalCase`, `EvalResult`, `EvalRun`, `Judge`, runner, and
SQLite concepts remain available as provenance and compatibility inputs. They
do not become dependencies of PeaRL's core Environment, Policy, Trajectory, or
Evaluation abstractions.

## Consequences

- This repository remains public and intact as historical provenance.
- Its git history is not rewritten.
- Its README is not redirected and the repository is not archived until PeaRL
  v1.0 is demonstrably functioning.
- Tested statistical code is migrated with MIT attribution.
- Existing independent-proportion power functions remain valid only for their
  documented designs; they must not be presented as paired-replay power
  analysis.
- Gnomon's planned generalized sequential testing is deferred from PeaRL v1 in
  favor of pre-specified samples, paired replay, held-out confirmation, and
  explicit power reporting.
- Search or validation evidence used to select a candidate cannot later be
  described as independent confirmation evidence.

## Alternatives considered

### Continue both projects as separate flagships

Rejected. It would duplicate evaluation and reporting concepts and make the
ownership of statistical decisions ambiguous.

### Rewrite Gnomon into PeaRL-native models immediately

Rejected. Rewriting tested statistical primitives or forcing legacy objects
into new domain models creates risk without adding product value.

### Archive Gnomon immediately

Rejected. PeaRL must first demonstrate a functioning replacement and preserve
an inspectable provenance trail.
