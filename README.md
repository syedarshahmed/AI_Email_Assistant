# MailMind — AI Email Assistant

An intelligent email classification and smart reply generation system built with Python, Machine Learning, and LLM integration.

---

## What It Does

- **Classifies email priority** — CRITICAL, HIGH, MEDIUM, LOW
- **Hybrid Intelligence** — combines Rule Based + ML model for accurate results
- **Generates smart replies** — powered by Groq LLM (Llama 3)
- **Clean web interface** — dark themed frontend with history tracking

---

## Project Structure

```
AI Email Assistant/
│
├── data/
│   ├── emails.csv              # 200 email training dataset
│   ├── data_loader.py          # loads and prepares data
│   └── text_processor.py       # cleans and vectorizes text
│
├── model/
│   ├── classifier.py           # trains logistic regression model
│   ├── rule_based.py           # keyword based priority rules
│   ├── predictor.py            # ML prediction function
│   ├── hybrid.py               # combines rule based + ML
│   ├── reply_generator.py      # Groq LLM reply generation
│   ├── model.pkl               # saved trained model
│   ├── vectorizer.pkl          # saved TF-IDF vectorizer
│   └── encoder.pkl             # saved label encoder
│
├── tests/
│   └── test_hybrid.py          # test suite for hybrid system
│
├── apps.py                     # FastAPI backend
├── main.py                     # model training pipeline
├── index.html                  # frontend UI
├── requirements.txt            # dependencies
├── .env                        # API keys (not committed)
└── .gitignore
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| ML Model | Logistic Regression (scikit-learn) |
| Text Processing | TF-IDF, NLTK |
| Hybrid System | Rule Based + ML |
| LLM | Groq API (Llama 3) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML, CSS, JavaScript |

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-email-assistant.git
cd ai-email-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download NLTK data
```python
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com)

---

## Running the Project

### Step 1 — Train the model
```bash
python3 main.py
```

### Step 2 — Start the backend
```bash
uvicorn apps:app --reload
```

### Step 3 — Open the frontend
```bash
open index.html
```

Backend runs at: `http://127.0.0.1:8000`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/priority` | Returns email priority + confidence |
| POST | `/reply` | Returns priority + generated reply |

### Example Request
```json
POST /reply
{
  "subject": "Server is down",
  "body": "Our production server crashed. All users affected."
}
```

### Example Response
```json
{
  "priority": "CRITICAL",
  "replies": "We have received your report and treated this as a critical incident..."
}
```

---

## How the Hybrid System Works

```
Email Input
    ↓
Rule Based System    → checks for priority keywords
    ↓
Confident? → use rule result
Not sure?  → pass to ML Model
    ↓
ML Model             → Logistic Regression on TF-IDF features
    ↓
Final Priority + Confidence Score
    ↓
Groq LLM             → generates smart reply based on priority
```

---

## Model Performance

| Class | Precision | Recall | F1 Score |
|---|---|---|---|
| CRITICAL | 1.00 | 0.98 | 0.99 |
| HIGH | 0.98 | 1.00 | 0.99 |
| LOW | 1.00 | 1.00 | 1.00 |
| MEDIUM | 1.00 | 1.00 | 1.00 |
| **Overall** | **1.00** | **0.99** | **0.99** |

Trained on 200 emails — 50 per priority class.

---
