"""REST API routes for AgriDoc (offline-first PWA sync)."""

from __future__ import annotations

import json
from typing import Any

from flask import Blueprint, current_app, jsonify, request

from pathlib import Path

from agridoc.models.database import get_connection
from agridoc.utils.ocr_engine import ocr_and_store

api_bp = Blueprint("api", __name__)


def _db() -> Any:
    return get_connection(current_app.config["DATABASE_PATH"])


@api_bp.route("/farmers", methods=["GET"])
def get_farmers() -> Any:
    """Return all farmers as JSON."""
    conn = _db()
    rows = conn.execute("SELECT * FROM farmers ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@api_bp.route("/farmers", methods=["POST"])
def create_farmer() -> Any:
    """Create a new farmer record."""
    data = request.get_json(force=True) or {}
    required = ["name"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    conn = _db()
    with conn:
        cur = conn.execute(
            """INSERT INTO farmers (name, phone, village, mandal, district, language)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                data["name"],
                data.get("phone"),
                data.get("village"),
                data.get("mandal"),
                data.get("district", "Hyderabad"),
                data.get("language", "te"),
            ),
        )
        farmer_id = cur.lastrowid
    conn.close()
    return jsonify({"id": farmer_id, "status": "created"}), 201


@api_bp.route("/documents", methods=["GET"])
def get_documents() -> Any:
    """Return documents list as JSON."""
    conn = _db()
    rows = conn.execute(
        """SELECT d.*, f.name as farmer_name FROM documents d
           LEFT JOIN farmers f ON d.farmer_id = f.id
           ORDER BY d.created_at DESC"""
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@api_bp.route("/doc-types", methods=["GET"])
def get_doc_types() -> Any:
    """Return all document types."""
    conn = _db()
    rows = conn.execute("SELECT * FROM doc_types ORDER BY category, name_en").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@api_bp.route("/stats", methods=["GET"])
def get_stats() -> Any:
    """Return dashboard statistics."""
    conn = _db()
    stats = {
        "total_documents": conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
        "total_farmers": conn.execute("SELECT COUNT(*) FROM farmers").fetchone()[0],
        "verified_documents": conn.execute(
            "SELECT COUNT(*) FROM documents WHERE is_verified=1"
        ).fetchone()[0],
        "pending_sync": conn.execute(
            "SELECT COUNT(*) FROM sync_log WHERE synced=0"
        ).fetchone()[0],
        "by_type": [
            dict(r)
            for r in conn.execute(
                "SELECT doc_type, COUNT(*) as count FROM documents GROUP BY doc_type"
            ).fetchall()
        ],
    }
    conn.close()
    return jsonify(stats)


@api_bp.route("/sync", methods=["POST"])
def sync() -> Any:
    """Mark pending records as synced (AgriStack integration stub)."""
    conn = _db()
    with conn:
        conn.execute("UPDATE sync_log SET synced=1 WHERE synced=0")
    conn.close()
    return jsonify({"status": "synced"})


@api_bp.route("/ocr/<int:doc_id>", methods=["POST"])
def retrigger_ocr(doc_id: int) -> Any:
    """Re-run CPU-first OCR on a document and return extracted fields.

    This runs entirely offline — no GPU, no cloud API.
    Runtime: Tesseract 4.x LSTM (CPU-only).
    """
    conn = _db()
    doc = conn.execute(
        "SELECT file_path, doc_type, language FROM documents WHERE id = ?",
        (doc_id,),
    ).fetchone()

    if not doc:
        conn.close()
        return jsonify({"error": "Document not found"}), 404

    if not doc["file_path"]:
        conn.close()
        return jsonify({"error": "No file attached to this document"}), 400

    upload_folder = str(Path(current_app.config["UPLOAD_FOLDER"]))

    result = ocr_and_store(
        file_path=doc["file_path"],
        doc_id=doc_id,
        doc_type=doc["doc_type"] or "unknown",
        language=doc["language"] or "te",
        upload_folder=upload_folder,
        db_conn=conn,
    )
    conn.close()

    return jsonify({
        "doc_id": doc_id,
        "ocr_status": result["ocr_status"],
        "ocr_engine": result["ocr_engine"],
        "ocr_confidence": result["ocr_confidence"],
        "processing_time_ms": result["processing_time_ms"],
        "ocr_text": result["ocr_text"][:500],   # preview only
        "ocr_fields": result["ocr_fields"],
    })
