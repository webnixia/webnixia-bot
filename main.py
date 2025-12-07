from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: Chat):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=data.message
    )
    return {"reply": response.text}
