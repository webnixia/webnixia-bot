from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Lee la API Key correctamente desde Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Webnixia Bot Activo ✅"}

@app.post("/chat")
def chat(data: Chat):
    try:
        # ✅ MODELO CORRECTO Y ESTABLE
        model = genai.GenerativeModel("models/text-bison-001")
        response = model.generate_content(data.message)

        return {"reply": response.text}

    except Exception as e:
        return {"error": str(e)}

