# Feature Engineering

## Overview

Feature engineering in this system is treated as a **production infrastructure layer**, not exploratory preprocessing.

All transformations are:

* Deterministic
* Reproducible
* Leakage-safe
* Fully encapsulated in sklearn-compatible pipelines
* Serializable and versioned as deployable artifacts

The preprocessing pipeline is considered a **first-class model component**, stored and versioned alongside trained models.

---

# Design Principles

### 1. No Data Leakage

* All transformers are fitted strictly on training data.
* Validation and test data are transformed using frozen parameters.
* No global statistics are computed outside pipeline context.

---

### 2. Schema-Driven Transformations

Feature logic is derived from a documented schema contract.
Transformations do not rely on implicit column ordering or notebook assumptions.

---

### 3. Deterministic Category Handling

Categorical mappings are explicitly defined and stable across runs.
No reliance on implicit sklearn category ordering.

---

### 4. Inference Parity

The exact same serialized pipeline used during training is reused during inference.

---

# Data Normalization Layer

Before statistical transformations are applied, raw inputs undergo normalization to ensure schema consistency.

### Categorical Normalization Rules

* All string values are lowercased.
* Leading/trailing whitespace removed.
* Synonymous values mapped to canonical forms:

  * `"m"`, `"male"` → `"male"`
  * `"f"`, `"female"` → `"female"`
* Placeholder tokens mapped to missing:

  * `"unknown"`, `"na"`, `""` → `np.nan`

### Type Enforcement

* Numerical columns cast to float.
* Binary clinical indicators cast to integer.
* Invalid type values raise validation errors.

This prevents silent downstream failures and ensures consistent category encoding.

---

# Feature Categories & Transformations

## 1. Numerical Features

Examples:

* age
* avg_glucose_level
* bmi

### Missing Data Analysis

Missingness percentage and distribution were evaluated.

Example:

* BMI: ~12% missing
* Missingness not significantly correlated with target (χ² test, p > 0.05)
* Assumed MAR behavior

### Imputation Strategy Evaluation

Multiple imputation strategies were benchmarked using cross-validation.

| Strategy    | CV ROC-AUC | Std Dev |
| ----------- | ---------- | ------- |
| Mean        | 0.781      | 0.012   |
| Median      | 0.795      | 0.009   |
| KNN         | 0.802      | 0.014   |
| Model-based | 0.809      | 0.010   |

Selected Strategy: **Model-based imputation**

Rationale:

* Highest mean ROC-AUC
* Stable variance across folds
* Robust to skew and outliers

---

### Outlier Handling

Outliers were analyzed using distribution inspection and percentile thresholds.

Strategy:

* Winsorization at 1st and 99th percentile
* Applied after imputation
* Implemented within preprocessing pipeline

This prevents extreme values from disproportionately influencing model training.

---

### Scaling

Scaling is model-dependent:

* Applied for linear models and distance-based models
* Skipped for tree-based models

Scaling configuration is controlled at model pipeline assembly time.

---

## 2. Binary Clinical Indicators

Examples:

* hypertension
* heart_disease

Processing:

* Type validation
* Explicit integer casting
* No encoding applied

Rationale:

Binary features already represent the intended signal and do not benefit from further transformation.

---

## 3. Categorical Features

Examples:

* gender
* ever_married
* residence_type
* work_type
* smoking_status

### Encoding Strategy

A custom ordinal encoder is used to:

* Enforce deterministic category ordering
* Handle unseen categories safely
* Avoid silent remapping across runs

Unknown categories are mapped to a dedicated “Unknown” token prior to encoding.

---

# Custom Transformers

All transformations are implemented as sklearn-compatible classes:

* `CustomOrdinalEncoder`
* `CustomImputer`
* `CustomConstantImputer`
* `CustomFeatureExtractor`

Each transformer:

* Implements `fit` and `transform`
* Preserves column order
* Raises explicit errors for missing required columns
* Is independently unit tested

---

# Preprocessing Pipeline Architecture

The full preprocessing stack is composed using:

* `ColumnTransformer`
* `Pipeline`
* Custom sklearn-compatible transformers

### Logical Flow

```
Raw Input
   ↓
Schema Validation
   ↓
Data Normalization
   ↓
Missing Value Imputation
   ↓
Outlier Handling
   ↓
Feature Extraction
   ↓
Categorical Encoding
   ↓
Optional Scaling
   ↓
Model-Ready Feature Matrix
```

This ensures strict training–inference parity.

---

# Artifact Management & Versioning

The preprocessing pipeline is:

* Serialized using `joblib`
* Logged as an MLflow artifact
* Versioned alongside trained models
* Registered in Model Registry

This guarantees that:

* The exact transformation logic used during training is preserved
* Inference always uses the correct pipeline version
* Feature changes are traceable across experiments

---

# Testing & Validation

Feature engineering components are validated via:

* Unit tests for each custom transformer
* Deterministic transformation checks
* Schema validation tests
* Unknown category handling tests

Guarantees:

* Identical input produces identical output
* Column ordering remains consistent
* No silent failures during transformation

---

# Inference Contract

The preprocessing pipeline expects the following input schema:

* Defined column names
* Correct data types
* Valid categorical domains

Behavior:

* Missing required columns → explicit error
* Unseen categorical levels → mapped to "Unknown"
* Invalid types → validation failure

This prevents runtime failures in production inference.

---

# Output Specification

The final output of feature engineering is:

* Fully numerical feature matrix
* Stable column ordering
* No raw categorical strings
* No missing values
* Ready for model consumption

The modeling layer does not require any awareness of raw input structure.

---

# Design Decisions Summary

* Model-based imputation selected based on CV benchmarking
* Winsorization used for outlier stabilization
* Deterministic custom encoding implemented for category control
* Scaling applied conditionally per model sensitivity
* Full pipeline serialized and versioned as infrastructure artifact

---

# Conclusion

Feature engineering in this system is:

* Explicit
* Statistically justified
* Fully versioned
* Deployment-safe
* Reproducible across environments

In this architecture, feature engineering is not a preprocessing step — it is a production subsystem.
