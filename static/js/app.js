/**
 * Legal Assistant – Frontend JavaScript
 * Features: chat, topic shortcuts, language switching, dark mode,
 *           suggestion chips, law browser (Kanoon search), char counter.
 */

(function () {
  "use strict";

  // ── Config from server ──────────────────────────────────────────────────
  const { lang: initialLang, ui: initialUi } = window.LEGAL_BOT;
  let currentLang = initialLang;
  let ui = initialUi;

  // ── DOM refs ────────────────────────────────────────────────────────────
  const chatWindow   = document.getElementById("chat-window");
  const chatForm     = document.getElementById("chat-form");
  const userInput    = document.getElementById("user-input");
  const langSelect   = document.getElementById("lang-select");
  const themeToggle  = document.getElementById("theme-toggle");
  const charCount    = document.getElementById("char-count");
  const browseInput  = document.getElementById("browse-input");
  const browseBtn    = document.getElementById("browse-btn");
  const browseResults = document.getElementById("browse-results");
  const tabBtns      = document.querySelectorAll(".tab-btn");
  const tabPanels    = document.querySelectorAll(".tab-panel");
  const chips        = document.querySelectorAll(".chip");

  // ── Dark mode ────────────────────────────────────────────────────────────

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const icon = themeToggle.querySelector(".theme-icon");
    if (icon) icon.textContent = theme === "dark" ? "☀️" : "🌙";
    try { localStorage.setItem("legal-bot-theme", theme); } catch (_) {}
  }

  function initTheme() {
    let saved;
    try { saved = localStorage.getItem("legal-bot-theme"); } catch (_) {}
    const preferred = saved ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    applyTheme(preferred);
  }

  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(current === "dark" ? "light" : "dark");
  });

  // ── Character counter ─────────────────────────────────────────────────────

  userInput.addEventListener("input", () => {
    const remaining = 500 - userInput.value.length;
    charCount.textContent = remaining;
    charCount.classList.toggle("warn", remaining < 50);
  });

  // ── Sidebar tabs ─────────────────────────────────────────────────────────

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("aria-controls");
      tabBtns.forEach(b => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      tabPanels.forEach(p => {
        p.classList.remove("active");
        p.hidden = true;
      });
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      const panel = document.getElementById(target);
      if (panel) {
        panel.classList.add("active");
        panel.hidden = false;
      }
    });
  });

  // ── Utilities ────────────────────────────────────────────────────────────

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  /** Safely encode text for display in HTML. */
  function esc(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Create and append a bot bubble; returns the inner bubble div. */
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

  // ── Render helpers ────────────────────────────────────────────────────────

  /** Build a topic card DOM element from server response data. */
  function buildTopicCard(data) {
    const card = document.createElement("div");
    card.className = "topic-card";

    const h3 = document.createElement("h3");
    h3.innerHTML = "⚖️ " + esc(data.title);
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
    const footer = document.createElement("div");
    footer.className = "law-footer";
    const lawTag = document.createElement("span");
    lawTag.className = "law-tag";
    lawTag.textContent = "📜 " + (ui.law_label || "Law") + ": " + data.law;
    footer.appendChild(lawTag);
    card.appendChild(footer);

    return card;
  }

  /** Build a law card DOM element from a structured-CSV law response. */
  function buildLawCard(data) {
    const card = document.createElement("div");
    card.className = "topic-card";

    const h3 = document.createElement("h3");
    h3.innerHTML = "📋 " + esc(data.title);
    card.appendChild(h3);

    const meta = document.createElement("p");
    meta.className = "summary";
    const parts = [];
    if (data.short_name) parts.push(data.short_name);
    if (data.year) parts.push(data.year);
    if (data.category) parts.push(data.category);
    if (data.status && data.status !== "Active") parts.push("(" + data.status + ")");
    meta.textContent = parts.join(" · ");
    card.appendChild(meta);

    const desc = document.createElement("p");
    desc.textContent = data.description;
    card.appendChild(desc);

    if (data.provisions_html) {
      const h4 = document.createElement("h4");
      h4.textContent = "Key Provisions";
      card.appendChild(h4);
      const div = document.createElement("div");
      div.innerHTML = data.provisions_html;
      card.appendChild(div);
    }

    const footer = document.createElement("div");
    footer.className = "law-footer";

    if (data.enforcing_authority) {
      const auth = document.createElement("span");
      auth.className = "law-tag";
      auth.textContent = "🏛️ " + data.enforcing_authority;
      footer.appendChild(auth);
    }
    if (data.helpline) {
      const hl = document.createElement("span");
      hl.className = "law-tag";
      hl.textContent = "📞 " + data.helpline;
      footer.appendChild(hl);
    }
    if (data.portal) {
      const pl = document.createElement("a");
      pl.className = "law-tag";
      pl.href = (data.portal.startsWith("http") ? "" : "https://") + data.portal;
      pl.target = "_blank";
      pl.rel = "noopener noreferrer";
      pl.textContent = "🌐 " + data.portal;
      footer.appendChild(pl);
    }

    if (footer.children.length > 0) card.appendChild(footer);

    return card;
  }

  /** Build a Kanoon list card from kanoon_list response. */
  function buildKanoonList(data) {
    const wrap = document.createElement("div");
    wrap.className = "kanoon-list";

    const h3 = document.createElement("h3");
    h3.textContent = "📚 " + (data.text || "Found in Indian law database:");
    wrap.appendChild(h3);

    (data.results || []).forEach(law => {
      const item = document.createElement("div");
      item.className = "kl-item";

      const title = document.createElement("div");
      title.className = "kl-title";
      title.textContent = law.title;
      item.appendChild(title);

      const meta = document.createElement("div");
      meta.className = "kl-meta";
      const metaParts = [];
      if (law.source) metaParts.push(law.source);
      if (law.place && law.place !== law.source) metaParts.push(law.place);
      if (law.published_date) metaParts.push("Published: " + law.published_date);
      meta.textContent = metaParts.join(" · ");
      item.appendChild(meta);

      if (law.url) {
        const link = document.createElement("a");
        link.className = "kl-link";
        link.href = law.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = "🔗 View on IndianKanoon";
        item.appendChild(link);
      }

      wrap.appendChild(item);
    });

    return wrap;
  }

  /** Render the server response into the chat window. */
  function renderResponse(data) {
    if (data.type === "topic") {
      appendBotBubble(buildTopicCard(data));
    } else if (data.type === "law") {
      appendBotBubble(buildLawCard(data));
    } else if (data.type === "kanoon_list") {
      appendBotBubble(buildKanoonList(data));
    } else if (data.type === "greeting" || data.type === "thanks") {
      appendBotBubble(data.text);
    } else {
      appendBotBubble(data.text || data.error || "Something went wrong.");
    }
  }

  // ── Chat send ─────────────────────────────────────────────────────────────

  async function sendMessage(text) {
    if (!text) return;
    appendUserBubble(text);
    userInput.value = "";
    charCount.textContent = "500";
    charCount.classList.remove("warn");

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

  // ── Topic shortcut buttons ───────────────────────────────────────────────

  function attachTopicButtons() {
    document.querySelectorAll(".topic-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const key   = btn.dataset.key;
        const label = btn.querySelector("span:last-child").textContent.trim();
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

  // ── Suggestion chips ─────────────────────────────────────────────────────

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      const msg = chip.dataset.msg;
      if (msg) sendMessage(msg);
    });
  });

  // ── Law browser (Kanoon search) ──────────────────────────────────────────

  async function doKanoonSearch(query) {
    if (!query.trim()) return;
    browseResults.innerHTML = '<p class="browse-hint">Searching…</p>';
    try {
      const res = await fetch(`/kanoon_search?q=${encodeURIComponent(query)}&n=15`);
      const results = await res.json();
      browseResults.innerHTML = "";
      if (!Array.isArray(results) || results.length === 0) {
        browseResults.innerHTML = '<p class="browse-hint">No laws found. Try different keywords.</p>';
        return;
      }
      results.forEach(law => {
        const card = document.createElement("div");
        card.className = "kanoon-card";

        const title = document.createElement("div");
        title.className = "kc-title";
        title.textContent = law.title;
        card.appendChild(title);

        const meta = document.createElement("div");
        meta.className = "kc-meta";
        const parts = [];
        if (law.source) parts.push(law.source);
        if (law.place && law.place !== law.source) parts.push(law.place);
        if (law.published_date) parts.push(law.published_date);
        meta.textContent = parts.join(" · ");
        card.appendChild(meta);

        if (law.url) {
          const link = document.createElement("a");
          link.className = "kc-link";
          link.href = law.url;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.innerHTML = "🔗 IndianKanoon";
          card.appendChild(link);
        }

        browseResults.appendChild(card);
      });
    } catch (err) {
      browseResults.innerHTML = '<p class="browse-hint">⚠️ Search failed. Please try again.</p>';
    }
  }

  browseBtn.addEventListener("click", () => doKanoonSearch(browseInput.value));
  browseInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      doKanoonSearch(browseInput.value);
    }
  });

  // ── Language switch ──────────────────────────────────────────────────────

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

        document.title                               = ui.title;
        document.querySelector("h1").textContent     = ui.title;
        document.querySelector(".subtitle").textContent = ui.subtitle;
        userInput.placeholder                        = ui.ask_placeholder;
        userInput.setAttribute("aria-label", ui.ask_placeholder);
        document.querySelector(".send-text").textContent = ui.send_btn;
        document.querySelector(".disclaimer").textContent = "⚠️ " + ui.disclaimer;
        document.documentElement.setAttribute("lang", newLang);

        // Update helplines
        const helplines = document.querySelectorAll(".helpline-item");
        if (helplines.length === 4) {
          helplines[0].textContent = "🚨 " + ui.emergency;
          helplines[1].textContent = "👩 " + ui.women_helpline;
          helplines[2].textContent = "👶 " + ui.child_helpline;
          helplines[3].textContent = "⚖️ " + ui.legal_aid;
        }

        appendBotBubble(ui.greeting);
      }
    } catch (err) {
      console.error("Language switch failed", err);
    }
  });

  // ── Form submit ──────────────────────────────────────────────────────────

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (text) sendMessage(text);
  });

  // ── Init ──────────────────────────────────────────────────────────────────

  function init() {
    initTheme();
    attachTopicButtons();
    appendBotBubble(ui.greeting);
    userInput.focus();
  }

  init();
})();
