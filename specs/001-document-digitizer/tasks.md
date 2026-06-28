# Tasks: Farm Document Digitizer (Core)
## specs/001-document-digitizer/tasks.md

---

## Phase 1: Foundation [DONE ✅]

- [x] [S] Initialize Flask app factory (`agridoc/app.py`)
- [x] [S] Create SQLite schema with all tables (`agridoc/models/database.py`)
- [x] [P] Seed document types (10 types, 3 languages)
- [x] [P] Create `.specify/` directory with constitution and templates

## Phase 2: Backend Routes [DONE ✅]

- [x] [S] Create `routes/main.py` blueprint (home, about)
- [x] [P] Create `routes/documents.py` blueprint (list, upload, view, delete)
- [x] [P] Create `routes/api.py` blueprint (stats, farmers, documents, sync)
- [x] [P] Add file validation (`_allowed_file()`, `secure_filename`)
- [x] [P] Add parameterized SQL queries (no injection risk)

## Phase 3: Frontend [DONE ✅]

- [x] [S] Create `templates/base.html` (nav, offline banner, flash messages)
- [x] [P] Create `templates/index.html` (dashboard, stats, category cards)
- [x] [P] Create `templates/documents/list.html` (search, grid, empty state)
- [x] [P] Create `templates/documents/upload.html` (drag-drop form)
- [x] [P] Create `templates/documents/view.html` (document details)
- [x] [P] Write `static/css/agridoc.css` (Telugu-first design, responsive)
- [x] [P] Write `static/js/app.js` (offline detection, SW registration)
- [x] [S] Write `static/js/sw.js` (Service Worker, cache strategy)
- [x] [P] Write `static/manifest.json` (PWA manifest)

## Phase 4: Tests [DONE ✅]

- [x] [P] Write route tests (home, documents CRUD)
- [x] [P] Write API tests (stats, farmers, documents, sync)
- [x] [P] Write DB tests (init, seed, idempotency)
- [x] [S] Verify coverage ≥70%

## Phase 5: Compliance [DONE ✅]

- [x] [P] Write README.md (full with badges)
- [x] [P] Write CONTRIBUTING.md
- [x] [P] Write USER_MANUAL.md (Telugu + English)
- [x] [P] Write AGENTS.md
- [x] [P] Write SECURITY.md
- [x] [P] Write CODE_OF_CONDUCT.md
- [x] [P] Write CHANGELOG.md
- [x] [P] Write .env.example
- [x] [P] Write Dockerfile + .dockerignore
- [x] [P] Write .gitignore + .editorconfig
- [x] [S] Write .gitlab-ci.yml (6 stages)
- [x] [S] Write .pre-commit-config.yaml (10 repos, 11 hooks)
- [x] [P] Write pyproject.toml (ruff, mypy, pylint, bandit, vulture, coverage)
- [x] [P] Write poc.md (proof-of-concept document)
- [x] [P] Write project_plan.md (full project plan)

## Phase 6: Spec-Kit [DONE ✅]

- [x] [S] Write .specify/memory/constitution.md
- [x] [P] Write .specify/templates/spec.md
- [x] [P] Write .specify/templates/plan.md
- [x] [P] Write .specify/templates/tasks.md
- [x] [P] Write .specify/scripts/bash/speckit.sh
- [x] [S] Write specs/001-document-digitizer/ (spec + plan + tasks + data-model + research)

---

**Status:** ✅ COMPLETE
**Version:** 1.0.0
**Compliance Score Target:** 100%
