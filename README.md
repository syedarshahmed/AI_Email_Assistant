# 📧 AI Email Assistant

An intelligent email processing system that automatically classifies emails and determines their priority using a hybrid approach combining Machine Learning and rule-based techniques.

---

## 🚀 Overview

Managing emails efficiently is a common challenge. This project provides an AI-powered solution that:

- Categorizes emails into meaningful classes  
- Detects the urgency of emails  
- Combines statistical learning with logical reasoning for better accuracy  

---

## ✨ Features

### 📂 Email Classification
- Classifies emails into:
  - Work  
  - Spam  
  - Personal  
- Built using:
  - TF-IDF vectorization  
  - Logistic Regression  

---

### ⚡ Priority Detection (Hybrid System)

#### 🔹 Rule-Based Analysis
- Detects urgency using:
  - Keywords (urgent, ASAP, deadline)  
  - Punctuation (!)  
  - Text patterns (ALL CAPS)  

#### 🔹 Machine Learning Model
- Learns contextual patterns from data  
- Uses TF-IDF + Logistic Regression  

#### 🔹 Combined Decision Logic
- Weighted scoring system:
  - Rule-based signals → 60%  
  - ML predictions → 40%  

---

## 🧠 How It Works

1. Email text is provided as input  
2. Text is preprocessed (cleaning, stopword removal)  
3. Converted into numerical features using TF-IDF  
4. Classification model predicts email category  
5. Rule-based system evaluates urgency signals  
6. ML model predicts contextual priority  
7. Final priority is determined using a hybrid scoring mechanism  

---

## 🛠 Tech Stack

- Python  
- Pandas  
- scikit-learn  
- NLTK  

---

## 📂 Project Structure

ai-email-assistant/
│
├── data/
│   ├── emails.csv
│   ├── data_loader.py
├   └── text_processor.py 
│
├── model/
│   ├── classifier.py
│   ├── predictor.py
│   ├── rule_based.py
│   ├── hybrid.py
│   └── *.pkl
│
├── main.py
├── .gitignore
└── README.md

---

## 🧪 Example

Input:
URGENT: Submit the report ASAP!

Output:
Category: Work  
Priority: HIGH 🔴

---

## ⚙️ Setup & Installation

1. Clone the repository
git clone https://github.com/your-username/AI_Email_Assistant.git
cd AI_Email_Assistant

2. Install dependencies
pip install pandas scikit-learn nltk

3. Run the project
python main.py

---

## 📈 Future Enhancements

- Smart reply generation using LLMs  
- Email summarization  
- Gmail API integration  
- Web-based interface (React + FastAPI)  

---

## 🎯 Key Highlights

- Hybrid AI system (ML + rule-based reasoning)  
- Real-world problem solving  
- Modular and scalable design  
- Clean and maintainable codebase  

---

## 👨‍💻 Author

Syed Arsh Ahmed  

---
