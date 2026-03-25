# app.py

import os
import sys
from data.data_loader import load_data, prepare_data, get_features_and_labels
from data.text_processor import preprocess_all, vectorize
from model.classifier import train_model, save_model
from model.hybrid import hybrid_predict, print_hybrid_result
from tests.tests_hybrid import run_tests


def train_pipeline():
    """Full training pipeline"""
    print("\n🚀 Starting Training Pipeline...")

    df                       = load_data("data/emails.csv")
    df, encoder              = prepare_data(df)
    X_raw, y                 = get_features_and_labels(df)
    X_cleaned                = preprocess_all(X_raw)
    X_vectorized, vectorizer = vectorize(X_cleaned)
    model                    = train_model(X_vectorized, y)
    save_model(model, vectorizer, encoder)

    print("✅ Training pipeline complete\n")


def predict_single(subject, body):
    """Predict priority for a single email"""
    result = hybrid_predict(subject, body)
    print_hybrid_result(result)
    return result


def interactive_mode():
    """Let user type emails and get predictions"""
    print("\n" + "="*55)
    print("📬 INTERACTIVE MODE — Type an email to classify")
    print("="*55)
    print("Type 'quit' to exit\n")

    while True:
        subject = input("📧 Subject : ").strip()
        if subject.lower() == "quit":
            print("👋 Goodbye!")
            break

        body = input("📝 Body    : ").strip()
        if body.lower() == "quit":
            print("👋 Goodbye!")
            break

        result = hybrid_predict(subject, body)
        print_hybrid_result(result)
        print()


if __name__ == "__main__":

    # Step 1: Train
    train_pipeline()

    # Step 2: Run Tests
    accuracy = run_tests()

    # Step 3: Interactive mode if tests pass
    if accuracy >= 70:
        print("\n✅ System ready for use!")
        interactive_mode()
    else:
        print(f"\n⚠️  Accuracy {accuracy}% is below threshold. Retrain with more data.")