# 🩺❤️ Heart Stroke Risk Stratification Platform

**Production-grade ML system for stroke risk prediction and stratification with a complete MLOps lifecycle.**

> 🚀 End-to-end ML system from data ingestion to deployment and monitoring.

![CI](https://github.com/Rahul-404/heart-stroke-prediction/actions/workflows/ml-training-ci.yml/badge.svg)
![Docs](https://github.com/Rahul-404/heart-stroke-prediction/actions/workflows/docs-ci.yml/badge.svg)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](https://rahul-404.github.io/heart-stroke-prediction/)

## 🚀 Demo

### 🔗 Live API

`POST /predict`

Deployed as a REST API for real-time inference.

### 📥 Sample Request

```json
{
  "gender": "M",
  "age": 67,
  "bmi": 28.5,
  "avg_glucose_level": 140,
  "hypertension": 1,
  "heart_disease": 0,
  "smoking_status": "formerly_smoked",
  "work_type": "gov_job",
  "ever_married": 1,
  "residence_type": "urban"
}
```

### 📤 Response

```json
{
  "stroke_probability": 0.78,
  "risk_level": "High"
}
```

### 🎥 Demo Video

<!-- [Watch Demo](YOUR_LINK) -->
[![Project Demo](https://img.youtube.com/vi/Z83Y36jqufg/0.jpg)](https://youtu.be/Z83Y36jqufg)

---

## 🧠 Problem & Business Impact

Stroke is a leading cause of mortality, but early detection enables prevention.

This system predicts stroke risk and stratifies patients into actionable tiers (Low / Medium / High), enabling healthcare providers to prioritize high-risk individuals and reduce unnecessary screenings.

---

## 📊 Key Results

### 🔍 Key Insight

The model is optimized for **early risk detection**, achieving high precision in the top risk segments, making it suitable for real-world clinical triaging.

### 🔍 Additional Insight

The production model significantly improves recall in top-risk segments, enabling better identification of high-risk patients without increasing screening overhead.

| Metric | Baseline | Production |
|---|---|---|
| ROC-AUC | 0.7117 (±0.0789) | 0.9017 (±0.0789) |
| PR-AUC | 0.6944 (±0.0490) | 0.8844 (±0.0490) |
| Recall @ 10% | 0.1867 (±0.0267) | 0.3567 (±0.0267) |
| Recall @ 15% | 0.2400 (±0.0327) | 0.4800 (±0.0327) |
| Recall @ 20% | 0.3467 (±0.0499) | 0.6967 (±0.0499) |
| Precision @ 10% | 0.7000 (±0.1000) | 0.8900 (±0.1000) |
| NNS @ 10% | 1.4667 (±0.2667) | 1.1200 (±0.2667) |

---

## 🏗️ System Architecture

![Architecture](flowcharts/architecture.png)

---

## ⚡ What Makes This Different

- End-to-end **production MLOps system**, not just a model
- Focus on **risk stratification**, not raw prediction
- Designed for **real-time inference + monitoring**
- Supports **automated retraining under drift**
- Combines **data engineering + ML + infra**

---

## 🧠 Key Design Decisions

- Used Recall@K due to imbalanced healthcare risk prioritization
- Optimized for precision in top risk segments for clinical usability
- Used MLflow for reproducibility and experiment tracking
- Designed modular pipelines for scalable retraining

---

## ⚙️ Tech Stack

![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white) • ![MongoDB](https://img.shields.io/badge/mongodb-%2347A248.svg?style=flat&logo=mongodb&logoColor=white) • ![PostgreSQL](https://img.shields.io/badge/postgresql-%23336791.svg?style=flat&logo=postgresql&logoColor=white)

![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white) • ![Optuna](https://img.shields.io/badge/Optuna-A78BFA?style=flat&logo=optuna&logoColor=white) • ![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow&logoColor=white) • ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

![Docker](https://img.shields.io/badge/docker-%23007ACC.svg?style=flat&logo=docker&logoColor=white) • ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) • ![Amazon SageMaker](https://img.shields.io/badge/Amazon%20SageMaker-FF9900?style=flat&logo=amazonaws&logoColor=white) • ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)

---

## 📖 Full Documentation

👉 https://rahul-404.github.io/heart-stroke-prediction/

---

## 📬 Contact

[rahulshelke3399@gmail.com](mailto:rahulshelke3399@gmail.com) |
[LinkedIn](https://www.linkedin.com/in/rahulshelke981) | [GitHub](https://github.com/Rahul-404)

---

## ⭐ If this project helps you, consider starring!
