import sqlite3

DATABASE = "relojes.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_base_datos():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS relojes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            imagen TEXT
        )
    """)

    columnas = {
        fila["name"]
        for fila in conexion.execute("PRAGMA table_info(relojes)").fetchall()
    }
    if "imagen" not in columnas:
        conexion.execute("ALTER TABLE relojes ADD COLUMN imagen TEXT")

    conexion.commit()

    cantidad = conexion.execute(
        "SELECT COUNT(*) FROM relojes"
    ).fetchone()[0]

    if cantidad == 0:
        relojes_iniciales = [
            (
                "Classic Silver",
                "Casio",
                85000,
                8,
                "Analógico",
                "Reloj clásico con correa metálica."
            ),
            (
                "Sport Black",
                "Q&Q",
                65000,
                12,
                "Deportivo",
                "Reloj deportivo resistente y moderno."
            ),
            (
                "Elegance Gold",
                "Fossil",
                150000,
                5,
                "Elegante",
                "Reloj elegante con detalles dorados."
            )
        ]

        conexion.executemany("""
            INSERT INTO relojes
            (nombre, marca, precio, stock, categoria, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, relojes_iniciales)

        conexion.commit()

    conexion.close()


def obtener_relojes():
    conexion = conectar()
    relojes = conexion.execute(
        "SELECT * FROM relojes ORDER BY id DESC"
    ).fetchall()
    conexion.close()

    return relojes


def obtener_reloj(id_reloj):
    conexion = conectar()

    reloj = conexion.execute(
        "SELECT * FROM relojes WHERE id = ?",
        (id_reloj,)
    ).fetchone()

    conexion.close()

    return reloj


def agregar_reloj(nombre, marca, precio, stock, categoria, descripcion, imagen=None):
    conexion = conectar()

    conexion.execute("""
        INSERT INTO relojes
        (nombre, marca, precio, stock, categoria, descripcion, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, marca, precio, stock, categoria, descripcion, imagen))

    conexion.commit()
    conexion.close()


def modificar_reloj(
    id_reloj,
    nombre,
    marca,
    precio,
    stock,
    categoria,
    descripcion,
    imagen=None
):
    conexion = conectar()

    conexion.execute("""
        UPDATE relojes
        SET nombre = ?,
            marca = ?,
            precio = ?,
            stock = ?,
            categoria = ?,
            descripcion = ?,
            imagen = COALESCE(?, imagen)
        WHERE id = ?
    """, (
        nombre,
        marca,
        precio,
        stock,
        categoria,
        descripcion,
        imagen,
        id_reloj
    ))

    conexion.commit()
    conexion.close()


def eliminar_reloj(id_reloj):
    conexion = conectar()

    conexion.execute(
        "DELETE FROM relojes WHERE id = ?",
        (id_reloj,)
    )

    conexion.commit()
    conexion.close()