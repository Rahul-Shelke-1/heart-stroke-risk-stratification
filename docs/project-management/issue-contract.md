# Issue Contract

## 1. Purpose

The Issue Contract defines the minimum structure and quality requirements for implementation issues in the project.

Its purpose is to ensure that work is clearly understood, appropriately scoped, independently executable, and objectively verifiable before implementation begins.

Every substantive implementation issue should provide enough information to answer:

* Why is this work needed?
* What is included?
* What does completion look like?
* What work needs to be performed?
* How much effort is expected?
* Which project milestone does the work contribute to?

The contract is intended to reduce ambiguity, prevent uncontrolled scope expansion, improve estimation, and make completed work traceable to project outcomes.

---

## 2. Applicability

The Issue Contract applies to substantive project work that requires planning and execution, including:

* Features
* Chores
* Infrastructure changes
* ML work
* Data work
* Testing work
* Documentation work with meaningful project scope
* Research or investigation work that requires a defined outcome

The standard contract contains seven required fields:

1. Title
2. Why
3. Scope
4. Acceptance Criteria
5. Tasks
6. Estimate
7. Milestone

Small administrative or maintenance changes may use a lighter structure when applying the complete contract would add unnecessary overhead.

The decision to use a lighter structure should be based on the size and complexity of the work, not to avoid defining scope or completion criteria.

---

## 3. Issue Structure

### 3.1 Title

The title provides a concise description of the work and should allow the issue to be understood without opening its body.

The title should:

* Clearly describe the intended change.
* Be concise and specific.
* Use an appropriate Conventional Commit-style type.
* Describe the work rather than the implementation details when possible.
* Avoid unnecessary context that belongs in the issue body.

Recommended format:

```text
<type>: <short imperative description>
```

Examples:

```text
chore: configure Python environment with uv
docs: define issue contract
feat: implement risk scoring pipeline
test: add model evaluation tests
fix: handle missing prediction inputs
```

The GitHub issue title is separate from the issue body.

---

### 3.2 Why

The `Why` section explains why the issue exists.

It should describe the problem, need, motivation, or project objective that justifies the work.

It should answer:

> Why is this work necessary?

The `Why` section should provide sufficient context for someone to understand the purpose of the issue without requiring knowledge of the author's internal reasoning.

Avoid using this section to describe implementation steps.

Example:

```markdown
## Why

Establish a reproducible Python development environment so project
dependencies and development tooling can be installed consistently
across local development and CI environments.
```

---

### 3.3 Scope

The `Scope` section defines the boundary of the work.

It should clearly describe what the issue includes and, where necessary, what it intentionally excludes.

The scope should:

* Define the work covered by the issue.
* Prevent unrelated work from being introduced during implementation.
* Be small enough to execute within the stated estimate.
* Avoid duplicating the scope of another issue.
* Identify important out-of-scope items when boundaries could be ambiguous.

Example:

```markdown
## Scope

- Configure the project Python version.
- Configure uv project metadata.
- Define runtime dependencies.
- Define development dependencies.
- Verify the environment locally.

Out of scope:

- CI configuration.
- Docker configuration.
- Production deployment.
```

Scope may be refined during execution when new evidence changes the understanding of the work. Such changes should be explicitly documented rather than silently expanding the issue.

---

### 3.4 Acceptance Criteria

Acceptance Criteria define the conditions that must be satisfied for the issue to be considered complete.

They should answer:

> How will we verify that this issue is done?

Acceptance criteria should be:

* Specific.
* Observable.
* Testable or verifiable.
* Directly related to the issue scope.
* Independent of unnecessary implementation details where possible.

Avoid vague criteria such as:

```text
- [ ] Environment is properly configured.
- [ ] Code is production ready.
- [ ] Documentation is good.
```

Prefer verifiable criteria such as:

```text
- [ ] `uv sync` completes successfully on a clean checkout.
- [ ] The supported Python version is declared in `pyproject.toml`.
- [ ] Development dependencies are installable.
- [ ] The existing test suite executes successfully.
```

An issue should not be considered complete solely because all implementation tasks were performed. The acceptance criteria must also be satisfied.

---

### 3.5 Tasks

The `Tasks` section breaks the scoped work into actionable implementation steps.

Tasks should:

* Be directly related to the scope.
* Be concrete enough to execute.
* Support completion of the acceptance criteria.
* Be ordered where dependencies exist.
* Be small enough to make progress visible.

Nested tasks may be used when additional decomposition improves clarity.

Example:

```markdown
## Tasks

- [ ] Configure Python version.
- [ ] Configure uv project metadata.
- [ ] Define runtime dependencies.
- [ ] Define development dependencies.
- [ ] Run environment validation.
- [ ] Run the test suite.
```

Tasks are implementation steps, not additional requirements. The acceptance criteria remain the source of truth for determining whether the issue is complete.

If implementation reveals that a task is unnecessary, the task may be removed or updated rather than performed purely because it was originally planned.

---

### 3.6 Estimate

The `Estimate` represents the expected focused effort required to complete the issue.

The estimate should:

* Represent active execution time rather than calendar duration.
* Be assigned before implementation begins.
* Include implementation, validation, and necessary documentation work within the issue scope.
* Be small enough to support short feedback loops.

Preferred estimates for implementation issues are generally in the range of approximately **1–2 hours**.

Example:

```markdown
Estimate: 1 hour
```

After completion, the actual effort may be recorded separately to support estimation learning and retrospective analysis.

If an issue consistently appears too large to estimate or is expected to require substantially more effort, consider decomposing it into smaller issues.

---

### 3.7 Milestone

The `Milestone` identifies the project delivery boundary to which the issue contributes.

A milestone should represent a meaningful project outcome or phase rather than a technical category.

Examples:

```text
M0 — Project Foundation
M1 — Problem Discovery
M2 — Scope & Requirements
M3 — Data & ML Feasibility
M5 — MVP
```

Milestones should not be used as substitutes for:

* Labels
* Epics
* Tasks
* Technical categories

The GitHub Milestone field is the authoritative project-management metadata. If the milestone is also written in the issue body, both should remain consistent.

---

## 4. Issue Template

The following template is the standard structure for substantive implementation issues:

```markdown
# <type>: <short imperative description>

## Why

<Explain why this work is necessary.>

## Scope

- <Included work>
- <Included work>
- <Included work>

Out of scope:

- <Explicit exclusion, if necessary>

## Acceptance Criteria

- [ ] <Verifiable completion condition>
- [ ] <Verifiable completion condition>
- [ ] <Verifiable completion condition>

## Tasks

- [ ] **<Task group>**
  - [ ] <Action>
  - [ ] <Action>

- [ ] **<Task group>**
  - [ ] <Action>
  - [ ] <Action>

---

**Estimate:** <X hours>

**Milestone:** <Milestone name>

**Epic:** <Epic name>
```

The `Epic` field may be included as project-management metadata when applicable, but it is not part of the seven-field Issue Contract.

---

## 5. Reference Example

The following example demonstrates the Issue Contract using the completed Python environment setup work.

```markdown
# chore: configure Python environment with uv

## Why

Establish a reproducible Python development environment so project
dependencies and development tooling can be managed consistently
across local development and CI environments.

## Scope

- Configure the supported Python version.
- Configure uv project metadata.
- Define runtime dependencies.
- Define development dependencies.
- Configure the project environment.
- Verify that the environment and test suite work correctly.

Out of scope:

- CI/CD configuration.
- Docker configuration.
- Production deployment.

## Acceptance Criteria

- [ ] Supported Python version is declared in the project configuration.
- [ ] uv project configuration is present and valid.
- [ ] Runtime and development dependencies are defined.
- [ ] Project dependencies can be installed successfully.
- [ ] Existing tests execute successfully in the configured environment.

## Tasks

- [ ] Configure supported Python version.
- [ ] Configure uv project metadata.
- [ ] Define runtime dependencies.
- [ ] Define development dependencies.
- [ ] Verify environment setup.
- [ ] Run the test suite.

---

**Estimate:** 1–2 hours

**Milestone:** M0 — Project Foundation

**Epic:** Epic 0.1 — Repository Foundation
```

The reference example demonstrates the intended relationship between the seven fields:

```text
Why
 ↓
Scope
 ↓
Acceptance Criteria
 ↓
Tasks
 ↓
Estimate
 ↓
Milestone
```

The fields are related but serve different purposes and should not duplicate one another.

---

## 6. Contract Rules

The following rules apply to substantive implementation issues.

### Rule 1 — Define before execution

An issue should contain the required contract fields before implementation begins.

The issue may be refined when new information is discovered, but significant changes should be documented rather than silently introduced.

### Rule 2 — Scope before tasks

Tasks must derive from the defined scope.

New work discovered during implementation should not automatically be added to the current issue. First determine whether it:

* Belongs within the existing scope.
* Requires an explicit scope change.
* Should become a separate follow-up issue.

### Rule 3 — Acceptance criteria are the completion boundary

Completing every task does not automatically mean the issue is complete.

The acceptance criteria must be satisfied.

### Rule 4 — Keep issues independently executable

An issue should contain enough context for execution without requiring undocumented assumptions.

Dependencies on other issues should be identified when they materially affect execution.

### Rule 5 — Keep issues small

Issues should generally represent a small, independently meaningful unit of work.

If an issue becomes too large, ambiguous, or difficult to estimate, decompose it.

### Rule 6 — Estimates are hypotheses

An estimate represents expected effort, not a commitment or deadline.

Actual effort should be compared with the estimate after completion when useful for improving future planning.

### Rule 7 — Avoid scope creep

New ideas, improvements, or unrelated discoveries should not automatically become part of the current issue.

Capture them as follow-up work when they are outside the agreed scope.

### Rule 8 — Update the issue when assumptions change

If implementation reveals that the original scope, approach, or acceptance criteria are no longer appropriate, update the issue and document the reason.

Do not allow the issue to silently diverge from its original contract.

### Rule 9 — Do not create unnecessary structure

The contract exists to improve clarity and execution, not to introduce administrative overhead.

Use additional sections, metadata, or decomposition only when they provide meaningful value.

### Rule 10 — Close only after validation

An issue should be closed only after:

1. Implementation is complete.
2. Acceptance criteria are satisfied.
3. Required validation has been performed.
4. Relevant documentation has been updated.
5. Any necessary follow-up work has been captured separately.

---

## 7. GitHub Issue Formatting

GitHub separates the issue title from the issue body and project metadata.

### Issue Title

The GitHub issue title should contain only the concise issue title:

```text
docs: define issue contract
```

### Issue Body

The issue body contains the contract fields:

```markdown
## Why

...

## Scope

...

## Acceptance Criteria

- [ ]

## Tasks

- [ ]

---

**Estimate:** 1 hour

**Milestone:** M0 — Project Foundation

**Epic:** Epic 0.2 — Project Management
```

### GitHub Metadata

Where supported by GitHub, project metadata should be configured using the corresponding GitHub fields rather than relying only on text in the issue body.

Examples include:

* Labels
* Milestone
* Project
* Assignees

The issue body may repeat important metadata for readability, but the native GitHub field remains the source of truth.

### Final Issue Structure

The resulting issue should therefore be understood as:

```text
GitHub Issue
│
├── Title
│
├── Body
│   ├── Why
│   ├── Scope
│   ├── Acceptance Criteria
│   ├── Tasks
│   ├── Estimate
│   └── Milestone
│
└── GitHub Metadata
    ├── Labels
    ├── Milestone
    ├── Project
    └── Assignees
```

This structure provides a consistent contract while keeping project-management overhead intentionally low.
