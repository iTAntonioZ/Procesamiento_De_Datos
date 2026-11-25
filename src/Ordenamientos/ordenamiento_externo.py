import os
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from zipfile import BadZipFile

from openpyxl import load_workbook
from src.Ordenamientos.mergesort import mergesort
from src.Util.cronometro import Cronometro


@dataclass
class ResultadoExterno:
    archivo: str
    resumen: str
    algoritmo: str
    orden: str
    cantidad: int
    bloques: int
    pasadas: int
    tamano_bloque: int
    tiempo: float


class OrdenamientoExterno:
    # Generador: entrega un entero a la vez, sin crear una lista completa.
    @staticmethod
    def leer_numeros(ruta):
        extension = os.path.splitext(ruta)[1].lower()
        if extension == '.txt':
            with open(ruta, encoding='utf-8-sig') as archivo:
                for fila, linea in enumerate(archivo, 1):
                    if linea.strip():
                        try:
                            yield int(linea.strip())
                        except ValueError:
                            raise ValueError(f'Valor no entero en la linea {fila}.') from None
        elif extension == '.xlsx':
            try:
                libro = load_workbook(ruta, read_only=True, data_only=True)
                try:
                    for fila, celdas in enumerate(libro.active.iter_rows(values_only=True), 1):
                        if not celdas:
                            continue
                        valor = celdas[0]
                        if any(c is not None for c in celdas[1:]):
                            raise ValueError(f'Fila {fila}: se esperaba una sola columna.')
                        if valor is None or (isinstance(valor, str) and not valor.strip()):
                            continue
                        if fila == 1 and isinstance(valor, str) and valor.strip().lower() in ('numero', 'número'):
                            continue
                        try:
                            if isinstance(valor, bool) or not isinstance(valor, (int, float, str)):
                                raise ValueError
                            numero = int(valor)
                            if isinstance(valor, float) and numero != valor:
                                raise ValueError
                        except (ValueError, TypeError, OverflowError):
                            raise ValueError(f'Valor no entero en la fila {fila}.') from None
                        yield numero
                finally:
                    libro.close()
            except BadZipFile:
                raise ValueError('El archivo XLSX esta dañado.') from None
        else:
            raise ValueError('Formato de entrada no compatible.')

    @staticmethod
    def guardar_bloque(datos, ruta, ascendente):
        mergesort(datos, ascendente)
        with open(ruta, 'w', encoding='utf-8') as archivo:
            for numero in datos:
                archivo.write(f'{numero}\n')

    @staticmethod
    def mezclar(izquierda, derecha, salida, ascendente):
        # Solo se mantiene un valor de cada archivo durante la mezcla.
        with open(izquierda, encoding='utf-8') as a, \
             open(derecha, encoding='utf-8') as b, \
             open(salida, 'w', encoding='utf-8') as destino:
            numeros_a = (int(linea) for linea in a)
            numeros_b = (int(linea) for linea in b)
            x = next(numeros_a, None)
            y = next(numeros_b, None)
            while x is not None and y is not None:
                if x <= y if ascendente else x >= y:
                    destino.write(f'{x}\n')
                    x = next(numeros_a, None)
                else:
                    destino.write(f'{y}\n')
                    y = next(numeros_b, None)
            while x is not None:
                destino.write(f'{x}\n')
                x = next(numeros_a, None)
            while y is not None:
                destino.write(f'{y}\n')
                y = next(numeros_b, None)

    @classmethod
    def procesar(cls, origen, salida, tamano_bloque, ascendente):
        cantidad = bloques = pasadas = 0
        directorio = os.path.dirname(os.path.abspath(salida))
        with TemporaryDirectory(prefix='mezcla_', dir=directorio) as temporal:
            rutas = []
            bloque = []
            lector = cls.leer_numeros(origen)
            try:
                for numero in lector:
                    bloque.append(numero)
                    cantidad += 1
                    if len(bloque) == tamano_bloque:
                        ruta = os.path.join(temporal, f'bloque_{len(rutas)}.txt')
                        cls.guardar_bloque(bloque, ruta, ascendente)
                        rutas.append(ruta)
                        bloque = []
            finally:
                lector.close()
            if bloque:
                ruta = os.path.join(temporal, f'bloque_{len(rutas)}.txt')
                cls.guardar_bloque(bloque, ruta, ascendente)
                rutas.append(ruta)
            if not rutas:
                raise ValueError('El archivo no contiene registros.')
            bloques = len(rutas)
            # Mezclar pares de bloques en cada pasada.
            while len(rutas) > 1:
                pasadas += 1
                nuevas = []
                for i in range(0, len(rutas), 2):
                    if i + 1 == len(rutas):
                        nuevas.append(rutas[i])
                        continue
                    destino = os.path.join(temporal, f'mezcla_{pasadas}_{i}.txt')
                    cls.mezclar(rutas[i], rutas[i + 1], destino, ascendente)
                    os.remove(rutas[i])
                    os.remove(rutas[i + 1])
                    nuevas.append(destino)
                rutas = nuevas
            # Publicar solo cuando el procesamiento termina correctamente.
            os.replace(rutas[0], salida)
        return cantidad, bloques, pasadas

    @classmethod
    def ordenar(cls, origen, salida, tamano_bloque=1000, ascendente=True):
        origen = os.path.abspath(origen)
        salida = os.path.abspath(salida)
        if type(tamano_bloque) is not int or tamano_bloque <= 0:
            raise ValueError('El tamaño del bloque debe ser un entero positivo.')
        if os.path.splitext(salida)[1].lower() != '.txt':
            raise ValueError('La salida externa debe ser TXT.')
        resumen = os.path.splitext(salida)[0] + '_resumen.txt'
        for destino in (salida, resumen):
            if os.path.normcase(os.path.realpath(origen)) == os.path.normcase(os.path.realpath(destino)) or (os.path.exists(destino) and os.path.samefile(origen, destino)):
                raise ValueError('La salida no puede reemplazar el archivo original.')
        os.makedirs(os.path.dirname(salida), exist_ok=True)
        (cantidad, bloques, pasadas), tiempo = Cronometro().ejecutar(
            cls.procesar, origen, salida, tamano_bloque, ascendente
        )
        orden = 'Ascendente' if ascendente else 'Descendente'
        algoritmo = 'External Merge Sort'
        with open(resumen, 'w', encoding='utf-8') as archivo:
            for campo, valor in {
                'Archivo original': os.path.basename(origen),
                'Algoritmo': algoritmo,
                'Orden': orden,
                'Total de registros': cantidad,
                'Tamaño de bloque': tamano_bloque,
                'Bloques iniciales': bloques,
                'Pasadas de mezcla': pasadas,
                'Tiempo de ordenamiento externo (s)': tiempo
            }.items():
                archivo.write(f'{campo}: {valor}\n')
        return ResultadoExterno(salida, resumen, algoritmo, orden, cantidad,
                                bloques, pasadas, tamano_bloque, tiempo)
