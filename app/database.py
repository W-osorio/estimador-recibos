import sqlite3

DB_PATH = "recibos.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def crear_tabla():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recibos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comercio TEXT,
            fecha TEXT,
            total REAL,
            items_json TEXT,
            coincide_total INTEGER
        )
    """)
    conn.commit()  
    conn.close()    


def guardar_recibos(comercio, fecha, total, items_json, coincide_total):
    conn = get_connection()
    conn.execute(
        "INSERT INTO recibos (comercio,fecha,total,items_json,coincide_total) VALUES (?,?,?,?,?)",
        (comercio, fecha, total, items_json, coincide_total)
    )
    conn.commit()
    conn.close()


def listar_recibos():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM recibos")
    filas = cursor.fetchall()
    conn.close()
    return filas


def buscar_por_comercio(nombre):
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM recibos WHERE comercio LIKE ?",  (f"%{nombre}%",))
    filas = cursor.fetchall()
    conn.close()
    return filas


def existe_recibo(comercio, fecha, total):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT 1 FROM recibos WHERE comercio = ? AND fecha = ? AND total = ?",
        (comercio, fecha, total),
    )
    fila = cursor.fetchone()
    conn.close()
    return fila is not None


if __name__ == "__main__":
    crear_tabla()
    #guardar_recibos("Jumbo", "2026-09-29", 8500, "[]", 1)
    print(listar_recibos())
    print(buscar_por_comercio("Jumbo"))