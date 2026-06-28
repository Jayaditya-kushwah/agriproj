# AGENTS.md — AI Agent Guidance for AgriDoc

This file guides AI coding agents (Claude, Copilot, Cursor, etc.) working on AgriDoc.

## Project Context

AgriDoc is an **offline-first Flask web application** for digitizing farm documents.
- Target users: Rural farmers in Telangana, India (low digital literacy)
- Primary language: Telugu (te), then Hindi (hi), then English (en)
- Constraints: CPU-only, SQLite, no external cloud services required

## Architecture

```
Flask App (app.py factory)
  ├── routes/main.py      → Home, About
  ├── routes/documents.py → CRUD for documents
  ├── routes/api.py       → REST API (JSON) for PWA/sync
  └── models/database.py  → SQLite via sqlite3 (no ORM)
```

## Coding Standards

- Python 3.10+ with full type annotations
- All functions must have Google-style docstrings
- No ORMs — use raw `sqlite3` with `get_connection(db_path)`
- Flask blueprints only — no monolithic `app.py` route definitions
- All user-visible strings should have Telugu + English versions

## Database Access Pattern

```python
from agridoc.models.database import get_connection

conn = get_connection(current_app.config["DATABASE_PATH"])
rows = conn.execute("SELECT * FROM documents").fetchall()
conn.close()
```

Never use `g` for database connections — always open/close explicitly.

## Adding a New Document Type

1. Add a row to the `doc_types` INSERT in `models/database.py`
2. Add an icon mapping in `templates/documents/list.html`
3. Add a category card in `templates/index.html`
4. Add test coverage in `tests/test_agridoc.py`

## Adding a New Language

1. Add language code to `SUPPORTED_LANGUAGES` in `app.py`
2. Add `name_xx` column to `doc_types` table (migration required)
3. Add radio option in upload form template
4. Update USER_MANUAL.md

## Testing Guidelines

- Use the `client` fixture from `conftest.py` (or inline in test file)
- Every new route needs at least: 200 status test + data validation test
- Database tests use `tmp_path` fixture from pytest
- Never hardcode paths — always use `tmp_path`

## Security Notes

- Never log user data or file contents
- Validate file extensions with `_allowed_file()` before saving
- Use `secure_filename()` from werkzeug for all uploads
- No SQL string interpolation — always use parameterized queries

## Spec-Kit Workflow

When adding features:
1. Create spec in `specs/NNN-feature-name/spec.md`
2. Fill plan in `specs/NNN-feature-name/plan.md`
3. List tasks in `specs/NNN-feature-name/tasks.md`
4. Implement and mark tasks complete

## Common Pitfalls

- Do NOT use `flask.g` for DB connections in this project
- Do NOT add external API calls that require internet (offline-first!)
- Do NOT import heavy ML libraries (CPU-compatible constraint)
- Do NOT add `print()` statements — use `app.logger` instead
