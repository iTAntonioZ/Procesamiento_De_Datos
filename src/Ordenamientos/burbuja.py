def burbuja(datos: list[int], ascendente: bool = True) -> list[int]:
    n = len(datos)
    for i in range(n - 1):
        intercambio = False
        for j in range(n - 1 - i):
            if (ascendente and datos[j] > datos[j + 1]) or (
                not ascendente and datos[j] < datos[j + 1]
            ):
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambio = True
        if not intercambio:
            break
    return datos
