
from pathlib import Path
from flask import Blueprint, jsonify, request

from Backend.autenticacion import requiere_autenticacion

from src.Procesamiento.gestor_datos import GestorDatos

from src.Ordenamientos.gestor_ordenamientos import (
    GestorOrdenamientos
)

from src.Busquedas.gestor_busquedas import GestorBusquedas

from src.Util.cronometro import Cronometro

from tempfile import TemporaryDirectory
from io import BytesIO
from flask import send_file

from src.Procesamiento.exportacion import Exportador

from src.Ordenamientos.ordenamiento_externo import (
    OrdenamientoExterno
)

api = Blueprint("api", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent

DATASETS = {
    "txt": BASE_DIR / "datasets" /
           "dataset_1000_duplicados.txt",

    "xlsx": BASE_DIR / "datasets" /
            "dataset_5000_duplicados.xlsx"
}

ALGORITMOS = {
    "Bubble Sort": "1",
    "Selection Sort": "2",
    "Insertion Sort": "3",
    "Shell Sort": "4",
    "Quick Sort": "5",
    "Merge Sort": "6",
    "Radix Sort": "7",
    "Heap Sort": "8"
}

BUSQUEDAS = {
    "Secuencial": "1",
    "Binaria": "2",
    "Hash": "3"
}


def datos_validos(datos):

    return (
        isinstance(datos, list)
        and 0 < len(datos) <= 5000
        and all(
            type(numero) is int
            and abs(numero) <= 9007199254740991
            for numero in datos
        )
    )


# ESTADO DEL SERVIDOR

@api.get("/estado")
def estado():

    return jsonify({
        "estado": "activo",
        "backend": "Python Flask"
    })


# CARGAR DATASET

@api.get("/datasets/<formato>")
@requiere_autenticacion
def cargar_dataset(formato):

    if formato not in DATASETS:

        return jsonify({
            "error": "Formato no permitido"
        }), 400

    ruta = DATASETS[formato]

    if not ruta.is_file():

        return jsonify({
            "error": "Dataset no encontrado"
        }), 404

    try:

        gestor = GestorDatos()
        cronometro = Cronometro()

        cantidad, tiempo = cronometro.ejecutar(
            gestor.cargar_archivo,
            str(ruta)
        )

        datos = gestor.obtener_datos()

        if not datos_validos(datos):

            return jsonify({
                "error": "Dataset fuera de los limites permitidos"
            }), 400

        return jsonify({
            "archivo": ruta.name,
            "cantidad": cantidad,
            "datos": datos,
            "tiempo": tiempo
        })

    except (ValueError, OSError):

        return jsonify({
            "error": "No se pudo cargar el dataset"
        }), 400


# ORDENAMIENTO INTERNO

@api.post("/ordenar")
@requiere_autenticacion
def ordenar():

    contenido = request.get_json(silent=True)

    if not isinstance(contenido, dict):

        return jsonify({
            "error": "Solicitud invalida"
        }), 400

    datos = contenido.get("datos", [])
    algoritmo = contenido.get("algoritmo")
    orden = contenido.get("orden", "asc")

    if not datos_validos(datos):

        return jsonify({
            "error": "Datos invalidos"
        }), 400

    if (
        not isinstance(algoritmo, str)
        or algoritmo not in ALGORITMOS
    ):

        return jsonify({
            "error": "Algoritmo no valido"
        }), 400

    if orden not in ("asc", "desc"):

        return jsonify({
            "error": "Orden no valido"
        }), 400

    try:

        gestor = GestorOrdenamientos()

        resultado = gestor.ordenar(
            datos,
            ALGORITMOS[algoritmo],
            ascendente=(orden == "asc")
        )

        return jsonify({
            "datos": resultado.datos,
            "algoritmo": resultado.algoritmo,
            "orden": resultado.orden,
            "cantidad": len(resultado.datos),
            "tiempo": resultado.tiempo
        })

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# BUSQUEDAS

@api.post("/buscar")
@requiere_autenticacion
def buscar():

    contenido = request.get_json(silent=True)

    if not isinstance(contenido, dict):

        return jsonify({
            "error": "Solicitud invalida"
        }), 400

    datos = contenido.get("datos", [])
    metodo = contenido.get("metodo")
    valor = contenido.get("valor")

    if not datos_validos(datos):

        return jsonify({
            "error": "Datos invalidos"
        }), 400

    if (
        not isinstance(metodo, str)
        or metodo not in BUSQUEDAS
    ):

        return jsonify({
            "error": "Metodo no valido"
        }), 400

    if (
        type(valor) is not int
        or abs(valor) > 9007199254740991
    ):

        return jsonify({
            "error": "Introduce un numero entero valido"
        }), 400

    try:

        gestor_datos = GestorDatos()
        gestor_datos.actualizar(datos)

        gestor_busquedas = GestorBusquedas()

        resultado = gestor_busquedas.buscar(
            gestor_datos,
            BUSQUEDAS[metodo],
            valor
        )

        return jsonify({
            "metodo": resultado.metodo,
            "valor": resultado.valor,
            "posiciones": resultado.posiciones,
            "coincidencias": resultado.coincidencias,
            "tiempo": resultado.tiempo,
            "tiempo_preparacion":
                resultado.tiempo_preparacion,
            "tiempo_indice":
                resultado.tiempo_indice
        })

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400
        
        
# ========================================
# ORDENAMIENTO EXTERNO
# ========================================

@api.post("/externo")
@requiere_autenticacion
def externo():

    contenido = request.get_json(silent=True)

    if not isinstance(contenido, dict):
        return jsonify({
            "error": "Solicitud invalida."
        }), 400

    formato = contenido.get("formato")
    bloque = contenido.get("bloque", 1000)
    orden = contenido.get("orden", "asc")

    if (
        not isinstance(formato, str)
        or formato not in DATASETS
    ):
        return jsonify({
            "error": "Dataset no valido."
        }), 400

    if type(bloque) is not int or not 1 <= bloque <= 5000:
        return jsonify({
            "error": "Tamano de bloque invalido."
        }), 400

    if orden not in ("asc", "desc"):
        return jsonify({
            "error": "Orden no valido."
        }), 400

    origen = DATASETS[formato]

    if not origen.is_file():
        return jsonify({
            "error": "Dataset no encontrado."
        }), 404

    try:

        with TemporaryDirectory() as temporal:

            salida = Path(temporal) / "resultado.txt"

            resultado = OrdenamientoExterno.ordenar(
                str(origen),
                str(salida),
                tamano_bloque=bloque,
                ascendente=(orden == "asc")
            )

            datos = [
                int(linea.strip())
                for linea in salida.read_text(
                    encoding="utf-8"
                ).splitlines()
                if linea.strip()
            ]

            return jsonify({
                "algoritmo": resultado.algoritmo,
                "orden": resultado.orden,
                "cantidad": resultado.cantidad,
                "bloques": resultado.bloques,
                "pasadas": resultado.pasadas,
                "tamano_bloque": resultado.tamano_bloque,
                "tiempo": resultado.tiempo,
                "datos": datos
            })

    except (ValueError, OSError):

        return jsonify({
            "error": "No se pudo completar el ordenamiento externo."
        }), 400


# ========================================
# COMPARACION DE RENDIMIENTO
# ========================================

@api.post("/rendimiento")
@requiere_autenticacion
def rendimiento():

    contenido = request.get_json(silent=True)

    if not isinstance(contenido, dict):
        return jsonify({
            "error": "Solicitud invalida."
        }), 400

    datos = contenido.get("datos", [])
    orden = contenido.get("orden", "asc")

    if not datos_validos(datos):
        return jsonify({
            "error": "Carga un dataset valido."
        }), 400

    if orden not in ("asc", "desc"):
        return jsonify({
            "error": "Orden no valido."
        }), 400

    try:

        gestor = GestorOrdenamientos()

        resultados = []

        for nombre, opcion in ALGORITMOS.items():

            resultado = gestor.ordenar(
                datos.copy(),
                opcion,
                ascendente=(orden == "asc")
            )

            resultados.append({
                "algoritmo": nombre,
                "cantidad": len(datos),
                "tiempo": resultado.tiempo
            })

        return jsonify({
            "resultados": resultados
        })

    except ValueError:

        return jsonify({
            "error": "No se pudo comparar los algoritmos."
        }), 400


# ========================================
# EXPORTACIONES TXT Y XLSX
# ========================================

@api.post("/exportar")
@requiere_autenticacion
def exportar():

    contenido = request.get_json(silent=True)

    if not isinstance(contenido, dict):
        return jsonify({
            "error": "Solicitud invalida."
        }), 400

    datos = contenido.get("datos", [])
    formato = contenido.get("formato", "txt")

    if not datos_validos(datos):
        return jsonify({
            "error": "No hay datos validos para exportar."
        }), 400

    if formato not in ("txt", "xlsx"):
        return jsonify({
            "error": "Formato no permitido."
        }), 400

    try:

        with TemporaryDirectory() as temporal:

            nombre = f"resultado.{formato}"

            ruta = Path(temporal) / nombre

            Exportador.exportar(
                datos,
                str(ruta),
                archivo_origen="DataProcess Web"
            )

            archivo = BytesIO(ruta.read_bytes())

        mime = (
            "text/plain"
            if formato == "txt"
            else "application/vnd.openxmlformats-"
                 "officedocument.spreadsheetml.sheet"
        )

        return send_file(
            archivo,
            mimetype=mime,
            as_attachment=True,
            download_name=nombre
        )

    except (ValueError, OSError):

        return jsonify({
            "error": "No se pudo generar el archivo."
        }), 400

