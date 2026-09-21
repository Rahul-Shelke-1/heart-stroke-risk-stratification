# Model Card

## Model Overview

This document serves as the **Model Card** for the Stroke Risk Stratification System. It provides a standardized and transparent summary of the selected model, its intended use, limitations, and operational considerations.

The purpose of this model card is to enable:

* Informed use of the model outputs
* Clear communication of risks and constraints
* Accountability across the model lifecycle

---

## Model Details

* **Model Type**: Supervised classification model for stroke risk estimation
* **Output**: Stroke risk probability, mapped to risk tiers (low / medium / high)
* **Model Family**: Tree-based / linear models evaluated; final selection based on stability and recall performance
* **Versioning**: Model versions are tracked and managed via a model registry

The model produces probabilistic outputs and does not generate clinical diagnoses.

---

## Intended Use

### Primary Intended Use

* Risk stratification of individuals based on structured patient attributes
* Decision-support input for analytical workflows
  nThe model is intended to **support** human decision-making, not replace it.

### Intended Users

* Data scientists and ML engineers
* Healthcare analytics teams (non-clinical)
* Researchers and reviewers evaluating ML systems

---

## Out-of-Scope Use

The model **must not** be used for:

* Clinical diagnosis or treatment decisions
* Autonomous medical decision-making
* Emergency or real-time clinical scenarios
* Use on populations outside the documented data assumptions

---

## Training Data

* **Data Type**: Retrospective, tabular patient data
* **Source**: Publicly available dataset used for educational and benchmarking purposes
* **Label**: Binary indicator of stroke occurrence

### Data Limitations

* No temporal ordering of events
* Potential population and reporting bias
* Imbalanced class distribution
* No clinical adjudication of labels

These limitations directly affect model generalizability.

---

## Evaluation Summary

The model is evaluated using metrics aligned with the project’s success criteria:

* Recall / Sensitivity (priority for high-risk cases)
* ROC-AUC
* Precision and F1-score

Evaluation is performed using stratified validation to account for class imbalance.

---

## Ethical Considerations

* The model does not infer sensitive attributes beyond the provided schema
* Predictions may reflect biases present in the data
* Model outputs are probabilistic and uncertain

Ethical use requires:

* Awareness of limitations
* Conservative interpretation of predictions
* Avoidance of overreliance on automated outputs

---

## Performance Caveats

* Performance metrics reflect retrospective evaluation only
* Results may degrade when applied to different populations
* Thresholds are context-dependent and not universally optimal

Users should treat model outputs as **relative risk indicators**, not absolute truth.

---

## Operational Considerations

* The model is packaged with its preprocessing pipeline
* Inputs must conform to the documented data schema
* Schema violations result in deterministic failures

Monitoring is required to detect:

* Data drift
* Prediction distribution shifts
  n

---

## Model Governance

* All models are versioned and tracked
* Promotion to higher stages requires metric and stability review
* Rollback is supported through the registry

The model card must be updated whenever a new model version is promoted.

---

## Summary

This model card documents the **capabilities, constraints, and responsibilities** associated with the Stroke Risk Stratification model.

> *A model is only as trustworthy as its documentation, governance, and monitoring allow it to be.*
