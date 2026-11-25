def construir_tabla(datos: list[int]) -> dict[int, list[int]]:
    tabla = {}
    for posicion, numero in enumerate(datos, 1):
        if numero not in tabla:
            tabla[numero] = []
        tabla[numero].append(posicion)
    return tabla


def busqueda_hash(tabla: dict[int, list[int]], valor: int) -> list[int]:
    # Copiar las posiciones para proteger el indice.
    return tabla.get(valor, []).copy()
