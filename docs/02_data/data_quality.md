# Data Quality, Bias & Limitations

## Purpose of This Section

In healthcare-related machine learning systems, **data quality and bias are often the dominant risk factors**, not model choice or algorithmic sophistication.

This section documents known and potential data quality issues, sources of bias, and leakage risks associated with the dataset used in this project, along with the mitigation strategies adopted.

---

## Class Imbalance

### Observation

Stroke events represent a **small minority** of the dataset, resulting in a highly imbalanced target distribution.

### Implications

* Accuracy becomes a misleading metric
* Models can achieve high accuracy by predicting the majority class
* Minority class (stroke) errors carry disproportionate cost

### Mitigation Strategies

* Use recall-sensitive metrics (Recall, ROC-AUC, PR-AUC)
* Stratified train/validation splits
* Threshold tuning based on risk trade-offs
* Explicit evaluation of confusion matrices by risk tier

Class imbalance is treated as a **first-order design constraint**, not a preprocessing inconvenience.

---

## Missing Data

### Observations

Some features contain missing values, most notably:

* Body Mass Index (BMI)

Missingness is unlikely to be completely random and may correlate with:

* Age
* Socioeconomic indicators
* Access to healthcare

### Risks

* Naïve imputation can introduce bias
* Missingness itself may carry signal
* Train–serve skew if imputation is inconsistent

### Mitigation Strategies

* Explicit imputation within the preprocessing pipeline
* Separation of numerical and categorical imputation logic
* Pipeline-level testing to ensure deterministic behavior
* Evaluation of model sensitivity to imputed values

All imputation logic is versioned and reproducible.

---

## Feature Quality & Measurement Noise

### Binary Clinical Indicators

Features such as hypertension and heart disease are encoded as binary flags, which:

* Mask severity and progression
* Introduce loss of clinical nuance

### Continuous Measurements

Features like glucose level and BMI:

* May suffer from measurement variability
* May be recorded under different conditions

These limitations restrict the **clinical granularity** of predictions.

---

## Bias & Representativeness

### Population Bias

The dataset does not guarantee representation across:

* Geographic regions
* Ethnic groups
* Socioeconomic strata

As a result:

* Learned patterns may not generalize
* Risk estimates may be systematically skewed

### Feature Bias

Lifestyle features (e.g., smoking status):

* Are often self-reported
* May be inconsistently recorded
* Can encode social and cultural bias

### Mitigation Strategies

* Explicit documentation of bias risks
* Conservative interpretation of predictions
* Avoidance of claims about fairness or equity

Bias is acknowledged and documented rather than implicitly ignored.

---

## Data Leakage Risks

### Potential Leakage Sources

* Features that may indirectly encode post-stroke information
* Improper train/test splitting
* Global preprocessing applied before splitting

### Controls Implemented

* Train/test split performed before fitting transformers
* All preprocessing encapsulated within sklearn pipelines
* No target-dependent feature engineering

Leakage prevention is enforced by **design**, not manual discipline.

---

## Temporal Limitations

The dataset lacks:

* Event timestamps
* Longitudinal follow-up

This prevents:

* Time-aware validation
* Survival analysis
* Realistic prospective evaluation

As a result, evaluation metrics should be interpreted as **retrospective performance only**.

---

## What This Means for Model Trust

Given the above factors:

* Model outputs should be treated as **risk indicators**, not ground truth
* Predictions are best used for **relative ranking**, not absolute probability
* Conservative thresholds are preferred

Trust in the system comes from **transparency and governance**, not raw performance metrics.

---

## Summary

This dataset exhibits several real-world challenges:

* Class imbalance
* Missing data
* Measurement noise
* Bias and representativeness risks
* Lack of temporal structure

Rather than hiding these issues, this project:

* Documents them explicitly
* Designs mitigations where feasible
* Accepts and communicates residual risk

> *In production machine learning, acknowledging data limitations is a prerequisite for responsible system design.*
