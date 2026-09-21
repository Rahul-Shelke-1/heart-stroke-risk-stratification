# Data Overview

## Purpose of This Section

Data is the foundation of any machine learning system. In healthcare-related problems, **data provenance, limitations, and assumptions** are often more important than model choice.

This section describes the dataset used in this project, how it is interpreted, and what constraints it introduces for modeling and deployment.

---

## Dataset Description

The dataset used in this project contains **structured, tabular patient-level data** with demographic, clinical, and lifestyle-related attributes, along with a binary indicator of stroke occurrence.

The data represents a **retrospective snapshot** of individuals and is commonly used for educational and benchmarking purposes in stroke prediction tasks.

> ⚠️ This dataset is **not collected under a clinical trial or hospital protocol** and should not be treated as clinically validated data.

---

## Target Variable

* **Target**: `stroke`
* **Type**: Binary (0 = No stroke, 1 = Stroke)

The target indicates whether an individual has experienced a stroke event at any point in the observed period.

### Interpretation Notes

* The target does **not** encode timing or severity of stroke
* No temporal ordering between features and stroke event is guaranteed
* The label should be treated as an outcome indicator, not a diagnosis timestamp

These limitations directly influence evaluation and deployment assumptions.

---

## Feature Groups

For clarity and governance, features are grouped by domain:

### 1. Demographic Features

* Age
* Gender
* Marital status
* Residence type

These features often act as **baseline risk indicators** and are typically stable over time.

---

### 2. Clinical Features

* Hypertension
* Heart disease
* Average glucose level
* Body Mass Index (BMI)

These features are directly linked to known stroke risk factors but may suffer from:

* Measurement variability
* Missing values
* Proxy encoding (e.g., binary indicators instead of clinical measurements)

---

### 3. Lifestyle & Behavioral Features

* Smoking status
* Work type

These features provide additional context but are often:

* Self-reported
* Noisy
* Incompletely captured

---

## Data Size & Class Distribution

Key characteristics:

- Total samples: 5,110
- Positive class (stroke): 249 (4.87%)
- Negative class (no stroke): 4,861 (95.13%)
- Class imbalance ratio: ~1:19

The low base rate **(~5%)** has significant implications:

- Accuracy is not a meaningful metric
- ROC-AUC alone is insufficient
- Precision-Recall curve is emphasized
- Threshold selection must be cost-aware
- Calibration is critical for probability interpretation

Train / Validation / Test split sizes :

- Train: 3,577
- Validation: 766
- Test: 767

**Stratified splitting** was used to preserve base rate.

---

## Missing Data Overview

Missingness is present in two features:

| Feature          | Missing Count | Missing (%) |
| ---------------- | ------------- | ----------- |
| `smoking_status` | 1,544         | 30.22%      |
| `bmi`            | 201           | 3.93%       |


### Observations

- `smoking_status` has **substantial missingness (~30%)**, which is material and cannot be ignored.
- `bmi` has **low-to-moderate missingness (~4%)**, but remains statistically relevant.
- No other features contain missing values.

### Missingness Assumptions

We do **not** assume Missing Completely At Random (MCAR).

- `smoking_status` missingness may reflect:

    - Non-response bias

    - Sensitive disclosure behavior

    - Demographic correlations

- `bmi` missingness may correlate with:

    - Healthcare access

    - Measurement practices

    - Age or comorbidity patterns

Missingness is treated as **potentially informative (MAR or MNAR)**,
Imputation strategies are therefore treated as **first-class design decisions** and are documented separately in the feature engineering section.

---

## Data Assumptions

This project operates under the following explicit assumptions:

* Feature values are reasonably accurate but not clinically verified
* The dataset represents a **proxy population**, not a universal one
* Relationships learned by the model may not generalize across regions or demographics

These assumptions are documented to avoid overgeneralization.

---

## What This Data Can and Cannot Support

### Supported Use Cases

* Demonstrating end-to-end ML system design
* Experimenting with feature engineering strategies
* Evaluating classification and risk stratification techniques
* Showcasing MLOps and governance practices

### Unsupported Use Cases

* Real clinical decision-making
* Policy recommendations
* Individual-level medical advice

---

## Transition to Data Quality & Bias

Understanding *what the data is* is only the first step.

The next section focuses on:

* Data quality issues
* Bias and representativeness risks
* Leakage considerations

These factors critically influence trustworthiness and downstream system behavior.
