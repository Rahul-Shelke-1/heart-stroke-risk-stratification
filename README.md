# Heart Stroke Risk Stratification

## Project Overview

A machine learning project for exploring and developing a heart stroke risk
stratification system.

The project is currently in the **M0 — Project Foundation** phase. Detailed
problem definition, domain research, data methodology, model development,
evaluation strategy, and system design will be established in subsequent
milestones.

## Repository Structure

```text
.
├── .github/       # GitHub workflows and repository configuration
├── configs/       # Project configuration
├── docs/          # Project documentation
├── research/      # Research and investigation artifacts
├── src/           # Application and ML source code
├── tests/         # Automated tests
├── pyproject.toml # Python project configuration
└── README.md      # Project overview
```

The repository is currently in the **project foundation phase**. Domain-specific implementation will be added in later milestones.

## Prerequisites

The following tools are required for local development:

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Git

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Rahul-Shelke-1/heart-stroke-risk-stratification.git
```

Create and synchronize the project environment:

```bash
uv sync
```

## Development Commands

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Run type checking:

```bash
uv run mypy .
```

## Testing

Run the complete test suite with:

```bash
uv run pytest
```

## Current Project Status

**Milestone:** M0 — Project Foundation

The repository foundation is currently being established, including project
structure, Python/uv configuration, dependency management, and initial test
infrastructure.

Completed foundation work includes:

- Repository structure
- Python project configuration
- `uv` environment and dependency management
- Initial test infrastructure

The detailed problem statement and machine learning methodology are deferred
to **M1**.