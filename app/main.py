from fastapi import FastAPI, UploadFile
from procesador import procesar_recibo
from database import buscar_por_comercio

app = FastAPI()


@app.post("/subir")
async def subir(archivo: UploadFile):
    imagen_bytes = await archivo.read()
    resultado = procesar_recibo(imagen_bytes, archivo.content_type)

    if resultado is None:
        return {"estado": "rechazado"}
    return {"estado": "guardado", "resultado": resultado}

@app.get("/buscar")
def buscar(comercio: str):
    return buscar_por_comercio(comercio)