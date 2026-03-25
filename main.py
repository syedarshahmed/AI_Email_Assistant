# main.py

from data.data_loader import load_data, prepare_data, get_features_and_labels
from data.text_processor import preprocess_all, vectorize
from model.classifier import train_model, evaluate_model, save_model
from model.hybrid import hybrid_predict, print_hybrid_result

# Steps 1-8 stay the same
df = load_data("data/emails.csv")
df, encoder = prepare_data(df)
X_raw, y = get_features_and_labels(df)
X_cleaned = preprocess_all(X_raw)
X_vectorized, vectorizer = vectorize(X_cleaned)
model = train_model(X_vectorized, y)
evaluate_model(model, X_vectorized, y, encoder)
save_model(model, vectorizer, encoder)

# ─────────────────────────────────────
# Test Hybrid System
# ─────────────────────────────────────
print("\n" + "="*55)
print("🧠 TESTING HYBRID INTELLIGENCE SYSTEM")
print("="*55)

test_emails = [
    (
        "Production server is down",
        "Our server crashed and all users are affected. Emergency fix needed immediately."
    ),
    (
        "Invoice overdue final warning",
        "Your payment of $5000 is overdue. Legal action will follow if not paid in 48 hours."
    ),
    (
        "Can we schedule a meeting?",
        "Hi would love to discuss the project updates. Are you free for a call this week?"
    ),
    (
        "Flash sale this weekend only",
        "Get 50 percent off everything this Saturday and Sunday. Do not miss out."
    ),
    (
        "Hello there",
        "Just wanted to say hi and check in with you today."
    ),
    (
        "Something went wrong with our system",
        "Users are reporting that they cannot access their accounts since this morning."
    ),
    (
        "Unauthorized access attempt",
        "We noticed someone tried to log into your account from an unknown location."
    ),
]

for subject, body in test_emails:
    result = hybrid_predict(subject, body)
    print_hybrid_result(result)