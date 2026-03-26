/**
 * Legal Assistant – Frontend JavaScript
 * Handles chat interactions, language switching, and topic shortcuts.
 */

(function () {
  "use strict";

  // ── Config from server ──────────────────────────────────────────────────
  const { lang: initialLang, ui: initialUi, topics } = window.LEGAL_BOT;
  let currentLang = initialLang;
  let ui = initialUi;

  // ── DOM refs ────────────────────────────────────────────────────────────
  const chatWindow  = document.getElementById("chat-window");
  const chatForm    = document.getElementById("chat-form");
  const userInput   = document.getElementById("user-input");
  const langSelect  = document.getElementById("lang-select");

  // ── Utilities ───────────────────────────────────────────────────────────

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  /** Create and append a bot bubble; returns the inner content div. */
  function appendBotBubble(content) {
    const row = document.createElement("div");
    row.className = "bubble-row bot";
    row.setAttribute("role", "listitem");

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "⚖️";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (typeof content === "string") {
      bubble.innerHTML = content;
    } else {
      bubble.appendChild(content);
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    scrollToBottom();
    return bubble;
  }

  /** Create and append a user bubble. */
  function appendUserBubble(text) {
    const row = document.createElement("div");
    row.className = "bubble-row user";
    row.setAttribute("role", "listitem");

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "🧑";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    scrollToBottom();
  }

  /** Show animated typing indicator; returns a function to remove it. */
  function showTyping() {
    const row = document.createElement("div");
    row.className = "bubble-row bot";
    row.id = "typing-row";

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "⚖️";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML =
      '<div class="typing-indicator" aria-label="Thinking">' +
      "<span></span><span></span><span></span></div>";

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    scrollToBottom();

    return function removeTyping() {
      const el = document.getElementById("typing-row");
      if (el) el.remove();
    };
  }

  // ── Render helpers ──────────────────────────────────────────────────────

  /** Build a topic card DOM element from server response data. */
  function buildTopicCard(data) {
    const card = document.createElement("div");
    card.className = "topic-card";

    const h3 = document.createElement("h3");
    h3.textContent = data.title;
    card.appendChild(h3);

    const summary = document.createElement("p");
    summary.className = "summary";
    summary.textContent = data.summary;
    card.appendChild(summary);

    // Details
    const h4Details = document.createElement("h4");
    h4Details.textContent = "Key Points";
    card.appendChild(h4Details);

    const detailsDiv = document.createElement("div");
    detailsDiv.innerHTML = data.details_html;
    card.appendChild(detailsDiv);

    // Steps
    const h4Steps = document.createElement("h4");
    h4Steps.textContent = ui.steps_heading || "What You Can Do";
    card.appendChild(h4Steps);

    const stepsDiv = document.createElement("div");
    stepsDiv.innerHTML = data.steps_html;
    card.appendChild(stepsDiv);

    // Law tag
    const lawTag = document.createElement("span");
    lawTag.className = "law-tag";
    lawTag.textContent = (ui.law_label || "Law") + ": " + data.law;
    card.appendChild(lawTag);

    return card;
  }

  /** Build a law card DOM element from a CSV-database law response. */
  function buildLawCard(data) {
    const card = document.createElement("div");
    card.className = "topic-card";

    // Title row: act name + year badge
    const h3 = document.createElement("h3");
    h3.textContent = data.title;
    card.appendChild(h3);

    // Meta row: short name, category, status
    const meta = document.createElement("p");
    meta.className = "summary";
    const parts = [];
    if (data.short_name) parts.push(data.short_name);
    if (data.year) parts.push(data.year);
    if (data.category) parts.push(data.category);
    if (data.status && data.status !== "Active") parts.push("(" + data.status + ")");
    meta.textContent = parts.join(" · ");
    card.appendChild(meta);

    // Description
    const desc = document.createElement("p");
    desc.textContent = data.description;
    card.appendChild(desc);

    // Key provisions
    if (data.provisions_html) {
      const h4 = document.createElement("h4");
      h4.textContent = "Key Provisions";
      card.appendChild(h4);
      const div = document.createElement("div");
      div.innerHTML = data.provisions_html;
      card.appendChild(div);
    }

    // Footer info
    const footer = document.createElement("div");
    footer.className = "law-footer";

    if (data.enforcing_authority) {
      const auth = document.createElement("span");
      auth.className = "law-tag";
      auth.textContent = "Enforced by: " + data.enforcing_authority;
      footer.appendChild(auth);
    }
    if (data.helpline) {
      const hl = document.createElement("span");
      hl.className = "law-tag";
      hl.textContent = "Helpline: " + data.helpline;
      footer.appendChild(hl);
    }
    if (data.portal) {
      const pl = document.createElement("a");
      pl.className = "law-tag";
      pl.href = "https://" + data.portal;
      pl.target = "_blank";
      pl.rel = "noopener noreferrer";
      pl.textContent = "🌐 " + data.portal;
      footer.appendChild(pl);
    }

    if (footer.children.length > 0) card.appendChild(footer);

    return card;
  }

  /** Render the server response into the chat window. */
  function renderResponse(data) {
    if (data.type === "topic") {
      appendBotBubble(buildTopicCard(data));
    } else if (data.type === "law") {
      appendBotBubble(buildLawCard(data));
    } else if (data.type === "greeting" || data.type === "thanks") {
      appendBotBubble(data.text);
    } else {
      // unknown / error
      appendBotBubble(data.text || data.error || "Something went wrong.");
    }
  }

  // ── Chat send ───────────────────────────────────────────────────────────

  async function sendMessage(text) {
    if (!text) return;
    appendUserBubble(text);
    userInput.value = "";

    const removeTyping = showTyping();

    try {
      const res = await fetch("/chat", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ message: text, lang: currentLang }),
      });
      const data = await res.json();
      removeTyping();
      renderResponse(data);
    } catch (err) {
      removeTyping();
      appendBotBubble("⚠️ Network error. Please check your connection and try again.");
    }
  }

  // ── Topic shortcut buttons ──────────────────────────────────────────────

  function attachTopicButtons() {
    document.querySelectorAll(".topic-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const key   = btn.dataset.key;
        const label = btn.textContent.trim();
        appendUserBubble(label);

        const removeTyping = showTyping();
        try {
          const res  = await fetch(`/topic/${encodeURIComponent(key)}`);
          const data = await res.json();
          removeTyping();
          renderResponse(data);
        } catch (err) {
          removeTyping();
          appendBotBubble("⚠️ Failed to load topic. Please try again.");
        }
      });
    });
  }

  // ── Language switch ─────────────────────────────────────────────────────

  langSelect.addEventListener("change", async () => {
    const newLang = langSelect.value;
    try {
      const res  = await fetch("/set_language", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ lang: newLang }),
      });
      const data = await res.json();
      if (data.status === "ok") {
        currentLang = newLang;
        ui          = data.ui;

        // Update all UI strings in place without losing chat history
        document.title                               = ui.title;
        document.querySelector("h1").textContent     = ui.title;
        document.querySelector(".subtitle").textContent = ui.subtitle;
        userInput.placeholder                        = ui.ask_placeholder;
        userInput.setAttribute("aria-label", ui.ask_placeholder);
        document.querySelector(".send-btn").textContent = ui.send_btn;
        document.querySelector(".disclaimer").textContent = ui.disclaimer;
        document.querySelector(".sidebar-heading").textContent = ui.topics_heading;
        document.documentElement.setAttribute("lang", newLang);

        // Update helplines
        const helplines = document.querySelectorAll(".helplines span");
        if (helplines.length === 4) {
          helplines[0].textContent = ui.emergency;
          helplines[1].textContent = ui.women_helpline;
          helplines[2].textContent = ui.child_helpline;
          helplines[3].textContent = ui.legal_aid;
        }

        // Append a language-change greeting in the new language
        appendBotBubble(ui.greeting);
      }
    } catch (err) {
      console.error("Language switch failed", err);
    }
  });

  // ── Form submit ─────────────────────────────────────────────────────────

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (text) sendMessage(text);
  });

  // ── Init ─────────────────────────────────────────────────────────────────

  function init() {
    attachTopicButtons();
    // Show greeting automatically on page load
    appendBotBubble(ui.greeting);
    userInput.focus();
  }

  init();
})();
