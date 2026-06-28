"""Translations for AgriDoc UI strings in Telugu, Hindi, and English."""

from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── App-wide ──────────────────────────────────────────────────────────────
    "app_name": {
        "te": "AgriDoc",
        "hi": "AgriDoc",
        "en": "AgriDoc",
    },
    "app_tagline": {
        "te": "రైతు పత్ర కేంద్రం",
        "hi": "किसान दस्तावेज़ केंद्र",
        "en": "Farmer Document Centre",
    },
    "app_description": {
        "te": "AgriDoc — రైతుల పత్రాలను డిజిటైజ్ చేయండి | Farm Document Digitizer for Telangana Farmers",
        "hi": "AgriDoc — किसानों के दस्तावेज़ डिजिटाइज़ करें | Farm Document Digitizer",
        "en": "AgriDoc — Farm Document Digitizer for Telangana Farmers",
    },
    # ── Offline banner ────────────────────────────────────────────────────────
    "offline_msg": {
        "te": "మీరు ఆఫ్‌లైన్‌లో ఉన్నారు — మీ డేటా సురక్షితంగా నిల్వ చేయబడుతోంది",
        "hi": "आप ऑफ़लाइन हैं — आपका डेटा सुरक्षित रूप से सहेजा जा रहा है",
        "en": "You are offline — your data is being saved locally",
    },
    # ── Navbar ────────────────────────────────────────────────────────────────
    "nav_home": {
        "te": "హోమ్",
        "hi": "होम",
        "en": "Home",
    },
    "nav_farmers": {
        "te": "రైతులు",
        "hi": "किसान",
        "en": "Farmers",
    },
    "nav_documents": {
        "te": "పత్రాలు",
        "hi": "दस्तावेज़",
        "en": "Documents",
    },
    "nav_upload": {
        "te": "అప్‌లోడ్",
        "hi": "अपलोड",
        "en": "Upload",
    },
    # ── Index / Hero ──────────────────────────────────────────────────────────
    "hero_badge": {
        "te": "Telangana Farmers · AgriStack Aligned",
        "hi": "तेलंगाना किसान · AgriStack संरेखित",
        "en": "Telangana Farmers · AgriStack Aligned",
    },
    "hero_desc": {
        "te": "మీ అన్ని వ్యవసాయ పత్రాలను సురక్షితంగా భద్రపరచండి — ఆఫ్‌లైన్‌లో కూడా పని చేస్తుంది",
        "hi": "अपने सभी कृषि दस्तावेज़ सुरक्षित रखें — ऑफ़लाइन भी काम करता है",
        "en": "Securely store all your farm documents — works offline too",
    },
    "btn_add_document": {
        "te": "పత్రం జోడించండి",
        "hi": "दस्तावेज़ जोड़ें",
        "en": "Add Document",
    },
    "btn_view_documents": {
        "te": "పత్రాలు చూడండి",
        "hi": "दस्तावेज़ देखें",
        "en": "View Documents",
    },
    # ── Stats ─────────────────────────────────────────────────────────────────
    "stat_documents": {
        "te": "పత్రాలు",
        "hi": "दस्तावेज़",
        "en": "Documents",
    },
    "stat_farmers": {
        "te": "రైతులు",
        "hi": "किसान",
        "en": "Farmers",
    },
    "stat_verified": {
        "te": "ధృవీకరించబడిన",
        "hi": "सत्यापित",
        "en": "Verified",
    },
    "stat_pending_sync": {
        "te": "సింక్ పెండింగ్",
        "hi": "सिंक बाकी",
        "en": "Pending Sync",
    },
    # ── Categories ────────────────────────────────────────────────────────────
    "section_categories": {
        "te": "పత్ర రకాలు",
        "hi": "दस्तावेज़ श्रेणियां",
        "en": "Document Categories",
    },
    "cat_pattadar": {
        "te": "పట్టాదార్ పాస్‌బుక్",
        "hi": "पट्टादार पासबुक",
        "en": "Pattadar Passbook",
    },
    "cat_adangal": {
        "te": "అదంగల్ / RoR",
        "hi": "अदंगल / RoR",
        "en": "Adangal / RoR",
    },
    "cat_rytu_bandhu": {
        "te": "రైతు బంధు",
        "hi": "रायतु बंधु",
        "en": "Rythu Bandhu",
    },
    "cat_pm_kisan": {
        "te": "పీఎం-కిసాన్",
        "hi": "पीएम-किसान",
        "en": "PM-KISAN",
    },
    "cat_crop_ins": {
        "te": "పంట బీమా",
        "hi": "फसल बीमा",
        "en": "Crop Insurance",
    },
    "cat_aadhaar": {
        "te": "ఆధార్ కార్డ్",
        "hi": "आधार कार्ड",
        "en": "Aadhaar Card",
    },
    "cat_bank_pass": {
        "te": "బ్యాంక్ పాస్‌బుక్",
        "hi": "बैंक पासबुक",
        "en": "Bank Passbook",
    },
    "cat_soil": {
        "te": "మట్టి ఆరోగ్య కార్డు",
        "hi": "मिट्टी स्वास्थ्य कार्ड",
        "en": "Soil Health Card",
    },
    # ── Tips ──────────────────────────────────────────────────────────────────
    "section_tips": {
        "te": "సహాయకరమైన చిట్కాలు",
        "hi": "उपयोगी सुझाव",
        "en": "Helpful Tips",
    },
    "tip_offline_title": {
        "te": "ఆఫ్‌లైన్ పని చేస్తుంది",
        "hi": "ऑफ़लाइन काम करता है",
        "en": "Works Offline",
    },
    "tip_offline_desc": {
        "te": "ఇంటర్నెట్ లేకుండా కూడా మీ పత్రాలను జోడించి చూడవచ్చు",
        "hi": "इंटरनेट के बिना भी अपने दस्तावेज़ जोड़ें और देखें",
        "en": "Add and view your documents even without internet",
    },
    "tip_mobile_title": {
        "te": "మొబైల్ ఫ్రెండ్లీ",
        "hi": "मोबाइल अनुकूल",
        "en": "Mobile Friendly",
    },
    "tip_mobile_desc": {
        "te": "ఫోన్‌లో కూడా సులభంగా వాడవచ్చు — ఫోటో తీసి అప్‌లోడ్ చేయండి",
        "hi": "फोन पर भी आसानी से उपयोग करें — फोटो लेकर अपलोड करें",
        "en": "Easy to use on phone too — take a photo and upload",
    },
    "tip_secure_title": {
        "te": "సురక్షితం",
        "hi": "सुरक्षित",
        "en": "Secure",
    },
    "tip_secure_desc": {
        "te": "మీ పత్రాలు మీ పరికరంలోనే నిల్వ అవుతాయి — బయటకు వెళ్ళవు",
        "hi": "आपके दस्तावेज़ आपके डिवाइस पर ही रहते हैं — बाहर नहीं जाते",
        "en": "Your documents stay on your device — never leave it",
    },
    # ── Farmers list ──────────────────────────────────────────────────────────
    "page_farmers_title": {
        "te": "రైతులు",
        "hi": "किसान",
        "en": "Farmers",
    },
    "page_farmers_sub": {
        "te": "నమోదు చేసిన రైతుల జాబితా",
        "hi": "पंजीकृत किसानों की सूची",
        "en": "List of registered farmers",
    },
    "btn_add_farmer": {
        "te": "రైతును జోడించు",
        "hi": "किसान जोड़ें",
        "en": "Add Farmer",
    },
    "search_farmers_placeholder": {
        "te": "పేరు, గ్రామం లేదా ఫోన్ వెతకండి...",
        "hi": "नाम, गांव या फोन खोजें...",
        "en": "Search by name, village or phone...",
    },
    "btn_search": {
        "te": "వెతకు",
        "hi": "खोजें",
        "en": "Search",
    },
    "label_documents": {
        "te": "పత్రాలు",
        "hi": "दस्तावेज़",
        "en": "documents",
    },
    "no_farmers_title": {
        "te": "రైతులు నమోదు కాలేదు",
        "hi": "कोई किसान पंजीकृत नहीं",
        "en": "No Farmers Registered",
    },
    "no_farmers_sub": {
        "te": "మొదటి రైతును జోడించండి",
        "hi": "पहला किसान जोड़ें",
        "en": "Add your first farmer",
    },
    "confirm_delete_farmer": {
        "te": "ను తొలగించాలా?",
        "hi": "को हटाएं?",
        "en": "Delete",
    },
    # ── Farmer form ───────────────────────────────────────────────────────────
    "page_register_farmer_title": {
        "te": "రైతును నమోదు చేయండి",
        "hi": "किसान पंजीकृत करें",
        "en": "Register Farmer",
    },
    "page_register_farmer_sub": {
        "te": "కొత్త రైతు వివరాలు నమోదు చేయండి",
        "hi": "नए किसान का विवरण दर्ज करें",
        "en": "Enter new farmer details",
    },
    "label_farmer_name": {
        "te": "రైతు పేరు",
        "hi": "किसान का नाम",
        "en": "Farmer Name",
    },
    "placeholder_farmer_name": {
        "te": "ఉదా: రాజు కుమార్",
        "hi": "उदा: राजू कुमार",
        "en": "e.g. Raju Kumar",
    },
    "label_phone": {
        "te": "ఫోన్ నంబర్",
        "hi": "फोन नंबर",
        "en": "Phone Number",
    },
    "label_village": {
        "te": "గ్రామం",
        "hi": "गांव",
        "en": "Village",
    },
    "placeholder_village": {
        "te": "గ్రామం పేరు",
        "hi": "गांव का नाम",
        "en": "Village name",
    },
    "label_mandal": {
        "te": "మండలం",
        "hi": "मंडल",
        "en": "Mandal",
    },
    "placeholder_mandal": {
        "te": "మండలం పేరు",
        "hi": "मंडल का नाम",
        "en": "Mandal name",
    },
    "label_district": {
        "te": "జిల్లా",
        "hi": "जिला",
        "en": "District",
    },
    "label_language_pref": {
        "te": "భాష ప్రాధాన్యత",
        "hi": "भाषा प्राथमिकता",
        "en": "Language Preference",
    },
    "btn_register_farmer": {
        "te": "రైతును నమోదు చేయండి",
        "hi": "किसान पंजीकृत करें",
        "en": "Register Farmer",
    },
    "btn_cancel": {
        "te": "రద్దు చేయండి",
        "hi": "रद्द करें",
        "en": "Cancel",
    },
    "btn_back": {
        "te": "వెనక్కి",
        "hi": "वापस",
        "en": "Back",
    },
    # ── Farmer view ───────────────────────────────────────────────────────────
    "farmer_profile_sub": {
        "te": "రైతు వివరాలు",
        "hi": "किसान प्रोफ़ाइल",
        "en": "Farmer Profile",
    },
    "btn_add_document_farmer": {
        "te": "పత్రం జోడించు",
        "hi": "दस्तावेज़ जोड़ें",
        "en": "Add Document",
    },
    "section_personal_details": {
        "te": "వ్యక్తిగత వివరాలు",
        "hi": "व्यक्तिगत विवरण",
        "en": "Personal Details",
    },
    "label_phone_short": {
        "te": "ఫోన్",
        "hi": "फोन",
        "en": "Phone",
    },
    "label_village_short": {
        "te": "గ్రామం",
        "hi": "गांव",
        "en": "Village",
    },
    "label_mandal_short": {
        "te": "మండలం",
        "hi": "मंडल",
        "en": "Mandal",
    },
    "label_district_short": {
        "te": "జిల్లా",
        "hi": "जिला",
        "en": "District",
    },
    "label_language_short": {
        "te": "భాష",
        "hi": "भाषा",
        "en": "Language",
    },
    "label_registered_date": {
        "te": "నమోదు తేదీ",
        "hi": "पंजीकरण तिथि",
        "en": "Registered Date",
    },
    "no_docs_yet": {
        "te": "ఇంకా పత్రాలు లేవు",
        "hi": "अभी कोई दस्तावेज़ नहीं",
        "en": "No documents yet",
    },
    # ── Documents list ────────────────────────────────────────────────────────
    "page_documents_title": {
        "te": "పత్రాలు",
        "hi": "दस्तावेज़",
        "en": "Documents",
    },
    "page_documents_sub": {
        "te": "మీ అన్ని వ్యవసాయ పత్రాల జాబితా",
        "hi": "आपके सभी कृषि दस्तावेज़ों की सूची",
        "en": "List of all your farm documents",
    },
    "btn_add_new": {
        "te": "కొత్తది జోడించు",
        "hi": "नया जोड़ें",
        "en": "Add New",
    },
    "search_docs_placeholder": {
        "te": "పేరు లేదా రైతు పేరు వెతకండి...",
        "hi": "नाम या किसान का नाम खोजें...",
        "en": "Search by name or farmer...",
    },
    "filter_all_types": {
        "te": "అన్ని రకాలు",
        "hi": "सभी प्रकार",
        "en": "All Types",
    },
    "btn_view": {
        "te": "చూడండి",
        "hi": "देखें",
        "en": "View",
    },
    "no_docs_title": {
        "te": "పత్రాలు ఏవీ లేవు",
        "hi": "कोई दस्तावेज़ नहीं मिला",
        "en": "No Documents Found",
    },
    "no_docs_sub": {
        "te": "మీ మొదటి పత్రాన్ని అప్‌లోడ్ చేయండి",
        "hi": "अपना पहला दस्तावेज़ अपलोड करें",
        "en": "Upload your first document",
    },
    "btn_upload_document": {
        "te": "పత్రం జోడించండి",
        "hi": "दस्तावेज़ जोड़ें",
        "en": "Add Document",
    },
    "confirm_delete_doc": {
        "te": "ఈ పత్రాన్ని తొలగించాలా?",
        "hi": "इस दस्तावेज़ को हटाएं?",
        "en": "Delete this document?",
    },
    # ── Upload form ───────────────────────────────────────────────────────────
    "page_upload_title": {
        "te": "పత్రం అప్‌లోడ్",
        "hi": "दस्तावेज़ अपलोड",
        "en": "Upload Document",
    },
    "page_upload_sub": {
        "te": "కొత్త పత్రాన్ని జోడించండి",
        "hi": "नया दस्तावेज़ जोड़ें",
        "en": "Add a new document",
    },
    "drop_zone_title": {
        "te": "ఫైల్ ఇక్కడ వదలండి లేదా క్లిక్ చేయండి",
        "hi": "फ़ाइल यहाँ छोड़ें या क्लिक करें",
        "en": "Drop file here or click to browse",
    },
    "drop_zone_sub": {
        "te": "PDF, JPG, PNG (max 16MB)",
        "hi": "PDF, JPG, PNG (अधिकतम 16MB)",
        "en": "PDF, JPG, PNG (max 16MB)",
    },
    "label_doc_title": {
        "te": "పత్రం పేరు",
        "hi": "दस्तावेज़ शीर्षक",
        "en": "Document Title",
    },
    "placeholder_doc_title": {
        "te": "ఉదా: పట్టాదార్ పాస్‌బుక్ 2024",
        "hi": "उदा: पट्टादार पासबुक 2024",
        "en": "e.g. Pattadar Passbook 2024",
    },
    "label_doc_type": {
        "te": "పత్రం రకం",
        "hi": "दस्तावेज़ प्रकार",
        "en": "Document Type",
    },
    "placeholder_doc_type": {
        "te": "పత్రం రకం ఎంచుకోండి...",
        "hi": "दस्तావेज़ प्रकार चुनें...",
        "en": "Select document type...",
    },
    "label_farmer_select": {
        "te": "రైతు ఎంచుకోండి",
        "hi": "किसान चुनें",
        "en": "Select Farmer",
    },
    "placeholder_farmer_select": {
        "te": "— రైతు ఎంచుకోండి (ఐచ్ఛికం) —",
        "hi": "— किसान चुनें (वैकल्पिक) —",
        "en": "— Select Farmer (optional) —",
    },
    "label_language": {
        "te": "భాష",
        "hi": "भाषा",
        "en": "Language",
    },
    "label_notes": {
        "te": "నోట్స్",
        "hi": "नोट्स",
        "en": "Notes",
    },
    "placeholder_notes": {
        "te": "అదనపు వివరాలు...",
        "hi": "अतिरिक्त विवरण...",
        "en": "Additional details...",
    },
    "btn_save_document": {
        "te": "పత్రం సేవ్ చేయండి",
        "hi": "दस्तावेज़ सहेजें",
        "en": "Save Document",
    },
    # ── Document view ─────────────────────────────────────────────────────────
    "label_farmer": {
        "te": "రైతు",
        "hi": "किसान",
        "en": "Farmer",
    },
    "label_date": {
        "te": "తేదీ",
        "hi": "तारीख",
        "en": "Date",
    },
    "label_size": {
        "te": "పరిమాణం",
        "hi": "आकार",
        "en": "Size",
    },
    "label_notes_short": {
        "te": "నోట్స్",
        "hi": "नोट्स",
        "en": "Notes",
    },
    "verified_badge": {
        "te": "ధృవీకరించబడింది",
        "hi": "सत्यापित",
        "en": "Verified",
    },
    "btn_download": {
        "te": "డౌన్‌లోడ్",
        "hi": "डाउनलोड",
        "en": "Download",
    },
    "btn_delete": {
        "te": "తొలగించు",
        "hi": "हटाएं",
        "en": "Delete",
    },
    # ── About page ────────────────────────────────────────────────────────────
    "page_about_title": {
        "te": "AgriDoc గురించి",
        "hi": "AgriDoc के बारे में",
        "en": "About AgriDoc",
    },
    "about_mission_title": {
        "te": "మా లక్ష్యం",
        "hi": "हमारा उद्देश्य",
        "en": "Our Mission",
    },
    "about_mission_te": {
        "te": "తెలంగాణలోని ప్రతి రైతుకు వారి వ్యవసాయ పత్రాలను డిజిటల్‌గా భద్రపరచే అవకాశం కల్పించడం — ఇంటర్నెట్ లేకుండా కూడా, తెలుగులో, తక్కువ ధర పరికరాల్లో కూడా.",
        "hi": "तेलंगाना के हर किसान को उनके कृषि दस्तावेज़ डिजिटल रूप से सुरक्षित करने का अवसर देना — ऑफ़लाइन भी, हिंदी में, सस्ते उपकरणों पर भी।",
        "en": "Provide every Telangana farmer the ability to digitally secure their farm documents — offline, in their own language, on any device.",
    },
    "about_impact_title": {
        "te": "ప్రభావం",
        "hi": "प्रभाव",
        "en": "Impact",
    },
    "about_tech_title": {
        "te": "సాంకేతికత",
        "hi": "तकनीक",
        "en": "Technology",
    },
    "about_built_title": {
        "te": "నిర్మించినవారు",
        "hi": "निर्माताओं",
        "en": "Built By",
    },
    "about_built_desc": {
        "te": "తెలంగాణ రైతుల కోసం స్వేచ్ఛా సాఫ్ట్‌వేర్ సంఘంచే నిర్మించబడింది.",
        "hi": "तेलंगाना किसानों के लिए मुक्त सॉफ़्टवेयर समुदाय द्वारा निर्मित।",
        "en": "Built by the Free Software community for Telangana farmers.",
    },
    # ── Language names ────────────────────────────────────────────────────────
    "lang_te": {
        "te": "తెలుగు",
        "hi": "తెలుగు",
        "en": "తెలుగు",
    },
    "lang_hi": {
        "te": "हिंदी",
        "hi": "हिंदी",
        "en": "हिंदी",
    },
    "lang_en": {
        "te": "English",
        "hi": "English",
        "en": "English",
    },
    # ── Footer ────────────────────────────────────────────────────────────────
    "footer_tagline": {
        "te": "Swecha × AgriStack × Telangana Farmers",
        "hi": "Swecha × AgriStack × तेलंगाना किसान",
        "en": "Swecha × AgriStack × Telangana Farmers",
    },
}


def get_t(lang: str) -> dict[str, str]:
    """Return a flat dict of key → translated string for *lang*.

    Falls back to English when a key is missing for the requested language.
    """
    result: dict[str, str] = {}
    for key, variants in TRANSLATIONS.items():
        result[key] = variants.get(lang) or variants.get("en") or ""
    return result
