from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Usa la API Key de Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ MODELO CORRECTO Y ACTIVO
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

app = FastAPI()

# ✅ Permite que tu web se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    response = model.generate_content(data.message)
    return {"reply": response.text}

