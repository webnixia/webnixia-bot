from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ CONFIGURACIÓN CORRECTA DE API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ MODELO CORRECTO Y COMPATIBLE
model = genai.GenerativeModel("models/gemini-pro")

app = FastAPI()

# ✅ PERMITIR CONEXIÓN DESDE TU WEB
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


