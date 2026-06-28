"""CPU-first OCR engine for AgriDoc using Tesseract.

Runs entirely offline with no GPU or cloud calls.
Runtime: pytesseract (Tesseract 4.x LSTM engine, CPU-only)
Model: tessdata LSTM models for Telugu (tel), Hindi (hin), English (eng)

Extracts structured fields from Indian agricultural documents:
- Pattadar Passbook (పట్టాదార్ పాస్‌బుక్)
- Adangal / RoR
- PM-KISAN certificates
- Aadhaar cards
- Rythu Bandhu slips
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Runtime detection — graceful fallback if tesseract not installed
# ---------------------------------------------------------------------------
try:
    import pytesseract
    from PIL import Image

    TESSERACT_AVAILABLE = True
except ImportError:  # pragma: no cover
    TESSERACT_AVAILABLE = False


def _tesseract_available() -> bool:
    """Return True if tesseract binary is callable."""
    if not TESSERACT_AVAILABLE:
        return False
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------------------
# Language config — CPU inference only, no cloud
# ---------------------------------------------------------------------------
LANG_MAP = {
    "te": "tel+eng",   # Telugu + English fallback
    "hi": "hin+eng",   # Hindi + English fallback
    "ta": "tam+eng",   # Tamil + English fallback
    "kn": "kan+eng",   # Kannada + English fallback
    "en": "eng",
}

# Tesseract PSM 3 = auto page segmentation (best for full docs)
# OEM 1 = LSTM neural net (CPU, no GPU required)
TESS_CONFIG = "--oem 1 --psm 3"


# ---------------------------------------------------------------------------
# Field extraction patterns — Indian agricultural documents
# ---------------------------------------------------------------------------

# Survey / khata number patterns (Telugu & Hindi land records)
_SURVEY_PATTERNS = [
    r"survey\s*no[.\s:]*([0-9A-Za-z/\-]+)",
    r"s\.no[.\s:]*([0-9A-Za-z/\-]+)",
    r"సర్వే\s*నం[.\s:]*([0-9A-Za-z/\-]+)",
    r"ఖాతా\s*నం[.\s:]*([0-9A-Za-z/\-]+)",
    r"खाता\s*संख्या[.\s:]*([0-9A-Za-z/\-]+)",
    r"khata[.\s:]*([0-9A-Za-z/\-]+)",
]

# Land area patterns (acres, guntas, hectares)
_AREA_PATTERNS = [
    r"(\d+[\.,]?\d*)\s*(?:acres?|ఎకరాలు|एकड़)",
    r"(\d+[\.,]?\d*)\s*(?:guntas?|గుంటలు)",
    r"(\d+[\.,]?\d*)\s*(?:hectares?|హెక్టారులు|हेक्टेयर)",
    r"area[.\s:]*(\d+[\.,]?\d*)",
    r"విస్తీర్ణం[.\s:]*(\d+[\.,]?\d*)",
]

# Farmer name patterns
_NAME_PATTERNS = [
    r"(?:farmer|owner|పట్టాదార్|రైతు)\s*(?:name)?[.\s:]*([A-Za-z\u0C00-\u0C7F\u0900-\u097F ]{3,40})",
    r"(?:S/o|D/o|W/o|son of|daughter of)[.\s:]*([A-Za-z\u0C00-\u0C7F\u0900-\u097F ]{3,40})",
    r"పేరు[.\s:]*([A-Za-z\u0C00-\u0C7F ]{3,40})",
    r"नाम[.\s:]*([A-Za-z\u0900-\u097F ]{3,40})",
]

# Village / mandal patterns
_VILLAGE_PATTERNS = [
    r"(?:village|గ్రామం|ग्राम)[.\s:]*([A-Za-z\u0C00-\u0C7F\u0900-\u097F ]{3,30})",
    r"(?:mandal|మండలం|मंडल)[.\s:]*([A-Za-z\u0C00-\u0C7F\u0900-\u097F ]{3,30})",
]

# District patterns
_DISTRICT_PATTERNS = [
    r"(?:district|జిల్లా|जिला)[.\s:]*([A-Za-z\u0C00-\u0C7F\u0900-\u097F ]{3,30})",
]

# Date patterns (Indian formats: DD/MM/YYYY, DD-MM-YYYY)
_DATE_PATTERNS = [
    r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
    r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
]

# Aadhaar (masked): XXXX XXXX 1234
_AADHAAR_PATTERN = r"[Xx*]{4}\s?[Xx*]{4}\s?(\d{4})"

# Amount / benefit patterns (PM-KISAN, Rythu Bandhu)
_AMOUNT_PATTERNS = [
    r"(?:amount|రూపాయలు|राशि|benefit)[.\s:₹]*([0-9,]+)",
    r"₹\s*([0-9,]+)",
    r"Rs\.?\s*([0-9,]+)",
]


def _extract_first(text: str, patterns: list[str]) -> str | None:
    """Return the first regex match across all patterns, case-insensitive."""
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.UNICODE)
        if m:
            return m.group(1).strip()
    return None


def _extract_all(text: str, patterns: list[str]) -> list[str]:
    """Return all unique matches across all patterns."""
    found: list[str] = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE | re.UNICODE):
            val = m.group(1).strip()
            if val and val not in found:
                found.append(val)
    return found


# ---------------------------------------------------------------------------
# Core OCR function
# ---------------------------------------------------------------------------

def run_ocr(
    file_path: str | Path,
    doc_type: str = "unknown",
    language: str = "te",
) -> dict[str, Any]:
    """Run CPU-first OCR on an image or PDF page.

    Args:
        file_path: Path to image file (PNG/JPG/WEBP) or PDF.
        doc_type:  AgriDoc document type code (pattadar, adangal, aadhaar…).
        language:  ISO 639-1 code for primary script (te/hi/ta/kn/en).

    Returns:
        dict with keys: ocr_text, ocr_fields, ocr_status, ocr_engine,
                        ocr_confidence, processing_time_ms.
    """
    start = time.monotonic()
    result: dict[str, Any] = {
        "ocr_text": "",
        "ocr_fields": {},
        "ocr_status": "pending",
        "ocr_engine": "tesseract-cpu",
        "ocr_confidence": 0.0,
        "processing_time_ms": 0,
    }

    if not _tesseract_available():
        result["ocr_status"] = "unavailable"
        result["ocr_text"] = (
            "[Tesseract not installed. Run: sudo apt install tesseract-ocr "
            "tesseract-ocr-tel tesseract-ocr-hin]"
        )
        return result

    path = Path(file_path)
    if not path.exists():
        result["ocr_status"] = "error"
        result["ocr_text"] = f"File not found: {file_path}"
        return result

    try:
        # Open image — pytesseract handles PNG/JPG/WEBP natively
        # For PDFs a single-page rasterise via pdf2image would be needed;
        # we skip multi-page PDFs here and OCR only image uploads.
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            result["ocr_status"] = "skipped"
            result["ocr_text"] = "[PDF: install pdf2image + poppler for OCR]"
            elapsed = (time.monotonic() - start) * 1000
            result["processing_time_ms"] = round(elapsed)
            return result

        img = Image.open(str(path))

        # Select tesseract language string (CPU LSTM engine)
        lang = LANG_MAP.get(language, "tel+eng")

        # Get text with confidence data
        data = pytesseract.image_to_data(
            img,
            lang=lang,
            config=TESS_CONFIG,
            output_type=pytesseract.Output.DICT,
        )

        # Build plain text
        words = [
            w for w, c in zip(data["text"], data["conf"])
            if str(w).strip() and int(c) > 0
        ]
        ocr_text = " ".join(words)

        # Average confidence (ignore -1 entries)
        confs = [int(c) for c in data["conf"] if int(c) >= 0]
        avg_conf = sum(confs) / len(confs) if confs else 0.0

        result["ocr_text"] = ocr_text
        result["ocr_confidence"] = round(avg_conf, 1)

        # --- Structured field extraction ---
        fields = _extract_fields(ocr_text, doc_type)
        result["ocr_fields"] = fields
        result["ocr_status"] = "success" if ocr_text.strip() else "empty"

    except Exception as exc:  # noqa: BLE001
        result["ocr_status"] = "error"
        result["ocr_text"] = f"OCR error: {exc}"

    elapsed = (time.monotonic() - start) * 1000
    result["processing_time_ms"] = round(elapsed)
    return result


def _extract_fields(text: str, doc_type: str) -> dict[str, Any]:
    """Extract structured fields from raw OCR text based on document type."""
    fields: dict[str, Any] = {}

    # Universal fields — present on almost all Indian agri docs
    name = _extract_first(text, _NAME_PATTERNS)
    if name:
        fields["farmer_name"] = name

    village = _extract_first(text, _VILLAGE_PATTERNS)
    if village:
        fields["village"] = village

    district = _extract_first(text, _DISTRICT_PATTERNS)
    if district:
        fields["district"] = district

    dates = _extract_all(text, _DATE_PATTERNS)
    if dates:
        fields["dates"] = dates

    # Land document specific (pattadar, adangal)
    if doc_type in ("pattadar", "adangal", "water", "soil"):
        survey = _extract_first(text, _SURVEY_PATTERNS)
        if survey:
            fields["survey_number"] = survey

        areas = _extract_all(text, _AREA_PATTERNS)
        if areas:
            fields["land_area"] = areas

    # Identity document
    if doc_type == "aadhaar":
        aadhaar_last4 = re.search(_AADHAAR_PATTERN, text)
        if aadhaar_last4:
            fields["aadhaar_last4"] = aadhaar_last4.group(1)

    # Scheme / benefit documents
    if doc_type in ("pm_kisan", "rytu_bandhu", "crop_ins"):
        amounts = _extract_all(text, _AMOUNT_PATTERNS)
        if amounts:
            fields["benefit_amount"] = amounts

    return fields


# ---------------------------------------------------------------------------
# Convenience wrapper used by Flask routes
# ---------------------------------------------------------------------------

def ocr_and_store(
    file_path: str | Path,
    doc_id: int,
    doc_type: str,
    language: str,
    upload_folder: str,
    db_conn: Any,
) -> dict[str, Any]:
    """Run OCR and write results back to the documents table.

    Args:
        file_path:     Filename (relative) inside upload_folder.
        doc_id:        Primary key in documents table.
        doc_type:      Document type code.
        language:      Language code.
        upload_folder: Absolute path to uploads directory.
        db_conn:       Open SQLite connection.

    Returns:
        OCR result dict.
    """
    full_path = Path(upload_folder) / file_path
    result = run_ocr(full_path, doc_type=doc_type, language=language)

    with db_conn:
        db_conn.execute(
            """UPDATE documents
               SET ocr_text   = ?,
                   ocr_fields = ?,
                   ocr_status = ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (
                result["ocr_text"],
                json.dumps(result["ocr_fields"], ensure_ascii=False),
                result["ocr_status"],
                doc_id,
            ),
        )

    return result
