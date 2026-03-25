# model/predictor.py

from data.text_processor import clean_text
from model.classifier import load_model

# Load model ONCE at module level
model, vectorizer, encoder = load_model()


def predict_with_ml(subject, body):
    """Predict email priority using the trained ML model."""

    # Combine subject + body
    text = subject + " " + body

    # Clean text
    cleaned = clean_text(text)

    # Vectorize
    X = vectorizer.transform([cleaned])

    # Predict
    prediction    = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    # Decode label
    priority   = encoder.inverse_transform([prediction])[0]
    confidence = round(max(probabilities) * 100, 2)

    # Full probability map
    prob_map = {
        label: round(prob * 100, 2)
        for label, prob in zip(encoder.classes_, probabilities)
    }

    return priority, confidence, prob_map


def print_ml_result(subject, priority, confidence, prob_map):
    """Pretty print the ML prediction result"""

    print(f"\n📧 Subject      : {subject}")
    print(f"🤖 ML Priority  : {priority}")
    print(f"📊 Confidence   : {confidence}%")
    print("\n📈 All Probabilities:")
    for label, prob in sorted(prob_map.items(), key=lambda x: -x[1]):
        bar = "█" * int(prob / 5)
        print(f"   {label:<10} {bar:<20} {prob}%")