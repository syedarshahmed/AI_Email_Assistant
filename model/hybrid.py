# model/hybrid.py

from model.rule_based import rule_based_predict
from model.predictor import predict_with_ml

# Confidence threshold — if rule based is above this we trust it
RULE_CONFIDENCE_THRESHOLD = 0.6


def hybrid_predict(subject, body):
    """
    Hybrid prediction system:
    1. Rule based runs first — fast and reliable for obvious emails
    2. If rule based is confident enough → use its result
    3. If not confident → pass to ML model for deeper analysis
    4. If both disagree on a close call → trust ML
    """

    # ─────────────────────────────────────
    # Step 1: Run Rule Based System
    # ─────────────────────────────────────
    rule_priority, rule_confidence, rule_matches = rule_based_predict(subject, body)

    # ─────────────────────────────────────
    # Step 2: Run ML Model
    # ─────────────────────────────────────
    ml_priority, ml_confidence, ml_prob_map = predict_with_ml(subject, body)

    # ─────────────────────────────────────
    # Step 3: Decision Logic
    # ─────────────────────────────────────

    # Case 1: No rule keywords matched → trust ML completely
    if rule_priority is None:
        final_priority   = ml_priority
        final_confidence = ml_confidence
        decision_reason  = "No keywords matched — ML model used"
        method_used      = "ML"

    # Case 2: Rule based is highly confident → trust rules
    elif rule_confidence >= RULE_CONFIDENCE_THRESHOLD:
        final_priority   = rule_priority
        final_confidence = round(rule_confidence * 100, 2)
        decision_reason  = f"Rule based highly confident ({final_confidence}%)"
        method_used      = "RULE"

    # Case 3: Both agree → use rule result with boost
    elif rule_priority == ml_priority:
        final_priority   = rule_priority
        final_confidence = round((rule_confidence * 100 + ml_confidence) / 2, 2)
        decision_reason  = "Rule based and ML agree"
        method_used      = "BOTH"

    # Case 4: They disagree and rule is not confident → trust ML
    else:
        final_priority   = ml_priority
        final_confidence = ml_confidence
        decision_reason  = f"Rule said {rule_priority} but ML overrides with higher confidence"
        method_used      = "ML OVERRIDE"

    return {
        "subject"          : subject,
        "final_priority"   : final_priority,
        "final_confidence" : final_confidence,
        "method_used"      : method_used,
        "decision_reason"  : decision_reason,
        "rule_priority"    : rule_priority,
        "rule_confidence"  : round(rule_confidence * 100, 2) if rule_priority else 0,
        "rule_matches"     : rule_matches.get(rule_priority, []) if rule_priority else [],
        "ml_priority"      : ml_priority,
        "ml_confidence"    : ml_confidence,
        "ml_probabilities" : ml_prob_map,
    }


def print_hybrid_result(result):
    """Pretty print the full hybrid result"""

    priority_icons = {
        "CRITICAL" : "🔴",
        "HIGH"     : "🟠",
        "MEDIUM"   : "🟡",
        "LOW"      : "🟢"
    }

    method_icons = {
        "RULE"        : "📏",
        "ML"          : "🤖",
        "BOTH"        : "🤝",
        "ML OVERRIDE" : "⚡"
    }

    icon   = priority_icons.get(result["final_priority"], "⚪")
    method = method_icons.get(result["method_used"], "❓")

    print(f"\n{'='*55}")
    print(f"📧 Subject       : {result['subject']}")
    print(f"{icon} Final Priority : {result['final_priority']}")
    print(f"📊 Confidence    : {result['final_confidence']}%")
    print(f"{method} Method Used   : {result['method_used']}")
    print(f"💡 Reason        : {result['decision_reason']}")
    print(f"{'─'*55}")
    print(f"📏 Rule Based    : {result['rule_priority'] or 'No match'} ({result['rule_confidence']}%)")
    if result["rule_matches"]:
        print(f"🔑 Keywords      : {result['rule_matches']}")
    print(f"🤖 ML Model      : {result['ml_priority']} ({result['ml_confidence']}%)")
    print(f"{'─'*55}")
    print("📈 ML Probabilities:")
    for label, prob in sorted(result["ml_probabilities"].items(), key=lambda x: -x[1]):
        bar = "█" * int(prob / 5)
        print(f"   {label:<10} {bar:<20} {prob}%")