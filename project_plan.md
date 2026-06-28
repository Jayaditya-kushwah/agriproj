# AgriDoc — Project Plan
## project_plan.md

**Project:** AgriDoc — Farm Document Digitizer
**Team:** Swecha Summer Internship 2024
**Duration:** 6 weeks (June–July 2024)
**Stack:** Flask · SQLite · PWA · Telugu-first UI

---

## 1. Vision

> Digitize every farm document for every Telangana farmer — offline, in Telugu, on any device.

AgriDoc bridges the gap between India's 110M+ farmers and the digital infrastructure
(AgriStack, DigiLocker, PM-KISAN) that requires digital documents they don't have.

---

## 2. Goals

### Primary
- Working offline-first web app for farm document digitization
- Telugu-first multilingual UI (Telugu, Hindi, English)
- Support for 10 critical Telangana document types
- Full Swecha Spec-Kit compliance (100% checker score)

### Secondary
- AgriStack API sync stub for future integration
- PWA installability on Android phones
- CPU-only — no GPU/cloud required

---

## 3. Project Phases

### Phase 0 — Specification (Week 1)
- [x] Write `poc.md` — validate feasibility
- [x] Write `specs/001-document-digitizer/spec.md` — requirements
- [x] Write `specs/001-document-digitizer/research.md` — Telangana context
- [x] Write `specs/001-document-digitizer/data-model.md` — DB schema
- [x] Write `specs/001-document-digitizer/plan.md` — technical blueprint
- [x] Write `specs/001-document-digitizer/tasks.md` — ordered task list
- [x] Write `.specify/memory/constitution.md` — project principles

### Phase 1 — Foundation (Week 2)
- [x] Flask app factory with blueprint registration
- [x] SQLite schema — farmers, documents, doc_types, sync_log
- [x] Seed 10 document types in 3 languages
- [x] pyproject.toml with all quality tool configs
- [x] .gitlab-ci.yml (test, lint, format, type_check, coverage, security)
- [x] .pre-commit-config.yaml (10 repos, 11 hooks)

### Phase 2 — Backend (Week 3)
- [x] `routes/main.py` — home dashboard, about
- [x] `routes/documents.py` — CRUD (list, upload, view, delete)
- [x] `routes/api.py` — REST JSON API (stats, farmers, docs, sync)
- [x] File upload with validation and secure filename
- [x] Farmer profile creation via API

### Phase 3 — Frontend (Week 4)
- [x] `base.html` — navbar, offline banner, flash messages, footer
- [x] `index.html` — dashboard with live stats, category cards, tips
- [x] `documents/list.html` — search bar, doc grid, empty state
- [x] `documents/upload.html` — drag-drop zone, bilingual form
- [x] `documents/view.html` — document detail view
- [x] `agridoc.css` — 600-line Telugu-first responsive stylesheet
- [x] `app.js` — offline detection, sync, nav toggle
- [x] `sw.js` — Service Worker with cache-first strategy
- [x] `manifest.json` — PWA manifest

### Phase 4 — Testing (Week 5)
- [x] 40+ pytest tests covering all routes and database
- [x] ≥70% coverage enforced via `--cov-fail-under=70`
- [x] Tests for: home, documents CRUD, API endpoints, DB init, seed

### Phase 5 — Documentation & Compliance (Week 6)
- [x] README.md (badges, quick-start, structure, features)
- [x] CONTRIBUTING.md (Spec-Kit workflow, commit format)
- [x] USER_MANUAL.md (Telugu + English, step-by-step)
- [x] AGENTS.md (AI agent guidance)
- [x] SECURITY.md (responsible disclosure)
- [x] CODE_OF_CONDUCT.md
- [x] CHANGELOG.md (Keep a Changelog format)
- [x] .env.example, .gitignore, .editorconfig
- [x] Dockerfile + .dockerignore
- [x] LICENSE (MIT)
- [x] cliff.toml (git-cliff automated changelog)

---

## 4. Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend | Flask 3.0 | Lightweight, Swecha-familiar |
| Database | SQLite (stdlib) | Zero-config, offline-first |
| Frontend | Jinja2 + Vanilla JS | No build step, works without JS |
| Styling | Custom CSS (CSS vars) | Telugu font support, responsive |
| Offline | Service Worker (PWA) | Browser-native, no framework |
| Testing | pytest + pytest-cov | Standard Python testing |
| Linting | ruff + flake8 + pylint | SpecKit requirements |
| Types | mypy --strict | Type safety |
| Security | bandit + detect-secrets + pip-audit | SpecKit security |
| CI | GitLab CI (6 stages) | SpecKit CI requirement |
| Changelog | git-cliff | Automated changelog generation |
| Containers | Docker | SpecKit Dockerfile requirement |

---

## 5. Key Metrics (Target → Actual)

| Metric | Target | Actual |
|--------|--------|--------|
| Test coverage | ≥70% | ✅ ~85% |
| CI stages | ≥5 | ✅ 6 |
| Pre-commit hooks | ≥8 | ✅ 11 |
| Doc types supported | 8 | ✅ 10 |
| Languages | 2 | ✅ 3 (te, hi, en) |
| Compliance score | 100% | ✅ 100% |
| Startup time | <5s | ✅ ~1.2s |

---

## 6. v2 Roadmap

| Feature | Priority | Effort |
|---------|----------|--------|
| Tesseract OCR for auto-title | High | 2 weeks |
| PIN-based multi-user auth | High | 1 week |
| Real AgriStack Farmer ID API | High | 3 weeks |
| QR code document sharing | Medium | 3 days |
| Encrypted ZIP backup/export | Medium | 1 week |
| Voice input (Telugu) | Low | 2 weeks |
| WhatsApp document sharing | Low | 1 week |

---

## 7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| AgriStack API changes | Medium | High | Sync is a stub in v1; design for change |
| Low-end device storage | Low | High | Compress JPGs before save |
| Telugu font not rendering | Low | Medium | Fallback to system sans-serif |
| Disk full on village PC | Low | High | Warn at 90% capacity (v2) |

---

## 8. Team

- **Developer:** Gireesh (IcfaiTech / IFHE Hyderabad, B.Tech CSE 2024–2028)
- **Organization:** Swecha Telangana
- **Domain Advisor:** Telangana Farmer Focus Group
- **Technical Mentor:** Dr. Prasad, NIT Warangal
