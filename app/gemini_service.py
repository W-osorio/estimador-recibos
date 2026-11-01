import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

INSTRUCCION = """
Analiza esta imagen de un recibo o boleta. Extrae la información y
responde SOLO con un JSON válido, sin explicación adicional, con
esta estructura exacta:

{
    "comercio": "nombre del negocio",
    "fecha": "fecha en formato YYYY-MM-DD",
    "total": 44515,
    "items": [
        {"nombre": "nombre del producto", "precio": 1234}
    ]
}

Si no puedes leer algún dato con claridad, usa null en vez de inventarlo.
Responde ÚNICAMENTE el JSON, nada de texto antes o después.
"""


def limpiar_json(texto):
    texto = texto.strip()
    texto = texto.removeprefix("```json")
    texto = texto.removesuffix("```")
    return texto.strip()


def convertir_a_dict(texto):
    try:
        return json.loads(limpiar_json(texto))
    except json.JSONDecodeError:
        print("Gemini no devolvió un JSON válido")
        return None


def analizar_recibo(imagen_bytes, mime_type):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            types.Part.from_bytes(data=imagen_bytes, mime_type=mime_type),
            INSTRUCCION
        ]
    )
    if response.text is None:
        print("Gemini no devolvió texto")
        return None
    return convertir_a_dict(response.text)



if __name__ == "__main__":
    with open("uploads/recibo_prueba.png", "rb") as archivo:
        imagen_bytes = archivo.read()

    resultado = analizar_recibo(imagen_bytes, "image/png")
    print(resultado)
    from validacion import validar_recibo
    print(validar_recibo(resultado))