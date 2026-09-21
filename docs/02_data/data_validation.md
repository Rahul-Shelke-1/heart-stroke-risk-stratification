# Data Validation Rules

## Purpose

This section defines the **formal validation constraints** applied to all incoming datasets prior to:

* Model training
* Batch scoring
* Online inference

Validation rules ensure:

* Schema consistency
* Statistical sanity
* Risk containment
* Reproducibility

Data that fails critical validation checks is rejected.

---

## 1. Schema Validation

All datasets must conform to a **versioned schema contract**.

### Required Columns

* `age`
* `hypertension`
* `heart_disease`
* `ever_married`
* `work_type`
* `Residence_type`
* `avg_glucose_level`
* `bmi`
* `smoking_status`
* `stroke` (training only)

### Column Constraints

* No unexpected columns
* No missing required columns
* Column names must match exactly (case-sensitive)
* Column order is not enforced (schema-based mapping used)

---

## 2. Data Type Enforcement

Each feature must match its expected type:

| Feature             | Expected Type   |
| ------------------- | --------------- |
| `age`               | float / numeric |
| `hypertension`      | binary (0/1)    |
| `heart_disease`     | binary (0/1)    |
| `ever_married`      | binary (0/1)    |
| `work_type`         | categorical     |
| `Residence_type`    | categorical     |
| `avg_glucose_level` | float           |
| `bmi`               | float           |
| `smoking_status`    | categorical     |
| `stroke`            | binary (0/1)    |

Type coercion is not silently performed. Invalid types trigger validation failure.

---

## 3. Value Range Constraints

### Numerical Features

| Feature             | Valid Range   | Rationale                 |
| ------------------- | ------------- | ------------------------- |
| `age`               | 0 ≤ age ≤ 120 | Biological plausibility   |
| `avg_glucose_level` | > 0           | Physiological constraint  |
| `bmi`               | 10 ≤ bmi ≤ 80 | Prevent data entry errors |

Out-of-range values:

* Training: rejected
* Inference: logged and rejected

---

### Binary Features

Must be strictly {0,1}.
No coercion from strings or booleans.

---

### Categorical Features

Allowed values are enumerated:

* `ever_married`: {"Yes", "No"}
* `Residence_type`: {"Urban", "Rural"}
* `smoking_status`: {"never smoked", "formerly smoked", "smokes", "Unknown"}
* `work_type`: predefined allowed categories

Unknown categories are rejected (no implicit mapping).

---

## 4. Missing Data Rules

Missingness thresholds are enforced:

| Feature          | Allowed Missingness |
| ---------------- | ------------------- |
| `smoking_status` | ≤ 35%               |
| `bmi`            | ≤ 10%               |
| Other features   | 0%                  |

If missingness exceeds thresholds:

* Training pipeline aborts
* Alert is generated

Imputation is handled downstream within the feature pipeline — not during validation.

---

## 5. Cross-Field Logical Constraints

Validation includes domain-aware rules:

* `age = 0` must not co-occur with `ever_married = "Yes"`
* `age < 18` cannot have certain `work_type` categories (if applicable)
* Binary disease indicators must not contain nulls

Logical violations trigger dataset rejection.

---

## 6. Distributional Sanity Checks (Training Only)

To prevent silent drift or corrupted training data:

* Class prevalence must remain within ±2% of expected base rate
* Numerical features must pass distribution shift checks (e.g., KS test)
* Feature cardinality must remain stable

These checks guard against:

* Data pipeline errors
* Incorrect joins
* Schema evolution

---

## 7. Train–Serve Parity Enforcement

The same validation logic is applied to:

* Offline training data
* Batch scoring data
* Real-time API requests

Validation is implemented inside the shared pipeline layer to prevent divergence.

---

## 8. Failure Handling Policy

Validation failures are handled deterministically:

* **Critical violations** → hard failure (job abort / API rejection)
* **Non-critical warnings** → logged with monitoring signal

All validation outcomes are:

* Logged
* Versioned
* Traceable

---

## 9. Versioning & Governance

Validation rules are:

* Version-controlled
* Tied to model version
* Documented in release artifacts

Any change to validation logic requires:

* Code review
* Test coverage
* Registry annotation

---

## Summary

Data validation is treated as a **safety boundary**, not a preprocessing convenience.

These rules ensure:

* Schema integrity
* Statistical plausibility
* Risk containment
* Reproducible model behavior

The model does not operate on unvalidated data.
