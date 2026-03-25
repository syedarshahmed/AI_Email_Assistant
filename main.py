# main.py

from data.data_loader import load_data, prepare_data, get_features_and_labels
from data.text_processor import preprocess_all, vectorize
from model.classifier import train_model, evaluate_model, save_model
from model.hybrid import hybrid_predict, print_hybrid_result
from model.reply_generator import generate_reply, print_reply


# function to integrate
def full_email_analysis(subject, body):
    email_text = subject + " " + body

    # Priority
    priority_result = hybrid_predict(subject, body)
    priority = priority_result["final_priority"]

    # Replies
    replies = generate_reply(subject, body, priority)

    return priority, replies

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
# Test Reply Generator
# ─────────────────────────────────────
print("\n" + "="*60)
print("🚀 FULL AI EMAIL ASSISTANT SYSTEM")
print("="*60)


test_emails = [
    (
        "Production server is down",
        "Our server crashed and all users are affected. Emergency fix needed immediately.",
        "CRITICAL"
    ),
    (
        "Can we schedule a meeting?",
        "Hi I would love to discuss a potential collaboration. Are you free for a call this week?",
        "MEDIUM"
    ),
    (
        "Flash sale this weekend",
        "Get 50 percent off everything this Saturday and Sunday. Do not miss out.",
        "LOW"
    ),
]

for subject, body, _ in test_emails:

    priority, replies = full_email_analysis(subject, body)

    print("\n" + "="*55)
    print(f"📧 Subject  : {subject}")
    print(f"🎯 Priority : {priority}")
    print("-" * 55)

    if isinstance(replies, str):
        print(replies)
    else:
        for i, r in enumerate(replies, 1):
            print(f"{i}. {r}")

    print("\nBest regards,\nTeam Support")  
    print("="*55)

