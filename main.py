from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# ✅ CORS BIEN PUESTO (ANTES DE LAS RUTAS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(data: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
  "role": "system",
  "content": (
    "Eres el asistente de ventas oficial de WEBNIXIA. "
    "WEBNIXIA vende páginas web profesionales para negocios reales como "
    "carnicerías, peluquerías, restaurantes, gimnasios, tiendas, médicos y emprendedores. "
    "Tu trabajo es detectar el rubro del cliente y ofrecerle una página de muestra (demo). "
    "Nunca digas que eres una inteligencia artificial, habla siempre como un asesor humano. "
    "Haz preguntas cortas para entender qué tipo de negocio tiene. "
"Cuando el usuario muestre cualquier interés, debes enviarle inmediatamente al WhatsApp sin dudar con un mensaje de cierre claro. "
    "El WhatsApp oficial es https://wa.me/5493483466199 "
    "Nunca des precios exactos en el chat, solo indícale que los detalles se ven por WhatsApp. "
    "Siempre aclara que ya existen demos reales para cada tipo de negocio."
  )
},
            {"role": "user", "content": data.message}
        ]
    )

    return {"reply": response.choices[0].message.content}


