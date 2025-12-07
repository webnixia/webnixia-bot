from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# ✅ API KEY desde Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# ✅ CORS habilitado
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
    # ✅ MODELO NUEVO QUE TU API KEY SÍ SOPORTA
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(data.message)
    return {"reply": response.text}

