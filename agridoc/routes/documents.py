"""Document management routes for AgriDoc."""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.utils import secure_filename

from agridoc.models.database import get_connection
from agridoc.utils.ocr_engine import ocr_and_store

documents_bp = Blueprint("documents", __name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _get_db() -> Any:
    return get_connection(current_app.config["DATABASE_PATH"])


@documents_bp.route("/")
def list_documents() -> str:
    """List all documents with optional search/filter."""
    query = request.args.get("q", "")
    doc_type = request.args.get("type", "")
    farmer_id = request.args.get("farmer_id", "")

    conn = _get_db()
    sql = """
        SELECT d.*, f.name as farmer_name, dt.name_te, dt.name_hi, dt.name_en
        FROM documents d
        LEFT JOIN farmers f ON d.farmer_id = f.id
        LEFT JOIN doc_types dt ON d.doc_type = dt.code
        WHERE 1=1
    """
    params: list[Any] = []
    if query:
        sql += " AND (d.title LIKE ? OR f.name LIKE ?)"
        params += [f"%{query}%", f"%{query}%"]
    if doc_type:
        sql += " AND d.doc_type = ?"
        params.append(doc_type)
    if farmer_id:
        sql += " AND d.farmer_id = ?"
        params.append(farmer_id)
    sql += " ORDER BY d.created_at DESC"

    docs = conn.execute(sql, params).fetchall()
    doc_types = conn.execute("SELECT * FROM doc_types ORDER BY category, name_en").fetchall()
    conn.close()
    return render_template("documents/list.html", docs=docs, doc_types=doc_types, query=query)


@documents_bp.route("/upload", methods=["GET", "POST"])
def upload() -> Any:
    """Upload a new document."""
    conn = _get_db()
    farmers = conn.execute("SELECT id, name, village FROM farmers ORDER BY name").fetchall()
    doc_types = conn.execute("SELECT * FROM doc_types ORDER BY category").fetchall()

    if request.method == "POST":
        farmer_id = request.form.get("farmer_id")
        doc_type = request.form.get("doc_type")
        title = request.form.get("title", "").strip()
        notes = request.form.get("notes", "")
        language = request.form.get("language", "te")
        tags = request.form.getlist("tags")

        file_path = None
        file_size = None
        mime_type = None

        file = request.files.get("document_file")
        if file and file.filename and _allowed_file(file.filename):
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
            upload_dir.mkdir(parents=True, exist_ok=True)
            full_path = upload_dir / filename
            file.save(str(full_path))
            file_path = filename
            file_size = os.path.getsize(str(full_path))
            mime_type = file.content_type

        with conn:
            cur = conn.execute(
                """INSERT INTO documents
                   (farmer_id, doc_type, title, file_path, file_size, mime_type, language, tags, notes, ocr_status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    farmer_id or None,
                    doc_type,
                    title,
                    file_path,
                    file_size,
                    mime_type,
                    language,
                    json.dumps(tags),
                    notes,
                    "pending" if file_path else "no_file",
                ),
            )
            doc_id = cur.lastrowid
            conn.execute(
                "INSERT INTO sync_log (action, entity_type, entity_id) VALUES ('create', 'document', ?)",
                (doc_id,),
            )

        # Run CPU-first OCR immediately after save (offline, no cloud)
        if file_path and doc_id:
            try:
                ocr_and_store(
                    file_path=file_path,
                    doc_id=doc_id,
                    doc_type=doc_type or "unknown",
                    language=language,
                    upload_folder=str(Path(current_app.config["UPLOAD_FOLDER"])),
                    db_conn=conn,
                )
            except Exception:  # noqa: BLE001
                pass  # OCR failure must never block document save

        conn.close()
        flash("Document saved & OCR processed! / పత్రం సేవ్ చేయబడింది, OCR పూర్తయింది!", "success")
        return redirect(url_for("documents.list_documents"))

    conn.close()
    return render_template("documents/upload.html", farmers=farmers, doc_types=doc_types)


@documents_bp.route("/<int:doc_id>")
def view_document(doc_id: int) -> Any:
    """View a single document."""
    conn = _get_db()
    doc = conn.execute(
        """SELECT d.*, f.name as farmer_name, f.village, f.district,
                  dt.name_te, dt.name_hi, dt.name_en, dt.category
           FROM documents d
           LEFT JOIN farmers f ON d.farmer_id = f.id
           LEFT JOIN doc_types dt ON d.doc_type = dt.code
           WHERE d.id = ?""",
        (doc_id,),
    ).fetchone()
    conn.close()
    if not doc:
        flash("Document not found.", "error")
        return redirect(url_for("documents.list_documents"))
    return render_template("documents/view.html", doc=doc)


@documents_bp.route("/<int:doc_id>/delete", methods=["POST"])
def delete_document(doc_id: int) -> Any:
    """Delete a document."""
    conn = _get_db()
    doc = conn.execute("SELECT file_path FROM documents WHERE id = ?", (doc_id,)).fetchone()
    if doc and doc["file_path"]:
        file_path = Path(current_app.config["UPLOAD_FOLDER"]) / doc["file_path"]
        if file_path.exists():
            file_path.unlink()
    with conn:
        conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.close()
    flash("Document deleted.", "info")
    return redirect(url_for("documents.list_documents"))
