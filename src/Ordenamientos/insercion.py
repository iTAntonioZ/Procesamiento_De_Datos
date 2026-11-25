def insercion(datos: list[int], ascendente: bool = True) -> list[int]:
    for i in range(1, len(datos)):
        actual = datos[i]
        j = i - 1
        while j >= 0 and (
            (ascendente and datos[j] > actual) or
            (not ascendente and datos[j] < actual)
        ):
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = actual
    return datos
