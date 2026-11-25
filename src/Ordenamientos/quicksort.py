def quicksort(datos: list[int], ascendente: bool = True) -> list[int]:
    # Pila de segmentos pendientes; no utiliza recursion.
    pendientes = [(0, len(datos) - 1)]
    while pendientes:
        inicio, fin = pendientes.pop()
        if inicio >= fin:
            continue
        pivote = datos[(inicio + fin) // 2]
        izquierda = inicio
        i = inicio
        derecha = fin
        # Particion en tres grupos: antes, iguales y despues del pivote.
        while i <= derecha:
            if (ascendente and datos[i] < pivote) or (
                not ascendente and datos[i] > pivote
            ):
                datos[izquierda], datos[i] = datos[i], datos[izquierda]
                izquierda += 1
                i += 1
            elif (ascendente and datos[i] > pivote) or (
                not ascendente and datos[i] < pivote
            ):
                datos[i], datos[derecha] = datos[derecha], datos[i]
                derecha -= 1
            else:
                i += 1
        pendientes.append((inicio, izquierda - 1))
        pendientes.append((derecha + 1, fin))
    return datos
