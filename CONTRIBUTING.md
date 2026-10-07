# Contributing

## Development Workflow

```bash
Issue
  ↓
Branch
  ↓
Implementation
  ↓
Commit
  ↓
Pull Request
  ↓
Review
  ↓
Merge into main
```

## Branching Convention

### Branch Types

```bash
feat/*
fix/*
docs/*
chore/*
refactor/*
test/*
hotfix/*
```

### Examples

```bash
feat/risk-scoring
fix/missing-values
docs/update-readme
```

## Commit Convention

Use Conventional Commits.

```
<type>: <description>
```

Examples:

- feat: add risk scoring
- fix: handle missing values
- docs: update project readme
- chore: update dependencies

## Pull Requests

1. Create a branch from main.
2. Implement the change.
3. Commit using the conventional commit format.
4. Push the branch.
5. Open a pull request.
6. Link the related issue.
7. Describe the change and validation.
8. Review and address feedback.
9. Squash and merge into main.
10. Delete the branch.

## Main Branch

- `main` is the stable integration branch.
- Direct commits to `main` should be avoided.
- Changes should enter through pull requests.
- Pull requests should reference an issue.
- Required automated checks will be enforced once CI is established.