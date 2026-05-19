# System Architecture

## Integrated Deployment Architecture

The following diagram represents the end-to-end production architecture, combining:

- The ML system (this repository)
- The Terraform-based MLOps platform responsible for infrastructure provisioning

This reflects the actual deployed workflow used to run training, evaluation, and inference pipelines in a production-like environment.

![architecture](flowcharts/end-to-end-ml-architectures-heart-stroke-prediction.drawio.svg)

## System Boundary Overview

### ML System Layer (This Repository)
- Feature engineering
- Model training
- Experiment tracking
- Inference API
- Model packaging

### MLOps Platform Layer (Terraform Repository)
- S3 storage provisioning
- ECR image registry
- IAM roles and policies
- Compute infrastructure
- Environment orchestration

### Integration Flow
- ML system consumes platform-provisioned resources
- Training jobs execute on platform-managed compute
- Artifacts stored in S3
- Docker images pushed to ECR for deployment

## Architectural Objective

The **Stroke Risk Stratification System** is designed as a **production-oriented, end-to-end ML system** that emphasizes reliability, traceability, and controlled risk exposure rather than raw model complexity.

The architecture follows these principles:

* Clear separation between experimentation, training, and inference
* Reproducibility and auditability at every stage
* Minimal operational coupling
* Cloud-native, managed-service-first design

This system is intended to demonstrate how a real-world healthcare risk model *should* be structured, even when built as a portfolio project.

---

## High-Level Architecture Overview

The system consists of the following logical layers:

1. **Data & Experimentation Layer**
2. **Training & Pipeline Layer**
3. **Model Registry & Artifact Store**
4. **Inference & Serving Layer**
5. **Monitoring & Governance Layer**

Each layer has explicit responsibilities and well-defined boundaries.

---

## Data & Experimentation Layer

### Components

* Source datasets (versioned snapshots)
* Exploratory notebooks
* Feature engineering pipelines
* MLflow experiment tracking

### Responsibilities

* Controlled exploration and hypothesis testing
* Feature pipeline convergence
* Logging of parameters, metrics, artifacts, and code references

### Design Rationale

Experimentation is intentionally **isolated from production systems**. Notebooks never directly deploy models. Only finalized pipelines and models promoted through the registry can advance.

---

## Training & Pipeline Layer

### Components

* Automated training pipeline (e.g., SageMaker Pipelines / containerized jobs)
* Scheduled or manually triggered runs
* Immutable training environments

### Responsibilities

* Deterministic data ingestion
* Feature transformation using frozen pipelines
* Model training and evaluation
* Emission of versioned model artifacts

### Design Rationale

Training is treated as a **repeatable manufacturing process**, not an ad-hoc script. Every run is reproducible from configuration alone.

---

## Model Registry & Artifact Store

### Components

* Model Registry (e.g., MLflow Model Registry)
* Artifact storage (models, preprocessing pipelines)
* Metadata store (metrics, lineage, approvals)

### Responsibilities

* Single source of truth for deployable models
* Stage transitions (Staging → Production)
* Governance and rollback support

### Design Rationale

No model can be deployed without passing through the registry. This enforces accountability and prevents shadow deployments.

---

## Inference & Serving Layer

### Components

* REST API (e.g., API Gateway)
* Stateless inference service (e.g., Lambda or container-based endpoint)
* Serialized preprocessing + model bundle

### Request Flow

1. Client submits patient feature payload
2. Request is validated against schema
3. Preprocessing pipeline is applied
4. Model generates probability score
5. Thresholding converts score into risk category
6. Structured response is returned

### Design Rationale

Inference services are **stateless and horizontally scalable**. All intelligence lives in versioned artifacts, not runtime logic.

---

## Monitoring & Governance Layer

### Components

* Prediction logging (inputs, outputs, metadata)
* Data drift and prediction drift monitors
* Performance tracking against delayed labels
* Alerting and dashboards

### Responsibilities

* Detect distribution shifts
* Surface calibration decay
* Provide audit trails for decisions

### Design Rationale

Monitoring is not optional. In healthcare-adjacent systems, *silent degradation is the primary risk*, not downtime.

---

## Security & Access Boundaries

* Training and inference run in isolated environments
* Secrets are managed via secure stores
* Least-privilege IAM roles are enforced
* No direct user access to model artifacts

These controls reduce blast radius and accidental misuse.

---

## Failure Modes & Safeguards

| Failure Mode          | Mitigation                              |
| --------------------- | --------------------------------------- |
| Bad training data     | Versioned datasets + validation checks  |
| Overfitted model      | Hold-out evaluation + registry gates    |
| Drift in production   | Monitoring + alerting                   |
| Misuse of predictions | Documented intended use + API contracts |

---

## Why This Is "Production-Grade" but Not Deployed Clinically

This architecture mirrors real production systems. However:

* No prospective clinical validation has been performed
* The dataset is retrospective and limited
* Regulatory approvals are not in place
* The system is positioned as **decision support**, not diagnosis

These constraints are ethical and legal, not technical.

---

## Summary

The architecture demonstrates how to design an ML system that is:

* Deployable
* Auditable
* Governable
* Safe by construction

It intentionally prioritizes **system integrity over experimentation velocity**, reflecting real-world healthcare ML practices.
