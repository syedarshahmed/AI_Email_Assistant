# tests/test_hybrid.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.hybrid import hybrid_predict

# ─────────────────────────────────────
# Test Cases
# ─────────────────────────────────────
TEST_CASES = [
    # (subject, body, expected_priority)

    # CRITICAL
    ("Production database is down",       "Our database crashed. All users affected. Losing revenue every minute.",           "CRITICAL"),
    ("Security breach detected",          "Unauthorized access to our servers. Customer data compromised. Act now.",           "CRITICAL"),
    ("Website completely offline",        "All services unreachable. 5000 users cannot login. Emergency response needed.",     "CRITICAL"),
    ("Ransomware attack in progress",     "Files are being encrypted right now. All staff locked out. Need help immediately.", "CRITICAL"),
    ("SSL certificate expired",           "Our SSL certificate expired. All HTTPS traffic is failing. Users getting warnings.","CRITICAL"),

    # HIGH
    ("I want a full refund now",          "Your product destroyed my data. I have contacted a lawyer. Refund me immediately.", "HIGH"),
    ("Invoice 60 days overdue",           "This is your final notice. Pay $8000 within 48 hours or we involve collections.",  "HIGH"),
    ("Client threatening to leave",       "Our biggest client is furious about the delays. They are cancelling the contract.", "HIGH"),
    ("Billing error charged twice",       "I was charged twice for my subscription. I want an immediate refund.",              "HIGH"),
    ("Wrong item delivered again",        "This is the second wrong order. I want a refund and filing a complaint.",           "HIGH"),

    # MEDIUM
    ("Can we schedule a call?",           "Hi I wanted to discuss a potential collaboration. Are you free this week?",        "MEDIUM"),
    ("Quick project status update",       "Can you give me a brief update on the project? Nothing urgent.",                   "MEDIUM"),
    ("Feedback needed on the proposal",   "We have a draft proposal ready for your review. Let us know your thoughts.",       "MEDIUM"),
    ("Timesheet reminder",                "Please submit your timesheet before end of Friday. Contact HR if questions.",       "MEDIUM"),
    ("Performance review next week",      "Your annual review is scheduled for Thursday at 2pm. Please prepare.",             "MEDIUM"),

    # LOW
    ("Weekly tech digest is here",        "Top AI tools new frameworks and a founder interview. Unsubscribe anytime.",        "LOW"),
    ("Flash sale ends tonight",           "Last chance to grab sale deals. Everything must go before midnight.",               "LOW"),
    ("New followers this week",           "You gained 47 new followers. See who is following you and grow your network.",     "LOW"),
    ("New episode just dropped",          "Our latest podcast episode is live. This week we talk about remote work.",         "LOW"),
    ("Monthly product highlights",        "Here is your monthly roundup of new features and community highlights.",           "LOW"),
]


def run_tests():
    """Run all test cases and print results"""

    print("\n" + "="*60)
    print("🧪 RUNNING TEST SUITE")
    print("="*60)

    passed  = 0
    failed  = 0
    results = []

    for subject, body, expected in TEST_CASES:
        result   = hybrid_predict(subject, body)
        got      = result["final_priority"]
        correct  = got == expected
        status   = "✅ PASS" if correct else "❌ FAIL"

        if correct:
            passed += 1
        else:
            failed += 1

        results.append({
            "subject"    : subject,
            "expected"   : expected,
            "got"        : got,
            "confidence" : result["final_confidence"],
            "method"     : result["method_used"],
            "correct"    : correct
        })

        print(f"{status} | {got:<10} (expected {expected:<10}) | {result['final_confidence']:>6}% | {result['method_used']:<12} | {subject}")

    # ─────────────────────────────────────
    # Summary
    # ─────────────────────────────────────
    total    = passed + failed
    accuracy = round(passed / total * 100, 2)

    print("\n" + "="*60)
    print(f"📊 TEST RESULTS SUMMARY")
    print("="*60)
    print(f"✅ Passed   : {passed}/{total}")
    print(f"❌ Failed   : {failed}/{total}")
    print(f"🎯 Accuracy : {accuracy}%")

    # Per class accuracy
    print("\n📈 Per Class Accuracy:")
    for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        class_tests   = [r for r in results if r["expected"] == priority]
        class_passed  = [r for r in class_tests if r["correct"]]
        class_acc     = round(len(class_passed) / len(class_tests) * 100, 2)
        bar           = "█" * int(class_acc / 10)
        print(f"   {priority:<10} {bar:<12} {class_acc}% ({len(class_passed)}/{len(class_tests)})")

    if failed > 0:
        print("\n❌ Failed Cases:")
        for r in results:
            if not r["correct"]:
                print(f"   Subject    : {r['subject']}")
                print(f"   Expected   : {r['expected']}")
                print(f"   Got        : {r['got']}")
                print(f"   Confidence : {r['confidence']}%")
                print()

    return accuracy


if __name__ == "__main__":
    run_tests()