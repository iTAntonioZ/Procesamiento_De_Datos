def mergesort(datos: list[int], ascendente: bool = True) -> list[int]:
    if len(datos) <= 1:
        return datos
    medio = len(datos) // 2
    izquierda = mergesort(datos[:medio], ascendente)
    derecha = mergesort(datos[medio:], ascendente)
    i = j = k = 0
    while i < len(izquierda) and j < len(derecha):
        if (ascendente and izquierda[i] <= derecha[j]) or (
            not ascendente and izquierda[i] >= derecha[j]
        ):
            datos[k] = izquierda[i]
            i += 1
        else:
            datos[k] = derecha[j]
            j += 1
        k += 1
    while i < len(izquierda):
        datos[k] = izquierda[i]
        i += 1
        k += 1
    while j < len(derecha):
        datos[k] = derecha[j]
        j += 1
        k += 1
    return datos
