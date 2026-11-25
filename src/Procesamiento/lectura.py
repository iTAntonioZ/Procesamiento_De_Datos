
import os
from zipfile import BadZipFile
from openpyxl import load_workbook


class LectorArchivos:

    # Lectura de archivos TXT
    @staticmethod
    def leer_txt(ruta) -> list[int]:
        numeros = []

        with open(ruta, 'r', encoding='utf-8-sig') as archivo:

            for fila, linea in enumerate(archivo, 1):
                linea = linea.strip()

                # Ignorar líneas vacías
                if not linea:
                    continue

                # Validar números enteros
                try:
                    numeros.append(int(linea))

                except ValueError:
                    raise ValueError(
                        f'Valor no entero en la línea {fila}: {linea}'
                    ) from None

        return numeros

    # Lectura de archivos XLSX
    @staticmethod
    def leer_xlsx(ruta) -> list[int]:
        numeros = []

        # Validar la integridad del archivo Excel
        try:
            libro = load_workbook(
                ruta,
                read_only=True,
                data_only=True
            )

        except BadZipFile:
            raise ValueError(
                'El archivo XLSX está dañado o no tiene '
                'un formato de Excel válido.'
            ) from None

        try:
            hoja = libro.active

            for fila, celdas in enumerate(
                hoja.iter_rows(values_only=True), 1
            ):

                if not celdas:
                    continue

                valor = celdas[0]

                # Validar que exista una sola columna de datos
                if any(c is not None for c in celdas[1:]):
                    raise ValueError(
                        f'Fila {fila}: se esperaba una sola columna.'
                    )

                # Ignorar celdas vacías
                if valor is None or (
                    isinstance(valor, str) and not valor.strip()
                ):
                    continue

                # Ignorar el encabezado
                if fila == 1 and isinstance(valor, str):
                    if valor.strip().lower() in ('numero', 'número'):
                        continue

                # Evitar valores booleanos
                if isinstance(valor, bool):
                    raise ValueError(
                        f'Valor no entero en la fila {fila}: {valor}'
                    )

                # Validar números enteros
                try:
                    numero = int(valor)

                    if isinstance(valor, float) and valor != numero:
                        raise ValueError

                    if not isinstance(valor, (int, float, str)):
                        raise ValueError

                except (ValueError, TypeError, OverflowError):
                    raise ValueError(
                        f'Valor no entero en la fila {fila}: {valor}'
                    ) from None

                numeros.append(numero)

        except BadZipFile:
            raise ValueError(
                'Se encontraron datos dañados durante '
                'la lectura del archivo XLSX.'
            ) from None

        finally:
            libro.close()

        return numeros

    # Identificar el formato y cargar el archivo
    @staticmethod
    def cargar(ruta) -> list[int]:

        ruta = os.fspath(ruta)

        # Verificar que el archivo exista
        if not os.path.isfile(ruta):
            raise FileNotFoundError(
                f'No se encontró el archivo: {ruta}'
            )

        extension = os.path.splitext(ruta)[1].lower()

        if extension == '.txt':
            return LectorArchivos.leer_txt(ruta)

        elif extension == '.xlsx':
            return LectorArchivos.leer_xlsx(ruta)

        else:
            raise ValueError(
                'Formato no compatible. Utiliza TXT o XLSX.'
            )
