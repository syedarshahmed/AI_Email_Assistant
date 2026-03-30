const API_URL = "https://ai-email-assistant-4ms9.onrender.com";
let currentReply = "";
let currentSubject = "";
let gmailConnected = false;

/* ===========================
   RIPPLE EFFECT ON BUTTON
=========================== */
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('analyzeBtn');
  if (btn) {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      btn.style.setProperty('--x', `${x}%`);
      btn.style.setProperty('--y', `${y}%`);
    });
  }
  loadHistory();
  checkGmailStatus();
});


/* ===========================
   ANALYZE EMAIL
=========================== */
async function analyzeEmail() {
  const subject   = document.getElementById("subject").value.trim();
  const body      = document.getElementById("body").value.trim();
  const resultDiv = document.getElementById("result");
  const button    = document.getElementById("analyzeBtn");
  const btnText   = document.getElementById("btnText");

  const API_URL = "https://ai-email-assistant-4ms9.onrender.com";

  // Reset borders
  document.getElementById("subject").style.border = "";
  document.getElementById("body").style.border    = "";

  if (!subject && !body) {
    resultDiv.innerHTML = `<div class="warn-msg">⚠️ Please enter a subject or email body.</div>`;
    document.getElementById("subject").style.border = "1px solid var(--high)";
    document.getElementById("body").style.border    = "1px solid var(--high)";

    // Shake the inputs
    ['subject', 'body'].forEach(id => {
      const el = document.getElementById(id);
      el.style.animation = 'none';
      requestAnimationFrame(() => {
        el.style.animation = 'shakeField 0.4s ease';
      });
      setTimeout(() => { el.style.animation = ''; }, 500);
    });
    return;
  }

  // Loading state
  resultDiv.innerHTML = `
    <div class="loading-msg">
      <div class="spinner"></div>
      <span class="loading-text">Analyzing email with AI</span>
      <span class="loading-dots"></span>
    </div>`;

  button.disabled = true;
  btnText.textContent = "Processing...";
  startLoadingDots();

  try {
    const response = await fetch(`${API_URL}/reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject, body })
    });

    const data = await response.json();
    const reply = data.reply || "No reply generated";

    saveToHistory(subject, body, data.priority, reply);
    loadHistory();

    // Small delay to feel snappier
    await delay(200);
    currentReply = reply;
    currentSubject = subject;
    renderResult(data.priority, reply);

  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = `<div class="error-msg">❌ ${error.message}</div>`;
  }

  button.disabled = false;
  btnText.textContent = "Analyze Email";
}


/* ===========================
   RENDER RESULT
=========================== */
function renderResult(priority, reply) {
  const resultDiv = document.getElementById("result");
  const p = (priority || "MEDIUM").toUpperCase();

  const priorityIcons = {
    CRITICAL: '🔴',
    HIGH:     '🟠',
    MEDIUM:   '🟡',
    LOW:      '🟢',
  };

  resultDiv.innerHTML = `
    <div class="result-content">
      <div class="priority-row">
        <span class="priority-badge badge-${p}">
          <span class="priority-dot"></span>
          ${p} PRIORITY
        </span>
        <span class="priority-emoji">${priorityIcons[p] || ''}</span>
      </div>
      <div>
        <div class="reply-label">// suggested reply</div>
        <div class="reply-box" id="replyText">
          <button class="copy-btn" onclick="copyReplies()">Copy</button>
          ${reply}
        </div>
        <p class="copy-status" id="copyStatus"></p>
        <button class="draft-btn" onclick="openDraftModal()">✦ Save as Draft in Gmail</button>
      </div>
    </div>`;
}


/* ===========================
   COPY REPLY
=========================== */
function copyReplies() {
  const text = document.getElementById("replyText").innerText.replace("Copy", "").trim();

  navigator.clipboard.writeText(text)
    .then(() => {
      const status = document.getElementById("copyStatus");
      const btn    = document.querySelector(".copy-btn");

      if (status) status.innerText = "✓ Copied to clipboard";
      if (btn) {
        btn.textContent = "Copied!";
        btn.style.color = "var(--low)";
        btn.style.borderColor = "var(--low-border)";
        btn.style.background = "var(--low-bg)";
      }

      setTimeout(() => {
        if (status) status.innerText = "";
        const b = document.querySelector(".copy-btn");
        if (b) {
          b.textContent = "Copy";
          b.style.color = "";
          b.style.borderColor = "";
          b.style.background = "";
        }
      }, 2000);
    })
    .catch(() => {
      const status = document.getElementById("copyStatus");
      if (status) status.innerText = "✕ Failed to copy";
    });
}


/* ===========================
   HISTORY
=========================== */
function saveToHistory(subject, body, priority, reply) {
  const history = JSON.parse(localStorage.getItem("emailHistory")) || [];

  history.unshift({
    subject, body, priority, reply,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });

  if (history.length > 5) history.pop();
  localStorage.setItem("emailHistory", JSON.stringify(history));
}


function loadHistory() {
  const historyDiv = document.getElementById("history");
  if (!historyDiv) return;

  const history = JSON.parse(localStorage.getItem("emailHistory")) || [];
  historyDiv.innerHTML = "";

  if (history.length === 0) {
    historyDiv.innerHTML = `<p class="history-empty">No history yet — analyze an email to get started.</p>`;
    return;
  }

  history.forEach((item, i) => {
    const p = (item.priority || "MEDIUM").toUpperCase();

    const div = document.createElement("div");
    div.className = "history-item";
    div.style.animationDelay = `${i * 0.06}s`;

    div.innerHTML = `
      <div class="history-subject">${item.subject || "(no subject)"}</div>
      <div>
        <span class="priority-badge badge-${p}" style="font-size:0.62rem;padding:4px 10px;">
          <span class="priority-dot"></span>${p}
        </span>
      </div>
      <div class="history-meta">${item.time || ""}</div>
    `;

    div.onclick = () => {
      document.getElementById("subject").value = item.subject || "";
      document.getElementById("body").value    = item.body    || "";
      renderResult(item.priority, item.reply);

      // Scroll to top on mobile
      if (window.innerWidth < 768) {
        document.querySelector('.main-grid')?.scrollIntoView({ behavior: 'smooth' });
      }
    };

    historyDiv.appendChild(div);
  });
}


function clearHistory() {
  localStorage.removeItem("emailHistory");
  loadHistory();

  document.getElementById("result").innerHTML = `
    <div class="empty-state">
      <div class="empty-icon-wrap">
        <svg class="empty-star" width="40" height="40" viewBox="0 0 20 20" fill="none">
          <path d="M10 2L12.5 7.5L18 8.5L14 12.5L15 18L10 15.5L5 18L6 12.5L2 8.5L7.5 7.5L10 2Z" stroke="currentColor" stroke-width="1" fill="none"/>
        </svg>
      </div>
      <p class="empty-title">History cleared</p>
      <span class="empty-sub">Analyze a new email to get started</span>
    </div>`;
}


/* ===========================
   HELPERS
=========================== */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let dotsInterval = null;
function startLoadingDots() {
  clearInterval(dotsInterval);
  const el = document.querySelector('.loading-dots');
  if (!el) return;
  let n = 0;
  dotsInterval = setInterval(() => {
    if (!document.querySelector('.loading-dots')) { clearInterval(dotsInterval); return; }
    el.textContent = '.'.repeat((n % 3) + 1);
    n++;
  }, 400);
}

/* ===========================
   SHAKE KEYFRAME (injected)
=========================== */
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes shakeField {
    0%   { transform: translateX(0); }
    20%  { transform: translateX(-6px); }
    40%  { transform: translateX(5px); }
    60%  { transform: translateX(-4px); }
    80%  { transform: translateX(3px); }
    100% { transform: translateX(0); }
  }
  .priority-row {
    display: flex; align-items: center; gap: 10px;
  }
  .priority-emoji {
    font-size: 1.1rem;
    animation: emojiPop 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
  }
  @keyframes emojiPop {
    from { transform: scale(0) rotate(-20deg); opacity: 0; }
    to   { transform: scale(1) rotate(0deg);   opacity: 1; }
  }
`;
document.head.appendChild(shakeStyle);



/* ===========================
   GMAIL CONNECT
=========================== */
async function handleGmailConnect() {
  if (gmailConnected) return;
  window.location.href = `${API_URL}/auth/login`;
}

async function checkGmailStatus() {
  try {
    const res = await fetch(`${API_URL}/auth/status`);
    const data = await res.json();
    gmailConnected = data.connected;
    const btn = document.getElementById("gmailBtn");
    const txt = document.getElementById("gmailBtnText");
    if (gmailConnected) {
      btn.classList.add("connected");
      txt.textContent = "✓ Gmail Connected";
    }
  } catch (e) { console.error("Status check failed", e); }
}

/* ===========================
   DRAFT MODAL
=========================== */
function openDraftModal() {
  if (!gmailConnected) {
    alert("Please connect your Gmail account first.");
    return;
  }
  document.getElementById("modalSubject").textContent = `Re: ${currentSubject}`;
  document.getElementById("modalPreview").textContent = currentReply;
  document.getElementById("modalTo").value = "";
  document.getElementById("modalOverlay").classList.add("active");
}

function closeModal() {
  document.getElementById("modalOverlay").classList.remove("active");
}

async function submitDraft() {
  const to = document.getElementById("modalTo").value.trim();
  if (!to) {
    document.getElementById("modalTo").style.borderColor = "var(--critical)";
    return;
  }

  const sendBtn = document.getElementById("modalSendBtn");
  const sendText = document.getElementById("modalSendText");
  sendBtn.disabled = true;
  sendText.textContent = "Saving...";

  try {
    const res = await fetch(`${API_URL}/draft`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject: currentSubject, body: document.getElementById("body").value, to })
    });
    const data = await res.json();
    if (data.success) {
      closeModal();
      const status = document.getElementById("copyStatus");
      if (status) {
        status.textContent = "✓ Draft saved to Gmail!";
        setTimeout(() => { status.textContent = ""; }, 3000);
      }
    }
  } catch (e) {
    sendText.textContent = "Failed — try again";
  }

  sendBtn.disabled = false;
  sendText.textContent = "Save Draft to Gmail";
}




