# Research: Farm Document Digitizer
## specs/001-document-digitizer/research.md

---

## 1. Problem Context

### Scale
- India has **110+ million** farm households (Census 2011)
- Telangana has **~5.8 million** farmer families
- **87%** of Indian farmers are smallholders (<2 hectares)

### Document Loss — Why It Matters
- Pattadar Passbook loss → cannot prove land ownership → loan rejection
- Missing Rythu Bandhu certificate → cannot claim ₹5,000/acre support
- Lost Aadhaar → delays in almost all government scheme enrollment
- Flood/fire events in Telangana regularly destroy physical documents

### Connectivity Reality
- Only **~40%** of rural Telangana has reliable 4G connectivity (TRAI 2023)
- Village CSCs (Common Service Centers) often have 2G-only backup
- **Offline-first is non-negotiable**, not a nice-to-have

---

## 2. Existing Solutions & Gaps

| Solution | What it does | Why AgriDoc is different |
|----------|-------------|--------------------------|
| DigiLocker | National document locker | Requires Aadhaar eKYC; English-only; online-only |
| mKisan | SMS-based alerts | No document storage |
| Bhulekh portals | Land records lookup | State-specific; read-only; no upload |
| AgriStack (planned) | Farmer database | Backend only; no farmer-facing UI |
| Google Drive | General cloud storage | Requires Google account; English; cloud-dependent |

**AgriDoc's niche:** Local-first, Telugu-language, farm-specific document organizer that works on cheap hardware without internet.

---

## 3. Telangana-Specific Document Types

Research from Telangana Agriculture Department website and field interviews:

| Document | Issuing Authority | Farmer Need |
|----------|-----------------|-------------|
| Pattadar Passbook | Revenue Dept | Prove land ownership for loans |
| Adangal (1B/RoR) | Revenue Dept | Crop details, tenancy proof |
| Rythu Bandhu cert | Agri Dept | ₹5,000/acre twice yearly |
| PM-KISAN | Central Govt | ₹6,000/year income support |
| Crop Insurance (PMFBY) | Insurance companies | Claim after crop failure |
| Kisan Credit Card | Banks | Short-term credit up to ₹3 lakh |
| Soil Health Card | Agri Dept | Fertilizer recommendations |
| Water Use Permit | Irrigation Dept | Borewell/irrigation rights |

---

## 4. AgriStack Alignment

[AgriStack](https://agristack.gov.in) is India's federated farmer database initiative:
- **Farmer ID** → Unique digital identity for every farmer
- **Land Records** → Linked to Pattadar, Adangal
- **Scheme Records** → PM-KISAN, Rythu Bandhu linked

**AgriDoc alignment:**
- `doc_types.code` maps to AgriStack document taxonomy
- `/api/sync` endpoint is designed for future AgriStack API push
- `farmers.aadhaar_last4` enables Farmer ID lookup without storing full Aadhaar

---

## 5. Technology Choices — Research Basis

### Why SQLite (not PostgreSQL)?
- Zero installation — works on any system
- Single file = easy backup (copy one file)
- Handles up to ~35GB / ~1M documents comfortably
- Used in production by Firefox, WhatsApp, iOS

### Why Flask (not Django)?
- Smaller memory footprint (~20MB vs ~60MB for Django at startup)
- Faster startup on old hardware
- Less scaffolding = easier for Swecha interns to understand
- Khetika (sibling project) also uses Flask → consistency

### Why Vanilla JS (not React)?
- Works on Chrome 80 (common on ₹8,000 Android phones)
- No build step — works without Node.js
- PWA Service Worker works without framework
- Page loads in <1s on slow connections

### Why Telugu-first UI?
- Field research: farmers respond better to Telugu interfaces
- State government communications are in Telugu
- Reduces friction for VLEs explaining the app

---

## 6. References

- [AgriStack Digital Public Infrastructure](https://agristack.gov.in)
- [Telangana Agriculture Department](https://agri.telangana.gov.in)
- [PM-KISAN Scheme](https://pmkisan.gov.in)
- [PMFBY Crop Insurance](https://pmfby.gov.in)
- [Offline First Manifesto](https://offlinefirst.org)
- [PWA Documentation — web.dev](https://web.dev/progressive-web-apps/)
- [Swecha Khetika Project](https://code.swecha.org/swecha/khetika)
- TRAI Annual Report 2023 — Rural Connectivity Statistics
