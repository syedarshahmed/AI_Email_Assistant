from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    return {"message": "AI Email Assistant API is running 🚀"}


# Priority endpoint
@app.post("/priority")
def get_priority(email: EmailRequest):
    result = hybrid_predict(email.subject, email.body)
    return {
        "priority": result["final_priority"],
        "confidence": float(result["final_confidence"])
    }


# Reply endpoint
@app.post("/reply")
def get_reply(email: EmailRequest):
    priority_result = hybrid_predict(email.subject, email.body)
    priority = priority_result["final_priority"]

    replies = generate_reply(email.subject, email.body, priority)

    return {
        "priority": priority,
        "replies": replies
    }