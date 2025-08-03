from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import extract_resume_text
from email_sender import send_email
from dotenv import load_dotenv
import requests
import os
import time
from requests.exceptions import Timeout, RequestException

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY not set in .env")

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load resume text once at startup
resume_text = extract_resume_text("resume.pdf")

# Request models
class ChatRequest(BaseModel):
    question: str

class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str

# Health check
@app.get("/")
def root():
    return {"message": "✅ MCP server is running. Visit /docs to test."}

# /chat endpoint with OpenRouter API
@app.post("/chat")
def chat_with_resume(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ More stable than gemma-7b
        "messages": [
            {
                "role": "system",
                "content": f"You are a helpful resume assistant. Resume summary: {resume_text[:750]}"
            },
            {
                "role": "user",
                "content": req.question
            }
        ]
    }

    # Retry logic (up to 3 attempts)
    for attempt in range(3):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return {"response": data["choices"][0]["message"]["content"]}
        except Timeout:
            if attempt < 2:
                time.sleep(2)
                continue
            else:
                raise HTTPException(status_code=504, detail="Gateway Timeout: OpenRouter API did not respond.")
        except RequestException as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

# /send-email endpoint
@app.post("/send-email")
def send_email_endpoint(req: EmailRequest):
    try:
        send_email(req.recipient, req.subject, req.body)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
