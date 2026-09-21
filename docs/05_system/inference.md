# System Configuration

## Purpose

This document describes how configuration is managed in the **Stroke Risk Stratification System** to ensure:

* Environment isolation (dev / staging / prod)
* Reproducibility and determinism
* Secure handling of secrets
* Zero hard-coded operational values

Configuration is treated as **first-class infrastructure**, not as ad-hoc constants inside code.

---

## Configuration Design Principles

* **Configuration ≠ Code**: No environment-specific values are hard-coded
* **Explicitness over convenience**: Defaults are minimal and documented
* **Immutability at runtime**: Configuration does not change while a service is running
* **Fail-fast behavior**: Missing or invalid config causes startup failure

---

## Configuration Layers

The system uses layered configuration with strict precedence:

1. **Base configuration** (shared across environments)
2. **Environment-specific overrides**
3. **Runtime secrets** (injected securely)

Later layers always override earlier ones.

---

## Base Configuration

Base configuration defines values that are stable across environments:

* Feature schema versions
* Model input/output contracts
* Logging formats
* Default thresholds (non-production only)

Example (YAML):

```yaml
project:
  name: stroke-risk-stratification
  domain: healthcare-risk

model:
  task: binary_classification
  output: probability

logging:
  level: INFO
```

---

## Environment-Specific Configuration

Environment configuration captures values that differ between deployments:

* Model registry stage (staging vs production)
* API rate limits
* Monitoring thresholds
* Resource sizing

Example:

```yaml
environment: production

model:
  registry_stage: Production
  decision_threshold: 0.65

api:
  rate_limit_per_minute: 300
```

Each environment has its own isolated configuration file.

---

## Secrets Management

Sensitive values are **never** stored in configuration files or source control.

Secrets include:

* API keys
* Registry credentials
* Encryption keys

Secrets are injected at runtime via:

* Secure parameter stores
* Managed secrets services
* IAM-based access where possible

If a required secret is unavailable, the system fails to start.

---

## Configuration for Training Pipelines

Training jobs are configured using explicit, versioned parameters:

* Dataset version identifiers
* Feature pipeline versions
* Hyperparameter ranges
* Random seeds

All training configuration is logged to MLflow to ensure full reproducibility.

---

## Configuration for Inference Services

Inference configuration controls:

* Active model version
* Decision thresholds
* Logging verbosity
* Monitoring hooks

Inference services load configuration at startup and treat it as read-only.

---

## Validation & Schema Enforcement

All configuration files are:

* Validated against a schema
* Checked for missing or incompatible values
* Rejected if deprecated fields are used

This prevents silent misconfiguration and runtime surprises.

---

## Change Management

* Configuration changes are reviewed like code
* All changes are version-controlled
* Production changes require explicit approval

Emergency changes are logged and audited.

---

## Failure Modes & Safeguards

| Failure Mode       | Mitigation                |
| ------------------ | ------------------------- |
| Missing config     | Startup failure           |
| Wrong environment  | Explicit environment flag |
| Secret leakage     | External secret stores    |
| Drifted thresholds | Registry + config linkage |

---

## Summary

Configuration management in this system is designed to support **safe deployment, reproducibility, and governance**. By externalizing all operational values and enforcing validation, the system avoids one of the most common causes of production ML failures: silent configuration drift.
