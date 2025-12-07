from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# ✅ API Key desde Render (NO desde GitHub)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# ✅ CORS PARA QUE TU WEB PUEDA ACCEDER AL BOT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego si querés se puede limitar solo a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    # ✅ ÚNICO MODELO QUE FUNCIONA CON TU SDK ACTUAL
    model = genai.GenerativeModel("models/gemini-1.0-pro")
    response = model.generate_content(data.message)
    return {"reply": response.text}
