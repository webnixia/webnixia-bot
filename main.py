from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ AQUÍ VA SOLO EL NOMBRE DE LA VARIABLE
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(data.message)
    return {"reply": response.text}
