from random import Random

from src.Procesamiento.gestor_datos import GestorDatos
from src.Busquedas.gestor_busquedas import GestorBusquedas
from src.Busquedas.binaria import busqueda_binaria
from src.Busquedas.hash import construir_tabla, busqueda_hash


def main():
    gestor = GestorDatos()
    buscador = GestorBusquedas()
    rng = Random(42)
    casos = [
        [7], [4, 4, 4], [-5, -2, 0, 3, 3, 8],
        [8, 3, 3, 0, -2, -5], [5, -1, 5, 0, 2],
        [rng.randint(-20, 20) for _ in range(1000)],
        [rng.randint(-20, 20) for _ in range(5000)],
        [i // 3 for i in range(5000)],
        [-(i // 3) for i in range(5000)]
    ]
    pruebas = 0
    for datos in casos:
        gestor.actualizar(datos)
        ordenado = (
            all(a <= b for a, b in zip(datos, datos[1:])) or
            all(a >= b for a, b in zip(datos, datos[1:]))
        )
        for valor in (-5, 0, 3, 4, 5, 7, 99999):
            esperado = [i for i, n in enumerate(datos, 1) if n == valor]
            for opcion in ('1', '2', '3'):
                if opcion == '2' and not ordenado:
                    try:
                        buscador.buscar(gestor, opcion, valor)
                    except ValueError:
                        pass
                    else:
                        raise AssertionError('Binaria acepto datos desordenados')
                else:
                    resultado = buscador.buscar(gestor, opcion, valor)
                    assert resultado.posiciones == esperado
                    assert resultado.coincidencias == len(esperado)
                    assert resultado.tiempo >= 0
                    assert resultado.tiempo_preparacion >= 0
                    assert resultado.tiempo_indice >= 0
                assert gestor.obtener_datos() == datos
                pruebas += 1
    gestor.limpiar()
    for opcion in ('1', '2', '3'):
        try:
            buscador.buscar(gestor, opcion, 1)
        except ValueError:
            pruebas += 1
        else:
            raise AssertionError('Se acepto un dataset vacio')
    assert busqueda_binaria([], 1) == []
    assert busqueda_hash(construir_tabla([]), 1) == []
    pruebas += 2
    print(f'{pruebas} pruebas de busqueda correctas.')


if __name__ == '__main__':
    main()
