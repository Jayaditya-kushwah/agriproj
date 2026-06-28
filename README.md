# 🌾 AgriDoc — రైతు పత్ర కేంద్రం | Farm Document Digitizer

[![CI Pipeline](https://img.shields.io/badge/CI-GitLab-orange)](https://code.swecha.org)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-AGPLv3-blue)](LICENSE)
[![AgriStack](https://img.shields.io/badge/AgriStack-Aligned-brightgreen)](https://agristack.gov.in)
[![Offline First](https://img.shields.io/badge/Offline-First-2d6a4f)](https://offlinefirst.org)

> **AgriDoc** helps India's 110M+ farmers digitize, store, and access their critical land and government documents — **offline-first, CPU-compatible, multilingual (Telugu · Hindi · English)**.

Developed as part of **Swecha Summer Internship 2024** | Telangana focus | AgriStack aligned.

---

## 🎯 Problem Statement

Indian farmers—especially in Telangana—struggle to:
- Locate physical copies of Pattadar Passbooks, Rythu Bandhu certificates, PM-KISAN docs
- Access documents in areas with poor internet connectivity
- Navigate government portals not available in Telugu

**AgriDoc solves this** with a local-first web app that stores scanned documents securely on the farmer's device/local server.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 Document Vault | Store 10+ types of farm docs (Pattadar, Adangal, PM-KISAN, Rythu Bandhu...) |
| 📱 PWA / Offline-First | Works without internet via Service Worker + SQLite |
| 🌐 Multilingual | Telugu · Hindi · English UI |
| 🔍 Smart Search | Filter by document type, farmer name, village |
| 👨‍🌾 Farmer Profiles | Link documents to individual farmer records |
| 🔄 AgriStack Sync | Sync stub for government AgriStack API integration |
| 🤖 CPU-First OCR | Tesseract LSTM extracts text from scanned docs — offline, no GPU |
| 📊 Field Extraction | Auto-detects survey number, farmer name, land area, dates from images |
| 🖥️ CPU-Compatible | No GPU required — runs on ₹15,000 laptops |
| 🔒 Privacy-First | All data stays on local device — no cloud required |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://code.swecha.org/<your-group>/agridoc.git
cd agridoc

# Install
pip install -e ".[dev]"

# Run
python run.py
# → Open http://localhost:5000
```

### CPU-First OCR Setup (Offline, No GPU)

AgriDoc uses **Tesseract 4.x LSTM** — a fully CPU-based OCR engine. No CUDA, no cloud API, no internet needed.

```bash
# 1. Install Tesseract + language packs (system dependency)
sudo apt install tesseract-ocr tesseract-ocr-tel tesseract-ocr-hin tesseract-ocr-tam tesseract-ocr-kan

# 2. Python bindings already in requirements (pytesseract + Pillow)
pip install -e ".[dev]"

# 3. Verify
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

**How it works:**
- Upload a Pattadar image → OCR runs instantly on CPU
- Tesseract extracts Telugu/Hindi/English text
- AgriDoc parses: farmer name, survey number, land area, village, dates
- All results stored in SQLite — works with Wi-Fi OFF

**Declared runtime:** `tesseract-ocr` (LSTM, CPU-only) + `pytesseract` Python wrapper

### Docker

```bash
docker build -t agridoc .
docker run -p 5000:5000 -v agridoc-data:/root/.agridoc agridoc
```

---

## 📁 Project Structure

```
agridoc/
├── agridoc/              # Flask application
│   ├── app.py            # App factory
│   ├── models/           # Database (SQLite)
│   ├── routes/           # Blueprints (main, documents, api)
│   ├── static/           # CSS, JS, PWA assets
│   └── templates/        # Jinja2 HTML templates
├── tests/                # pytest test suite
├── specs/                # Spec-Kit driven development
│   └── 001-document-digitizer/
├── .specify/             # Spec-Kit project memory
├── .gitlab-ci.yml        # CI/CD pipeline
├── .pre-commit-config.yaml
├── pyproject.toml        # All tool configs
└── Dockerfile
```

---

## 🧪 Testing

```bash
pytest                          # Run all tests
pytest --cov=agridoc            # With coverage
pytest -v tests/test_agridoc.py # Verbose
```

---

## 📊 Supported Document Types

- **Land**: Pattadar Passbook, Adangal/RoR, Water Use Permit
- **Government Schemes**: Rythu Bandhu, PM-KISAN
- **Identity**: Aadhaar Card
- **Finance**: Bank Passbook, Kisan Credit Card
- **Agriculture**: Soil Health Card, Crop Insurance

---

## 🌍 Telangana & AgriStack Alignment

- Document types aligned with Telangana Agriculture Department taxonomy
- API endpoints designed for AgriStack integration (`/api/sync`)
- Telugu-first UI with Noto Sans Telugu font
- Offline support for rural areas with poor connectivity

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License — see [LICENSE](LICENSE).

## 🙏 Acknowledgements

Built with ❤️ by Swecha interns for Telangana farmers.
Inspired by Khetika AgriTech chatbot project.
