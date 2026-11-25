
from dataclasses import dataclass

from src.Ordenamientos.burbuja import burbuja
from src.Ordenamientos.seleccion import seleccion
from src.Ordenamientos.insercion import insercion
from src.Ordenamientos.shellsort import shell_sort
from src.Ordenamientos.quicksort import quicksort
from src.Ordenamientos.mergesort import mergesort
from src.Ordenamientos.radixsort import radixsort
from src.Ordenamientos.heapsort import heapsort

from src.Util.cronometro import Cronometro


@dataclass
class ResultadoOrdenamiento:
    datos: list[int]
    algoritmo: str
    orden: str
    tiempo: float


class GestorOrdenamientos:

    def __init__(self):

        self.cronometro = Cronometro()

        self.algoritmos = {
            "1": ("Bubble Sort", burbuja),
            "2": ("Selection Sort", seleccion),
            "3": ("Insertion Sort", insercion),
            "4": ("Shell Sort", shell_sort),
            "5": ("Quick Sort", quicksort),
            "6": ("Merge Sort", mergesort),
            "7": ("Radix Sort", radixsort),
            "8": ("Heap Sort", heapsort)
        }

    # Obtener los algoritmos disponibles
    def obtener_algoritmos(self) -> dict[str, str]:

        return {
            clave: nombre
            for clave, (nombre, funcion)
            in self.algoritmos.items()
        }

    # Ejecutar un algoritmo de ordenamiento
    def ordenar(
        self,
        datos: list[int],
        opcion: str,
        ascendente: bool = True
    ) -> ResultadoOrdenamiento:

        if not datos:
            raise ValueError("No hay datos para ordenar.")

        if opcion not in self.algoritmos:
            raise ValueError("Algoritmo no válido.")

        nombre, funcion = self.algoritmos[opcion]

        # Trabajar sobre una copia de los datos
        copia = datos.copy()

        # Medir exclusivamente el algoritmo
        resultado, tiempo = self.cronometro.ejecutar(
            funcion,
            copia,
            ascendente
        )

        # Identificar el sentido del ordenamiento
        orden = "Ascendente" if ascendente else "Descendente"

        return ResultadoOrdenamiento(
            datos=resultado,
            algoritmo=nombre,
            orden=orden,
            tiempo=tiempo
        )
