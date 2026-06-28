# Feature Spec: Farm Document Digitizer (Core)
## specs/001-document-digitizer/spec.md

---

## Problem Statement

Farmers in Telangana carry physical copies of Pattadar Passbooks, Rythu Bandhu
certificates, PM-KISAN documents, and Aadhaar cards. These get lost in floods,
damaged in storage, and are hard to produce quickly at government offices.

There is no easy, offline-capable, Telugu-language tool to digitize and organize
these documents on a basic smartphone or shared village computer.

---

## User Stories

```
As a Telangana farmer (రైతు),
I want to photograph and store my Pattadar Passbook digitally,
So that I never lose access to my land ownership proof.

As a village-level entrepreneur (VLE),
I want to organize 50+ farmers' documents by type,
So that I can quickly find the right document during camp drives.

As a farmer with limited connectivity,
I want the app to work without internet,
So that I can access my documents from any remote location.
```

---

## Requirements

### Must Have (P0)
- [ ] Upload PDF/JPG/PNG documents (max 16MB)
- [ ] Tag documents with type (Pattadar, Adangal, Aadhaar, etc.)
- [ ] Link documents to farmer profiles
- [ ] Works fully offline (SQLite + Service Worker)
- [ ] Telugu language UI (primary)
- [ ] Search documents by name and type
- [ ] View and download stored documents

### Should Have (P1)
- [ ] Hindi language UI option
- [ ] Drag-and-drop file upload
- [ ] Dashboard with document count stats
- [ ] Document verification flag
- [ ] AgriStack sync stub endpoint

### Nice to Have (P2)
- [ ] OCR extraction of text from images
- [ ] QR code sharing of documents
- [ ] Batch upload of multiple documents

---

## Success Criteria

- [ ] A farmer can upload a document in <60 seconds without instructions
- [ ] App works with no internet connection (verified with Network tab)
- [ ] All 10 Telangana document types are supported
- [ ] Telugu text renders correctly on mobile Chrome
- [ ] App loads in <5s on a ₹15,000 Android device

---

## Out of Scope (v1.0)

- OCR text extraction
- Multi-user authentication
- Cloud storage backup
- Direct government portal integration

---

## References

- [AgriStack Framework](https://agristack.gov.in)
- [Telangana Agriculture Portal](https://agri.telangana.gov.in)
- [Rythu Bandhu Scheme](https://rythu.telangana.gov.in)
- [Khetika Chatbot](../khetika/) — sibling project
