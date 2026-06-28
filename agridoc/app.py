"""Flask application factory for AgriDoc."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

from flask import Flask, session

from agridoc.models.database import init_db
from agridoc.routes.main import main_bp
from agridoc.routes.documents import documents_bp
from agridoc.routes.api import api_bp
from agridoc.routes.farmers import farmers_bp
from agridoc.utils.translations import get_t


def create_app(config: Optional[dict] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # Default configuration
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "agridoc-dev-secret-2024"),
        DATABASE_PATH=os.environ.get(
            "DATABASE_PATH",
            str(Path.home() / ".agridoc" / "agridoc.db"),
        ),
        UPLOAD_FOLDER=os.environ.get(
            "UPLOAD_FOLDER",
            str(Path.home() / ".agridoc" / "uploads"),
        ),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB
        SUPPORTED_LANGUAGES=["en", "te", "hi"],
        DEFAULT_LANGUAGE="te",
        OFFLINE_MODE=os.environ.get("OFFLINE_MODE", "true").lower() == "true",
    )

    if config:
        app.config.update(config)

    # Ensure required directories exist
    Path(app.config["DATABASE_PATH"]).parent.mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    # Initialize database
    with app.app_context():
        init_db(app.config["DATABASE_PATH"])

    # ── Context processor — injects `t` and `lang` into every template ───────
    @app.context_processor
    def inject_translations() -> dict:
        lang = session.get("lang", app.config["DEFAULT_LANGUAGE"])
        return {"t": get_t(lang), "lang": lang}

    # ── Jinja2 custom filters ─────────────────────────────────────────────────
    @app.template_filter("from_json")
    def from_json_filter(value: Any) -> Any:
        """Parse a JSON string inside templates (used for ocr_fields)."""
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value or "{}")
        except (json.JSONDecodeError, TypeError):
            return {}

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(documents_bp, url_prefix="/documents")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(farmers_bp, url_prefix="/farmers")

    return app
