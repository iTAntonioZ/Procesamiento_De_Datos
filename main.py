import os

from Estructura.listas_ligadas import ListaEnlazada
from src.Procesamiento.lectura import LectorArchivos


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


def mostrar_menu():

    print("\n======================================")
    print(" SISTEMA DE PROCESAMIENTO DE DATOS")
    print("======================================")

    print("1. Cargar dataset de 1,000 registros")
    print("2. Cargar dataset de 5,000 registros")
    print("3. Mostrar primeros 20 elementos")
    print("4. Mostrar últimos 20 elementos")
    print("5. Mostrar total de registros")
    print("0. Salir")

    print("======================================")


def main():

    lista = ListaEnlazada()

    while True:

        mostrar_menu()

        opcion = input("Selecciona una opción: ").strip()

        try:

            if opcion in ("1", "2"):

                if opcion == "1":
                    ruta = DATASET_TXT
                else:
                    ruta = DATASET_XLSX

                numeros = LectorArchivos.cargar(ruta)

                lista.cargar(numeros)

                print("\nArchivo cargado correctamente.")
                print("Archivo:", os.path.basename(ruta))
                print("Total de registros:", lista.cantidad())

            elif opcion == "3":

                if lista.cantidad() == 0:
                    print("\nNo hay datos cargados.")
                else:
                    print("\nPrimeros 20 elementos:")
                    print(lista.obtener_datos()[:20])

            elif opcion == "4":

                if lista.cantidad() == 0:
                    print("\nNo hay datos cargados.")
                else:
                    print("\nÚltimos 20 elementos:")
                    print(lista.obtener_datos()[-20:])

            elif opcion == "5":

                print("\nTotal de registros:", lista.cantidad())

            elif opcion == "0":

                print("\nFinalizando programa...")
                break

            else:

                print("\nOpción no válida.")

        except (OSError, ValueError) as error:

            print(f"\nError: {error}")


if __name__ == "__main__":
    main()