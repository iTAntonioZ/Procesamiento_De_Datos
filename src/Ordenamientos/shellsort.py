def shell_sort(datos: list[int], ascendente: bool = True) -> list[int]:
    salto = len(datos) // 2
    while salto > 0:
        for i in range(salto, len(datos)):
            actual = datos[i]
            j = i
            while j >= salto and (
                (ascendente and datos[j - salto] > actual) or
                (not ascendente and datos[j - salto] < actual)
            ):
                datos[j] = datos[j - salto]
                j -= salto
            datos[j] = actual
        salto //= 2
    return datos
