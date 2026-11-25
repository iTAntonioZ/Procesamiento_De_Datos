
import time


class Cronometro:

    def __init__(self):
        self.inicio = None
        self.fin = None

    # Iniciar el cronómetro
    def iniciar(self) -> None:
        self.inicio = time.perf_counter()
        self.fin = None

    # Detener el cronómetro
    def detener(self) -> float:

        if self.inicio is None:
            raise ValueError("El cronómetro no ha sido iniciado.")

        if self.fin is None:
            self.fin = time.perf_counter()

        return self.fin - self.inicio

    # Ejecutar una función y medir su duración
    def ejecutar(self, funcion, *args, **kwargs):

        self.iniciar()

        try:
            resultado = funcion(*args, **kwargs)

        finally:
            tiempo = self.detener()

        return resultado, tiempo

    # Convertir segundos a milisegundos
    @staticmethod
    def milisegundos(segundos: float) -> float:
        return segundos * 1000

    # Formatear el tiempo para mostrarlo al usuario
    @staticmethod
    def formatear(segundos: float) -> str:

        milisegundos = segundos * 1000

        return (
            f"{segundos:.6f} segundos "
            f"({milisegundos:.3f} ms)"
        )

    # Reiniciar el cronómetro
    def reiniciar(self) -> None:
        self.inicio = None
        self.fin = None
