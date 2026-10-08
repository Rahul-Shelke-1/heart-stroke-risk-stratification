# M0 — Project Foundation Retrospective

## 1. What Was the Goal?

M0 was intended to establish the repository and project-management foundation required to execute the project in a structured and repeatable way.

The milestone was divided into two epics:

* **Epic 0.1 — Repository Foundation**
* **Epic 0.2 — Project Management**

Both epics were completed successfully.

## 2. What Went Well?

* The repository structure was established before domain and ML implementation began.
* The Python/uv environment and basic development workflow were established early.
* GitHub Projects provided a clear place to track milestones, epics, and issues.
* The issue contract made individual tasks easier to define with explicit scope and acceptance criteria.
* The decision log and risk register established mechanisms for recording important project decisions and risks.
* Breaking work into small issues made estimation and actual effort easier to observe.

## 3. What Didn't Go Well?

### M0 Was Decomposed Too Granularly

The decision to divide M0 into two separate epics was useful initially, but the distinction became less valuable as the milestone progressed.

By the time Epic 0.2 was reached, several project-management tasks felt repetitive because the fundamental repository and development patterns had already been established during Epic 0.1.

Some Epic 0.2 tasks were still important because they introduced new mechanisms, such as:

* issue contracts
* decision logs
* risk registers
* GitHub Project views

However, once these mechanisms were understood and established, much of the associated setup became a repeatable project-initiation procedure rather than work requiring significant project-specific planning.

## 4. Key Learning

Not every important setup activity needs to remain a separately planned epic or a series of project-specific tasks.

There are two different types of foundation work:

1. **Learning / design work** — requires deliberate planning because the process is being established or validated for the first time.
2. **Reusable setup work** — becomes a standard project bootstrap procedure after the process has been understood.

M0 contained too much of the second type as individually managed project work.

The first implementation of these practices was valuable because it exposed what was actually necessary. Repeating the same detailed planning structure in every future project would add process overhead without providing equivalent value.

## 5. Process Change for Future Projects

For future portfolio projects:

* Maintain a lightweight **Project Bootstrap** checklist/template containing the proven M0 setup.
* Do not recreate every foundational setup activity as a separate epic and issue.
* Create individual issues only when a setup activity requires project-specific investigation, design, or a meaningful decision.
* Reuse standardized repository, GitHub Project, CI, documentation, and project-management patterns where appropriate.
* Keep project-specific decisions and risks separate from reusable bootstrap configuration.

### New Principle

> **Learn the process once, standardize it, then reuse it.**

The purpose of project management is to reduce cognitive overhead and improve execution, not to reproduce the management process itself for every project.

## 6. Actions for M1+

* Treat the M0 structure as the first version of a reusable project-bootstrap template.
* Avoid creating issues solely because a setup step exists in the template.
* Use issues for meaningful work, decisions, research, implementation, or project-specific configuration.
* Review process overhead at the end of major milestones and simplify where the workflow has become routine.

## 7. Overall Assessment

M0 successfully established the foundation required to manage and develop the project.

The main improvement identified is **process compression**: activities that were valuable to learn during the first project should become reusable defaults rather than repeated planning overhead.

This retrospective will be used to simplify project initialization for future projects while retaining the practices that materially improve execution and traceability.
