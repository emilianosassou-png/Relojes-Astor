from pathlib import Path
from uuid import uuid4

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

import database

app = Flask(__name__)
UPLOAD_FOLDER = Path(app.root_path) / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

database.inicializar_base_datos()

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def guardar_imagen():
    archivo = request.files.get("imagen")
    if not archivo or not archivo.filename:
        return None

    extension = Path(secure_filename(archivo.filename)).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        abort(400, description="Formato de imagen no permitido.")

    encabezado = archivo.stream.read(12)
    archivo.stream.seek(0)
    imagen_valida = (
        (extension in {".jpg", ".jpeg"} and encabezado.startswith(b"\xff\xd8\xff"))
        or (extension == ".png" and encabezado.startswith(b"\x89PNG\r\n\x1a\n"))
        or (extension == ".gif" and encabezado.startswith((b"GIF87a", b"GIF89a")))
        or (
            extension == ".webp"
            and encabezado.startswith(b"RIFF")
            and encabezado[8:12] == b"WEBP"
        )
    )
    if not imagen_valida:
        abort(400, description="El archivo seleccionado no es una imagen válida.")

    nombre_archivo = f"{uuid4().hex}{extension}"
    archivo.save(UPLOAD_FOLDER / nombre_archivo)
    return nombre_archivo


def eliminar_archivo_imagen(nombre_archivo):
    if nombre_archivo:
        (UPLOAD_FOLDER / nombre_archivo).unlink(missing_ok=True)


@app.route("/")
def inicio():
    relojes = database.obtener_relojes()
    return render_template("index.html", relojes=relojes)


@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    marca = request.form["marca"]
    precio = float(request.form["precio"])
    stock = int(request.form["stock"])
    categoria = request.form["categoria"]
    descripcion = request.form["descripcion"]
    imagen = guardar_imagen()

    database.agregar_reloj(
        nombre,
        marca,
        precio,
        stock,
        categoria,
        descripcion,
        imagen
    )

    return redirect(url_for("inicio"))


@app.route("/editar/<int:id_reloj>", methods=["POST"])
def editar(id_reloj):
    reloj = database.obtener_reloj(id_reloj)
    if reloj is None:
        abort(404)

    nombre = request.form["nombre"]
    marca = request.form["marca"]
    precio = float(request.form["precio"])
    stock = int(request.form["stock"])
    categoria = request.form["categoria"]
    descripcion = request.form["descripcion"]
    imagen = guardar_imagen()

    database.modificar_reloj(
        id_reloj,
        nombre,
        marca,
        precio,
        stock,
        categoria,
        descripcion,
        imagen
    )

    if imagen:
        eliminar_archivo_imagen(reloj["imagen"])

    return redirect(url_for("inicio"))


@app.route("/eliminar/<int:id_reloj>", methods=["POST"])
def eliminar(id_reloj):
    reloj = database.obtener_reloj(id_reloj)
    database.eliminar_reloj(id_reloj)
    if reloj is not None:
        eliminar_archivo_imagen(reloj["imagen"])

    return redirect(url_for("inicio"))


@app.route("/uploads/<path:nombre_archivo>")
def archivo_subido(nombre_archivo):
    return send_from_directory(UPLOAD_FOLDER, nombre_archivo)


@app.route("/api/relojes")
def api_relojes():
    relojes = database.obtener_relojes()

    resultado = []

    for reloj in relojes:
        resultado.append({
            "id": reloj["id"],
            "nombre": reloj["nombre"],
            "marca": reloj["marca"],
            "precio": reloj["precio"],
            "stock": reloj["stock"],
            "categoria": reloj["categoria"],
            "descripcion": reloj["descripcion"],
            "imagen": (
                url_for("archivo_subido", nombre_archivo=reloj["imagen"])
                if reloj["imagen"]
                else None
            ),
        })

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)