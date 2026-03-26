"""
Legal Assistant – main Flask application.

Provides a conversational interface to Indian legal information
in 10 languages (English + 9 major Indian languages).
"""

from __future__ import annotations

import re
import os

from flask import Flask, render_template, request, jsonify, session

from legal_knowledge import (
    find_topic,
    is_greeting,
    is_gratitude,
    get_topics_list,
    get_topic_by_key,
)
from language_support import (
    get_ui_strings,
    detect_language,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)
from laws_database import (
    search_law,
    get_law_by_short_name,
    get_all_laws,
    get_law_categories,
    search_kanoon,
    load_kanoon_database,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "legal-assistant-dev-secret")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _markdown_to_html(text: str) -> str:
    """Convert a small subset of markdown (**bold** and newlines) to HTML."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = text.replace("\n", "<br>")
    return text


def _build_topic_response(topic: dict) -> dict:
    """Convert a topic dict into a structured chat response payload."""
    details_html = "".join(
        f"<li>{_markdown_to_html(d)}</li>" for d in topic["details"]
    )
    steps_html = "".join(
        f"<li>{_markdown_to_html(s)}</li>" for s in topic["steps"]
    )
    return {
        "type": "topic",
        "title": topic["title"],
        "summary": topic["summary"],
        "details_html": f"<ul>{details_html}</ul>",
        "steps_html": f"<ol>{steps_html}</ol>",
        "law": topic["law"],
    }


def _build_law_response(law: dict) -> dict:
    """Convert a laws-database row dict into a structured chat response payload."""
    provisions = [p.strip() for p in law.get("key_provisions", "").split("|") if p.strip()]
    provisions_html = "".join(f"<li>{_markdown_to_html(p)}</li>" for p in provisions)
    return {
        "type": "law",
        "title": law.get("act_name", ""),
        "short_name": law.get("short_name", ""),
        "year": law.get("year", ""),
        "category": law.get("category", ""),
        "description": law.get("description", ""),
        "provisions_html": f"<ul>{provisions_html}</ul>" if provisions_html else "",
        "enforcing_authority": law.get("enforcing_authority", ""),
        "helpline": law.get("helpline", ""),
        "portal": law.get("portal", ""),
        "status": law.get("status", ""),
    }


def _build_kanoon_response(law: dict) -> dict:
    """Convert a Kanoon-index row dict into a structured chat response payload."""
    return {
        "type": "kanoon",
        "title": law.get("title", ""),
        "source": law.get("source", ""),
        "place": law.get("place", ""),
        "published_date": law.get("published_date", ""),
        "commencement_date": law.get("commencement_date", ""),
        "url": law.get("url", ""),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main chat interface."""
    lang = session.get("lang", DEFAULT_LANGUAGE)
    ui = get_ui_strings(lang)
    topics = get_topics_list()
    return render_template(
        "index.html",
        ui=ui,
        lang=lang,
        supported_languages=SUPPORTED_LANGUAGES,
        topics=topics,
    )


@app.route("/set_language", methods=["POST"])
def set_language():
    """Persist the user's chosen language in the session."""
    data = request.get_json(silent=True) or {}
    lang = data.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    session["lang"] = lang
    ui = get_ui_strings(lang)
    return jsonify({"status": "ok", "lang": lang, "ui": ui})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Process a user message and return a structured JSON response.

    Expected JSON body: {"message": "<user text>", "lang": "<lang_code>"}
    Returns: {"type": "greeting"|"thanks"|"topic"|"unknown", ...}
    """
    data = request.get_json(silent=True) or {}
    message: str = (data.get("message") or "").strip()
    lang: str = data.get("lang") or session.get("lang", DEFAULT_LANGUAGE)

    if not message:
        return jsonify({"type": "error", "text": "Empty message"}), 400

    ui = get_ui_strings(lang)

    # Auto-detect language if not explicitly set
    if lang == DEFAULT_LANGUAGE:
        detected = detect_language(message)
        if detected != DEFAULT_LANGUAGE and detected in SUPPORTED_LANGUAGES:
            lang = detected
            ui = get_ui_strings(lang)

    # 1. Greeting
    if is_greeting(message):
        return jsonify({"type": "greeting", "text": ui["greeting"]})

    # 2. Gratitude
    if is_gratitude(message):
        return jsonify({"type": "thanks", "text": ui["thanks_reply"]})

    # 3. Keyword topic match (structured legal topics)
    topic = find_topic(message)
    if topic:
        return jsonify(_build_topic_response(topic))

    # 4. CSV laws-database search (fallback for specific act/law queries)
    laws = search_law(message, max_results=1)
    if laws:
        return jsonify(_build_law_response(laws[0]))

    # 5. Kanoon index search (broad search across 7 500+ Indian laws)
    kanoon_results = search_kanoon(message, max_results=3)
    if kanoon_results:
        return jsonify({
            "type": "kanoon_list",
            "text": "I found the following laws in the Indian legal database:",
            "results": [_build_kanoon_response(r) for r in kanoon_results],
        })

    # 6. No match
    return jsonify({"type": "unknown", "text": ui["no_match"]})


@app.route("/topic/<topic_key>", methods=["GET"])
def get_topic(topic_key: str):
    """Return the full details of a specific legal topic."""
    topic = get_topic_by_key(topic_key)
    if not topic:
        return jsonify({"error": "Topic not found"}), 404
    return jsonify(_build_topic_response(topic))


@app.route("/languages", methods=["GET"])
def get_languages():
    """Return the list of supported languages."""
    return jsonify(SUPPORTED_LANGUAGES)


@app.route("/topics", methods=["GET"])
def list_topics():
    """Return the list of available legal topics."""
    return jsonify(get_topics_list())


@app.route("/search_law", methods=["GET"])
def search_law_route():
    """
    Search the laws database by keyword/abbreviation.

    Query parameters:
      q   - search query (required)
      n   - max number of results (optional, default 5, max 20)

    Returns a JSON list of matching law objects.
    """
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    try:
        n = min(int(request.args.get("n", 5)), 20)
    except ValueError:
        n = 5
    results = search_law(query, max_results=n)
    return jsonify([_build_law_response(law) for law in results])


@app.route("/laws", methods=["GET"])
def list_laws():
    """
    Return all laws in the database.

    Optional query parameter:
      category - filter by category (case-insensitive)
    """
    category_filter = (request.args.get("category") or "").strip().lower()
    all_laws = get_all_laws()
    if category_filter:
        all_laws = [law for law in all_laws if law.get("category", "").lower() == category_filter]
    return jsonify([_build_law_response(law) for law in all_laws])


@app.route("/kanoon_search", methods=["GET"])
def kanoon_search_route():
    """
    Search the Kanoon index (10 000+ Indian laws) by keyword.

    Query parameters:
      q   - search query (required)
      n   - max number of results (optional, default 10, max 50)

    Returns a JSON list of matching Kanoon law objects.
    """
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    try:
        n = min(int(request.args.get("n", 10)), 50)
    except ValueError:
        n = 10
    results = search_kanoon(query, max_results=n)
    return jsonify([_build_kanoon_response(r) for r in results])


@app.route("/kanoon_stats", methods=["GET"])
def kanoon_stats():
    """Return count of entries in the Kanoon index."""
    from laws_database import load_kanoon_database
    return jsonify({"count": len(load_kanoon_database())})


@app.route("/law_categories", methods=["GET"])
def list_law_categories():
    """Return the list of law categories in the database."""
    return jsonify(get_law_categories())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
