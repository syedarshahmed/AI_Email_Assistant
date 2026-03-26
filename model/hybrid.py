def rule_based_priority(text):
    text = text.lower()

    if any(word in text for word in ["down", "crashed", "error", "urgent", "immediately"]):
        return "CRITICAL"

    if any(word in text for word in ["issue", "problem", "delay", "asap"]):
        return "HIGH"

    if any(word in text for word in ["meeting", "schedule", "discussion"]):
        return "MEDIUM"

    return "LOW"


def hybrid_predict(subject, body, model, vectorizer, encoder):
    text = subject + " " + body

    print("🔥 HYBRID RUNNING:", text)

    # Rule-based
    rule_pred = rule_based_priority(text)

    # ML-based
    X = vectorizer.transform([text])
    ml_pred = model.predict(X)[0]
    ml_label = encoder.inverse_transform([ml_pred])[0]

    # Final decision
    if rule_pred == "CRITICAL":
        return "CRITICAL"

    return ml_label