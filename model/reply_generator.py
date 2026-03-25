# model/reply_generator.py

import os
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

print(f"✅ Groq API Key loaded: {api_key[:15]}...")

# Initialize Groq client
client = Groq(api_key=api_key)


def build_prompt(subject, body, priority, tone="professional"):
    """Build a smart prompt based on email context"""

    prompt = f"""
You are a professional email assistant.
Write a short {tone} reply to this {priority} priority email.

Subject : {subject}
Body    : {body}

Rules:
- If CRITICAL → reply with urgency and clear action steps
- If HIGH     → reply with clear resolution plan
- If MEDIUM   → reply in a helpful and friendly manner
- If LOW      → reply briefly and politely
- Sign off as "Team Support"
- Write only the reply body. Nothing else.
"""
    return prompt

def generate_reply(subject, body, priority, tone="professional"):
    """Generate 3 smart replies using Groq"""

    try:
        print("🤖 Sending request to Groq...")

        prompt = f"""
You are a professional email assistant.

Generate exactly 3 short {tone} replies.

Email Details:
Priority: {priority}
Subject: {subject}
Body: {body}

Rules:
- CRITICAL → urgent tone
- HIGH → solution-oriented
- MEDIUM → helpful and friendly
- LOW → brief and polite
- Each reply should be 1–2 lines
- Sign off as "Team Support"

Format:
1.
2.
3.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You generate professional email replies."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        reply_text = response.choices[0].message.content.strip()

        reply_text = reply_text.replace("Team Support", "").strip()

        print("✅ Reply received!")

        return reply_text

    except Exception as e:
        print(f"❌ Groq error: {e}")

        # ✅ fallback (VERY IMPORTANT)
        return [
            "We are looking into this and will get back shortly. - Team Support",
            "Thanks for the update. We’ll address this soon. - Team Support",
            "Received your email. We will respond shortly. - Team Support"
        ]


def print_reply(subject, priority, reply):
    """Pretty print the generated reply"""

    print(f"\n{'='*55}")
    print(f"📧 Subject  : {subject}")
    print(f"🎯 Priority : {priority}")
    print(f"{'─'*55}")
    if reply:
        print(f"✉️  Generated Reply:\n")
        print(reply)
    else:
        print("⚠️  No reply generated")
    print(f"{'='*55}")