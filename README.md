# MailMind — AI Email Intelligence

> Classify email priority instantly. Generate smart replies automatically.

---

## Overview

MailMind is a full-stack AI-powered email assistant that combines machine learning, rule-based intelligence, and large language models to classify emails by priority and generate context-aware replies — all in real time.

Built from scratch: custom dataset, lightweight NLP pipeline, hybrid ML system, LLM integration, REST API, and a polished dark-themed frontend.

---

## Features

- **Priority Classification** — Classifies emails into CRITICAL, HIGH, MEDIUM, or LOW using a hybrid ML + rule-based engine
- **Smart Reply Generation** — Generates tone-adjusted replies via Groq API (Llama 3.3 70B)
- **Hybrid Intelligence** — Rule-based system runs first; ML model takes over when confidence is low
- **Session History** — Stores last 5 analyzed emails locally for quick reference
- **Responsive UI** — Works seamlessly on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| ML Model | Logistic Regression (scikit-learn) |
| NLP | Regex cleaning + TF-IDF Vectorization (scikit-learn) |
| LLM | Groq API — Llama 3.3 70B |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render (backend) · Vercel (frontend) |

---


## Project Structure

```
MailMind/
│
├── data/
│   ├── emails.csv              # 1200-email training dataset
│   ├── data_loader.py          # Data loading & preparation
│   └── text_processor.py       # Regex cleaning + TF-IDF pipeline
│
├── model/
│   ├── classifier.py           # ML model training
│   ├── rule_based.py           # Keyword-based rule engine
│   ├── predictor.py            # ML prediction with probability map
│   ├── hybrid.py               # Hybrid intelligence system
│   └── reply_generator.py      # Groq LLM reply generation
│
├── frontend/
│    ├── index.html                  # Frontend UI
│    ├── style.css                   # Styles & animations
│    └── script.js                   # Frontend logic
│
├── saved/
│   ├── model.pkl               # Trained classifier
│   ├── vectorizer.pkl          # TF-IDF vectorizer
│   └── encoder.pkl             # Label encoder
│
├── apps.py                     # FastAPI backend
└── main.py                     # Training pipeline entry point

```

---

## How It Works

### 1. Hybrid Classification Engine

```
Email Input
    │
    ▼
Rule-Based System ──► Confidence > 60%? ──► YES ──► Use Rule Result
    │
    │ NO
    ▼
ML Prediction ──► Both Agree? ──► YES ──► Combine Scores
    │
    │ NO
    ▼
ML Override (final decision)
```

Four decision methods: `RULE` · `ML` · `BOTH` · `ML_OVERRIDE`

### 2. Reply Tone by Priority

| Priority | Reply Tone |
|---|---|
| 🔴 CRITICAL | Urgent, immediate action steps |
| 🟠 HIGH | Clear resolution plan |
| 🟡 MEDIUM | Helpful and friendly |
| 🟢 LOW | Brief and polite |

---

## API Reference

Base URL: `https://ai-email-assistant-4ms9.onrender.com/docs`

### `POST /priority`
Returns the predicted priority and confidence score.

**Request**
```json
{
  "subject": "Server is down",
  "body": "Production database is unreachable since 3AM."
}
```

**Response**
```json
{
  "priority": "CRITICAL",
  "confidence": 0.97,
  "method": "BOTH"
}
```

---

### `POST /reply`
Returns the predicted priority and a generated smart reply.

**Request**
```json
{
  "subject": "Invoice overdue",
  "body": "Your invoice #1042 is 30 days past due."
}
```

**Response**
```json
{
  "priority": "HIGH",
  "reply": "Thank you for reaching out. I'll review invoice #1042 immediately and arrange payment within 24 hours..."
}
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/syedarshahmed/AI_Email_Assistant.git

cd AI_Email_Assistant

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY=your_key_here

# Train the model
python main.py

# Start the backend
uvicorn apps:app --reload
```

Then open `index.html` in your browser or serve it with any static file server.

---

## Model Performance

| Metric | Value |
|---|---|
| Training emails | 1,200 |
| Priority classes | 4 |
| Model accuracy | 99.5% |
| Test cases | 20 |
| Dataset versions | 4 (7 → 24 → 200 → 1200) |

---

## Deployment

| Service | Purpose | URL |
|---|---|---|
| Render (free tier) | FastAPI backend | `https://ai-email-assistant-4ms9.onrender.com` |
| Vercel | Frontend | `https://ai-email-assistant-nu.vercel.app` |
> **Note:** Render's free tier spins down after inactivity. The first request may take 30–60 seconds to wake the server.

---

## Roadmap

- [ ] Multi-language email support
- [ ] Outlook / Gmail browser extension
- [ ] User authentication & email history sync
- [ ] Fine-tuned LLM for reply generation
- [ ] Confidence score visualization in UI

---

<p align="center">Built with 🤖 ML · ⚡ FastAPI · ✦ GroqAI</p>