# 1.1.1 — Define domain research questions and search strategy

## 1. Define the research questions

We'll use the following questions to guide the research. They are intentionally focused on understanding the problem space, not deciding which model to train.

ID | Research question | Why it matters
--|--|--
RQ1 | What is stroke, and what major types and clinical distinctions matter for risk assessment? | Establishes the clinical context.
RQ2 | What established factors are associated with stroke risk, and how are they assessed? | Helps understand relevant patient characteristics and risk factors.
RQ3 | How is stroke risk currently assessed, and what decisions can that assessment inform? | Establishes current practice and decision context.
RQ4 | Who participates in risk assessment, prevention, and related care decisions? | Identifies potential users and stakeholders.
RQ5 | What information is collected, interpreted, communicated, and acted upon during the workflow? | Supports workflow mapping and identification of information gaps.
RQ6 | What established clinical scores and data-driven prediction approaches already exist? | Prevents reinventing existing approaches and helps reveal limitations.
RQ7 | What limitations or unmet needs have been documented in existing assessment practices and prediction tools? | Generates evidence-backed candidate problems.
RQ8 | What evidence supports these findings, and what remains uncertain or unvalidated? | Keeps discovery rigorous and transparent.

## 2. Research Boundaries and Time Budget

* **Research boundary:** We are investigating stroke-risk assessment and prevention, not acute stroke diagnosis or emergency detection. Those are different problem contexts and should not be mixed without a clear reason.

Also, the current project idea—using risk stratification to help prioritize further assessment—is a working hypothesis, not a validated user need. We should investigate whether the evidence supports it before committing to that problem.

* **Initial planning issue:** 1–2 hours.
* **Overall discovery research:** Initially time-boxed to 3–5 working days, then reassessed based on evidence gaps.

The time budget is a constraint against unfocused research, not a reason to stop when important questions remain unanswered.

## 3. Establish the search strategy

Start with authoritative clinical guidelines and public health sources, then use peer-reviewed studies to investigate specific practices, workflows, prediction approaches, and reported limitations.

### Source hierarchy

> **Tier 1 - Clienical guidelines and public health authorities**
> - Use for established clinical context, prevention recommendations, and current practices.
> - [WHO - Cardiovascular diseases](https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-%28CVDs%29)
> - [American Heart Association - 2024 primary prevention of stroke guideline](https://professional.heart.org/en/science-news/2024-guideline-for-the-primary-prevention-of-stroke/top-things-to-know)

> **Tier 2 - Peer-reviewed clinical research**
> - Use for specific evidence, assessment practices, study populations, and reported limitations.
> - [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
> - [Google Scholar](https://scholar.google.com/)

> **Tier 3 - Prediction-model methodology**
> - Use to understand what makes clinical prediction research transparent and how to assess its limitations.
> - [TRIPOD+AI (2024) - Reporting prediction model studies](https://www.bmj.com/content/385/bmj-2023-078378)
> - [PROBAST+AI (2025) - Prediction-model quality and risk of bias](https://www.bmj.com/content/388/bmj-2024-082505)

The WHO provides foundational information about cardiovascular risk factors, while the AHA guideline gives a more specific primary-prevention perspective. TRIPOD+AI and PROBAST+AI are useful methodological references for later work; they are not clinical guidelines or proof that a particular prediction model is appropriate.

### Search queries to use

Copy these into PubMed or Google Scholar as you work through the subsequent issues.

Topic | Suggested search query
--|--
Stroke background | `stroke types risk factors prevention clinical review`
Risk factors | `stroke risk factors primary prevention guideline`
Current assessment | `stroke risk assessment clinical practice primary prevention`
Workflow | `primary care cardiovascular risk assessment workflow stroke prevention`
Clinical scores | `stroke risk prediction score inteded population validation`
ML approaches. | `machine learning models stroke risk prediction external validation calibration`
Model limitaions | `stroke prediction model limitaions bias generalizability clinical utility`
Decision support | `clinical decision support risk stratfication stroke prevention workflow`

Use specific terms such as `primary prevention`, `prognostic model`, `external validation`, and `calibration` to narrow results when searches are too broad.

## 4. Define source-selection rules

Use these rules consistently so the research stays focused and defensible.

- **Prefer:** Current clinical guidelines, government and public health sources, systematic reviews, and relevant peer-reviewed studies.

- **Use older sources when justified:** Foundational studies or established assessment tools may require older publications. Record publication dates and check whether newer guidance supersedes them.

- **Check applicability:** Record the population, country or healthcare setting, prediction target, and time horizon when the source reports them.

- **Avoid relying on:** Unreferenced blogs, commercial claims, copied articles, and model-performance claims that cannot be traced to an original study.

- **Do not overgeneralize:** Evidence from one population or hospital does not automatically apply to another.

- **Separate facts from hypotheses:** A published association between a risk factor and stroke does not, by itself, prove that a particular workflow is failing or that an ML system would improve outcomes.

For each source, capture its title, authors or organization, publication year, URL or DOI, source type, key findings, limitations, and relevance to the research question.

## 5. Establish the research documentation structure

For this issue, keep the documentation lightweight. You don't need a separate document for every question.

Recommended repository layout:

```
research/
└── domain-and-workflow/
    ├── research-strategy.md
    └── source-log.csv
```

- `research-strategy.md` — research questions, search strategy, source-selection rules, and research boundaries.
- `source-log.csv` — one row per source, with its metadata, findings, limitations, and associated research question IDs.

## 6. Use this source-log template

Field | What to record
--|--
source_id |	Unique identifier, e.g. SRC-001
research_question |	RQ1, RQ2, etc.
title |	Publication or guideline title
organization_or_authors	| Publisher, organization, or authors
year |	Publication year
source_type |	Guideline, review, observational study, prediction study, etc.
url_or_doi|	Traceable source location
key_findings|	Relevant findings in your own words
limitations|	Applicability, study limitations, or evidence gaps
relevance|	Why the source matters to the project
evidence_status|	Established finding, indirect evidence, or hypothesis

