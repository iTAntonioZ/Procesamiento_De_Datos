def heapsort(datos: list[int], ascendente: bool = True) -> list[int]:
    def domina(a, b):
        return a > b if ascendente else a < b
    def heapify(n, i):
        while True:
            extremo = i
            izquierda = 2 * i + 1
            derecha = 2 * i + 2
            if izquierda < n and domina(datos[izquierda], datos[extremo]):
                extremo = izquierda
            if derecha < n and domina(datos[derecha], datos[extremo]):
                extremo = derecha
            if extremo == i:
                break
            datos[i], datos[extremo] = datos[extremo], datos[i]
            i = extremo
    n = len(datos)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        datos[0], datos[i] = datos[i], datos[0]
        heapify(i, 0)
    return datos
