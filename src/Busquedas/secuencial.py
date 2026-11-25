from Estructura.listas_ligadas import ListaEnlazada


def busqueda_secuencial(lista: ListaEnlazada, valor: int) -> list[int]:
    # Reutilizar la busqueda de nuestra lista enlazada.
    return [posicion for posicion, nodo in lista.buscar(valor)]
