# Stroke and Relevant Risk Factors

## 1. Purpose

This document summarizes the clinical background of stroke and its established risk factors to support problem discovery for the Heart Stroke Risk Stratification project.

The purpose is to understand the clinical context, not to provide medical advice, recommend treatment, or select ML features before the dataset and prediction objective have been assessed.

## 2. Stroke: Definition and Major Types

A stroke occurs when blood flow to part of the brain is interrupted by a blockage or bleeding, potentially damaging brain tissue.

The major types are:

- **Ischaemic stroke:** Occurs when a blood vessel supplying the brain is blocked.
- **Haemorrhagic stroke:** Occurs when a blood vessel ruptures and bleeding occurs in or around the brain.
- **Transient ischaemic attack (TIA):** A temporary episode of neurological dysfunction caused by focal ischaemia without acute infarction. It is not itself classified as a stroke, but it is an important warning event requiring medical assessment.

These distinctions matter because stroke mechanisms, risk factors, clinical assessment, and prevention strategies may differ.

**Source:** World Health Organization, *Stroke* fact sheet.

## 3. Risk Factors

Risk factors are characteristics, conditions, or exposures associated with the likelihood of developing a condition. Their presence does not establish that a particular individual will experience a stroke.

### 3.1 Modifiable or Potentially Modifiable Factors

| Factor | Research notes |
|---|---|
| High blood pressure | An important established risk factor for stroke. |
| Tobacco use | Associated with increased vascular risk. |
| Diabetes and elevated blood glucose | Relevant to vascular health and stroke prevention. |
| Abnormal blood lipids | Relevant to atherosclerotic cardiovascular risk. |
| Atrial fibrillation and certain cardiac conditions | May increase the risk of embolic stroke. |
| Physical inactivity | Relevant to cardiovascular health and stroke prevention. |
| Unhealthy dietary patterns | Relevant to cardiovascular risk management. |
| Overweight and obesity | Associated with cardiometabolic risk. |
| Harmful alcohol use | Associated with adverse health outcomes, including stroke risk. |
| Kidney disease and air pollution | Also identified in public health evidence as relevant risk factors or contributors. |

The factors above are not interchangeable, and their importance may depend on stroke type, population, and clinical context. Some are directly modifiable; others are managed through clinical care or changes in exposure.

### 3.2 Non-Modifiable or Historical Factors

| Factor | Research notes |
|---|---|
| Age | Stroke risk generally increases with age. |
| Family history and genetic predisposition | May contribute to differences in individual susceptibility. |
| Biological sex and life-stage-related factors | May affect risk patterns and prevention considerations. |
| Previous stroke | Cannot be changed as a historical event and is important when considering recurrent stroke rather than only first-stroke risk. |

This classification is a starting point, not a complete clinical taxonomy. A factor may be non-modifiable in itself while its associated risks remain amenable to assessment or management.

## 4. Relevance to Risk Assessment

The presence of established risk factors provides clinical context for investigating stroke risk. However, identifying risk factors is not the same as constructing a validated prediction model.

Several distinctions must be maintained:

- **Risk factor:** A characteristic or exposure associated with a higher likelihood of an outcome.
- **Risk marker:** A measurable characteristic that indicates risk but may not itself be a causal factor.
- **Predictive variable:** A variable used by a particular prediction model to estimate an outcome.
- **Clinical intervention target:** A factor that healthcare professionals may assess or manage to reduce risk.

A clinically relevant risk factor is not automatically an appropriate ML feature. Feature selection must also consider availability at prediction time, data quality, the target population, potential leakage, and the intended prediction horizon.

## 5. Important Limitations

- Evidence from one population or healthcare setting may not generalize to another.
- Risk factors may differ in relevance across ischaemic and haemorrhagic stroke.
- Association does not, by itself, establish causation.
- A factor identified in clinical guidelines may be absent or poorly measured in a particular dataset.
- Retrospective dataset variables do not automatically represent information available before the predicted event.
- This background research does not establish that an ML-based risk stratification system is needed or would improve clinical outcomes.

## 6. Open Questions

- Which population and healthcare setting should the project focus on?
- Is the intended outcome a first stroke, recurrent stroke, or a broader stroke-related outcome?
- What prediction horizon would be meaningful for the intended use?
- Which risk factors are available and reliably measured in the candidate dataset?
- How should established clinical assessment approaches inform later evaluation?

These questions will inform subsequent research into current assessment practices, clinical workflows, prediction tools, and data feasibility.

## 7. References

1. World Health Organization. *Stroke*. https://www.who.int/news-room/fact-sheets/detail/stroke
2. American Heart Association/American Stroke Association. *2024 Guideline for the Primary Prevention of Stroke: Top Things to Know*. https://professional.heart.org/en/science-news/2024-guideline-for-the-primary-prevention-of-stroke/top-things-to-know

Publication details, relevant findings, and limitations should be verified against the original sources and recorded in `source-log.csv`.
