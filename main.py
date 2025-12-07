from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Chat(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok", "message": "API funcionando correctamente"}

@app.post("/chat")
def chat(data: Chat):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sos el asistente de Webnixia"},
                {"role": "user", "content": data.message}
            ]
        )

        return {"reply": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
