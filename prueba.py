
from collections import Counter
from random import Random

from src.Ordenamientos.burbuja import burbuja
from src.Ordenamientos.seleccion import seleccion
from src.Ordenamientos.insercion import insercion
from src.Ordenamientos.shellsort import shell_sort
from src.Ordenamientos.quicksort import quicksort
from src.Ordenamientos.mergesort import mergesort
from src.Ordenamientos.radixsort import radixsort
from src.Ordenamientos.heapsort import heapsort


algoritmos = [
    burbuja,
    seleccion,
    insercion,
    shell_sort,
    quicksort,
    mergesort,
    radixsort,
    heapsort
]

rng = Random(42)

casos = [
    [],
    [7],
    [3, -1, 3, 0, -5, 8, -1],
    [4] * 100,
    list(range(100)),
    list(range(99, -1, -1)),
    [-10**21, 0, 10**21],
    [rng.randint(-500, 500) for _ in range(1000)],
    [rng.randint(-500, 500) for _ in range(5000)]
]

for algoritmo in algoritmos:

    for caso in casos:

        for ascendente in (True, False):

            datos = caso.copy()

            resultado = algoritmo(datos, ascendente)

            # Verificar que se modifica la lista recibida
            assert resultado is datos

            # Verificar que no se pierdan elementos
            assert Counter(resultado) == Counter(caso)

            # Verificar el sentido del ordenamiento
            assert all(
                (a <= b if ascendente else a >= b)
                for a, b in zip(resultado, resultado[1:])
            )

    print(
        f"{algoritmo.__name__}: "
        f"{len(casos) * 2} pruebas correctas"
    )

print(
    f"\nTotal: "
    f"{len(algoritmos) * len(casos) * 2} "
    f"pruebas correctas"
)
