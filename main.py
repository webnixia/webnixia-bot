from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Cargar API Key correctamente desde Render
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "✅ WEBNIXIA BOT ACTIVO"}

@app.post("/chat")
async def chat(data: Chat):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(data.message)
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}

