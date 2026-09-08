import base64
import json
import os
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# Allow CORS for Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcode test if needed or read from env
api_key = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are ScamShield. Analyze text for scams.
Return ONLY JSON format:
{
  "risk_score": 95,
  "verdict": "HIGH RISK - SCAM",
  "reasons": ["Reason 1", "Reason 2"],
  "action_plan": ["Action 1", "Action 2"]
}
"""

@app.post("/analyze")
async def analyze_scam(text: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this message: {text}"},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}