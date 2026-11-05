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
    filas = buscar_por_comercio(comercio)
    return [
        {"id": f[0], "comercio": f[1], "fecha": f[2], "total": f[3]}
        for f in filas
    ]