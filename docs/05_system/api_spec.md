# API Specification

## Purpose and Scope

This API exposes the **Stroke Risk Stratification System** as a **decision-support service**. It is explicitly **not** a diagnostic API and must not be used as a sole basis for clinical decisions.

The API is designed to be:

* Deterministic
* Versioned
* Strictly validated
* Safe by default

---

## API Design Principles

* **Schema-first**: All requests and responses conform to a predefined schema
* **Backward compatibility**: Breaking changes require a new API version
* **Explicit constraints**: Invalid or out-of-scope inputs are rejected
* **Explainable outputs**: Responses include confidence and risk context

---

## Base URL & Versioning

```
POST /v1/predict/stroke-risk
```

Versioning is encoded in the URL to ensure:

* Safe evolution of models
* Parallel support for legacy consumers
* Clear audit trails

---

## Authentication & Authorization

* Requests are authenticated using API keys or IAM-based authorization
* Access is restricted to approved consumers
* Rate limiting is enforced to prevent abuse

Authentication failures return `401 Unauthorized`.

---

## Request Schema

### Content-Type

```
application/json
```

### Request Body

```json
{
  "age": 67,
  "gender": "male",
  "hypertension": 1,
  "heart_disease": 0,
  "ever_married": "yes",
  "work_type": "private",
  "residence_type": "urban",
  "avg_glucose_level": 156.2,
  "bmi": 28.4,
  "smoking_status": "formerly_smoked"
}
```

### Validation Rules

* All required fields must be present
* Data types and value ranges are strictly enforced
* Categorical values must belong to known vocabularies
* Requests failing validation return `400 Bad Request`

No implicit coercion is performed.

---

## Response Schema

### Successful Response (200 OK)

```json
{
  "model_version": "stroke-risk-model:v1.0.0",
  "prediction_timestamp": "2026-02-07T10:15:30Z",
  "stroke_risk_probability": 0.73,
  "risk_category": "high",
  "decision_threshold": 0.65,
  "disclaimer": "This output is a decision-support signal and not a medical diagnosis."
}
```

### Field Semantics

| Field                   | Description                         |
| ----------------------- | ----------------------------------- |
| model_version           | Registry-qualified model identifier |
| stroke_risk_probability | Calibrated risk score in [0, 1]     |
| risk_category           | Derived label based on thresholding |
| decision_threshold      | Threshold used for categorization   |

---

## Error Responses

| Status Code | Meaning               | Example Cause             |
| ----------- | --------------------- | ------------------------- |
| 400         | Bad Request           | Schema validation failure |
| 401         | Unauthorized          | Invalid credentials       |
| 403         | Forbidden             | Access not permitted      |
| 422         | Unprocessable Entity  | Logically invalid input   |
| 500         | Internal Server Error | Unexpected failure        |

Error responses include a machine-readable error code and message.

---

## Idempotency & Determinism

* Identical requests against the same model version return identical responses
* No state is stored between requests
* Randomness is not used during inference

This guarantees reproducibility for audits and investigations.

---

## Logging & Observability

For each request, the system logs:

* Request metadata (excluding PII)
* Model version and threshold
* Prediction output
* Latency and error signals

Logs are used exclusively for monitoring, debugging, and governance.

---

## Security Considerations

* Payloads are encrypted in transit
* No raw predictions are cached client-side
* Access keys can be rotated without downtime

Sensitive patient identifiers are intentionally excluded from the API contract.

---

## Usage Constraints

This API must not be used:

* For autonomous clinical decision-making
* As a diagnostic substitute
* Without human review

Misuse constitutes a violation of system intent and governance policy.

---

## Change Management

* All breaking changes require a new version
* Model upgrades do not change the API contract
* Deprecation notices are issued before removal

---

## Summary

This API specification prioritizes **safety, clarity, and governance** over flexibility. It exposes a controlled interface that aligns with healthcare-adjacent production requirements while remaining auditable and reproducible.
