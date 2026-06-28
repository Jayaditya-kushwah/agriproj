"""SQLite database initialization and models for AgriDoc."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional


def get_connection(db_path: str) -> sqlite3.Connection:
    """Return a SQLite connection with row factory enabled.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        SQLite connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str) -> None:
    """Initialize the database schema.

    Args:
        db_path: Path to the SQLite database file.
    """
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection(db_path)
    with conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS farmers (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                phone       TEXT,
                village     TEXT,
                mandal      TEXT,
                district    TEXT DEFAULT 'Hyderabad',
                state       TEXT DEFAULT 'Telangana',
                aadhaar_last4 TEXT,
                language    TEXT DEFAULT 'te',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS documents (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id    INTEGER REFERENCES farmers(id) ON DELETE CASCADE,
                doc_type     TEXT NOT NULL,
                title        TEXT NOT NULL,
                file_path    TEXT,
                file_size    INTEGER,
                mime_type    TEXT,
                language     TEXT DEFAULT 'te',
                tags         TEXT DEFAULT '[]',
                notes        TEXT,
                is_verified  INTEGER DEFAULT 0,
                ocr_text     TEXT,
                ocr_fields   TEXT DEFAULT '{}',
                ocr_status   TEXT DEFAULT 'pending',
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS doc_types (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                code        TEXT UNIQUE NOT NULL,
                name_en     TEXT NOT NULL,
                name_te     TEXT NOT NULL,
                name_hi     TEXT NOT NULL,
                category    TEXT NOT NULL,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS sync_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                action      TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id   INTEGER,
                synced      INTEGER DEFAULT 0,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            -- Seed document types
            INSERT OR IGNORE INTO doc_types (code, name_en, name_te, name_hi, category) VALUES
                ('pattadar', 'Pattadar Passbook', 'పట్టాదార్ పాస్‌బుక్', 'पट्टादार पासबुक', 'land'),
                ('adangal',  'Adangal / RoR',     'అదంగల్',              'अदंगल',            'land'),
                ('aadhaar',  'Aadhaar Card',       'ఆధార్ కార్డ్',         'आधार कार्ड',        'identity'),
                ('pm_kisan', 'PM-KISAN Certificate','పీఎం-కిసాన్',         'पीएम-किसान',        'scheme'),
                ('rytu_bandhu','Rythu Bandhu',     'రైతు బంధు',           'रैतु बंधु',          'scheme'),
                ('crop_ins', 'Crop Insurance',     'పంట బీమా',            'फसल बीमा',          'insurance'),
                ('bank_pass','Bank Passbook',      'బ్యాంక్ పాస్‌బుక్',    'बैंक पासबुक',        'finance'),
                ('loan',     'Kisan Credit Card',  'కిసాన్ క్రెడిట్ కార్డ్','किसान क्रेडिट कार्ड','finance'),
                ('water',    'Water Use Permit',   'నీటి వినియోగ అనుమతి', 'जल उपयोग परमिट',    'water'),
                ('soil',     'Soil Health Card',   'మట్టి ఆరోగ్య కార్డు',  'मृदा स्वास्थ्य कार्ड','agriculture');
            """
        )
    conn.close()
