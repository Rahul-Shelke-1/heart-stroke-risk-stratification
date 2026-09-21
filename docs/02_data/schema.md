# Data Schema

## Purpose of This Section

A clearly defined data schema is critical for **reproducibility, validation, and safe system integration**. In production ML systems, the schema acts as a contract between:

* Data producers
* Feature engineering pipelines
* Models and inference services

This section documents the **expected structure, types, and semantics** of the input data used by the Stroke Risk Stratification System.

---

## Schema Scope

The schema defined here represents:

* The **model input contract** for training and inference
* The canonical feature set after raw ingestion but before feature transformations

It does **not** represent:

* EHR-native schemas
* Real-time streaming schemas
* Post-feature-engineering representations

---

## Feature Schema Overview

| Feature Name      | Type            | Domain      | Description                    |
| ----------------- | --------------- | ----------- | ------------------------------ |
| age               | Numeric (int)   | Demographic | Age of the individual in years |
| gender            | Categorical     | Demographic | Gender of the individual       |
| ever_married      | Categorical     | Demographic | Marital status indicator       |
| residence_type    | Categorical     | Demographic | Urban or Rural residence       |
| work_type         | Categorical     | Lifestyle   | Type of employment             |
| hypertension      | Binary (0/1)    | Clinical    | History of hypertension        |
| heart_disease     | Binary (0/1)    | Clinical    | History of heart disease       |
| avg_glucose_level | Numeric (float) | Clinical    | Average glucose level          |
| bmi               | Numeric (float) | Clinical    | Body Mass Index                |
| smoking_status    | Categorical     | Lifestyle   | Smoking behavior category      |
| stroke            | Binary (0/1)    | Target      | Stroke occurrence indicator    |

---

## Feature Semantics & Constraints

### Numeric Features

* **age**

    * Expected range: ≥ 0
    * Non-negative integer

* **avg_glucose_level**

    * Positive continuous value
    * May contain outliers

* **bmi**

    * Positive continuous value
    * May contain missing values

---

### Binary Features

* **hypertension**, **heart_disease**

    * Encoded as {0, 1}
    * No severity information encoded

---

### Categorical Features

* **gender**: {Male, Female, Other}
* **ever_married**: {Yes, No}
* **residence_type**: {Urban, Rural}
* **work_type**: {Private, Self-employed, Govt_job, children, Never_worked}
* **smoking_status**: {formerly smoked, never smoked, smokes, Unknown}

Unexpected categories are handled explicitly by preprocessing pipelines.

---

## Target Variable Schema

* **stroke**

    * Binary indicator
    * Highly imbalanced
    * Used only for training and evaluation
    * Never available during inference

---

## Schema Validation & Enforcement

To prevent silent failures and training–serving skew:

* Schema assumptions are enforced via:

    * Explicit column selection
    * Type-aware preprocessing pipelines
* Invalid or missing columns cause deterministic failures

Schema enforcement is treated as a **system reliability concern**, not just a data cleaning task.

---

## Limitations of the Schema

* Does not encode temporal information
* Does not capture clinical severity
* Does not represent causal relationships

The schema is sufficient for **risk stratification demonstrations**, but not for clinical-grade modeling.

---

## Summary

This schema defines a clear and auditable contract between data and model components. Explicit schema documentation:

* Reduces ambiguity
* Prevents integration errors
* Improves long-term maintainability

> *In production ML systems, undocumented schemas are a common source of hidden failures.*
