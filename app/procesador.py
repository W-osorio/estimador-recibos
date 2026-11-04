import json
from gemini_service import analizar_recibo
from validacion import validar_recibo
from database import crear_tabla, guardar_recibos, listar_recibos, existe_recibo


def procesar_recibo(imagen_bytes, mime_type):
    crear_tabla()

    datos = analizar_recibo(imagen_bytes, mime_type)
    es_valido, avisos = validar_recibo(datos)

    if not es_valido:
        print("Recibo no válido:", avisos)
        return None
    if existe_recibo(datos["comercio"],datos["fecha"],datos["total"]):
        print("Recibo dupliado, NO se guarda")
        return None

    coincide_total = 1 if not avisos else 0

    guardar_recibos(
        datos["comercio"],
        datos["fecha"],
        datos["total"],
        json.dumps(datos["items"], ensure_ascii=False),
        coincide_total
    )
    return {"datos": datos, "avisos": avisos}


if __name__ == "__main__":
    with open("uploads/recibo_prueba.png", "rb") as archivo:
        imagen_bytes = archivo.read()

    resultado = procesar_recibo(imagen_bytes, "image/png")
    print(resultado)
    print(len(listar_recibos()), "recibos guardados")