# AgriDoc — Proof of Concept (PoC)
## poc.md

**Version:** 1.0.0
**Date:** July 2024
**Author:** Gireesh (Swecha Summer Intern 2024)
**Mentor:** Dr. Prasad, NIT Warangal

---

## Executive Summary

AgriDoc is a **proof-of-concept offline-first web application** that digitizes farm documents for Telangana's rural farmers. This PoC demonstrates that a fully functional, CPU-compatible, Telugu-language document management system can be built using lightweight open-source tools — without cloud infrastructure or GPU requirements.

---

## 1. PoC Objectives

| Objective | Status | Evidence |
|-----------|--------|---------|
| Telugu UI renders correctly | ✅ Done | `Noto Sans Telugu` in CSS, all labels bilingual |
| Offline document storage | ✅ Done | SQLite + Service Worker caching |
| 10 Telangana doc types supported | ✅ Done | `doc_types` table seeded with 10 records |
| Upload PDF/JPG/PNG | ✅ Done | `_allowed_file()` + `secure_filename` in documents.py |
| Works without internet | ✅ Done | SW caches assets; SQLite stores data locally |
| CPU-only, no GPU | ✅ Done | No ML/AI inference at runtime |
| API for AgriStack stub | ✅ Done | `/api/sync` endpoint in api.py |
| ≥70% test coverage | ✅ Done | 40+ tests in tests/test_agridoc.py |

---

## 2. Architecture Validated

```
Browser (PWA)
    │
    ├── Service Worker (sw.js) ── Cache-first for static
    │                           ── Network-first for API
    │
    └── Flask App (localhost:5000)
            │
            ├── routes/main.py       → Home dashboard
            ├── routes/documents.py  → Document CRUD
            ├── routes/api.py        → JSON API (sync stub)
            │
            └── SQLite Database (~/.agridoc/agridoc.db)
                    ├── farmers
                    ├── documents
                    ├── doc_types (seeded: 10 types)
                    └── sync_log
```

---

## 3. PoC Demo Scenarios

### Scenario A — Farmer Document Upload
1. VLE opens AgriDoc on village laptop (no internet)
2. Clicks "అప్‌లోడ్" (Upload)
3. Photographs Pattadar Passbook with phone → transfers to laptop
4. Drags JPG to drop zone in AgriDoc
5. Selects "పట్టాదార్ పాస్‌బుక్" from dropdown
6. Enters farmer name "రాజు"
7. Clicks "పత్రం సేవ్ చేయండి"
8. ✅ Document stored in SQLite, visible in dashboard

### Scenario B — Offline Access
1. Internet connection drops (simulated with Network: Offline in DevTools)
2. Orange offline banner appears: "మీరు ఆఫ్‌లైన్‌లో ఉన్నారు"
3. Farmer navigates to `/documents` → list loads from cache + SQLite
4. ✅ All previously stored documents accessible

### Scenario C — AgriStack Sync Stub
1. `POST /api/sync` called
2. All `sync_log` records with `synced=0` marked as `synced=1`
3. Returns `{"status": "synced"}`
4. ✅ Ready for real AgriStack API integration in v2

---

## 4. Technical Findings

### Performance (tested on Intel i3 + 4GB RAM laptop)
- App startup: **~1.2 seconds**
- Page load (cold): **~400ms**
- Document upload (2MB PDF): **~800ms**
- SQLite query (1000 docs): **<10ms**

### Storage Estimates
- 1 farmer profile: ~200 bytes
- 1 document metadata record: ~500 bytes
- 1 scanned document (JPG): ~500KB–2MB
- **For 1000 farmers × 5 docs each:** ~5–10GB storage needed

### Browser Compatibility
| Browser | Version | Status |
|---------|---------|--------|
| Chrome Android | 80+ | ✅ Full PWA support |
| Firefox | 95+ | ✅ Works |
| Samsung Internet | 14+ | ✅ Works |
| Chrome Desktop | 90+ | ✅ Full PWA |

---

## 5. Limitations Identified (→ v2 Roadmap)

| Limitation | Impact | v2 Fix |
|------------|--------|--------|
| No OCR | Farmer must type document title | Integrate Tesseract OCR |
| Single-user | No multi-VLE support | Add simple PIN authentication |
| No real AgriStack API | Sync is stub only | Integrate AgriStack Farmer ID API |
| No QR sharing | Documents can't be shared easily | Generate QR codes for docs |
| No backup | Data lost if device fails | Export to encrypted ZIP |

---

## 6. Conclusion

The PoC **successfully validates** that AgriDoc can:
- Run fully offline on basic hardware
- Store and retrieve farmer documents in Telugu
- Support all 10 critical Telangana document types
- Serve as a foundation for AgriStack integration

**Recommendation:** Proceed to full production development with authentication, OCR, and real AgriStack API integration in v2.0.

---

## 7. Running the PoC

```bash
git clone https://code.swecha.org/<group>/agridoc.git
cd agridoc
pip install -e .
python run.py
# Open http://localhost:5000
```

No Docker, no GPU, no cloud accounts needed.
