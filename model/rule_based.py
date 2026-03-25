# model/rule_based.py

# ─────────────────────────────────────
# Keyword rules for each priority level
# ─────────────────────────────────────

CRITICAL_KEYWORDS = [
    "down", "outage", "crashed", "breach", "hacked", "compromised",
    "emergency", "critical", "urgent", "immediate", "lawsuit", "legal action",
    "data loss", "system failure", "not working", "offline", "unreachable",
    "security", "attack", "virus", "ransomware", "exposed","unauthorized", "access attempt", "intrusion"
]

HIGH_KEYWORDS = [
    "overdue", "refund", "complaint", "disappointed", "unacceptable",
    "escalate", "threatening", "cancel", "frustrated", "demand",
    "invoice", "payment", "late fee", "unresponsive", "issue", "problem",
    "dissatisfied", "angry", "terrible", "horrible"
]

MEDIUM_KEYWORDS = [
    "meeting", "schedule", "call", "discuss", "follow up", "update",
    "reminder", "timesheet", "deadline", "collaboration", "proposal",
    "question", "clarify", "feedback", "review"
]

LOW_KEYWORDS = [
    "newsletter", "sale", "discount", "offer", "promotion", "deal",
    "unsubscribe", "digest", "weekly", "monthly", "roundup", "follow",
    "highlights", "tips", "announcement", "fyi", "update"
]


def check_keywords(text, keywords):
    """Count how many keywords appear in the text"""
    text = text.lower()
    matches = [kw for kw in keywords if kw in text]
    return len(matches), matches


def rule_based_predict(subject, body):
    """
    Predict priority using keyword rules.
    Returns priority and confidence score.
    """
    text = subject.lower() + " " + body.lower()

    # Count keyword matches per priority
    critical_count, critical_matches = check_keywords(text, CRITICAL_KEYWORDS)
    high_count,     high_matches     = check_keywords(text, HIGH_KEYWORDS)
    medium_count,   medium_matches   = check_keywords(text, MEDIUM_KEYWORDS)
    low_count,      low_matches      = check_keywords(text, LOW_KEYWORDS)

    scores = {
        "CRITICAL" : critical_count,
        "HIGH"     : high_count,
        "MEDIUM"   : medium_count,
        "LOW"      : low_count
    }

    matches = {
        "CRITICAL" : critical_matches,
        "HIGH"     : high_matches,
        "MEDIUM"   : medium_matches,
        "LOW"      : low_matches
    }

    # Get priority with highest score
    top_priority = max(scores, key=scores.get)
    top_score    = scores[top_priority]

    # If no keywords matched at all
    if top_score == 0:
        return None, 0.0, {}

    # Calculate confidence (0.0 to 1.0)
    total_matches = sum(scores.values())
    confidence    = round(top_score / total_matches, 2)

    return top_priority, confidence, matches


def print_rule_result(subject, priority, confidence, matches):
    """Pretty print the rule based result"""
    if priority is None:
        print(f"\n📧 Subject : {subject}")
        print(f"⚠️  No keyword matches found — passing to ML model")
        return

    print(f"\n📧 Subject    : {subject}")
    print(f"🎯 Priority   : {priority}")
    print(f"📊 Confidence : {confidence * 100:.1f}%")
    print(f"🔑 Matched Keywords : {matches[priority]}")