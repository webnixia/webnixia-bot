from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyBOd_7ezHiL1j_h2cLBTtJ23SBwYHykdGM"))

app = FastAPI()

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(data.message)
    return {"reply": response.text}
