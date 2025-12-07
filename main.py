from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Lee la API Key desde las variables de entorno de Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    # ✅ Usar el modelo que SÍ existe en tu versión del SDK
    model = genai.GenerativeModel("models/gemini-1.0-pro")
    response = model.generate_content(data.message)
    return {"reply": response.text}
