# Roadmap & Future Work

## Purpose

This roadmap outlines **responsible future extensions** of the Stroke Risk Stratification System. It distinguishes between:

* Technically feasible improvements
* Operational hardening steps
* Requirements that would be mandatory for real-world clinical use

The roadmap is intentionally conservative and avoids speculative claims.

---

## Guiding Principles for Evolution

All future work is guided by the following principles:

* **Safety before capability**
* **Evidence before deployment**
* **Governance before automation**
* **Transparency over performance gains**

No roadmap item implies readiness for clinical deployment.

---

## Short-Term Enhancements (Technical)

### Improved Feature Engineering

* Incorporate interaction features informed by domain literature
* Evaluate temporal aggregation if longitudinal data becomes available
* Strengthen missingness-aware representations

These changes focus on **model robustness**, not complexity.

---

### Model Evaluation Improvements

* Expand subgroup analysis granularity
* Introduce uncertainty quantification for predictions
* Stress-test calibration under simulated drift

The goal is deeper risk understanding, not metric inflation.

---

## Medium-Term Enhancements (System & MLOps)

### Advanced Monitoring

* Automated drift-triggered retraining proposals (human-approved)
* Improved explainability dashboards for monitoring signals
* Better linkage between monitoring alerts and model registry actions

---

### CI/CD & Automation

* Infrastructure-as-code hardening
* Canary deployments for inference endpoints
* Automated rollback on severe degradation signals

Automation remains **human-in-the-loop**.

---

## Long-Term Considerations (High-Risk / Regulated)

### Clinical Validation Pathway

For any real-world clinical use, the following would be mandatory:

* Prospective data collection
* Clinical trial design and execution
* Independent validation studies
* Regulatory approval processes

These steps are outside the scope of this project.

---

### Ethical & Governance Expansion

* Formal bias audits
* Stakeholder review processes
* Clear accountability and escalation ownership

Governance complexity grows faster than model complexity.

---

## Explicit Non-Goals

The roadmap does **not** include:

* Autonomous clinical decision-making
* Replacement of medical professionals
* Claims of diagnostic accuracy

These exclusions are intentional and permanent.

---

## Success Criteria for Future Work

Progress along this roadmap is measured by:

* Reduced uncertainty and clearer risk boundaries
* Improved auditability and traceability
* Safer operational behavior under change

Not by leaderboard performance alone.

---

## Summary

This roadmap demonstrates how the Stroke Risk Stratification System could evolve **responsibly and incrementally**. It reinforces that production-grade engineering does not imply clinical readiness, and that maturity in ML systems is defined by governance, not ambition.
