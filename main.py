from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from resume_parser import extract_resume_text
from email_sender import send_email
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
resume_text = extract_resume_text()

class Question(BaseModel):
    query: str

class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str

@app.post("/ask")
def ask_question(q: Question):
    try:
        prompt = f"Based on this resume: {resume_text}\nAnswer: {q.query}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"answer": response['choices'][0]['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-email")
def send_email_endpoint(email: EmailRequest):
    try:
        send_email(email.recipient, email.subject, email.body)
        return {"status": "Email sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
