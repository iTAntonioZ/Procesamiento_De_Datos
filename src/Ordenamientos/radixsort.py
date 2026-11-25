def radixsort(datos: list[int], ascendente: bool = True) -> list[int]:
    if not datos:
        return datos
    minimo = min(datos)
    maximo = max(datos)
    def clave(numero):
        return numero - minimo if ascendente else maximo - numero
    exp = 1
    while (maximo - minimo) // exp > 0:
        conteo = [0] * 10
        salida = [0] * len(datos)
        for numero in datos:
            digito = (clave(numero) // exp) % 10
            conteo[digito] += 1
        for i in range(1, 10):
            conteo[i] += conteo[i - 1]
        for i in range(len(datos) - 1, -1, -1):
            numero = datos[i]
            digito = (clave(numero) // exp) % 10
            conteo[digito] -= 1
            salida[conteo[digito]] = numero
        datos[:] = salida
        exp *= 10
    return datos
