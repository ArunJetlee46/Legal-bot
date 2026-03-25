# ⚖️ Legal Assistant – Know Your Rights

A user-friendly digital assistant providing **free legal information in 10 languages**, designed to enhance legal awareness and accessibility for marginalized communities in India.

---

## ✨ Features

- **Multi-language support** – English, Hindi (हिन्दी), Bengali (বাংলা), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ), Gujarati (ગુજરાતી)
- **9 major legal topics** covering the most important rights for marginalized communities:
  - Consumer Rights (Consumer Protection Act, 2019)
  - Right to Information / RTI (RTI Act, 2005)
  - Labour Rights (Minimum Wages Act, ID Act, EPF, ESI)
  - Protection from Domestic Violence (PWDVA, 2005)
  - Fundamental Rights (Indian Constitution, Part III)
  - Free Legal Aid (Legal Services Authorities Act, 1987)
  - Tenant Rights (State Rent Control Acts, Model Tenancy Act, 2021)
  - Property & Land Rights (RERA, Transfer of Property Act)
  - Child Rights (RTE, POCSO, Child Labour Act)
- **Keyword-based intent detection** with Hindi keywords for bilingual queries
- **Language auto-detection** – automatically detects user's language from typed text
- **Emergency helplines** always visible in header (112, 1091, 1098, 15100)
- **Accessible design** – ARIA roles, keyboard navigation, high-contrast, mobile-friendly
- **No login required** – immediate help for anyone

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+

### Installation

```bash
# Clone the repository
git clone https://github.com/ArunJetlee46/Legal-bot.git
cd Legal-bot

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

Open your browser and navigate to **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
Legal-bot/
├── app.py                  # Flask application (routes, chat logic)
├── legal_knowledge.py      # Legal knowledge base (9 topics, keyword matching)
├── language_support.py     # Multi-language UI strings + translation utilities
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Chat interface template
├── static/
│   ├── css/style.css       # Accessible, mobile-first stylesheet
│   └── js/app.js           # Frontend chat logic
└── tests/
    └── test_app.py         # 51 unit and integration tests
```

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

All **51 tests** should pass.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Main chat interface |
| `POST` | `/chat` | Send a message; returns structured JSON response |
| `GET`  | `/topic/<key>` | Get details for a specific legal topic |
| `POST` | `/set_language` | Switch UI language |
| `GET`  | `/languages` | List supported languages |
| `GET`  | `/topics` | List all available topics |

### Chat API Example

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I bought a defective product", "lang": "en"}'
```

---

## 📖 Legal Topics Covered

| Topic | Key Law |
|-------|---------|
| Consumer Rights | Consumer Protection Act, 2019 |
| Right to Information | RTI Act, 2005 |
| Labour Rights | Minimum Wages Act 1948, ID Act 1947 |
| Domestic Violence | PWDVA, 2005 |
| Fundamental Rights | Constitution of India, Art. 12–35 |
| Free Legal Aid | Legal Services Authorities Act, 1987 |
| Tenant Rights | Model Tenancy Act, 2021 |
| Property & Land | RERA 2016, Transfer of Property Act 1882 |
| Child Rights | RTE 2009, POCSO 2012 |

---

## ⚠️ Disclaimer

This chatbot provides **general legal information only** and does not constitute legal advice. For specific legal matters, please consult a qualified lawyer or visit your nearest Legal Services Authority (NALSA helpline: **15100**).

---

## 🤝 Contributing

Contributions are welcome! To add a new language or legal topic, edit `language_support.py` and `legal_knowledge.py` respectively.
