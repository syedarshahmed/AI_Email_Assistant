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

@app.get("/debug/env")
def debug_env():
    return {
        "client_id":     CLIENT_ID[:10] + "..." if CLIENT_ID else "MISSING",
        "client_secret": CLIENT_SECRET[:5] + "..." if CLIENT_SECRET else "MISSING",
        "redirect_uri":  REDIRECT_URI or "MISSING"
    }


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
    # 1. Check auth
    if "user" not in token_store:
        raise HTTPException(
            status_code=401,
            detail="Gmail not connected. Please visit /auth/login first."
        )

    # 2. Classify + generate reply
    priority = hybrid_predict(req.subject, req.body, model, vectorizer, encoder)
    reply    = generate_reply(req.subject, req.body, priority)

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
        scopes        = data["scopes"],
    )

    # 5. Call Gmail API → create draft
    service  = build("gmail", "v1", credentials=creds)
    draft    = service.users().drafts().create(
        userId  = "me",
        body    = {"message": {"raw": raw_message}},
    ).execute()

    return {
        "success":  True,
        "draft_id": draft.get("id"),
        "priority": priority,
        "reply":    reply,
    }


