
async function analyzeEmail() {
    const subject = document.getElementById("subject").value;
    const body = document.getElementById("body").value;

    const resultDiv = document.getElementById("result");
    const button = document.getElementById("analyzeBtn");

    // 🚨 VALIDATION
    if (!subject && !body) {
        resultDiv.innerHTML = "⚠️ Please enter subject or email body.";


        document.getElementById("subject").style.border = "2px solid red";
        document.getElementById("body").style.border = "2px solid red";

        return;
    }
    // 🔥 Show loading
    resultDiv.innerHTML = "⏳ Analyzing email...";
    button.disabled = true;
    button.innerText = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/reply", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ subject, body })
        });

        const data = await response.json();

        saveToHistory(subject, body, data.priority, data.replies);
        loadHistory();

        resultDiv.innerHTML =
            `<p><strong>Priority:</strong> ${data.priority}</p>
     <p><strong>Replies:</strong></p>
     <pre id="replyText">${data.replies}</pre>
     <button onclick="copyReplies()" style="margin-top:10px;">📋 Copy Replies</button>
     <p id="copyStatus"></p>`;

    } catch (error) {
        console.error("❌ Error:", error);
        resultDiv.innerHTML = "❌ Error: " + error.message;
    }

    // 🔥 Reset button
    button.disabled = false;
    button.innerText = "Analyze Email";
}


function copyReplies() {
    const text = document.getElementById("replyText").innerText;

    navigator.clipboard.writeText(text)
        .then(() => {
            document.getElementById("copyStatus").innerText = "✅ Copied!";
        })
        .catch(err => {
            document.getElementById("copyStatus").innerText = "❌ Failed to copy";
            console.error(err);
        });
}

function saveToHistory(subject, body, priority, replies) {
    const history = JSON.parse(localStorage.getItem("emailHistory")) || [];

    history.unshift({
        subject,
        body,
        priority,
        replies
    });

    // Keep only last 5
    if (history.length > 5) history.pop();

    localStorage.setItem("emailHistory", JSON.stringify(history));
}


function loadHistory() {
    const historyDiv = document.getElementById("history");

    if (!historyDiv) return;  // 🔥 prevents crash

    const history = JSON.parse(localStorage.getItem("emailHistory")) || [];

    historyDiv.innerHTML = "";

    history.forEach((item) => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${item.subject}</strong><br>Priority: ${item.priority}`;
        historyDiv.appendChild(div);
    });
}

function clearHistory() {
    localStorage.removeItem("emailHistory");
    loadHistory();

    document.getElementById("result").innerHTML = "🗑 History cleared!";
}

// Load history on page load
window.onload = loadHistory;
