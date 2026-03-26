from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.classifier import load_model

model, vectorizer, encoder = load_model()

# Import your existing functions
from model.hybrid import hybrid_predict
from model.reply_generator import generate_reply

app = FastAPI()

# ✅ ADD THIS RIGHT AFTER app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],   # VERY IMPORTANT
    allow_headers=["*"],   # VERY IMPORTANT
)


# Request schema (VERY IMPORTANT)
class EmailRequest(BaseModel):
    subject: str
    body: str


# Root endpoint (test)
@app.get("/")
def home():
    return {"message": "AI Email Assistant API is running"}


# Priority endpoint
@app.post("/priority")
def get_priority(email: EmailRequest):
    priority = hybrid_predict(email.subject, email.body, model, vectorizer, encoder)
    return {
    "priority": priority
        }


# Reply endpoint
@app.post("/reply")
def get_reply(email: EmailRequest):
    priority = hybrid_predict(email.subject, email.body, model, vectorizer, encoder)

    reply = generate_reply(email.subject, email.body, priority)

    return {
    "priority": priority,
    "reply": reply   # IMPORTANT: singular
    }
