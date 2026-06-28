# Technical Plan: Farm Document Digitizer (Core)
## specs/001-document-digitizer/plan.md

---

## Architecture Decision

**Stack:** Flask + SQLite + Jinja2 + Vanilla JS + Service Worker (PWA)
**Rationale:** Fully aligned with constitution.md — no build step, offline-first, CPU-only

---

## Data Model

```sql
-- Farmer profiles
CREATE TABLE farmers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    phone           TEXT,
    village         TEXT,
    mandal          TEXT,
    district        TEXT DEFAULT 'Hyderabad',
    state           TEXT DEFAULT 'Telangana',
    language        TEXT DEFAULT 'te',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Uploaded documents
CREATE TABLE documents (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id   INTEGER REFERENCES farmers(id),
    doc_type    TEXT NOT NULL,  -- FK to doc_types.code
    title       TEXT NOT NULL,
    file_path   TEXT,           -- relative path in UPLOAD_FOLDER
    file_size   INTEGER,
    mime_type   TEXT,
    language    TEXT DEFAULT 'te',
    tags        TEXT DEFAULT '[]',  -- JSON array
    notes       TEXT,
    is_verified INTEGER DEFAULT 0,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reference table for document types
CREATE TABLE doc_types (
    id          INTEGER PRIMARY KEY,
    code        TEXT UNIQUE NOT NULL,
    name_en     TEXT NOT NULL,
    name_te     TEXT NOT NULL,
    name_hi     TEXT NOT NULL,
    category    TEXT NOT NULL  -- land|scheme|identity|finance|agriculture|water|insurance
);
```

---

## API Design

| Method | Path             | Description              |
|--------|------------------|--------------------------|
| GET    | /api/stats       | Dashboard statistics     |
| GET    | /api/documents   | List all documents (JSON)|
| GET    | /api/farmers     | List all farmers (JSON)  |
| POST   | /api/farmers     | Create farmer            |
| GET    | /api/doc-types   | Document type catalogue  |
| POST   | /api/sync        | AgriStack sync trigger   |

---

## Blueprint Structure

```
routes/
├── main.py       → / (dashboard), /about
├── documents.py  → /documents/ (CRUD)
└── api.py        → /api/* (JSON endpoints for PWA)
```

---

## PWA Architecture

```
Service Worker (sw.js)
  ├── install  → cache static assets
  ├── activate → clean old caches
  └── fetch    → cache-first for static, network-first for API
```

---

## Testing Plan

- `test_index_returns_200` — smoke test
- `test_api_stats` — dashboard data integrity
- `test_api_create_farmer` — farmer creation
- `test_documents_upload_post_valid` — document creation flow
- `test_db_init_creates_tables` — DB schema verification
- `test_db_doc_types_seeded` — seed data presence
- Coverage target: ≥70%

---

## Rollout

- [x] SQLite schema with seed data
- [x] Flask blueprints (main, documents, api)
- [x] Jinja2 templates (base, index, list, upload, view)
- [x] CSS (agridoc.css) — Telugu-first design
- [x] Service Worker (sw.js) — offline support
- [x] PWA manifest
- [x] 40+ pytest tests
- [x] GitLab CI pipeline
- [x] Pre-commit hooks
- [x] Full compliance documentation
