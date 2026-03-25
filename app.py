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

    # 3. Keyword topic match
    topic = find_topic(message)
    if topic:
        return jsonify(_build_topic_response(topic))

    # 4. No match
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
