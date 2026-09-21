# Testing Strategy

## Purpose

Testing in the **Stroke Risk Stratification System** is designed to provide **confidence to change**. The objective is not just to detect bugs, but to ensure that data pipelines, models, and system interfaces behave **safely, deterministically, and consistently** across environments.

Given the healthcare-adjacent nature of the system, testing prioritizes:

* Prevention of silent failures
* Early detection of data and schema drift
* Protection against unsafe deployments

---

## Testing Philosophy

The testing approach follows these principles:

* **Shift-left**: Catch failures as early as possible
* **Layered coverage**: Different tests for different failure modes
* **Determinism**: Tests must be repeatable and stable
* **Automation-first**: All critical tests run in CI

No single test is considered sufficient in isolation.

---

## Test Pyramid Overview

The system follows a layered test pyramid:

1. Unit Tests (fast, isolated)
2. Integration Tests (component interaction)
3. Contract Tests (schema guarantees)
4. End-to-End Smoke Tests (deployment sanity)

Each layer has a clear scope and responsibility.

---

## Unit Testing

### Scope

Unit tests validate individual components in isolation:

* Feature transformers
* Imputation logic
* Encoding mappings
* Utility functions

### Key Assertions

* Deterministic outputs for fixed inputs
* Correct handling of missing values
* Stable category mappings
* Explicit failure on invalid inputs

Mocking is used to isolate external dependencies.

---

## Feature Pipeline Tests

Feature pipelines are treated as **critical infrastructure** and tested accordingly.

Tests include:

* Schema validation before and after transformation
* Column order and type stability
* Idempotency of transformations
* Backward compatibility checks for serialized pipelines

These tests prevent training–serving skew.

---

## Integration Testing

### Scope

Integration tests validate interactions between components:

* Data loading → feature pipeline → model inference
* Model artifact loading from registry
* Configuration resolution

### Environment

Integration tests run in a controlled environment using:

* Test containers or local services
* Synthetic or sampled datasets

Failures here indicate broken system wiring rather than logic errors.

---

## API Contract Testing

### Purpose

Contract tests ensure that the API remains safe and predictable for consumers.

Assertions include:

* Request and response schema validation
* Backward compatibility guarantees
* Correct error codes for invalid inputs

These tests protect downstream systems from breaking changes.

---

## End-to-End Smoke Tests

### Scope

Smoke tests validate that a deployed system is fundamentally operational:

* Service starts successfully
* Health checks pass
* A known-good request returns a valid response

Smoke tests do not validate model quality—they validate **system viability**.

---

## Data Validation Tests

Data-related tests detect upstream issues early:

* Missing or null rate checks
* Value range assertions
* Category drift detection
* Schema compatibility checks

These tests run during training and optionally during batch inference.

---

## Model Evaluation Gates

Testing is integrated with model promotion:

* Evaluation metrics must meet minimum thresholds
* Calibration checks must pass
* Subgroup performance regressions block promotion

Failing a gate prevents registry promotion.

---

## CI/CD Integration

All tests are executed as part of the CI pipeline:

* Unit and feature tests on every commit
* Integration and contract tests on merge
* Smoke tests before production deployment

Test failures block deployment automatically.

---

## Non-Goals of Testing

The testing strategy explicitly does not aim to:

* Prove clinical effectiveness
* Replace prospective validation studies
* Guarantee real-world outcomes

Testing ensures **engineering correctness**, not medical efficacy.

---

## Summary

The testing strategy ensures that changes to data, features, models, or infrastructure can be made **safely and confidently**. By combining layered testing with automated enforcement, the system minimizes the risk of silent failures and unsafe deployments.
