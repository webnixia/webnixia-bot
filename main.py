from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ CARGA CORRECTA DE API KEY DESDE RENDER
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# ✅ CORS TOTAL PARA QUE TU WEB SE PUEDA CONECTAR
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # podés restringir después
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(data.message)
    return {"reply": response.text}

