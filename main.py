from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Lee la API Key desde Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Modelo correcto que sí funciona
model = genai.GenerativeModel("models/text-bison-001")

app = FastAPI()

# ✅ Permitir conexión desde tu web
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

