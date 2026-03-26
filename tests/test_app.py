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


# ---------------------------------------------------------------------------
# Laws database tests
# ---------------------------------------------------------------------------

from laws_database import (
    load_laws_database,
    search_law,
    get_law_by_short_name,
    get_all_laws,
    get_law_categories,
)


class TestLawsDatabase:
    def test_csv_loads_successfully(self):
        laws = load_laws_database()
        assert len(laws) > 0

    def test_csv_has_expected_columns(self):
        laws = load_laws_database()
        required_cols = {
            "act_name", "short_name", "year", "category",
            "description", "key_provisions", "enforcing_authority",
            "helpline", "portal", "status",
        }
        assert required_cols.issubset(set(laws[0].keys()))

    def test_all_laws_have_act_name(self):
        for law in load_laws_database():
            assert law["act_name"].strip(), f"Empty act_name: {law}"

    def test_all_laws_have_category(self):
        for law in load_laws_database():
            assert law["category"].strip(), f"Empty category: {law['act_name']}"

    def test_at_least_70_laws(self):
        assert len(load_laws_database()) >= 70

    def test_search_by_short_name_exact(self):
        results = search_law("IPC")
        assert len(results) >= 1
        assert results[0]["short_name"] == "IPC"

    def test_search_by_short_name_lowercase(self):
        results = search_law("ipc")
        assert len(results) >= 1
        assert results[0]["short_name"] == "IPC"

    def test_search_by_short_name_in_sentence(self):
        results = search_law("Tell me about the POCSO Act")
        assert len(results) >= 1
        assert results[0]["short_name"] == "POCSO Act"

    def test_search_by_act_name_keyword(self):
        results = search_law("consumer protection")
        assert len(results) >= 1
        assert any("Consumer" in r["act_name"] for r in results)

    def test_search_rti(self):
        results = search_law("right to information RTI")
        assert len(results) >= 1
        assert any("RTI" in r["short_name"] or "Information" in r["act_name"] for r in results)

    def test_search_returns_empty_for_nonsense(self):
        results = search_law("xyzqqqweather12345")
        assert results == []

    def test_search_empty_query_returns_empty(self):
        results = search_law("")
        assert results == []

    def test_search_max_results_respected(self):
        results = search_law("act", max_results=3)
        assert len(results) <= 3

    def test_get_law_by_short_name_found(self):
        law = get_law_by_short_name("RERA")
        assert law is not None
        assert law["short_name"] == "RERA"

    def test_get_law_by_short_name_case_insensitive(self):
        law = get_law_by_short_name("rera")
        assert law is not None

    def test_get_law_by_short_name_not_found(self):
        law = get_law_by_short_name("NONEXISTENT_ACT_XYZ")
        assert law is None

    def test_get_all_laws_returns_list(self):
        laws = get_all_laws()
        assert isinstance(laws, list)
        assert len(laws) >= 70

    def test_get_law_categories_returns_sorted_list(self):
        cats = get_law_categories()
        assert isinstance(cats, list)
        assert len(cats) > 0
        assert cats == sorted(cats)

    def test_expected_categories_present(self):
        cats = get_law_categories()
        for expected in ["Criminal", "Labour", "Family", "Consumer", "Digital", "Environment"]:
            assert expected in cats, f"Category '{expected}' not found"

    def test_key_provisions_pipe_separated(self):
        for law in load_laws_database():
            provisions = law.get("key_provisions", "")
            if provisions:
                parts = [p.strip() for p in provisions.split("|") if p.strip()]
                assert len(parts) >= 1, f"No provisions for {law['act_name']}"


class TestSearchLawRoute:
    def test_search_returns_200(self, client):
        rv = client.get("/search_law?q=IPC")
        assert rv.status_code == 200

    def test_search_returns_list(self, client):
        rv = client.get("/search_law?q=IPC")
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_search_result_has_required_fields(self, client):
        rv = client.get("/search_law?q=RERA")
        data = rv.get_json()
        assert len(data) >= 1
        result = data[0]
        for field in ["type", "title", "short_name", "year", "category",
                      "description", "provisions_html", "enforcing_authority",
                      "helpline", "portal", "status"]:
            assert field in result, f"Missing field: {field}"

    def test_search_result_type_is_law(self, client):
        rv = client.get("/search_law?q=POCSO")
        data = rv.get_json()
        assert data[0]["type"] == "law"

    def test_search_missing_q_returns_400(self, client):
        rv = client.get("/search_law")
        assert rv.status_code == 400

    def test_search_empty_q_returns_400(self, client):
        rv = client.get("/search_law?q=")
        assert rv.status_code == 400

    def test_search_n_parameter_limits_results(self, client):
        rv = client.get("/search_law?q=act&n=2")
        data = rv.get_json()
        assert len(data) <= 2

    def test_search_n_capped_at_20(self, client):
        rv = client.get("/search_law?q=act&n=100")
        data = rv.get_json()
        assert len(data) <= 20

    def test_search_provisions_html_present(self, client):
        rv = client.get("/search_law?q=RERA")
        data = rv.get_json()
        assert "<ul>" in data[0]["provisions_html"]
        assert "<li>" in data[0]["provisions_html"]

    def test_search_specific_laws(self, client):
        queries_expected = [
            ("Consumer Protection Act", "Consumer"),
            ("POCSO", "Child Rights"),
            ("RERA", "Property"),
            ("EPF Act", "Labour"),
        ]
        for q, expected_cat in queries_expected:
            rv = client.get(f"/search_law?q={q}")
            data = rv.get_json()
            assert len(data) >= 1, f"No results for '{q}'"
            assert any(expected_cat in r["category"] for r in data), \
                f"Expected category '{expected_cat}' not found for query '{q}'"


class TestListLawsRoute:
    def test_returns_200(self, client):
        rv = client.get("/laws")
        assert rv.status_code == 200

    def test_returns_all_laws(self, client):
        rv = client.get("/laws")
        data = rv.get_json()
        assert isinstance(data, list)
        assert len(data) >= 70

    def test_category_filter_works(self, client):
        rv = client.get("/laws?category=Labour")
        data = rv.get_json()
        assert len(data) > 0
        for item in data:
            assert item["category"].lower() == "labour"

    def test_category_filter_case_insensitive(self, client):
        rv_lower = client.get("/laws?category=labour")
        rv_upper = client.get("/laws?category=Labour")
        assert rv_lower.get_json() == rv_upper.get_json()

    def test_category_filter_unknown_returns_empty(self, client):
        rv = client.get("/laws?category=NonExistentCategory12345")
        data = rv.get_json()
        assert data == []

    def test_each_law_has_type_law(self, client):
        rv = client.get("/laws")
        data = rv.get_json()
        for item in data:
            assert item["type"] == "law"


class TestLawCategoriesRoute:
    def test_returns_200(self, client):
        rv = client.get("/law_categories")
        assert rv.status_code == 200

    def test_returns_sorted_list(self, client):
        rv = client.get("/law_categories")
        data = rv.get_json()
        assert isinstance(data, list)
        assert data == sorted(data)

    def test_contains_expected_categories(self, client):
        rv = client.get("/law_categories")
        data = rv.get_json()
        for cat in ["Criminal", "Labour", "Family", "Consumer", "Digital"]:
            assert cat in data


class TestChatWithLawsFallback:
    def test_chat_returns_law_type_for_specific_act(self, client):
        rv = client.post("/chat", json={"message": "Tell me about RERA", "lang": "en"})
        assert rv.status_code == 200
        data = rv.get_json()
        # Either "topic" from legal_knowledge or "law" from CSV database
        assert data["type"] in ("topic", "law")

    def test_chat_law_response_has_required_fields(self, client):
        rv = client.post("/chat", json={"message": "What is POCSO Act", "lang": "en"})
        assert rv.status_code == 200
        data = rv.get_json()
        if data["type"] == "law":
            for field in ["title", "short_name", "year", "category",
                          "description", "provisions_html"]:
                assert field in data, f"Missing field: {field}"

    def test_chat_ipc_query(self, client):
        rv = client.post("/chat", json={"message": "Tell me about IPC", "lang": "en"})
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] in ("topic", "law")

    def test_chat_still_returns_unknown_for_nonsense(self, client):
        rv = client.post(
            "/chat",
            json={"message": "xyzqqqweather12345", "lang": "en"},
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["type"] == "unknown"
