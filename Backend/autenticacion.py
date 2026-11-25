
import os

from pathlib import Path
from functools import wraps
from flask import request, jsonify, g
from supabase import create_client
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def requiere_autenticacion(funcion):

    @wraps(funcion)
    def verificar(*args, **kwargs):

        autorizacion = request.headers.get(
            "Authorization", ""
        )

        if not autorizacion.startswith("Bearer "):
            return jsonify({
                "error": "Sesion requerida."
            }), 401

        token = autorizacion[7:].strip()

        if not token:
            return jsonify({
                "error": "Token requerido."
            }), 401

        try:

            cliente = create_client(
                os.environ["SUPABASE_URL"],
                os.environ["SUPABASE_KEY"]
            )

            respuesta = cliente.auth.get_user(token)

            if not respuesta.user:
                return jsonify({
                    "error": "Usuario no autorizado."
                }), 401

            g.usuario = respuesta.user

        except Exception:

            return jsonify({
                "error": "No se pudo validar la sesion."
            }), 401

        return funcion(*args, **kwargs)

    return verificar
