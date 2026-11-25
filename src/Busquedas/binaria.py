def busqueda_binaria(datos: list[int], valor: int,
                     ascendente: bool = True) -> list[int]:
    # Encontrar el limite izquierdo del valor.
    inicio, fin = 0, len(datos)
    while inicio < fin:
        medio = (inicio + fin) // 2
        if (ascendente and datos[medio] < valor) or (
            not ascendente and datos[medio] > valor
        ):
            inicio = medio + 1
        else:
            fin = medio
    primero = inicio

    if primero == len(datos) or datos[primero] != valor:
        return []

    # Encontrar el limite derecho (exclusivo).
    inicio, fin = primero, len(datos)
    while inicio < fin:
        medio = (inicio + fin) // 2
        if (ascendente and datos[medio] <= valor) or (
            not ascendente and datos[medio] >= valor
        ):
            inicio = medio + 1
        else:
            fin = medio

    return list(range(primero + 1, inicio + 1))
