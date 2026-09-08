import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_scam(text: str = Form(...)):
    # Simple Mock AI Logic for Testing/Demo
    low_text = text.lower()
    
    scam_keywords = ["lottery", "urgent", "bank", "otp", "account", "won", "winner", "link", "click"]
    is_scam = any(word in low_text for word in scam_keywords) or len(text) < 5

    if is_scam:
        return {
            "risk_score": 92,
            "verdict": "HIGH RISK - SCAM",
            "reasons": [
                "Contains suspicious promotional words or urgency.",
                "Unverified link or request for sensitive actions.",
                "Common pattern seen in phishing attacks."
            ],
            "action_plan": [
                "Do not click on any links provided in the message.",
                "Never share your OTP or banking details.",
                "Block and report the sender immediately."
            ]
        }
    else:
        return {
            "risk_score": 15,
            "verdict": "LOW RISK - SAFE",
            "reasons": [
                "No typical scam phrases detected.",
                "Normal conversation format."
            ],
            "action_plan": [
                "Message looks safe, but always remain cautious of unknown senders."
            ]
        }