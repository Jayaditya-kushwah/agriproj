"""Main routes for AgriDoc."""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """Render the home/dashboard page."""
    return render_template("index.html")


@main_bp.route("/about")
def about() -> str:
    """Render the about page."""
    return render_template("about.html")


@main_bp.route("/set-language/<lang>")
def set_language(lang: str) -> object:
    """Persist the user's language choice in the session."""
    supported = {"te", "hi", "en"}
    if lang in supported:
        session["lang"] = lang
    return redirect(request.referrer or url_for("main.index"))
