# AgriDoc Project Constitution
## .specify/memory/constitution.md

> "Technology should reach the last farmer in the last village."

---

## Mission

Build the simplest, most reliable tool to help Telangana farmers digitize and access
their critical documents — offline-first, multilingual, privacy-preserving.

---

## Core Principles

### 1. Farmer First
Every decision is evaluated: "Does this help a farmer in Warangal with a ₹8,000 Android phone?"
- Prefer simplicity over cleverness
- Telugu UI is primary; English is secondary
- Assume low digital literacy

### 2. Offline First
The app MUST work without internet.
- SQLite is the only database
- No mandatory cloud services
- Service Worker caches all critical assets
- Data syncs opportunistically, never blocks

### 3. CPU Compatible
No GPU, no heavy ML models, no Docker-required setup.
- Target: ₹15,000 laptops and shared village computers
- App must start in <5 seconds on old hardware
- No model inference at runtime

### 4. Privacy by Design
Farmer data never leaves the device without explicit consent.
- Local-first storage
- No analytics, no telemetry
- AgriStack sync is opt-in

### 5. Quality Without Compromise
Code quality is non-negotiable.
- All commits must pass CI (lint, type-check, security, tests)
- Coverage ≥ 70% enforced
- Pre-commit hooks run before every commit
- Secrets never in code

### 6. Spec-Kit Discipline
Features start as specs, not code.
1. Write `spec.md` (WHAT & WHY) before any implementation
2. Write `plan.md` (HOW) before any code
3. Break into `tasks.md` before executing
4. Never skip steps under deadline pressure

---

## Technology Choices (Non-Negotiable)

| Choice | Rationale |
|--------|-----------|
| Flask | Lightweight, teachable, Swecha-familiar |
| SQLite | Zero-config, offline-first, works on cheap hardware |
| Vanilla JS | No build step, works on slow connections |
| Jinja2 | Server-side rendering = works without JS |
| Noto Sans Telugu | Official Google font for Telugu script |

## Anti-Patterns to Avoid

- ❌ External databases (Postgres, MySQL) as hard requirements
- ❌ API-only frontends (React SPA) — must work without JS
- ❌ Cloud storage as default
- ❌ English-only UI
- ❌ Features that require GPU/CUDA
