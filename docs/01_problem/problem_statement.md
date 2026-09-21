# Problem Statement

## Background

Stroke is a leading cause of mortality and long-term disability worldwide. Many strokes are **preventable** if high-risk individuals are identified early and provided with appropriate interventions (lifestyle changes, medication, or closer clinical monitoring).

Healthcare systems often operate under constrained resources, making **risk prioritization** essential. Rather than treating stroke prediction as a purely academic classification task, this project frames it as a **risk stratification problem** aligned with real-world clinical and operational needs.

---

## Core Problem

Given structured patient data containing demographic, clinical, and lifestyle attributes, the goal is to **estimate an individual’s risk of experiencing a stroke** and stratify patients into clinically meaningful risk categories.

The system must:

* Identify **high-risk individuals** with high sensitivity
* Provide **consistent and reproducible predictions**
* Produce outputs suitable for downstream clinical decision-support systems (not autonomous decision-making)

---

## Why Risk Stratification (Not Just Classification)

In real healthcare settings:

* Binary predictions (stroke / no-stroke) are often insufficient
* Clinicians and care managers think in **risk tiers**, not raw probabilities
* Intervention strategies differ by risk level

Therefore, this project treats stroke prediction as:

> **A risk stratification task built on top of probabilistic classification**

Where:

* The model estimates stroke probability
* Probabilities are mapped to risk bands (e.g., low / medium / high)
* Thresholds are chosen based on cost and safety considerations

---

## Stakeholders

This system is designed with the following stakeholders in mind:

* **Clinicians** – Need interpretable and conservative risk signals
* **Healthcare administrators** – Need population-level risk insights
* **ML Engineers / Data Scientists** – Need reproducibility and governance
* **Auditors / Reviewers** – Need traceability and documentation

Each design decision balances the needs of these groups.

---

## Constraints & Assumptions

### Data Constraints

* Dataset is retrospective and observational
* Labels are assumed to be correct but not clinically adjudicated
* Population may not represent all demographics equally

### System Constraints

* The system is **decision-support only**, not autonomous
* Predictions are advisory and must be reviewed by humans
* No real-time clinical integration is assumed

These constraints are explicitly acknowledged and documented to avoid overclaiming.

---

## Out of Scope

The following are intentionally **out of scope** for this project:

* Clinical diagnosis or treatment recommendation
* Regulatory approval (e.g., FDA / CE / CDSCO)
* Real patient data ingestion
* Direct integration with Electronic Health Record (EHR) systems

This project focuses on **engineering correctness and MLOps maturity**, not clinical deployment.

---

## Problem Framing Summary

In summary, the problem addressed is:

> *How can we design a reliable, auditable, and production-ready machine learning system that stratifies individuals by stroke risk, while respecting real-world constraints, uncertainties, and ethical boundaries?*

This framing guides all downstream decisions in feature engineering, modeling, evaluation, and system design.
