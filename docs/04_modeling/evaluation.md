# Model Evaluation

## Objective of Evaluation

The goal of model evaluation in the **Stroke Risk Stratification System** is not merely to maximize aggregate accuracy, but to **quantify clinical risk trade-offs**, ensure robustness across sub-populations, and validate that the model is safe and useful as a **decision-support component**.

Evaluation is therefore aligned with:

* Medical risk tolerance (false negatives are costlier than false positives)
* Deployment constraints (threshold-based inference)
* Regulatory and audit expectations

---

## Evaluation Dataset

### Dataset Split Strategy

The dataset is split using a **stratified approach** to preserve the base rate of stroke events:

* Training set: Used for model fitting
* Validation set: Used for model selection and hyperparameter tuning
* Test set (hold-out): Used **only once** for final evaluation

No records from the test set are used during feature engineering, model tuning, or threshold calibration.

---

## Primary Evaluation Metrics

Given the asymmetric cost of errors in stroke prediction, evaluation prioritizes **sensitivity and risk coverage**.

### Core Metrics

| Metric               | Rationale                                              |
| -------------------- | ------------------------------------------------------ |
| Recall (Sensitivity) | Missing a high-risk patient is clinically unacceptable |
| Precision            | Controls alert fatigue and downstream resource usage   |
| ROC-AUC              | Measures overall ranking ability                       |
| PR-AUC               | More informative under class imbalance                 |
| F1-score             | Used as a secondary balance metric                     |

Accuracy is reported for completeness but **not used for decision-making**.

---

## Threshold-Based Evaluation

### Why Thresholding Matters

In production, the model does not operate on raw probabilities alone. A **decision threshold** converts probabilities into actionable risk flags.

Evaluation is therefore performed at multiple thresholds:

* Conservative (high recall)
* Balanced
* Precision-oriented

For each threshold, the following are reported:

* Confusion matrix
* Recall / Precision trade-off
* Expected false negatives per 1,000 patients

The selected production threshold is documented in the **Model Card**.

---

## Calibration Analysis

Probability calibration is critical when predictions are interpreted as **risk scores**.

Evaluation includes:

* Calibration curve (reliability diagram)
* Brier score
* Comparison of raw vs calibrated probabilities (if calibration applied)

Poor calibration is treated as a **blocking issue** for production deployment.

---

## Subgroup & Fairness Evaluation

To assess model stability and bias, metrics are evaluated across key subgroups:

* Age brackets
* Gender
* Known clinical risk factors (e.g., hypertension, diabetes)

For each subgroup:

* Recall and precision deltas are analyzed
* Significant performance drops are flagged

This analysis informs risk disclosures and monitoring priorities.

---

## Error Analysis

### False Negative Review

False negatives are explicitly reviewed to identify:

* Feature patterns associated with missed risk
* Data sparsity or measurement gaps
* Potential label noise

### False Positive Review

False positives are analyzed to ensure:

* Alerts remain clinically plausible
* The system does not over-trigger on benign profiles

Insights from error analysis feed back into **feature engineering and data quality improvements**, not post-hoc threshold hacks.

---

## Robustness Checks

Additional evaluation checks include:

* Performance stability across random seeds
* Sensitivity to minor feature perturbations
* Comparison against baseline heuristics (e.g., rule-based risk scoring)

These checks help detect fragile or overfit models.

---

## Experiment Tracking & Reproducibility

All evaluation results are:

* Logged to MLflow with dataset version references
* Linked to a specific model artifact and feature pipeline
* Reproducible via pinned environments and seeds

The test set evaluation is immutable once finalized.

---

## Go / No-Go Decision Criteria

A model is considered **eligible for deployment** only if:

* Recall exceeds the minimum clinically acceptable threshold
* Calibration error is within defined bounds
* No severe subgroup degradation is observed
* Evaluation is reproducible and auditable

Failure on any criterion blocks promotion to production.

---

## Known Evaluation Limitations

* Dataset reflects retrospective observations, not prospective outcomes
* Certain demographic groups may be underrepresented
* Evaluation does not replace clinical validation studies

These limitations are explicitly documented to avoid over-claiming model capabilities.

---

## Summary

Model evaluation in this system is treated as a **risk assessment exercise**, not a leaderboard optimization task. The results inform deployment decisions, governance controls, and monitoring strategy rather than serving as marketing metrics.
