from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Cargar la API Key desde Render
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ MODELO CORRECTO Y VÁLIDO ACTUAL
model = genai.GenerativeModel("models/gemini-1.5-flash")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Servidor OK"}

@app.post("/chat")
def chat(data: ChatRequest):
    response = model.generate_content(data.message)
    return {"response": response.text}

