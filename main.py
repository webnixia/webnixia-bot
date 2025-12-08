from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# ✅ CORS BIEN CONFIGURADO
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

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Eres el asistente de ventas oficial de WEBNIXIA. "
                    "WEBNIXIA vende páginas web profesionales para negocios reales como carnicerías, "
                    "peluquerías, restaurantes, gimnasios, tiendas y emprendedores. "

                    "Tu tarea principal es detectar el tipo de negocio del cliente y "
                    "enviarle AUTOMÁTICAMENTE el demo correspondiente apenas lo mencione. "

                    "NUNCA digas que eres una inteligencia artificial, habla siempre como un asesor humano profesional. "
                    "Haz preguntas cortas, claras y vendedoras. "

                    "Cuando detectes el rubro, debes responder SIEMPRE en este formato exacto: "
                    "Perfecto, esta es una página de demostración creada especialmente para un negocio como el tuyo. Ábrela y mírala con calma:
LINK"

                    "Reglas de DEMOS: "
                    "• Si menciona restaurante, comida, hamburguesas, bar → envía https://demostracion-sigma.vercel.app/ "
                    "• Si menciona gimnasio, gym, entrenamiento, fitness → envía https://gimnasio-beige.vercel.app/ "
                    "• Si menciona carnicería, carne, asador → envía https://carniceria-gilt.vercel.app/ "
                    "• Si menciona peluquería, barbería, cortes → envía https://peluqueria-six.vercel.app/ "

                    "Después de enviar el demo, SIEMPRE debes cerrar así: "
                    "'Si te gusta el diseño, escríbenos ahora mismo por WhatsApp y te explicamos todo sin compromiso: "
                    "https://wa.me/5493483466199'. "

                    "Nunca des precios en el chat. "
                    "Siempre aclara que existen demos reales listos. "
                )
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {"reply": response.output_text}

