
import os

from src.Procesamiento.gestor_datos import GestorDatos
from src.Procesamiento.exportacion import Exportador
from src.Util.cronometro import Cronometro


# Directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas de los datasets
DATASET_TXT = os.path.join(
    BASE_DIR,
    "datasets",
    "dataset_1000_duplicados.txt"
)

DATASET_XLSX = os.path.join(
    BASE_DIR,
    "datasets",
    "dataset_5000_duplicados.xlsx"
)

# Directorio de resultados
DIRECTORIO_RESULTADOS = os.path.join(
    BASE_DIR,
    "Resultados"
)


def mostrar_menu():

    print("\n======================================")
    print(" SISTEMA DE PROCESAMIENTO DE DATOS")
    print("======================================")

    print("1. Cargar dataset de 1,000 registros")
    print("2. Cargar dataset de 5,000 registros")
    print("3. Mostrar primeros 20 elementos")
    print("4. Mostrar últimos 20 elementos")
    print("5. Mostrar total de registros")
    print("6. Mostrar información del dataset")
    print("7. Limpiar datos")
    print("8. Exportar resultados")
    print("0. Salir")

    print("======================================")


def exportar_resultados(
    gestor,
    cronometro,
    tiempo_carga
):

    if not gestor.hay_datos():

        print("\nNo hay datos para exportar.")
        return

    print("\n--- EXPORTAR RESULTADOS ---")
    print("1. Archivo TXT")
    print("2. Archivo XLSX")
    print("0. Cancelar")

    opcion = input("Selecciona un formato: ").strip()

    if opcion == "0":
        return

    elif opcion == "1":
        extension = ".txt"

    elif opcion == "2":
        extension = ".xlsx"

    else:
        print("\nFormato no válido.")
        return

    # Obtener nombre del archivo original
    nombre_original = gestor.obtener_archivo()

    nombre_base = os.path.splitext(nombre_original)[0]

    # Generar nombre del resultado
    nombre_salida = (
        nombre_base + "_exportado" + extension
    )

    ruta = os.path.join(
        DIRECTORIO_RESULTADOS,
        nombre_salida
    )

    # Recuperar datos de la lista enlazada
    datos = gestor.obtener_datos()

    # Exportar y medir tiempo de ejecución
    archivos, tiempo_exportacion = cronometro.ejecutar(
        Exportador.exportar,
        datos,
        ruta,
        archivo_origen=nombre_original,
        tiempo_carga=tiempo_carga
    )

    print("\nExportación realizada correctamente.")

    print("Archivos generados:")

    for archivo in archivos:
        print("-", archivo)

    print("Total de registros:", len(datos))

    print(
        "Tiempo de exportación:",
        cronometro.formatear(tiempo_exportacion)
    )


def main():

    gestor = GestorDatos()
    cronometro = Cronometro()

    tiempo_carga = None

    while True:

        mostrar_menu()

        opcion = input("Selecciona una opción: ").strip()

        try:

            # Cargar archivos
            if opcion in ("1", "2"):

                if opcion == "1":
                    ruta = DATASET_TXT
                else:
                    ruta = DATASET_XLSX

                cantidad, tiempo_carga = cronometro.ejecutar(
                    gestor.cargar_archivo,
                    ruta
                )

                print("\nArchivo cargado correctamente.")
                print("Archivo:", gestor.obtener_archivo())
                print("Total de registros:", cantidad)

                print(
                    "Tiempo de carga:",
                    cronometro.formatear(tiempo_carga)
                )

            # Mostrar primeros 20 elementos
            elif opcion == "3":

                if gestor.hay_datos():

                    print("\nPrimeros 20 elementos:")
                    print(gestor.primeros())

                else:
                    print("\nNo hay datos cargados.")

            # Mostrar últimos 20 elementos
            elif opcion == "4":

                if gestor.hay_datos():

                    print("\nÚltimos 20 elementos:")
                    print(gestor.ultimos())

                else:
                    print("\nNo hay datos cargados.")

            # Mostrar cantidad
            elif opcion == "5":

                print(
                    "\nTotal de registros:",
                    gestor.cantidad()
                )

            # Mostrar información del dataset
            elif opcion == "6":

                if gestor.hay_datos():

                    print("\n--- INFORMACIÓN DEL DATASET ---")
                    print("Archivo:", gestor.obtener_archivo())
                    print("Registros:", gestor.cantidad())
                    print("Estructura: Lista enlazada")
                    print("Estado: Datos cargados")

                    if tiempo_carga is not None:

                        print(
                            "Tiempo de carga:",
                            cronometro.formatear(tiempo_carga)
                        )

                else:
                    print("\nNo hay datos cargados.")

            # Limpiar datos
            elif opcion == "7":

                gestor.limpiar()
                cronometro.reiniciar()

                tiempo_carga = None

                print("\nDatos eliminados de la memoria.")

            # Exportar resultados
            elif opcion == "8":

                exportar_resultados(
                    gestor,
                    cronometro,
                    tiempo_carga
                )

            # Salir del sistema
            elif opcion == "0":

                print("\nFinalizando programa...")
                break

            else:

                print("\nOpción no válida.")

        except (OSError, ValueError) as error:

            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
