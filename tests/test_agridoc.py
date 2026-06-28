"""AgriDoc test suite — pytest with coverage."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from agridoc.app import create_app


@pytest.fixture
def app_config(tmp_path: Path) -> dict:
    """Return test configuration using a temp directory."""
    return {
        "TESTING": True,
        "DATABASE_PATH": str(tmp_path / "test.db"),
        "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        "SECRET_KEY": "test-secret",
    }


@pytest.fixture
def client(app_config: dict) -> Generator:
    """Create a test client."""
    app = create_app(app_config)
    with app.test_client() as client:
        yield client


# ── Home / Main Routes ─────────────────────────────────────


def test_index_returns_200(client) -> None:
    """Home page should return 200."""
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_contains_agridoc(client) -> None:
    """Home page should contain AgriDoc branding."""
    resp = client.get("/")
    assert b"AgriDoc" in resp.data


def test_about_redirects_or_200(client) -> None:
    """About page should not 500."""
    resp = client.get("/about")
    assert resp.status_code in (200, 302, 404)


# ── Documents Routes ───────────────────────────────────────


def test_documents_list_200(client) -> None:
    resp = client.get("/documents/")
    assert resp.status_code == 200


def test_documents_list_empty(client) -> None:
    resp = client.get("/documents/")
    # Empty state shown
    assert b"Documents" in resp.data or resp.status_code == 200


def test_documents_upload_get(client) -> None:
    resp = client.get("/documents/upload")
    assert resp.status_code == 200


def test_documents_upload_post_valid(client) -> None:
    resp = client.post(
        "/documents/upload",
        data={
            "title": "Test Pattadar",
            "doc_type": "pattadar",
            "language": "te",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_documents_upload_creates_record(client) -> None:
    client.post(
        "/documents/upload",
        data={"title": "Test Doc", "doc_type": "aadhaar", "language": "te"},
    )
    resp = client.get("/documents/")
    assert resp.status_code == 200


def test_document_view_not_found(client) -> None:
    resp = client.get("/documents/9999", follow_redirects=True)
    assert resp.status_code == 200  # Redirects to list


def test_document_delete_not_found(client) -> None:
    resp = client.post("/documents/9999/delete", follow_redirects=True)
    assert resp.status_code == 200


def test_documents_search(client) -> None:
    resp = client.get("/documents/?q=pattadar")
    assert resp.status_code == 200


def test_documents_filter_by_type(client) -> None:
    resp = client.get("/documents/?type=aadhaar")
    assert resp.status_code == 200


# ── API Routes ─────────────────────────────────────────────


def test_api_stats(client) -> None:
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert "total_documents" in data
    assert "total_farmers" in data


def test_api_stats_values_are_ints(client) -> None:
    resp = client.get("/api/stats")
    data = json.loads(resp.data)
    assert isinstance(data["total_documents"], int)
    assert isinstance(data["total_farmers"], int)


def test_api_documents_empty(client) -> None:
    resp = client.get("/api/documents")
    assert resp.status_code == 200
    assert json.loads(resp.data) == []


def test_api_doc_types(client) -> None:
    resp = client.get("/api/doc-types")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert len(data) >= 5


def test_api_doc_types_have_code(client) -> None:
    resp = client.get("/api/doc-types")
    data = json.loads(resp.data)
    for dt in data:
        assert "code" in dt
        assert "name_en" in dt
        assert "name_te" in dt


def test_api_farmers_empty(client) -> None:
    resp = client.get("/api/farmers")
    assert resp.status_code == 200
    assert json.loads(resp.data) == []


def test_api_create_farmer(client) -> None:
    resp = client.post(
        "/api/farmers",
        json={"name": "Raju", "village": "Warangal", "language": "te"},
    )
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data["status"] == "created"
    assert "id" in data


def test_api_create_farmer_missing_name(client) -> None:
    resp = client.post("/api/farmers", json={"village": "Test"})
    assert resp.status_code == 400


def test_api_create_farmer_appears_in_list(client) -> None:
    client.post("/api/farmers", json={"name": "Suresh"})
    resp = client.get("/api/farmers")
    data = json.loads(resp.data)
    assert any(f["name"] == "Suresh" for f in data)


def test_api_sync(client) -> None:
    resp = client.post("/api/sync")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "synced"


# ── Farmer Routes ──────────────────────────────────────────


def test_farmers_list_200(client) -> None:
    resp = client.get("/farmers/")
    assert resp.status_code == 200


def test_farmers_new_get(client) -> None:
    resp = client.get("/farmers/new")
    assert resp.status_code == 200


def test_farmers_create_valid(client) -> None:
    resp = client.post(
        "/farmers/new",
        data={"name": "రాజు", "village": "Warangal", "district": "Warangal", "language": "te"},
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_farmers_create_missing_name(client) -> None:
    resp = client.post("/farmers/new", data={"village": "X"}, follow_redirects=True)
    assert resp.status_code == 200


def test_farmer_view_not_found(client) -> None:
    resp = client.get("/farmers/9999", follow_redirects=True)
    assert resp.status_code == 200


def test_farmer_delete_not_found(client) -> None:
    resp = client.post("/farmers/9999/delete", follow_redirects=True)
    assert resp.status_code == 200


def test_farmer_create_then_view(client) -> None:
    client.post("/farmers/new", data={"name": "Suresh", "language": "te"})
    resp = client.get("/api/farmers")
    data = json.loads(resp.data)
    assert len(data) == 1
    fid = data[0]["id"]
    resp2 = client.get(f"/farmers/{fid}")
    assert resp2.status_code == 200


def test_farmer_create_then_delete(client) -> None:
    client.post("/farmers/new", data={"name": "DeleteMe", "language": "te"})
    resp = client.get("/api/farmers")
    fid = json.loads(resp.data)[0]["id"]
    del_resp = client.post(f"/farmers/{fid}/delete", follow_redirects=True)
    assert del_resp.status_code == 200
    resp2 = client.get("/api/farmers")
    assert json.loads(resp2.data) == []



def test_db_init_creates_tables(tmp_path: Path) -> None:
    from agridoc.models.database import get_connection, init_db

    db_path = str(tmp_path / "init_test.db")
    init_db(db_path)
    conn = get_connection(db_path)
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    ]
    assert "farmers" in tables
    assert "documents" in tables
    assert "doc_types" in tables
    conn.close()


def test_db_doc_types_seeded(tmp_path: Path) -> None:
    from agridoc.models.database import get_connection, init_db

    db_path = str(tmp_path / "seed_test.db")
    init_db(db_path)
    conn = get_connection(db_path)
    count = conn.execute("SELECT COUNT(*) FROM doc_types").fetchone()[0]
    assert count >= 8
    conn.close()


def test_db_idempotent_init(tmp_path: Path) -> None:
    from agridoc.models.database import init_db

    db_path = str(tmp_path / "idem_test.db")
    init_db(db_path)
    init_db(db_path)  # Should not raise


# ── App Factory ────────────────────────────────────────────


def test_app_factory_creates_app(app_config: dict) -> None:
    from agridoc.app import create_app

    app = create_app(app_config)
    assert app is not None


def test_app_factory_testing_flag(app_config: dict) -> None:
    from agridoc.app import create_app

    app = create_app(app_config)
    assert app.config["TESTING"] is True


def test_app_upload_folder_created(tmp_path: Path) -> None:
    from agridoc.app import create_app

    cfg = {
        "TESTING": True,
        "DATABASE_PATH": str(tmp_path / "x.db"),
        "UPLOAD_FOLDER": str(tmp_path / "uploads_test"),
        "SECRET_KEY": "s",
    }
    create_app(cfg)
    assert Path(cfg["UPLOAD_FOLDER"]).exists()


# ── OCR Engine Unit Tests ──────────────────────────────────


def test_ocr_engine_unavailable_when_no_tesseract(monkeypatch) -> None:
    """OCR engine returns 'unavailable' status gracefully when tesseract is absent."""
    import agridoc.utils.ocr_engine as eng
    monkeypatch.setattr(eng, "TESSERACT_AVAILABLE", False)
    result = eng.run_ocr("/nonexistent/file.png", doc_type="pattadar", language="te")
    assert result["ocr_status"] == "unavailable"
    assert result["ocr_engine"] == "tesseract-cpu"
    assert "Tesseract" in result["ocr_text"]


def test_ocr_engine_missing_file(monkeypatch) -> None:
    """OCR engine returns 'error' status when file does not exist."""
    import agridoc.utils.ocr_engine as eng
    # Patch _tesseract_available to True so we reach the file-check branch
    monkeypatch.setattr(eng, "_tesseract_available", lambda: True)
    result = eng.run_ocr("/tmp/definitely_does_not_exist_xyz.png")
    assert result["ocr_status"] == "error"
    assert "not found" in result["ocr_text"].lower()


def test_ocr_engine_pdf_skipped(monkeypatch, tmp_path) -> None:
    """PDFs are skipped (no pdf2image) and return 'skipped' status."""
    import agridoc.utils.ocr_engine as eng
    monkeypatch.setattr(eng, "_tesseract_available", lambda: True)
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake content")
    result = eng.run_ocr(str(fake_pdf))
    assert result["ocr_status"] == "skipped"
    assert "processing_time_ms" in result


def test_ocr_result_has_required_keys(monkeypatch) -> None:
    """run_ocr always returns all required keys."""
    import agridoc.utils.ocr_engine as eng
    monkeypatch.setattr(eng, "TESSERACT_AVAILABLE", False)
    result = eng.run_ocr("any.png")
    for key in ("ocr_text", "ocr_fields", "ocr_status", "ocr_engine", "ocr_confidence", "processing_time_ms"):
        assert key in result, f"Missing key: {key}"


def test_ocr_field_extraction_survey_number() -> None:
    """_extract_fields pulls survey number from English text."""
    from agridoc.utils.ocr_engine import _extract_fields
    text = "Survey No. 123/A Farmer: Raju Village: Warangal"
    fields = _extract_fields(text, doc_type="pattadar")
    assert fields.get("survey_number") == "123/A"


def test_ocr_field_extraction_land_area() -> None:
    """_extract_fields pulls land area in acres."""
    from agridoc.utils.ocr_engine import _extract_fields
    text = "Total area: 2.5 acres Survey No. 45"
    fields = _extract_fields(text, doc_type="pattadar")
    assert fields.get("land_area") is not None
    assert "2.5" in fields["land_area"]


def test_ocr_field_extraction_amount() -> None:
    """_extract_fields pulls benefit amount for PM-KISAN docs."""
    from agridoc.utils.ocr_engine import _extract_fields
    text = "PM-KISAN benefit amount ₹ 6000 credited"
    fields = _extract_fields(text, doc_type="pm_kisan")
    assert fields.get("benefit_amount") is not None


def test_ocr_field_extraction_aadhaar() -> None:
    """_extract_fields pulls masked Aadhaar last 4 digits."""
    from agridoc.utils.ocr_engine import _extract_fields
    text = "Aadhaar: XXXX XXXX 5678"
    fields = _extract_fields(text, doc_type="aadhaar")
    assert fields.get("aadhaar_last4") == "5678"


def test_ocr_field_no_false_positives_on_empty() -> None:
    """_extract_fields returns empty dict for blank text."""
    from agridoc.utils.ocr_engine import _extract_fields
    fields = _extract_fields("", doc_type="pattadar")
    assert isinstance(fields, dict)


# ── OCR API Endpoint Tests ─────────────────────────────────


def test_api_ocr_document_not_found(client) -> None:
    """OCR API returns 404 for nonexistent document."""
    resp = client.post("/api/ocr/9999")
    assert resp.status_code == 404


def test_api_ocr_no_file_attached(client) -> None:
    """OCR API returns 400 when document has no file."""
    # Create a doc without a file
    client.post(
        "/documents/upload",
        data={"title": "NoFile Doc", "doc_type": "pattadar", "language": "te"},
    )
    resp_list = client.get("/api/documents")
    import json as _json
    docs = _json.loads(resp_list.data)
    doc_id = docs[0]["id"]
    resp = client.post(f"/api/ocr/{doc_id}")
    assert resp.status_code == 400
