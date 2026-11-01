def validar_recibo(datos):
    """Devuelve (es_valido, avisos)."""
    avisos = []

    if not isinstance(datos, dict):
        return False, ["La respuesta no es un diccionario"]

    for campo in ["comercio", "fecha", "total", "items"]:
        if campo not in datos:
            return False, [f"Falta el campo {campo}"]

    if datos["comercio"] is None:
        return False, ["No se pudo leer el comercio"]

    if datos["total"] is None:
        return False, ["No se pudo leer el total"]

    if not isinstance(datos["items"], list):
        return False, ["Los ítems no son una lista"]

    suma = 0
    for item in datos["items"]:
        if item.get("precio") is not None:
            suma += item["precio"]

    diferencia = suma - datos["total"]
    if diferencia != 0:
        avisos.append(
            f"Los ítems suman {suma} y el total es {datos['total']} "
            f"(diferencia: {diferencia}, posibles descuentos)"
        )

    return True, avisos


if __name__ == "__main__":
    print(validar_recibo({"comercio": None, "fecha": "2026-10-14", "total": 500, "items": []}))
    print(validar_recibo({"comercio": "Jumbo", "fecha": "2026-10-14", "total": 500, "items": []}))