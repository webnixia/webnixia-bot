from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Lee la API desde Render
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "WEBNIXIA BOT ONLINE ✅"}

@app.post("/chat")
async def chat(data: Chat):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-002")
        response = model.generate_content(data.message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"❌ Error interno IA: {str(e)}"}



