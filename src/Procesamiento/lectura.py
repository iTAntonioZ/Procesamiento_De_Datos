import os
from openpyxl import load_workbook


class LectorArchivos:

    # Lectura de archivos TXT
    @staticmethod
    def leer_txt(ruta) -> list[int]:
        numeros = []

        with open(ruta, 'r', encoding='utf-8-sig') as archivo:

            for fila, linea in enumerate(archivo, 1):
                linea = linea.strip()

                if not linea:
                    continue

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

        libro = load_workbook(
            ruta,
            read_only=True,
            data_only=True
        )

        try:
            hoja = libro.active

            for fila, celdas in enumerate(
                hoja.iter_rows(values_only=True), 1
            ):
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

        finally:
            libro.close()

        return numeros

    # Identificar el formato y cargar el archivo
    @staticmethod
    def cargar(ruta) -> list[int]:

        ruta = os.fspath(ruta)
        extension = os.path.splitext(ruta)[1].lower()

        if extension == '.txt':
            return LectorArchivos.leer_txt(ruta)

        elif extension == '.xlsx':
            return LectorArchivos.leer_xlsx(ruta)

        else:
            raise ValueError(
                'Formato no compatible. Utiliza TXT o XLSX.'
            )