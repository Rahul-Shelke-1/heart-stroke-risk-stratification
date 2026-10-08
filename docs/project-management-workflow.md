# Project Management Workflow

## 1. Purpose

This document defines how work is planned, executed, validated, and completed for the Heart Stroke Risk Stratification project.

the goal is to maintain a predictable and lightweight workflow while keeping scope, decisions, validation and project progress traceable through GitHub.

## 2. Workflow Overview

Workflow follows this lifecycle:

Idea
→ Issue
→ Planning Context
→ Implementation
→ Pull Request
→ Review
→ Merge
→ Validation
→ Done

Epics and milestone provide planning and delivery context around issues; 
they are not execution stage;

### Change Workflow

| Stage | Purpose |
|---|---|
| Idea | capture a potential problem, improvement, or piece of work. |
| Issue | Turn the idea into a clearly scoped, actionable unit of work. |
| Planning Context | Associate the issue with the appropriate epic and milestone. |
| Implementation | Make the completed change for review. |
| Pull Request | Present the completed change for review. |
| Review | Varfiy scope, correctness, quality, and acceptance criteria. |
| Merge | Integrate the approved change into `main`. |
| Validation | Vefrify the merged change behaves as expected. |
| Done | close the issue and record the outcome and actual effort. |

## 3. Lean Interation Loop

Each issue is executed through a lightweight iteartion loop:

Understand
→ Plan
→ implement
→ Validate
→ Review
→ Decide next action

Then describe each step briefly.

## 4. Definition of Ready (DoR)

An issue is considered Ready when:

- [ ] The problem or purpose is clear.
- [ ] The expected outcome is understood.
- [ ] Scope is defined.
- [ ] Acceptance criteria are testable.
- [ ] Important assumptions and dependencies are identified.
- [ ] The issue has an estimate.
- [ ] The issue is associated with the appropriate milestone/epic.

## 5. Definition of Done (DoD)

An issue is considered Done when:

- [ ] Agreed scope has been implemented.
- [ ] Acceptabce criteria have been satisifed.
- [ ] Relevant tests/checks pass.
- [ ] The imeplementation has been self-reviewed.
- [ ] Required documentation has been updated.
- [ ] The change has been merged into `main`.
- [ ] The merged result has been validated.
- [ ] Any newly discovered work has been captured separately.
- [ ] The issue has been closed with a completion note and actual effort.

## 6. Issue → PR → Merge

1. Start from a ready issue.
2. Create a branch following the repository branching convention.
3. Implement the scoped change.
4. Run the relevant validation locally.
5. Review the change and diff yourself.
6. Open a pull request referencing the issue.
7. Verify CI and required checks.
8. Address review findings, if any.
9. Merge the pull request.
10. Validate the resulting change on `main`.
11. Close the issue with the completion summary.

## 7. Follow-up Work and Scope Changes

Work discovered during implementation shoudl not sliently expand the scope of the current issue.

### Scope Changes

If new work is discovered:

- If it is necessary to satisfy the existing acceptance criteria, it remains part of the current issue.
- If it is useful but not required to satisfy the current acceptance criteria, crate a separate issue.
- If the change materially alerts the original objective or acceptance criteria, update the issue scope explicitly before continuing.
- Do not leave discovered work as undocumented future work.

### Follow-up Issues

Follow-up work should:

- Clearly describe the newly identifies work.
- Reference the issue where it was discovered.
- Be assigned to the appropriate milestone or backlog.
- Avoid blocking completion of the current issue useless it is required for the current acceptance criteria.

The current issue should be completed against its agrred scope, while additional work is tracked separately.

## 8. Milestone Completion

A milestone is considered complete when:

- All committed issues are Done or explicitly moved out with justification.
- Milestone acceptance criteria have been satisfied.
- Required validation has been completed.
- Critical blockers have been resolved or explicitly documented.
- Follow-up work has been captured as separate issues.
- A milestone review/retrospective has been completed.
- The milestone outcome has been recorded.
