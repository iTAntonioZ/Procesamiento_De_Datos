def seleccion(datos: list[int], ascendente: bool = True) -> list[int]:
    n = len(datos)
    for i in range(n - 1):
        indice = i
        for j in range(i + 1, n):
            if (ascendente and datos[j] < datos[indice]) or (
                not ascendente and datos[j] > datos[indice]
            ):
                indice = j
        if indice != i:
            datos[i], datos[indice] = datos[indice], datos[i]
    return datos
