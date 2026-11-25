
from pathlib import Path

from flask import Flask, send_from_directory
from dotenv import load_dotenv

from Backend.api import api


BASE_DIR = Path(__file__).resolve().parent.parent

WEB_DIR = BASE_DIR / "Web"

load_dotenv(BASE_DIR / ".env")

app = Flask(
    __name__,
    static_folder=None
)

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

app.register_blueprint(
    api,
    url_prefix="/api"
)


@app.get("/")
def inicio():

    return send_from_directory(
        WEB_DIR,
        "index.html"
    )


@app.get("/<pagina>.html")
def pagina_web(pagina):

    return send_from_directory(
        WEB_DIR,
        f"{pagina}.html"
    )


@app.get("/css/<path:archivo>")
def estilos(archivo):

    return send_from_directory(
        WEB_DIR / "css",
        archivo
    )


@app.get("/js/<path:archivo>")
def javascript(archivo):

    return send_from_directory(
        WEB_DIR / "js",
        archivo
    )


@app.get("/img/<path:archivo>")
def imagenes(archivo):

    return send_from_directory(
        WEB_DIR / "img",
        archivo
    )


@app.after_request
def seguridad(respuesta):

    respuesta.headers["X-Content-Type-Options"] = "nosniff"

    respuesta.headers["X-Frame-Options"] = "DENY"

    respuesta.headers["Referrer-Policy"] = "no-referrer"

    respuesta.headers["Cache-Control"] = "no-store"

    return respuesta


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
