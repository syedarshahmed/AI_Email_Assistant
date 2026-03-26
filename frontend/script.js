async function analyzeEmail() {
    const subject   = document.getElementById("subject").value.trim();
    const body      = document.getElementById("body").value.trim();
    const resultDiv = document.getElementById("result");
    const button    = document.getElementById("analyzeBtn");
    const btnText   = document.getElementById("btnText");

    document.getElementById("subject").style.border = "";
    document.getElementById("body").style.border    = "";

    if (!subject && !body) {
        resultDiv.innerHTML = `<div class="warn-msg">⚠️ Please enter a subject or email body.</div>`;
        document.getElementById("subject").style.border = "1px solid var(--high)";
        document.getElementById("body").style.border    = "1px solid var(--high)";
        return;
    }

    resultDiv.innerHTML = `
        <div class="loading-msg">
            <div class="spinner"></div>
            Analyzing email with AI...
        </div>`;
    button.disabled = true;
    btnText.textContent = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/reply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ subject, body })
        });

        const data = await response.json();
        saveToHistory(subject, body, data.priority, data.replies);
        loadHistory();
        renderResult(data.priority, data.replies);

    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerHTML = `<div class="error-msg">❌ ${error.message}</div>`;
    }

    button.disabled = false;
    btnText.textContent = "Analyze Email";
}

function renderResult(priority, replies) {
    const resultDiv = document.getElementById("result");
    const p = (priority || "MEDIUM").toUpperCase();
    resultDiv.innerHTML = `
        <div class="result-content">
            <div>
                <span class="priority-badge badge-${p}">
                    <span class="priority-dot"></span>
                    ${p} PRIORITY
                </span>
            </div>
            <div>
                <div class="reply-label">// suggested reply</div>
                <div class="reply-box" id="replyText">
                    <button class="copy-btn" onclick="copyReplies()">Copy</button>${replies}
                </div>
                <p class="copy-status" id="copyStatus"></p>
            </div>
        </div>`;
}

function copyReplies() {
    const text = document.getElementById("replyText").innerText.replace("Copy", "").trim();
    navigator.clipboard.writeText(text)
        .then(() => {
            document.getElementById("copyStatus").innerText = "✅ Copied to clipboard";
            document.querySelector(".copy-btn").textContent = "Copied!";
            setTimeout(() => {
                document.getElementById("copyStatus").innerText = "";
                const btn = document.querySelector(".copy-btn");
                if (btn) btn.textContent = "Copy";
            }, 2000);
        })
        .catch(() => {
            document.getElementById("copyStatus").innerText = "❌ Failed to copy";
        });
}

function saveToHistory(subject, body, priority, replies) {
    const history = JSON.parse(localStorage.getItem("emailHistory")) || [];
    history.unshift({ subject, body, priority, replies, time: new Date().toLocaleTimeString() });
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
    history.forEach((item) => {
        const p = (item.priority || "MEDIUM").toUpperCase();
        const div = document.createElement("div");
        div.className = "history-item";
        div.innerHTML = `
            <div class="history-subject">${item.subject || "(no subject)"}</div>
            <div>
                <span class="priority-badge badge-${p}" style="font-size:0.65rem;padding:3px 10px;">
                    <span class="priority-dot"></span>${p}
                </span>
            </div>
            <div class="history-meta">${item.time || ""}</div>`;
        div.onclick = () => {
            document.getElementById("subject").value = item.subject || "";
            document.getElementById("body").value    = item.body    || "";
            renderResult(item.priority, item.replies);
        };
        historyDiv.appendChild(div);
    });
}

function clearHistory() {
    localStorage.removeItem("emailHistory");
    loadHistory();
    document.getElementById("result").innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">✦</span>
            <p>History cleared</p>
            <span>Analyze a new email to get started</span>
        </div>`;
}

window.onload = loadHistory;