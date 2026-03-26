"""
Tests for the Legal Assistant application.
"""

import pytest
from app import app as flask_app
from legal_knowledge import (
    find_topic,
    is_greeting,
    is_gratitude,
    get_topics_list,
    get_topic_by_key,
    LEGAL_TOPICS,
)
from language_support import (
    get_ui_strings,
    detect_language,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret"
    with flask_app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Legal knowledge tests
# ---------------------------------------------------------------------------

class TestFindTopic:
    def test_consumer_keyword(self):
        topic = find_topic("I bought a defective product")
        assert topic is not None
        assert topic["title"] == "Consumer Rights"

    def test_rti_keyword(self):
        topic = find_topic("How do I file an RTI application?")
        assert topic is not None
        assert topic["title"] == "Right to Information (RTI)"

    def test_labour_keyword(self):
        topic = find_topic("My employer is not paying minimum wages")
        assert topic is not None
        assert topic["title"] == "Labour Rights"

    def test_domestic_violence_keyword(self):
        topic = find_topic("I am facing domestic violence and abuse")
        assert topic is not None
        assert topic["title"] == "Protection from Domestic Violence"

    def test_fundamental_rights_keyword(self):
        topic = find_topic("What are my fundamental rights under the constitution?")
        assert topic is not None
        assert topic["title"] == "Fundamental Rights"

    def test_legal_aid_keyword(self):
        topic = find_topic("I need free legal aid")
        assert topic is not None
        assert topic["title"] == "Free Legal Aid"

    def test_tenant_rights_keyword(self):
        topic = find_topic("My landlord is trying to evict me")
        assert topic is not None
        assert topic["title"] == "Tenant Rights"

    def test_property_rights_keyword(self):
        topic = find_topic("There is an encroachment on my property")
        assert topic is not None
        assert topic["title"] == "Property & Land Rights"

    def test_child_rights_keyword(self):
        topic = find_topic("Child labour in factory")
        assert topic is not None
        assert topic["title"] == "Child Rights"

    def test_sc_st_rights_keyword(self):
        topic = find_topic("I am a Dalit facing atrocities and caste abuse")
        assert topic is not None
        assert topic["title"] == "SC/ST Rights & Anti-Atrocity Protection"

    def test_sc_st_rights_hindi_keyword(self):
        topic = find_topic("दलित अत्याचार")
        assert topic is not None
        assert topic["title"] == "SC/ST Rights & Anti-Atrocity Protection"

    def test_criminal_rights_arrest_keyword(self):
        topic = find_topic("I have been arrested by the police")
        assert topic is not None
        assert topic["title"] == "Rights During Arrest & Criminal Proceedings"

    def test_criminal_rights_fir_keyword(self):
        topic = find_topic("How do I file an FIR?")
        assert topic is not None
        assert topic["title"] == "Rights During Arrest & Criminal Proceedings"

    def test_criminal_rights_bail_keyword(self):
        topic = find_topic("I need bail from custody")
        assert topic is not None
        assert topic["title"] == "Rights During Arrest & Criminal Proceedings"

    def test_women_rights_posh_keyword(self):
        topic = find_topic("I want to report sexual harassment under the POSH act")
        assert topic is not None
        assert topic["title"] == "Women's Rights"

    def test_women_rights_maternity_keyword(self):
        topic = find_topic("I was denied my maternity benefit")
        assert topic is not None
        assert topic["title"] == "Women's Rights"

    def test_disability_rights_keyword(self):
        topic = find_topic("I am disabled and need a UDID card")
        assert topic is not None
        assert topic["title"] == "Disability Rights"

    def test_disability_rights_hindi_keyword(self):
        topic = find_topic("दिव्यांग व्यक्ति के अधिकार")
        assert topic is not None
        assert topic["title"] == "Disability Rights"

    def test_senior_citizen_rights_keyword(self):
        topic = find_topic("I am a senior citizen not receiving pension")
        assert topic is not None
        assert topic["title"] == "Senior Citizen Rights"

    def test_senior_citizen_rights_parents_keyword(self):
        topic = find_topic("I need old age support as an elderly parent")
        assert topic is not None
        assert topic["title"] == "Senior Citizen Rights"

    def test_cyber_crime_keyword(self):
        topic = find_topic("I am a victim of cybercrime and hacking")
        assert topic is not None
        assert topic["title"] == "Cyber Crime & Digital Rights"

    def test_cyber_crime_upi_keyword(self):
        topic = find_topic("Someone did UPI fraud via phishing")
        assert topic is not None
        assert topic["title"] == "Cyber Crime & Digital Rights"

    def test_cyber_crime_otp_keyword(self):
        topic = find_topic("I received a phishing call and lost money")
        assert topic is not None
        assert topic["title"] == "Cyber Crime & Digital Rights"

    def test_hindi_consumer_keyword(self):
        topic = find_topic("उपभोक्ता शिकायत")
        assert topic is not None
        assert topic["title"] == "Consumer Rights"

    def test_no_match_returns_none(self):
        topic = find_topic("What is the weather today?")
        assert topic is None

    def test_empty_string_returns_none(self):
        topic = find_topic("")
        assert topic is None


class TestGreetingDetection:
    def test_hello(self):
        assert is_greeting("hello") is True

    def test_namaste(self):
        assert is_greeting("Namaste") is True

    def test_hindi_namaste(self):
        assert is_greeting("नमस्ते") is True

    def test_non_greeting(self):
        assert is_greeting("Tell me about RTI") is False


class TestGratitudeDetection:
    def test_thanks(self):
        assert is_gratitude("thanks") is True

    def test_dhanyawad(self):
        assert is_gratitude("dhanyawad") is True

    def test_hindi_dhanyawad(self):
        assert is_gratitude("धन्यवाद") is True

    def test_non_gratitude(self):
        assert is_gratitude("What is consumer rights?") is False


class TestTopicList:
    def test_all_topics_returned(self):
        topics = get_topics_list()
        assert len(topics) == len(LEGAL_TOPICS)
        for t in topics:
            assert "key" in t
            assert "title" in t

    def test_get_topic_by_valid_key(self):
        topic = get_topic_by_key("rti")
        assert topic is not None
        assert topic["title"] == "Right to Information (RTI)"

    def test_get_topic_by_invalid_key(self):
        topic = get_topic_by_key("nonexistent_key")
        assert topic is None


# ---------------------------------------------------------------------------
# Language support tests
# ---------------------------------------------------------------------------

class TestLanguageSupport:
    def test_default_language_english(self):
        assert DEFAULT_LANGUAGE == "en"

    def test_supported_languages_count(self):
        # en + 9 Indian languages
        assert len(SUPPORTED_LANGUAGES) == 10

    def test_all_major_languages_present(self):
        for code in ["en", "hi", "bn", "ta", "te", "mr", "kn", "ml", "pa", "gu"]:
            assert code in SUPPORTED_LANGUAGES

    def test_get_ui_strings_english(self):
        ui = get_ui_strings("en")
        assert "greeting" in ui
        assert "send_btn" in ui
        assert "disclaimer" in ui
        assert "Legal Assistant" in ui["title"]

    def test_get_ui_strings_hindi(self):
        ui = get_ui_strings("hi")
        assert "greeting" in ui
        assert ui["lang_name"] == "हिन्दी"

    def test_get_ui_strings_fallback(self):
        # Unknown language should fallback to English
        ui = get_ui_strings("xx")
        assert ui["lang_name"] == "English"

    def test_detect_language_english(self):
        lang = detect_language("What are my consumer rights in India?")
        assert lang == "en"

    def test_detect_language_hindi(self):
        lang = detect_language("मुझे अपने अधिकार जानने हैं")
        # Should detect as Hindi or fallback gracefully to a valid code
        assert lang in SUPPORTED_LANGUAGES

    def test_detect_language_unknown_fallback(self):
        # Very short text may not detect reliably; should return valid code
        lang = detect_language("x")
        assert lang in SUPPORTED_LANGUAGES


# ---------------------------------------------------------------------------
# Flask route tests
# ---------------------------------------------------------------------------

class TestIndexRoute:
    def test_get_returns_200(self, client):
        rv = client.get("/")
        assert rv.status_code == 200

    def test_html_contains_title(self, client):
        rv = client.get("/")
        assert b"Legal Assistant" in rv.data

    def test_html_contains_chat_form(self, client):
        rv = client.get("/")
        assert b"chat-form" in rv.data
        assert b"user-input" in rv.data
        assert b"send-btn" in rv.data


class TestChatRoute:
    def test_greeting_en(self, client):
        rv = client.post(
            "/chat",
            json={"message": "hello", "lang": "en"},
            content_type="application/json",
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "greeting"
        assert "text" in data

    def test_greeting_hi(self, client):
        rv = client.post(
            "/chat",
            json={"message": "नमस्ते", "lang": "hi"},
            content_type="application/json",
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "greeting"

    def test_thanks_response(self, client):
        rv = client.post(
            "/chat",
            json={"message": "thank you", "lang": "en"},
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "thanks"

    def test_topic_consumer(self, client):
        rv = client.post(
            "/chat",
            json={"message": "I bought a defective product", "lang": "en"},
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "topic"
        assert data["title"] == "Consumer Rights"
        assert "details_html" in data
        assert "steps_html" in data
        assert "law" in data

    def test_topic_rti(self, client):
        rv = client.post(
            "/chat",
            json={"message": "how to file RTI", "lang": "en"},
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "topic"
        assert "RTI" in data["title"] or "Information" in data["title"]

    def test_unknown_query(self, client):
        rv = client.post(
            "/chat",
            json={"message": "what is the temperature today", "lang": "en"},
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "unknown"
        assert "text" in data

    def test_empty_message_returns_400(self, client):
        rv = client.post("/chat", json={"message": "", "lang": "en"})
        assert rv.status_code == 400

    def test_missing_body_returns_400(self, client):
        rv = client.post("/chat", json={})
        assert rv.status_code == 400


class TestTopicRoute:
    def test_valid_topic(self, client):
        rv = client.get("/topic/rti")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "topic"
        assert "RTI" in data["title"] or "Information" in data["title"]

    def test_invalid_topic_returns_404(self, client):
        rv = client.get("/topic/nonexistent")
        assert rv.status_code == 404

    def test_all_topics_via_route(self, client):
        for key in LEGAL_TOPICS:
            rv = client.get(f"/topic/{key}")
            assert rv.status_code == 200, f"Topic {key} returned {rv.status_code}"

    def test_new_topics_have_required_fields(self, client):
        new_keys = [
            "sc_st_rights", "criminal_rights", "women_rights",
            "disability_rights", "senior_citizen_rights", "cyber_crime",
        ]
        for key in new_keys:
            rv = client.get(f"/topic/{key}")
            assert rv.status_code == 200, f"Topic {key} returned {rv.status_code}"
            data = rv.get_json()
            assert data["type"] == "topic", f"Topic {key} has wrong type"
            assert "title" in data and data["title"], f"Topic {key} missing title"
            assert "summary" in data and data["summary"], f"Topic {key} missing summary"
            assert "details_html" in data, f"Topic {key} missing details_html"
            assert "steps_html" in data, f"Topic {key} missing steps_html"
            assert "law" in data and data["law"], f"Topic {key} missing law"


class TestLanguagesRoute:
    def test_returns_dict(self, client):
        rv = client.get("/languages")
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, dict)
        assert "en" in data
        assert "hi" in data

    def test_returns_10_languages(self, client):
        rv = client.get("/languages")
        data = rv.get_json()
        assert len(data) == 10


class TestTopicsRoute:
    def test_returns_list(self, client):
        rv = client.get("/topics")
        assert rv.status_code == 200
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) == len(LEGAL_TOPICS)


class TestSetLanguageRoute:
    def test_valid_language(self, client):
        rv = client.post("/set_language", json={"lang": "hi"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["status"] == "ok"
        assert data["lang"] == "hi"
        assert "ui" in data

    def test_invalid_language_defaults_to_en(self, client):
        rv = client.post("/set_language", json={"lang": "xx"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["lang"] == "en"
