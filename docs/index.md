# Stroke Risk Stratification System

> Production-grade end-to-end ML system for clinical stroke risk stratification

---

## Overview

The Stroke Risk Stratification System is a production-oriented machine learning platform designed to predict stroke risk using demographic, clinical, and lifestyle data.

The project demonstrates how machine learning systems move from experimentation to reproducible training, deployment, monitoring, and governance using modern MLOps practices.

The system follows a **decoupled architecture**, where ML workflows are separated from infrastructure provisioning.

---

## Key Capabilities

- End-to-end ML pipelines
- Feature engineering and preprocessing workflows
- Experiment tracking with MLflow
- Model registry and lineage tracking
- CI/CD-driven workflows
- AWS-aligned deployment architecture
- Monitoring for drift and performance degradation

---

## Success Criteria

### Clinical Objectives
- Maximize recall for high-risk patients
- Support risk-based patient stratification
- Reduce missed high-risk cases

### Engineering Objectives
- Reproducible pipelines
- Deterministic preprocessing
- Tested modular architecture

### Production Objectives
- Model versioning
- Deployment-ready artifacts
- Monitoring and governance

---

## Infrastructure Layer (External MLOps Platform)

This project runs on a Terraform-based MLOps platform that provisions scalable cloud infrastructure for ML workloads.

### Platform responsibilities:
- S3 buckets for datasets and artifacts
- ECR repositories for container images
- IAM roles and access control
- Compute infrastructure for training and inference
- Environment separation (dev/staging/prod patterns)

### ML system responsibilities (this repository):
- Training and evaluation pipelines
- Feature engineering workflows
- Model packaging and versioning
- Inference API implementation
- Integration with platform-provisioned resources

This separation enables independent evolution of ML workflows and infrastructure layers.

---

## End-to-End System Architecture

This architecture represents the deployed production workflow integrating both the ML application layer and the underlying MLOps platform.

The end-to-end system is composed of the following logical components:

- Data Ingestion & Sources
- Experimentation & MLflow Tracking
- Training & Feature Pipelines
- Model Registry & Versioning
- Inference Service Layer
- Monitoring, Drift & Observability

![architecture](assets/flowcharts/end-to-end-ml-architecture-heart-stroke-prediction.drawio.svg)

The infrastructure layer is implemented in a dedicated Terraform-based MLOps platform repository:
👉 <LINK_TO_YOUR_TERRAFORM_REPO>

### System-of-Systems Design

This system is designed as part of a larger ML platform ecosystem:

- This repository defines the ML application layer (training, evaluation, inference)
- The Terraform-based platform provides infrastructure provisioning, scaling, and environment management

Together, they form a production-grade, multi-layer ML system architecture.

---

## Documentation Guide

The documentation is organized into the following major sections:

| Section | Description |
|---|---|
| Getting Started | Local setup, environment configuration, and project initialization |
| Problem Framing | Business framing, objectives, and success criteria |
| Data Foundation | Dataset structure, schema, validation, quality checks, and bias considerations |
| Feature Engineering | Missing data handling, encoding strategies, normalization, and preprocessing pipelines |
| Modeling | Experiment tracking, evaluation strategy, and model governance |
| System Design | End-to-end architecture, inference workflows, and API specifications |
| Reliability & Quality | Testing strategy, monitoring, and drift detection |
| Governance | Ethical considerations, risks, and future roadmap |

---

## Tech Stack

- Python
- Scikit-learn
- MLflow
- AWS
- Docker
- FastAPI
- GitHub Actions

---

???+ warning "Disclaimer"
    This project is intended for educational and demonstrational purposes only.
    It is not a medical device and should not be used for real clinical decision-making.
