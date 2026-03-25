# 📧 AI Email Assistant

An intelligent full-stack application that classifies email priority and generates smart replies using Machine Learning and LLMs.

---

## 🚀 Features

- 🧠 Email Priority Classification (ML + Rule-based Hybrid)
- 🤖 AI-generated Smart Replies (LLM integration via Groq)
- 🎨 Clean and responsive UI
- 📜 Email History (stored locally)
- 📋 Copy-to-clipboard replies
- ⚡ Real-time API interaction with FastAPI backend

---

## 🧱 Tech Stack

### Backend
- FastAPI
- Scikit-learn
- Python

### Frontend
- HTML
- CSS
- JavaScript

### AI / ML
- TF-IDF Vectorization
- Logistic Regression / Naive Bayes
- Hybrid rule-based system
- LLM (Groq - LLaMA 3)

---

## 📂 Project Structure

```
AI Email Assistant/
│
├── backend/
│   ├── app.py
│   ├── model/
│   ├── data/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── model/
├── data/
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/ai-email-assistant.git
cd ai-email-assistant
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Add API Key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4️⃣ Run Backend

```
uvicorn backend.app:app --reload
```

---

### 5️⃣ Run Frontend

Open:

```
frontend/index.html
```

---

## 🧠 How It Works

1. User inputs email
2. Text is preprocessed and vectorized
3. ML model predicts priority
4. Rule-based system enhances prediction
5. LLM generates smart replies
6. Results displayed in UI

---

## 📊 Sample Output

- Priority: CRITICAL
- Replies:
  - Immediate response with action steps
  - Technical resolution acknowledgment
  - Follow-up communication

---

## 🎯 Future Improvements

- 🌙 Dark mode
- ⚛️ React frontend
- 📊 Email analytics dashboard
- 🔐 Authentication system
- ☁️ Deployment (Vercel / Render)

---

## 👨‍💻 Author

**Syed Arsh Ahmed**

---

## ⭐ If you like this project, give it a star!