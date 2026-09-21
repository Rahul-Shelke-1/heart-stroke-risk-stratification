# Feature Engineering

## Purpose of Feature Engineering

Feature engineering in this system is treated as a **production infrastructure layer**, not exploratory preprocessing.

All transformations are:

* Deterministic
* Reproducible
* Leakage-safe
* Fully encapsulated in sklearn-compatible pipelines
* Serializable and versioned as deployable artifacts

The preprocessing pipeline is considered a **first-class model component**, stored and versioned alongside trained models.

---

## Design Principles

The feature engineering strategy is guided by the following principles:

1. **No data leakage**

   - All transformers are fitted strictly on training data.
   - Validation and test data are transformed using frozen parameters.
   - No global statistics are computed outside pipeline context.

2. **Schema-driven transformations**

   - Feature logic is derived from a documented schema contract.
   - Transformations do not rely on implicit column ordering or notebook assumptions.

3. **Deterministic Category Handling**

   - Categorical mappings are explicitly defined and stable across runs.
   - No reliance on implicit sklearn category ordering.

4. **Inference Parity**
   - The exact same serialized pipeline used during training is reused during inference.

---

## Feature Categories

Based on the data schema, features are grouped and processed as follows:

### 1. Numerical Features

Examples:

* age
* avg_glucose_level
* bmi

#### Transformations Applied

* Missing value imputation
* Optional scaling (model-dependent)

#### Rationale

* Numerical features may contain missing values and outliers
* Imputation is required for most ML algorithms
* Scaling is applied only when the downstream model is sensitive to feature magnitude

---

### 2. Binary Clinical Features

Examples:

* hypertension
* heart_disease

#### Transformations Applied

* Type validation
* Pass-through or casting to integer

#### Rationale

* Binary indicators already encode the intended signal
* No additional encoding improves interpretability or performance

---

### 3. Categorical Features

Examples:

* gender
* ever_married
* residence_type
* work_type
* smoking_status

#### Transformations Applied

* Custom ordinal or nominal encoding
* Explicit handling of unknown categories

#### Rationale

* Healthcare-related categorical features often contain rare or unseen categories
* Default encoders may fail silently or reorder categories
* Custom encoders provide full control over category mapping and behavior

---

## Custom Transformers

### Custom Ordinal Encoder

This project implements a **custom ordinal encoder** to:

* Explicitly control category ordering
* Ensure deterministic mappings across runs
* Handle unknown or missing categories safely

Key properties:

* sklearn-compatible (`fit`, `transform`)
* Serializable as part of the pipeline
* Tested independently

This avoids common pitfalls of off-the-shelf encoders when used in production systems.

---

## Imputation Strategy

Missing data is handled explicitly within the preprocessing pipeline.

### Numerical Imputation

* Strategy: statistical imputation (e.g., median)
* Fitted only on training data
* Applied consistently during inference

### Categorical Imputation

* Missing categories mapped to an explicit `Unknown` token
* Preserves information carried by missingness

Imputation decisions are logged and versioned as part of the experiment artifacts.

---

## Pipeline Architecture

All feature transformations are composed using **sklearn Pipelines and ColumnTransformers**.

Benefits:

* Prevents train–test leakage
* Enables end-to-end serialization
* Simplifies testing and validation
* Ensures training and inference parity

The preprocessing pipeline is treated as a **deployable artifact**, not an intermediate object.

---

## Testing & Validation

Feature engineering logic is validated through:

* Unit tests for custom transformers
* Schema validation tests
* Deterministic output checks

Testing ensures:

* Identical inputs always produce identical outputs
* Unknown categories are handled safely
* No silent failures occur during transformation

---

## Feature Engineering Outputs

The output of feature engineering is:

* A fully numerical, model-ready feature matrix
* Consistent column ordering
* No dependency on raw input schema at inference time

This output feeds directly into the modeling and evaluation stages.

---

## Summary

Feature engineering in this system is:

* Explicit
* Auditable
* Reproducible
* Production-safe

By encapsulating all transformations inside tested pipelines, the project ensures that feature logic remains consistent across experimentation, deployment, and monitoring.

> *In production ML systems, feature engineering is infrastructure, not experimentation.*
