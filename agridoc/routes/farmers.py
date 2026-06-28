"""Farmer profile management routes for AgriDoc."""

from __future__ import annotations

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

from agridoc.models.database import get_connection

farmers_bp = Blueprint("farmers", __name__)


def _db() -> Any:
    return get_connection(current_app.config["DATABASE_PATH"])


@farmers_bp.route("/")
def list_farmers() -> str:
    """List all registered farmers."""
    query = request.args.get("q", "")
    conn = _db()
    sql = "SELECT f.*, COUNT(d.id) as doc_count FROM farmers f LEFT JOIN documents d ON f.id = d.farmer_id WHERE 1=1"
    params: list[Any] = []
    if query:
        sql += " AND (f.name LIKE ? OR f.village LIKE ? OR f.phone LIKE ?)"
        params += [f"%{query}%"] * 3
    sql += " GROUP BY f.id ORDER BY f.name"
    farmers = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("farmers/list.html", farmers=farmers, query=query)


@farmers_bp.route("/new", methods=["GET", "POST"])
def create_farmer() -> Any:
    """Register a new farmer."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("రైతు పేరు అవసరం | Farmer name is required.", "error")
            return render_template("farmers/form.html")
        conn = _db()
        with conn:
            conn.execute(
                """INSERT INTO farmers (name, phone, village, mandal, district, language)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    name,
                    request.form.get("phone", "").strip() or None,
                    request.form.get("village", "").strip() or None,
                    request.form.get("mandal", "").strip() or None,
                    request.form.get("district", "Hyderabad").strip(),
                    request.form.get("language", "te"),
                ),
            )
        conn.close()
        flash(f"రైతు '{name}' విజయవంతంగా నమోదు చేయబడ్డారు! | Farmer registered!", "success")
        return redirect(url_for("farmers.list_farmers"))
    return render_template("farmers/form.html")


@farmers_bp.route("/<int:farmer_id>")
def view_farmer(farmer_id: int) -> Any:
    """View a farmer profile and their documents."""
    conn = _db()
    farmer = conn.execute("SELECT * FROM farmers WHERE id = ?", (farmer_id,)).fetchone()
    if not farmer:
        flash("రైతు కనుగొనబడలేదు | Farmer not found.", "error")
        return redirect(url_for("farmers.list_farmers"))
    docs = conn.execute(
        """SELECT d.*, dt.name_te, dt.name_hi, dt.name_en FROM documents d
           LEFT JOIN doc_types dt ON d.doc_type = dt.code
           WHERE d.farmer_id = ? ORDER BY d.created_at DESC""",
        (farmer_id,),
    ).fetchall()
    conn.close()
    return render_template("farmers/view.html", farmer=farmer, docs=docs)


@farmers_bp.route("/<int:farmer_id>/delete", methods=["POST"])
def delete_farmer(farmer_id: int) -> Any:
    """Delete a farmer and cascade their documents."""
    conn = _db()
    farmer = conn.execute("SELECT name FROM farmers WHERE id = ?", (farmer_id,)).fetchone()
    if farmer:
        with conn:
            conn.execute("DELETE FROM farmers WHERE id = ?", (farmer_id,))
        flash(f"రైతు '{farmer['name']}' తొలగించబడ్డారు | Farmer deleted.", "info")
    conn.close()
    return redirect(url_for("farmers.list_farmers"))
