from Estructura.listas_ligadas import ListaEnlazada


def main():

    # Crear nuestra estructura de datos
    lista = ListaEnlazada()

    # Datos de prueba
    datos = [50, 20, 10, 20, 80, 5]

    # Cargar datos en la lista enlazada
    lista.cargar(datos)

    # Mostrar información
    print("======================================")
    print(" SISTEMA DE PROCESAMIENTO DE DATOS")
    print("======================================")

    print("\nDatos:", lista.obtener_datos())
    print("Total de registros:", lista.cantidad())
    print("Existe ciclo:", lista.hay_ciclo())

    # Prueba de búsqueda secuencial
    valor = 20
    resultados = lista.buscar(valor)

    print(f"\nResultados de búsqueda del número {valor}:")

    if resultados:

        for posicion, nodo in resultados:
            print(f"Posición: {posicion}, Valor: {nodo.dato}")

        print(f"Total de coincidencias: {len(resultados)}")

    else:
        print("No se encontraron coincidencias.")


if __name__ == "__main__":
    main()