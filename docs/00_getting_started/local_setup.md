### A) Environment Setup

* Python version
* Poetry install
* Install dependencies

Example:

```
poetry install
```

---

### B) Run Training

```
make train
```

or

```
poetry run python src/train.py
```

---

### C) Run API

```
docker-compose up
```

or

```
uvicorn app.main:app --reload
```

---

### D) View MLflow UI

```
mlflow ui
```

## Infrastructure Requirement

This project assumes AWS infrastructure is already provisioned via a separate Terraform repository (S3, ECR, IAM, etc.).

---
