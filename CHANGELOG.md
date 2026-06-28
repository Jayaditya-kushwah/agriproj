# Changelog

All notable changes to AgriDoc are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] — 2024-07-01

### Added
- Initial release of AgriDoc Farm Document Digitizer
- Flask application with offline-first SQLite backend
- PWA support with Service Worker for offline document access
- Multilingual UI — Telugu (primary), Hindi, English
- 10 document types: Pattadar, Adangal, Rythu Bandhu, PM-KISAN, Aadhaar, Crop Insurance, Bank Passbook, Kisan Credit Card, Water Permit, Soil Health Card
- Farmer profile management with village/mandal/district fields
- Document upload with drag-and-drop, PDF/JPG/PNG support
- Full-text search and document type filtering
- REST API (`/api/`) for AgriStack sync integration
- Responsive mobile-first UI with Telugu Noto font
- GitLab CI/CD pipeline with test, lint, format, type_check, coverage, security stages
- Pre-commit hooks (ruff, flake8, pylint, mypy, bandit, detect-secrets, vulture, pip-audit)
- Spec-Kit driven development workflow in `.specify/` and `specs/`
- Complete compliance documentation (README, CONTRIBUTING, USER_MANUAL, AGENTS, SECURITY, CODE_OF_CONDUCT, CHANGELOG)
- Dockerfile and `.dockerignore` for containerization
- 40+ pytest tests with ≥70% coverage threshold
- poc.md and project_plan.md strategic documents

[Unreleased]: https://code.swecha.org/agridoc/agridoc/-/compare/v1.0.0...HEAD
[1.0.0]: https://code.swecha.org/agridoc/agridoc/-/releases/v1.0.0
