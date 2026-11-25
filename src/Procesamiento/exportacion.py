
import os
from openpyxl import Workbook


class Exportador:

    # Exportar números y resumen en formato TXT
    @staticmethod
    def exportar_txt(datos, ruta, informacion):

        with open(ruta, "w", encoding="utf-8") as archivo:

            for numero in datos:
                archivo.write(f"{numero}\n")

        # Crear archivo adicional con los metadatos
        ruta_resumen = (
            os.path.splitext(ruta)[0] + "_resumen.txt"
        )

        with open(
            ruta_resumen, "w", encoding="utf-8"
        ) as archivo:

            for campo, valor in informacion.items():
                archivo.write(f"{campo}: {valor}\n")

        return [ruta, ruta_resumen]

    # Exportar datos en formato XLSX
    @staticmethod
    def exportar_xlsx(datos, ruta, informacion):

        libro = Workbook()

        try:

            # Primera hoja: registros
            hoja = libro.active
            hoja.title = "Datos"

            hoja.append(["Numero"])

            for numero in datos:
                hoja.append([numero])

            # Segunda hoja: información del procesamiento
            resumen = libro.create_sheet("Resumen")

            resumen.append(["Campo", "Valor"])

            for campo, valor in informacion.items():
                resumen.append([campo, valor])

            # Ajustar ancho de columnas
            resumen.column_dimensions["A"].width = 34
            resumen.column_dimensions["B"].width = 45

            # Guardar archivo
            libro.save(ruta)

        finally:
            libro.close()

        return [ruta]

    # Seleccionar formato de exportación
    @staticmethod
    def exportar(
        datos,
        ruta,
        *,
        archivo_origen,
        algoritmo=None,
        orden=None,
        tiempo_ordenamiento=None,
        tiempo_carga=None
    ):

        if not datos:
            raise ValueError("No hay datos para exportar.")

        ruta = os.fspath(ruta)

        extension = os.path.splitext(ruta)[1].lower()

        if extension not in (".txt", ".xlsx"):
            raise ValueError(
                "Formato no compatible. Utiliza TXT o XLSX."
            )

        # Información del procesamiento
        informacion = {
            "Archivo original": archivo_origen,

            "Total de registros": len(datos),

            "Algoritmo": (
                algoritmo if algoritmo is not None
                else "No ejecutado"
            ),

            "Orden": (
                orden if orden is not None
                else "No ejecutado"
            ),

            "Tiempo de ordenamiento (s)": (
                tiempo_ordenamiento
                if tiempo_ordenamiento is not None
                else "No ejecutado"
            ),

            "Tiempo de carga (s)": (
                tiempo_carga
                if tiempo_carga is not None
                else "No registrado"
            )
        }

        # Crear directorio si no existe
        os.makedirs(
            os.path.dirname(ruta) or ".",
            exist_ok=True
        )

        # Ejecutar exportación
        if extension == ".txt":

            return Exportador.exportar_txt(
                datos,
                ruta,
                informacion
            )

        return Exportador.exportar_xlsx(
            datos,
            ruta,
            informacion
        )
