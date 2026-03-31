from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from model.classifier import load_model
from model.hybrid import hybrid_predict
from model.reply_generator import generate_reply

import os
import base64
from email.mime.text import MIMEText
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

load_dotenv()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# ── Load ML model ────────────────────────────────────────────────
model, vectorizer, encoder = load_model()

# ── Google OAuth config ──────────────────────────────────────────
CLIENT_ID      = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET  = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI   = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES         = ["https://www.googleapis.com/auth/gmail.compose"]

# In-memory token store  (swap for a DB in production)
token_store: dict = {}

# ── App setup ────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request schemas ──────────────────────────────────────────────
class EmailRequest(BaseModel):
    subject: str
    body: str

class DraftRequest(BaseModel):
    subject: str
    body: str
    to: str                  # recipient email address

# ── Existing endpoints ───────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "AI Email Assistant API is running"}


@app.post("/priority")
def get_priority(email: EmailRequest):
    priority = hybrid_predict(email.subject, email.body, model, vectorizer, encoder)
    return {"priority": priority}


@app.post("/reply")
def get_reply(email: EmailRequest):
    priority = hybrid_predict(email.subject, email.body, model, vectorizer, encoder)
    reply    = generate_reply(email.subject, email.body, priority)
    return {"priority": priority, "reply": reply}


# ── OAuth endpoints ──────────────────────────────────────────
@app.get("/auth/login")
def auth_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id":     CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                "token_uri":     "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.code_verifier = ""
    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    token_store["oauth_state"] = state
    return RedirectResponse(auth_url)


@app.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id":     CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                "token_uri":     "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.code_verifier = ""
    flow.fetch_token(code=code)
    creds = flow.credentials

    token_store["user"] = {
        "token":         creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri":     creds.token_uri,
        "client_id":     creds.client_id,
        "client_secret": creds.client_secret,
        "scopes":        list(creds.scopes) if creds.scopes else SCOPES,
    }

    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://your-vercel-url.vercel.app")
    return RedirectResponse(f"{FRONTEND_URL}?gmail=connected")

@app.get("/auth/status")
def auth_status():
    """Check whether the user has already connected Gmail."""
    connected = "user" in token_store
    return {"connected": connected}


# ── Draft injection endpoint ─────────────────────────────────────
@app.post("/draft")
def create_draft(req: DraftRequest):
    """
    Full pipeline:
      1. Run hybrid priority classifier
      2. Generate tone-adjusted reply via Groq
      3. Inject reply as a Gmail draft via Gmail API
    Returns the draft ID so the frontend can confirm success.
    """
    try:  # 1. Check auth
        if "user" not in token_store:
         raise HTTPException(
            status_code=401,
            detail="Gmail not connected. Please visit /auth/login first."
        )

        # 2. Classify + generate reply
        priority = hybrid_predict(req.subject, req.body, model, vectorizer, encoder)
        reply    = generate_reply(req.subject, req.body, priority)
        if isinstance(reply, list):
            reply = " ".join(reply)

        # 3. Build MIME message
        mime_msg              = MIMEText(reply)
        mime_msg["to"]        = req.to
        mime_msg["subject"]   = f"Re: {req.subject}"
        raw_message           = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()

        # 4. Rebuild credentials from store
        data  = token_store["user"]
        creds = Credentials(
            token         = data["token"],
            refresh_token = data["refresh_token"],
            token_uri     = data["token_uri"],
            client_id     = data["client_id"],
            client_secret = data["client_secret"],
            scopes        = SCOPES,
        )

        # 5. Call Gmail API → create draft
        service  = build("gmail", "v1", credentials=creds)
        draft    = service.users().drafts().create(
            userId  = "me",
            body    = {"message": {"raw": raw_message}},
        ).execute()

        return JSONResponse({"success": True, "draft_id": draft.get("id"), "priority": priority, "reply": reply})

    except Exception as e:
        import traceback
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

from fastapi.responses import HTMLResponse

@app.get("/privacy", response_class=HTMLResponse)
def privacy_policy():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MailMind — Privacy Policy</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 60px auto; padding: 0 24px; line-height: 1.7; color: #333; }
    h1 { font-size: 2rem; margin-bottom: 8px; }
    h2 { margin-top: 32px; color: #444; }
    p, li { color: #555; }
  </style>
</head>
<body>
  <h1>MailMind Privacy Policy</h1>
  <p>Last updated: March 2026</p>
  <h2>What We Access</h2>
  <p>MailMind requests the <strong>gmail.compose</strong> scope only — to create email drafts on your behalf. We cannot read, delete, modify, or send your emails.</p>
  <h2>What We Store</h2>
  <p>We temporarily store your OAuth access token in server memory to facilitate draft creation. It is never written to a database or shared with anyone.</p>
  <h2>What We Never Do</h2>
  <ul>
    <li>Never read your emails</li>
    <li>Never send emails on your behalf</li>
    <li>Never store your email content</li>
    <li>Never sell or share your data</li>
  </ul>
  <h2>Third Party Services</h2>
  <p>MailMind uses the Groq API to generate reply suggestions. Only the email subject and body you manually paste are sent to Groq. Your Gmail data is never shared.</p>
  <h2>Revoking Access</h2>
  <p>You can revoke MailMind's Gmail access anytime at <a href="https://myaccount.google.com/permissions">Google Account Permissions</a>.</p>
  <h2>Contact</h2>
  <p>For privacy concerns: syedarsh7860@gmail.com</p>
</body>
</html>
"""


