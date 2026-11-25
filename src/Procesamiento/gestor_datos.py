
import os

from Estructura.listas_ligadas import ListaEnlazada
from src.Procesamiento.lectura import LectorArchivos


class GestorDatos:

    def __init__(self):
        self.lista = ListaEnlazada()
        self.archivo_actual = None

    # Cargar los datos de un archivo
    def cargar_archivo(self, ruta) -> int:

        numeros = LectorArchivos.cargar(ruta)

        if not numeros:
            raise ValueError(
                "El archivo no contiene registros."
            )

        self.lista.cargar(numeros)

        self.archivo_actual = os.path.basename(ruta)

        return len(numeros)

    # Verificar si existen datos cargados
    def hay_datos(self) -> bool:
        return self.lista.inicio is not None

    # Obtener todos los datos
    def obtener_datos(self) -> list[int]:
        return self.lista.obtener_datos()

    # Obtener la cantidad de registros
    def cantidad(self) -> int:
        return self.lista.cantidad()

    # Obtener los primeros elementos
    def primeros(self, cantidad: int = 20) -> list[int]:

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return self.obtener_datos()[:cantidad]

    # Obtener los últimos elementos
    def ultimos(self, cantidad: int = 20) -> list[int]:

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        if cantidad == 0:
            return []

        return self.obtener_datos()[-cantidad:]

    # Obtener el nombre del archivo cargado
    def obtener_archivo(self):
        return self.archivo_actual

    # Actualizar los datos después de un procesamiento
    def actualizar(self, numeros: list[int]) -> None:
        self.lista.cargar(numeros)

    # Limpiar todos los registros
    def limpiar(self) -> None:
        self.lista.limpiar()
        self.archivo_actual = None
