# Monitoring & Drift Detection

## Purpose

Monitoring in the **Stroke Risk Stratification System** exists to detect **silent model failure** after deployment. In healthcare-adjacent ML systems, models rarely fail loudly; they fail by gradually becoming wrong.

The goal of monitoring is to:

* Detect data and prediction shifts early
* Identify degradation in model reliability
* Enable timely intervention, rollback, or retraining

Monitoring is treated as a **core production requirement**, not an operational afterthought.

---

## Monitoring Principles

* **Measure what can break decisions**, not just infrastructure
* **Prefer leading indicators** over lagging metrics
* **Separate detection from action** to avoid overreaction
* **Make signals auditable and explainable**

---

## Monitoring Layers

The system monitors behavior across four layers:

1. Input Data Monitoring
2. Prediction Monitoring
3. Performance Monitoring (Delayed Labels)
4. System Health Monitoring

Each layer targets different failure modes.

---

## Input Data Monitoring

### What Is Monitored

* Feature distributions (mean, variance, quantiles)
* Missing value rates
* Categorical value frequency
* Schema violations

### Drift Detection

* Statistical distance metrics (e.g., PSI, KS)
* Rule-based thresholds for critical features

### Why It Matters

If incoming data no longer resembles training data, model predictions become unreliable—even if the model code has not changed.

---

## Prediction Monitoring

### What Is Monitored

* Distribution of predicted probabilities
* Risk category proportions (low / medium / high)
* Sudden spikes or collapses in confidence scores

### Drift Signals

* Shift in score distribution without corresponding data drift
* Collapse toward extreme probabilities

These patterns often indicate **model misuse or upstream data issues**.

---

## Performance Monitoring (Delayed Labels)

### Scope

Where outcome labels become available with delay, the system tracks:

* Recall and precision over time
* Calibration error drift
* Performance by key subgroups

### Constraints

* Labels may be delayed, noisy, or incomplete
* Monitoring windows are aligned with data availability

Performance monitoring is advisory but highly actionable.

---

## System Health Monitoring

### Metrics Tracked

* API latency
* Error rates (4xx / 5xx)
* Request volume anomalies

These metrics ensure availability but are **not substitutes** for model-quality monitoring.

---

## Alerting Strategy

Alerts are designed to be **actionable**, not noisy:

* Warning alerts for mild drift
* Critical alerts for sustained or severe deviation

Each alert defines:

* Trigger condition
* Severity
* Expected response

Alerts without a defined action are intentionally avoided.

---

## Response Playbooks

For each alert category, a predefined response exists:

* Data drift → investigate upstream data, freeze deployment
* Prediction drift → validate preprocessing and thresholds
* Performance degradation → rollback or retrain

All actions are logged for auditability.

---

## Monitoring Data Governance

* Monitoring logs exclude direct identifiers
* Access is restricted to authorized personnel
* Retention policies are enforced

Monitoring data is used strictly for system reliability and governance.

---

## Known Limitations

* Drift detection is probabilistic, not definitive
* Some failures require human interpretation
* Monitoring does not replace periodic model review

False positives are expected and managed conservatively.

---

## Summary

Monitoring ensures that the Stroke Risk Stratification System remains **trustworthy after deployment**. By combining data, prediction, performance, and system signals, the platform minimizes the risk of undetected degradation and supports responsible long-term operation.
