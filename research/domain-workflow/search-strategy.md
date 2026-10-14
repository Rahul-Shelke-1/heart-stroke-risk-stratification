# Domain & Workflow Research — Search Strategy

## 1. Purpose

Establish an evidence-based understanding of stroke, current risk-assessment practices, existing prediction approaches, and potential gaps in clinical workflows.

The purpose of this research is to identify and evaluate candidate problems for a Heart Stroke Risk Stratification system. It is not to establish clinical recommendations, select a final ML model, or claim clinical validation.

## 2. Research Boundaries and Time Budget

* **Initial planning issue:** 1–2 hours.
* **Overall discovery research:** Initially time-boxed to 3–5 working days, then reassessed based on evidence gaps.
* **Research approach:** Targeted searches, structured source screening, evidence extraction, and iterative synthesis.
* **Geographic focus:** Global evidence for clinical and methodological context, supplemented by Indian evidence where relevant.
* **Intended output:** A traceable evidence base that supports problem discovery, stakeholder hypotheses, and subsequent feasibility decisions.

The time budget is a constraint against unfocused research, not a reason to stop when important questions remain unanswered.

## 3. Core Research Pillars

### Pillar A — Clinical Standards and Stroke Prevention

**Objective:** Understand stroke, its risk factors, prevention practices, and established clinical guidance.

Research questions:

* What are the main types of stroke, and what distinguishes primary prevention from secondary prevention and acute stroke detection?
* Which modifiable and non-modifiable factors are associated with stroke?
* How are stroke risk factors assessed and managed in clinical practice?
* What established guidelines and risk-assessment approaches are relevant?
* What populations and clinical contexts do these guidelines and approaches address?

Preferred sources:

* WHO and other authoritative public-health organizations.
* American Heart Association/American Stroke Association (AHA/ASA) guidelines.
* Peer-reviewed systematic reviews and relevant original studies.

### Pillar B — Indian Epidemiology and Healthcare Context

**Objective:** Understand the relevance of global findings to Indian populations and healthcare settings.

Research questions:

* What is known about stroke burden and its variation across India?
* Which risk factors and population characteristics are relevant in Indian studies?
* What evidence exists about access to preventive care, risk-factor assessment, and follow-up?
* What data sources and clinical measurements are available in the intended setting?
* Where does evidence from other populations have limited applicability?

Preferred sources:

* Indian Council of Medical Research (ICMR).
* Indian public-health authorities and relevant professional organizations.
* Peer-reviewed Indian cohort studies, systematic reviews, and epidemiological research.
* World Stroke Organization (WSO) reports where relevant.

Do not assume that findings from one Indian region, hospital, or cohort represent the entire country.

### Pillar C — Prediction Models and Evaluation Methodology

**Objective:** Understand established stroke-risk prediction approaches and how their quality and applicability are evaluated.

Research questions:

* Which established clinical scores and statistical or ML prediction models address stroke risk?
* What outcome, prediction horizon, population, and intended use does each model target?
* What predictors, data sources, and assumptions does each approach require?
* How are discrimination, calibration, clinical usefulness, and generalizability evaluated?
* What limitations, validation gaps, and reporting weaknesses are documented?
* What evidence would be required before considering a model suitable for a new population?

Preferred sources:

* Peer-reviewed clinical prediction-model studies.
* Systematic reviews of stroke-risk prediction.
* TRIPOD+AI reporting guidance.
* Relevant methodological guidance on prediction-model bias, validation, calibration, and clinical utility.

### Pillar D — Clinical Workflow and Stakeholder Needs

**Objective:** Understand how risk assessment relates to real decisions and identify possible workflow problems.

Research questions:

* Who may assess stroke risk, and in what settings?
* What information is collected, reviewed, and acted upon?
* Which decisions follow an assessment?
* What documented workflow limitations, information gaps, or access constraints exist?
* Which users might benefit from better risk stratification, and how would it support their decisions?
* What assumptions require direct confirmation from clinicians or other stakeholders?

Preferred sources:

* Clinical guidelines and care pathways.
* Published workflow studies and implementation research.
* Relevant healthcare-system reports.
* Direct stakeholder interviews, if access becomes available.

Desk-research findings must not be represented as interview-validated user needs.

## 4. Search and Source-Selection Strategy

### 4.1 Discovery sources

Use:

* PubMed for biomedical literature.
* Google Scholar for broader academic discovery and citation tracking.
* Official WHO, ICMR, AHA/ASA, and WSO resources for relevant guidance and reports.
* Reference lists of high-quality reviews and influential prediction-model studies.

### 4.2 Search-query construction

Combine four elements where applicable:

1. Condition or population: stroke, Indian adults, primary prevention.
2. Research topic: risk factors, assessment, workflow, prediction.
3. Method or context: clinical prediction model, cohort, calibration, healthcare access.
4. Evidence type or geography: guideline, systematic review, India.

Example searches:

* `stroke primary prevention guideline risk assessment`
* `stroke risk prediction model systematic review calibration`
* `stroke epidemiology India risk factors cohort`
* `stroke prevention primary care India workflow`
* `stroke clinical prediction model external validation`
* `TRIPOD+AI clinical prediction model reporting`

Record the query, search platform, date, and relevant selection decisions so the search can be repeated.

### 4.3 Screening funnel

**Stage 1 — Initial triage**

Review the title, abstract, publication date, population, and conclusion. Inspect tables and figures when they are relevant.

Retain a source if it contributes meaningful evidence to one or more research questions.

**Stage 2 — Focused review**

For important sources, inspect the methods, study population, outcome definition, prediction horizon, results, limitations, and funding or conflicts of interest where relevant.

Do not use an abstract or conclusion alone to establish a model's validity or clinical applicability.

**Stage 3 — Evidence extraction**

Record the key findings, source limitations, applicability to the project, and remaining questions in the research log.

**Stage 4 — Synthesis**

Compare findings across sources, identify agreement and disagreement, record evidence gaps, and distinguish supported findings from hypotheses.

### 4.4 Source-quality principles

Prioritize:

* Authoritative clinical guidelines for clinical recommendations.
* Systematic reviews for a broad overview of available evidence.
* Original studies for population-specific findings and detailed methods.
* Methodological guidance for evaluating prediction models.
* Transparent reporting of study limitations, uncertainty, and applicability.

Prefer current guidance where available, but retain older landmark studies when they remain relevant. Record publication dates and avoid assuming that newer automatically means better.

## 5. Evidence-Extraction Template

Use this template for important papers, guidelines, and reports.

### [Author/Organization, Year] — [Short Title]

* **Source and link:**
* **Source type:**
* **Research question addressed:**
* **Objective:**
* **Population and setting:**
* **Methods or guideline scope:**
* **Key findings:**
* **Limitations and uncertainty:**
* **Relevance to the project:**
* **Implications for problem discovery:**
* **Evidence classification:** Established evidence / desk-research inference / unvalidated hypothesis.
* **Follow-up questions:**

For prediction-model studies, also record the target outcome, prediction horizon, predictors, sample size, outcome frequency, validation design, discrimination, calibration, and clinical utility where reported.

Do not compare reported model metrics without considering differences in populations, outcomes, prediction horizons, and validation methods.

## 6. Practical Constraints to Investigate

Research the following as questions, not predetermined requirements:

* **Clinical:** How risk factors are measured and interpreted; which prevention guidelines apply; and which decisions belong to qualified healthcare professionals.
* **Data:** Availability, missingness, measurement quality, representativeness, outcome definitions, and the timing of predictor measurements.
* **Technical:** Baselines, data leakage, validation strategy, class imbalance, calibration, generalization, and interpretability.
* **Workflow:** How users might interpret and act on risk estimates, and what information they would need.
* **Ethical and regulatory:** Privacy, consent, fairness, explainability, intended-use boundaries, and applicable regulatory requirements.

Do not establish treatment thresholds, diagnostic claims, or clinical deployment requirements from literature review alone.

## 7. Research Log and Traceability

Maintain a separate `research-log.md` with the following fields:

| Field                   | Description                                    |
| ----------------------- | ---------------------------------------------- |
| Source ID               | Stable identifier for referencing the source   |
| Bibliographic details   | Title, author, year, DOI or URL                |
| Search details          | Search platform, query, and date found         |
| Research pillar         | A, B, C, or D                                  |
| Evidence summary        | Findings in your own words                     |
| Limitations             | Applicability and uncertainty                  |
| Evidence classification | Established evidence, inference, or hypothesis |
| Project implication     | Relevance to the candidate problem             |
| Follow-up               | Unanswered questions                           |

Keep the full source details and evidence trail in the research artifacts so that later decisions can be traced back to the evidence.

## 8. Stopping and Completion Criteria

The research phase is ready for synthesis when:

* All four research pillars have been addressed at an initial level.
* Key clinical and methodological sources have been reviewed beyond abstracts.
* Relevant Indian evidence has been considered, or the lack of suitable evidence is documented.
* Major uncertainties and contradictory findings are recorded.
* Candidate workflow and stakeholder questions are documented.
* Additional research questions are prioritized by their likely impact on project decisions.
* Findings can be traced to sources and separated from assumptions.

At the end of the initial time budget, review progress and remaining evidence gaps. Extend the investigation only when the unanswered questions could materially affect problem selection, safety, or feasibility.

## 9. Expected Deliverables

* `research/domain-workflow/search-strategy.md`
* `research/domain-workflow/research-log.md`

Subsequent issues will produce focused research artifacts for stroke risk factors, existing assessment practices, care workflows, prediction approaches, and the final synthesis.