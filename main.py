from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from supabase import create_client
import os

# ✅ EMAIL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ OPENAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ MODELOS
class ChatRequest(BaseModel):
    message: str

class ContactRequest(BaseModel):
    nombre: str
    email: str
    tipo: str
    mensaje: str

# ✅ SUPABASE
def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise Exception("Supabase credentials not loaded")

    return create_client(url, key)

# ✅ FUNCIÓN EMAIL AUTOMÁTICO
def enviar_email_respuesta(destinatario, nombre):
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = "✅ Recibimos tu consulta - WEBNIXIA"

    cuerpo = f"""
Hola {nombre},

✅ Recibimos correctamente tu consulta y ya estamos revisando tu solicitud.
En breve un asesor de nuestro equipo se va a contactar con vos.

Gracias por confiar en WEBNIXIA 🚀
Desarrollo web profesional
"""

    mensaje.attach(MIMEText(cuerpo, "plain"))

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, password)
    servidor.send_message(mensaje)
    servidor.quit()

# ✅ CHATBOT
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

                    "Primero debes preguntar de forma clara qué tipo de negocio quiere abrir el cliente. "

                    "Cuando el cliente mencione su rubro, debes responder de forma profesional con este estilo: "
                    "'Perfecto, esta es una página de demostración creada especialmente para un negocio como el tuyo. "
                    "Ábrela y mírala con calma:' seguido del link correspondiente. "

                    "NUNCA digas que eres una inteligencia artificial. Habla como un asesor humano profesional. "
                    "Haz preguntas cortas, claras y vendedoras. "

                    "Reglas de DEMOS: "
                    "• Restaurante, comida, hamburguesas, bar → https://demostracion-sigma.vercel.app/ "
                    "• Gimnasio, gym, entrenamiento, fitness → https://gimnasio-beige.vercel.app/ "
                    "• Carnicería, carne, asador → https://carniceria-gilt.vercel.app/ "
                    "• Peluquería, barbería, cortes → https://peluqueria-six.vercel.app/ "

                    "Después de enviar el demo, SIEMPRE debes cerrar con este mensaje exacto: "
                    "'Si te gusta el diseño, escríbenos ahora mismo por WhatsApp y te explicamos todo sin compromiso: "
                    "https://wa.me/5493483466199'. "

                    "Nunca hables de precios dentro del chat."
                )
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {"reply": response.output_text}


# ✅ FORMULARIO → SUPABASE + EMAIL AUTOMÁTICO
@app.post("/contact")
def guardar_contacto(data: ContactRequest):
    supabase = get_supabase()

    # ✅ GUARDA EN SUPABASE
    supabase.table("leads").insert({
        "nombre": data.nombre,
        "email": data.email,
        "tipo": data.tipo,
        "mensaje": data.mensaje
    }).execute()

    # ✅ ENVÍA EMAIL AUTOMÁTICO AL CLIENTE
    enviar_email_respuesta(data.email, data.nombre)

    return {"ok": True, "message": "Contacto guardado y email enviado"}
