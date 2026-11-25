from dataclasses import dataclass

from src.Busquedas.secuencial import busqueda_secuencial
from src.Busquedas.binaria import busqueda_binaria
from src.Busquedas.hash import construir_tabla, busqueda_hash
from src.Util.cronometro import Cronometro


@dataclass
class ResultadoBusqueda:
    metodo: str
    valor: int
    posiciones: list[int]
    tiempo: float
    tiempo_preparacion: float = 0.0
    tiempo_indice: float = 0.0

    @property
    def coincidencias(self) -> int:
        return len(self.posiciones)


class GestorBusquedas:
    def __init__(self):
        self.cronometro = Cronometro()
        self.metodos = {
            '1': 'Secuencial',
            '2': 'Binaria',
            '3': 'Hash'
        }

    @staticmethod
    def detectar_orden(datos: list[int]) -> bool:
        if all(datos[i] <= datos[i + 1] for i in range(len(datos) - 1)):
            return True
        if all(datos[i] >= datos[i + 1] for i in range(len(datos) - 1)):
            return False
        raise ValueError('Ordena los datos antes de usar la busqueda binaria.')

    def preparar_binaria(self, gestor):
        datos = gestor.obtener_datos()
        return datos, self.detectar_orden(datos)

    def buscar(self, gestor, opcion: str, valor: int) -> ResultadoBusqueda:
        if not gestor.hay_datos():
            raise ValueError('No hay datos cargados.')
        if opcion not in self.metodos:
            raise ValueError('Metodo de busqueda no valido.')

        preparacion = 0.0
        indice = 0.0

        if opcion == '1':
            posiciones, tiempo = self.cronometro.ejecutar(
                busqueda_secuencial, gestor.lista, valor
            )
        elif opcion == '2':
            (datos, ascendente), preparacion = self.cronometro.ejecutar(
                self.preparar_binaria, gestor
            )
            posiciones, tiempo = self.cronometro.ejecutar(
                busqueda_binaria, datos, valor, ascendente
            )
        else:
            datos, preparacion = self.cronometro.ejecutar(gestor.obtener_datos)
            tabla, indice = self.cronometro.ejecutar(construir_tabla, datos)
            posiciones, tiempo = self.cronometro.ejecutar(
                busqueda_hash, tabla, valor
            )

        return ResultadoBusqueda(
            metodo=self.metodos[opcion], valor=valor,
            posiciones=posiciones, tiempo=tiempo,
            tiempo_preparacion=preparacion, tiempo_indice=indice
        )
