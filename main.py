import os

from src.Procesamiento.gestor_datos import GestorDatos
from src.Procesamiento.exportacion import Exportador
from src.Util.cronometro import Cronometro
from src.Ordenamientos.gestor_ordenamientos import GestorOrdenamientos
from src.Busquedas.gestor_busquedas import GestorBusquedas
from src.Ordenamientos.ordenamiento_externo import OrdenamientoExterno

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_TXT = os.path.join(BASE_DIR, 'datasets', 'dataset_1000_duplicados.txt')
DATASET_XLSX = os.path.join(BASE_DIR, 'datasets', 'dataset_5000_duplicados.xlsx')
DIRECTORIO_RESULTADOS = os.path.join(BASE_DIR, 'Resultados')


def mostrar_menu():
    print('\n====== SISTEMA DE PROCESAMIENTO DE DATOS ======')
    print('1. Cargar dataset de 1,000 registros')
    print('2. Cargar dataset de 5,000 registros')
    print('3. Mostrar primeros 20 elementos')
    print('4. Mostrar últimos 20 elementos')
    print('5. Mostrar total de registros')
    print('6. Mostrar información del dataset')
    print('7. Limpiar datos')
    print('8. Exportar resultados')
    print('9. Ordenamientos internos')
    print('10. Buscar un valor')
    print('11. Ordenamiento externo')
    print('0. Salir')


def ordenar_datos(gestor, gestor_ordenamientos):
    if not gestor.hay_datos():
        print('\nNo hay datos para ordenar.')
        return None

    print('\n--- ORDENAMIENTOS INTERNOS ---')
    for clave, nombre in gestor_ordenamientos.obtener_algoritmos().items():
        print(f'{clave}. {nombre}')
    print('0. Regresar')

    opcion = input('Selecciona un algoritmo: ').strip()
    if opcion == '0':
        return None
    if opcion not in gestor_ordenamientos.obtener_algoritmos():
        raise ValueError('Algoritmo no válido.')

    print('\n1. Ascendente')
    print('2. Descendente')
    print('0. Cancelar')
    sentido = input('Selecciona el orden: ').strip()
    if sentido == '0':
        return None
    if sentido not in ('1', '2'):
        raise ValueError('Orden no válido.')

    resultado = gestor_ordenamientos.ordenar(
        gestor.obtener_datos(), opcion, ascendente=(sentido == '1')
    )
    gestor.actualizar(resultado.datos)

    print('\nOrdenamiento realizado correctamente.')
    print('Algoritmo:', resultado.algoritmo)
    print('Orden:', resultado.orden)
    print('Registros:', len(resultado.datos))
    print('Tiempo:', Cronometro.formatear(resultado.tiempo))
    print('Primeros 20:', gestor.primeros())
    print('Últimos 20:', gestor.ultimos())
    return resultado


def exportar_resultados(gestor, cronometro, tiempo_carga, resultado):
    if not gestor.hay_datos():
        print('\nNo hay datos para exportar.')
        return

    print('\n--- EXPORTAR RESULTADOS ---')
    print('1. Archivo TXT')
    print('2. Archivo XLSX')
    print('0. Cancelar')
    opcion = input('Selecciona un formato: ').strip()
    if opcion == '0':
        return
    if opcion not in ('1', '2'):
        raise ValueError('Formato no válido.')

    extension = '.txt' if opcion == '1' else '.xlsx'
    nombre_original = gestor.obtener_archivo()
    nombre_base = os.path.splitext(nombre_original)[0]

    if resultado is None:
        sufijo = '_exportado'
    else:
        algoritmo = resultado.algoritmo.lower().replace(' ', '_')
        orden = resultado.orden.lower()
        sufijo = f'_{algoritmo}_{orden}'

    ruta = os.path.join(DIRECTORIO_RESULTADOS, nombre_base + sufijo + extension)
    datos = gestor.obtener_datos()
    archivos, tiempo_exportacion = cronometro.ejecutar(
        Exportador.exportar,
        datos,
        ruta,
        archivo_origen=nombre_original,
        algoritmo=resultado.algoritmo if resultado else None,
        orden=resultado.orden if resultado else None,
        tiempo_ordenamiento=resultado.tiempo if resultado else None,
        tiempo_carga=tiempo_carga
    )
    print('\nExportación realizada correctamente.')
    for archivo in archivos:
        print('-', archivo)
    print('Tiempo de exportación:', cronometro.formatear(tiempo_exportacion))


def buscar_datos(gestor, gestor_busquedas):
    if not gestor.hay_datos():
        print('\nNo hay datos para buscar.')
        return

    print('\n--- METODOS DE BUSQUEDA ---')
    for clave, nombre in gestor_busquedas.metodos.items():
        print(f'{clave}. {nombre}')
    print('0. Regresar')

    opcion = input('Selecciona un metodo: ').strip()
    if opcion == '0':
        return
    if opcion not in gestor_busquedas.metodos:
        raise ValueError('Metodo de busqueda no valido.')

    valor = int(input('Numero a buscar: ').strip())
    resultado = gestor_busquedas.buscar(gestor, opcion, valor)

    print('\n--- RESULTADO DE BUSQUEDA ---')
    print('Metodo:', resultado.metodo)
    print('Valor:', resultado.valor)
    print('Coincidencias:', resultado.coincidencias)
    if resultado.posiciones:
        print('Posiciones (desde 1):', resultado.posiciones)
    else:
        print('No se encontro el valor.')

    print('Tiempo de busqueda:', Cronometro.formatear(resultado.tiempo))
    if opcion in ('2', '3'):
        print('Tiempo de preparacion:', Cronometro.formatear(resultado.tiempo_preparacion))
    if opcion == '3':
        print('Tiempo de construccion hash:', Cronometro.formatear(resultado.tiempo_indice))
    total = resultado.tiempo + resultado.tiempo_preparacion + resultado.tiempo_indice
    print('Tiempo total medido:', Cronometro.formatear(total))


def ordenar_externo():
    print('\n--- ORDENAMIENTO EXTERNO ---')
    print('1. Dataset TXT de 1,000 registros')
    print('2. Dataset XLSX de 5,000 registros')
    print('0. Regresar')
    opcion = input('Selecciona un archivo: ').strip()
    if opcion == '0':
        return
    if opcion not in ('1', '2'):
        raise ValueError('Archivo no válido.')
    origen = DATASET_TXT if opcion == '1' else DATASET_XLSX
    print('1. Ascendente')
    print('2. Descendente')
    print('0. Cancelar')
    sentido = input('Selecciona el orden: ').strip()
    if sentido == '0':
        return
    if sentido not in ('1', '2'):
        raise ValueError('Orden no válido.')
    tamano = int(input('Tamaño de bloque [1000]: ').strip() or '1000')
    orden = 'ascendente' if sentido == '1' else 'descendente'
    nombre = os.path.splitext(os.path.basename(origen))[0]
    salida = os.path.join(DIRECTORIO_RESULTADOS, f'{nombre}_external_merge_sort_{orden}.txt')
    resultado = OrdenamientoExterno.ordenar(origen, salida, tamano, sentido == '1')
    print('\nOrdenamiento externo realizado correctamente.')
    print('Algoritmo:', resultado.algoritmo)
    print('Orden:', resultado.orden)
    print('Registros:', resultado.cantidad)
    print('Bloques iniciales:', resultado.bloques)
    print('Pasadas de mezcla:', resultado.pasadas)
    print('Tiempo:', Cronometro.formatear(resultado.tiempo))
    print('Archivo ordenado:', resultado.archivo)
    print('Resumen:', resultado.resumen)
    print('Los datos en memoria no se modificaron.')


def main():
    gestor = GestorDatos()
    gestor_ordenamientos = GestorOrdenamientos()
    gestor_busquedas = GestorBusquedas()
    cronometro = Cronometro()
    tiempo_carga = None
    resultado = None

    while True:
        mostrar_menu()
        opcion = input('Selecciona una opción: ').strip()

        try:
            if opcion in ('1', '2'):
                ruta = DATASET_TXT if opcion == '1' else DATASET_XLSX
                cantidad, tiempo_carga = cronometro.ejecutar(gestor.cargar_archivo, ruta)
                resultado = None
                print('\nArchivo cargado correctamente.')
                print('Archivo:', gestor.obtener_archivo())
                print('Total de registros:', cantidad)
                print('Tiempo de carga:', cronometro.formatear(tiempo_carga))

            elif opcion == '3':
                if gestor.hay_datos():
                    print('\nPrimeros 20 elementos:', gestor.primeros())
                else:
                    print('\nNo hay datos cargados.')

            elif opcion == '4':
                if gestor.hay_datos():
                    print('\nÚltimos 20 elementos:', gestor.ultimos())
                else:
                    print('\nNo hay datos cargados.')

            elif opcion == '5':
                print('\nTotal de registros:', gestor.cantidad())

            elif opcion == '6':
                if not gestor.hay_datos():
                    print('\nNo hay datos cargados.')
                    continue
                print('\n--- INFORMACIÓN DEL DATASET ---')
                print('Archivo:', gestor.obtener_archivo())
                print('Registros:', gestor.cantidad())
                print('Estructura: Lista enlazada')
                if tiempo_carga is not None:
                    print('Tiempo de carga:', cronometro.formatear(tiempo_carga))
                if resultado is None:
                    print('Estado: Sin ordenamiento aplicado')
                else:
                    print('Algoritmo:', resultado.algoritmo)
                    print('Orden:', resultado.orden)
                    print('Tiempo:', cronometro.formatear(resultado.tiempo))

            elif opcion == '7':
                gestor.limpiar()
                cronometro.reiniciar()
                tiempo_carga = None
                resultado = None
                print('\nDatos eliminados de la memoria.')

            elif opcion == '8':
                exportar_resultados(gestor, cronometro, tiempo_carga, resultado)

            elif opcion == '9':
                nuevo_resultado = ordenar_datos(gestor, gestor_ordenamientos)
                if nuevo_resultado is not None:
                    resultado = nuevo_resultado

            elif opcion == '10':
                buscar_datos(gestor, gestor_busquedas)

            elif opcion == '11':
                ordenar_externo()

            elif opcion == '0':
                print('\nFinalizando programa...')
                break

            else:
                print('\nOpción no válida.')

        except (OSError, ValueError) as error:
            print(f'\nError: {error}')


if __name__ == '__main__':
    main()
