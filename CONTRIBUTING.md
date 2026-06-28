# Contributing to AgriDoc

Thank you for contributing to AgriDoc — a project built for India's farmers! 🌾

## Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

1. Fork the repository on `code.swecha.org`
2. Clone your fork: `git clone https://code.swecha.org/<you>/agridoc.git`
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Install dev dependencies: `pip install -e ".[dev]"`
5. Install pre-commit hooks: `pre-commit install`

## Development Workflow (Spec-Kit)

We follow the **7-Step Spec-Kit** workflow:

1. `specify init` — Bootstrap feature spec in `specs/`
2. Write `constitution.md` — Project principles
3. `spec.md` — Requirements (WHAT & WHY, no tech stack yet)
4. `clarify` — Q&A to fill gaps
5. `plan.md` — Technical blueprint with stack
6. `tasks.md` — Ordered, parallelizable tasks
7. Implement systematically

## Code Standards

- Python 3.10+ type hints everywhere
- `ruff` + `flake8` + `pylint` for linting
- `mypy --strict` for type checking
- `bandit` for security scanning
- All functions must have docstrings
- Test coverage ≥ 70%

## Commit Message Format

```
type(scope): short description

feat(docs): add Soil Health Card upload support
fix(api): handle empty farmer_id gracefully
docs(readme): add Docker setup instructions
test(api): add coverage for /api/sync endpoint
```

Types: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`, `style`

## Submitting a Merge Request

1. Ensure all CI checks pass
2. Write/update tests for your changes
3. Update `CHANGELOG.md` under `[Unreleased]`
4. Request review from a maintainer

## Multilingual Contributions

AgriDoc supports Telugu, Hindi, and English. When adding UI strings:
- Add Telugu (`te`) translation first — it's the primary language
- Add Hindi (`hi`) and English (`en`) equivalents
- Use `Noto Sans Telugu` font class for Telugu text

## Reporting Issues

Use GitLab Issues with the appropriate label:
- `bug` — Something broken
- `enhancement` — New feature request
- `translation` — Language/localization issue
- `accessibility` — Usability for low-literacy farmers
