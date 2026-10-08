# Decision Log

This directory contains Architecture Decision Records (ADRs) documenting significant project decisions that affect scope, architecture, data, ML methodology, infrastructure, or other long-lived project behavior.

The decision log is intended to preserve **why** a decision was made, the evidence supporting it, and the conditions under which it should be reconsidered.

It is **not** a daily project diary or a record of every implementation choice.

## Decision Index

| ID | Decision                  | Status | Area | Date |
| -- | ------------------------- | ------ | ---- | ---- |
| —  | No decisions recorded yet | —      | —    | —    |

New decisions should be added to this index when an ADR is created.

## When to Create an ADR

Create an ADR when a decision:

* Has meaningful impact on project scope, architecture, data, ML methodology, infrastructure, or system behavior.
* Has multiple reasonable alternatives or trade-offs.
* May need to be revisited later.
* Would be difficult for a future contributor to understand without knowing the reasoning behind it.

Do not create an ADR for routine implementation details, temporary experiments, or decisions that are already obvious from the code.

## ADR Naming

Use the following naming convention:

```text
NNNN-short-decision-name.md
```

Examples:

```text
0001-define-risk-stratification-as-primary-use-case.md
0002-select-model-evaluation-metrics.md
0003-choose-model-serving-architecture.md
```

Use sequential numeric IDs to make decisions easy to reference.

## ADR Template

Each ADR should contain the following sections.

### Status

Describe the current state of the decision.

Recommended values:

* `Proposed` — decision is under consideration.
* `Accepted` — decision has been made and is currently in effect.
* `Superseded` — replaced by a later decision.
* `Rejected` — considered but not adopted.

### Context

Explain the problem, constraints, assumptions, and relevant alternatives that led to the decision.

Focus on the information needed to understand **why the decision was necessary**.

### Decision

State the decision clearly and concisely.

This section should describe **what was decided**, not the entire reasoning process.

### Evidence

Record the evidence supporting the decision.

Evidence may include:

* Research findings
* Experiments
* Benchmark results
* Dataset characteristics
* Domain or stakeholder requirements
* Technical constraints
* References to issues, pull requests, or other project documentation

Link to supporting artifacts where appropriate.

### Revisit Condition

Define the conditions under which the decision should be reconsidered.

A revisit condition should be specific enough that a future contributor can recognize when the original decision may no longer be valid.

## ADR Skeleton

Copy this structure when creating a new ADR:

```markdown
# NNNN — Decision Title

**Status:** Proposed | Accepted | Superseded | Rejected  
**Date:** YYYY-MM-DD

## Context

Describe the problem, constraints, assumptions, and relevant alternatives.

## Decision

State the decision that was made.

## Evidence

Document the evidence supporting the decision.

- Evidence item 1
- Evidence item 2
- Evidence item 3

## Revisit Condition

Describe the conditions that would cause this decision to be reconsidered.
```

## Principles

The decision log should follow these principles:

1. **Record significant decisions, not everything.**
2. **Capture reasoning, not just outcomes.**
3. **Link decisions to evidence whenever possible.**
4. **Keep decisions concise and understandable.**
5. **Define when decisions should be revisited.**
6. **Never create decisions merely to populate the log.**
