# Data Model: Farm Document Digitizer
## specs/001-document-digitizer/data-model.md

---

## Entity Relationship Diagram (text)

```
farmers (1) ──────────────── (N) documents
    │                               │
    │                               │ doc_type (FK)
    │                               │
                              doc_types (1) ──── (N) documents

sync_log (N) ── records every create/update/delete → used for AgriStack sync
```

---

## Table Definitions

### `farmers`
Stores individual farmer profiles linked to their documents.

| Column         | Type    | Constraints             | Notes                        |
|----------------|---------|-------------------------|------------------------------|
| id             | INTEGER | PK, AUTOINCREMENT       |                              |
| name           | TEXT    | NOT NULL                | Full name in local script    |
| phone          | TEXT    |                         | 10-digit mobile number       |
| village        | TEXT    |                         | Village name (Telugu)        |
| mandal         | TEXT    |                         | Mandal/Block name            |
| district       | TEXT    | DEFAULT 'Hyderabad'     | Telangana district           |
| state          | TEXT    | DEFAULT 'Telangana'     |                              |
| aadhaar_last4  | TEXT    |                         | Last 4 digits only (privacy) |
| language       | TEXT    | DEFAULT 'te'            | UI language preference       |
| created_at     | DATETIME| DEFAULT CURRENT_TIMESTAMP|                             |
| updated_at     | DATETIME| DEFAULT CURRENT_TIMESTAMP|                             |

**Indexes:** `name`, `village`, `phone`

---

### `documents`
Core table — stores metadata for every uploaded document.

| Column      | Type    | Constraints                    | Notes                        |
|-------------|---------|--------------------------------|------------------------------|
| id          | INTEGER | PK, AUTOINCREMENT              |                              |
| farmer_id   | INTEGER | FK → farmers(id) ON DELETE CASCADE|                           |
| doc_type    | TEXT    | NOT NULL                       | FK → doc_types.code          |
| title       | TEXT    | NOT NULL                       | Human-readable label         |
| file_path   | TEXT    |                                | Relative path in UPLOAD_FOLDER|
| file_size   | INTEGER |                                | Bytes                        |
| mime_type   | TEXT    |                                | e.g. application/pdf         |
| language    | TEXT    | DEFAULT 'te'                   | Document language            |
| tags        | TEXT    | DEFAULT '[]'                   | JSON array of string tags    |
| notes       | TEXT    |                                | Free-form remarks            |
| is_verified | INTEGER | DEFAULT 0                      | 0=unverified, 1=verified     |
| created_at  | DATETIME| DEFAULT CURRENT_TIMESTAMP      |                              |
| updated_at  | DATETIME| DEFAULT CURRENT_TIMESTAMP      |                              |

**Indexes:** `farmer_id`, `doc_type`, `created_at`

---

### `doc_types`
Reference/lookup table for supported document types. Seeded at DB init.

| Column      | Type | Notes                              |
|-------------|------|------------------------------------|
| id          | INT  | PK                                 |
| code        | TEXT | UNIQUE — used as FK string key     |
| name_en     | TEXT | English name                       |
| name_te     | TEXT | Telugu name (primary)              |
| name_hi     | TEXT | Hindi name                         |
| category    | TEXT | land / scheme / identity / finance / agriculture / water / insurance |
| description | TEXT | Optional description               |

**Seeded records (10):**

| code        | name_en               | category    |
|-------------|-----------------------|-------------|
| pattadar    | Pattadar Passbook     | land        |
| adangal     | Adangal / RoR         | land        |
| aadhaar     | Aadhaar Card          | identity    |
| pm_kisan    | PM-KISAN Certificate  | scheme      |
| rytu_bandhu | Rythu Bandhu          | scheme      |
| crop_ins    | Crop Insurance        | insurance   |
| bank_pass   | Bank Passbook         | finance     |
| loan        | Kisan Credit Card     | finance     |
| water       | Water Use Permit      | water       |
| soil        | Soil Health Card      | agriculture |

---

### `sync_log`
Audit trail for AgriStack synchronization.

| Column      | Type    | Notes                            |
|-------------|---------|----------------------------------|
| id          | INTEGER | PK                               |
| action      | TEXT    | create / update / delete         |
| entity_type | TEXT    | document / farmer                |
| entity_id   | INTEGER | ID of affected record            |
| synced      | INTEGER | 0=pending, 1=synced              |
| created_at  | DATETIME| Timestamp                        |

---

## Privacy Considerations

- `aadhaar_last4` stores only the last 4 digits — never the full 12-digit number
- `file_path` is a random UUID prefix + secure filename — not guessable
- No PII is logged in `sync_log`
- All data is local-only unless `/api/sync` is explicitly triggered

---

## Migration Strategy (v1 → v2)

Future migrations will use a simple version table:
```sql
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
Migration scripts will live in `agridoc/models/migrations/`.
