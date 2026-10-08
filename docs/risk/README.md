# Risk Register

The Risk Register provides a structured mechanism for identifying, assessing,
monitoring, and managing project risks throughout the project lifecycle.

Risks should be recorded when there is credible evidence that an event or
condition could negatively affect project scope, data quality, model quality,
system reliability, delivery, or operational outcomes.

This register is intentionally evidence-driven. Risks should not be created
simply to populate the register.

## Risk Assessment Workflow

1. **Identify** — Record a risk when a credible risk is discovered.
2. **Assess** — Evaluate its potential impact and probability.
3. **Rate** — Assign an overall severity based on the impact/probability matrix.
4. **Mitigate** — Define actions that reduce the probability or impact of the risk.
5. **Monitor** — Track the risk and its trigger events as the project evolves.
6. **Resolve** — Mark the risk as Mitigated, Accepted, or Closed when appropriate.

## Risk Register

| Risk ID | Risk Description | Impact | Probability | Severity | Mitigation Strategy | Owner | Status | Trigger Event |
|---|---|---|---|---|---|---|---|---|
| — | No risks recorded yet. | — | — | — | — | — | — | — |

> Do not add artificial risks solely to populate this table. Add a risk when
> there is sufficient evidence or a credible reason to track it.

## Field Definitions

| Field | Definition |
|---|---|
| **Risk ID** | Unique identifier for the risk, e.g. `R-001`. |
| **Risk Description** | Clear description of the uncertain event or condition and its potential consequence. |
| **Impact** | Potential effect if the risk occurs: `High`, `Medium`, or `Low`. |
| **Probability** | Estimated likelihood that the risk will occur: `High`, `Medium`, or `Low`. |
| **Severity** | Overall risk rating derived from Impact and Probability using the severity matrix below. |
| **Mitigation Strategy** | Actions intended to reduce the probability and/or impact of the risk. |
| **Owner** | Person responsible for monitoring and managing the risk. |
| **Status** | Current state: `Open`, `Mitigated`, `Accepted`, or `Closed`. |
| **Trigger Event** | Observable condition or event indicating that the risk is occurring or requires reassessment. |

## Risk Rating Criteria

### Impact

| Rating | Guideline |
|---|---|
| **High** | Could materially affect project objectives, ML validity, system reliability, delivery, or stakeholder outcomes. |
| **Medium** | Could require meaningful rework, scope adjustment, or additional resources but is unlikely to invalidate the project. |
| **Low** | Limited effect that can be handled with minor corrective action. |

### Probability

| Rating | Guideline |
|---|---|
| **High** | The risk is likely to occur given current evidence or project conditions. |
| **Medium** | The risk is plausible but there is uncertainty about whether it will occur. |
| **Low** | The risk is possible but currently has limited supporting evidence. |

### Severity Matrix

Severity is determined from the combination of Impact and Probability.

| Impact \ Probability | Low | Medium | High |
|---|---|---|---|
| **Low** | Low | Low | Medium |
| **Medium** | Low | Medium | High |
| **High** | Medium | High | High |

Severity should be reassessed when new evidence changes the expected impact
or probability of a risk.

## Risk Status

| Status | Meaning |
|---|---|
| **Open** | Risk is identified and requires monitoring and/or mitigation. |
| **Mitigated** | Mitigation actions have reduced the risk to an acceptable level. |
| **Accepted** | Risk remains but has been consciously accepted because further mitigation is not justified or practical. |
| **Closed** | Risk is no longer relevant or cannot reasonably occur due to a change in project conditions. |

## Risk Management Principles

- Prefer evidence over speculation.
- Record risks early when they could materially affect project decisions.
- Keep risks distinct from ordinary tasks or known problems.
- Reassess risks when new evidence, requirements, or architectural decisions emerge.
- Link significant risks to relevant issues, decisions, research, or experiments when useful.
- Do not use the register as a daily project diary.