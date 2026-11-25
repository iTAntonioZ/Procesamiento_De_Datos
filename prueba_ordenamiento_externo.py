from collections import Counter
from pathlib import Path
from random import Random
from tempfile import TemporaryDirectory
from openpyxl import Workbook
from src.Ordenamientos.ordenamiento_externo import OrdenamientoExterno


def verificar(origen, salida, datos, bloque, ascendente):
    resultado = OrdenamientoExterno.ordenar(origen, salida, bloque, ascendente)
    numeros = [int(linea) for linea in salida.read_text(encoding='utf-8').splitlines()]
    assert Counter(numeros) == Counter(datos)
    assert all((a <= b if ascendente else a >= b) for a, b in zip(numeros, numeros[1:]))
    assert resultado.cantidad == len(datos)
    assert resultado.bloques == (len(datos) + bloque - 1) // bloque
    assert resultado.tiempo >= 0
    assert Path(resultado.resumen).is_file()
    assert not list(salida.parent.glob('mezcla_*'))


def main():
    rng = Random(42)
    pruebas = 0
    with TemporaryDirectory() as temporal:
        carpeta = Path(temporal)
        txt = carpeta / 'entrada.txt'
        xlsx = carpeta / 'entrada.xlsx'
        salida = carpeta / 'salida.txt'
        for datos in ([7], [3, -1, 3, 0, -5, 8, -1], [4] * 17,
                      [rng.randint(-500, 500) for _ in range(1000)],
                      [rng.randint(-500, 500) for _ in range(5000)]):
            txt.write_text(''.join(f'{n}\n' for n in datos), encoding='utf-8')
            libro = Workbook()
            libro.active.append(['Numero'])
            for n in datos:
                libro.active.append([n])
            libro.save(xlsx)
            libro.close()
            for origen in (txt, xlsx):
                for bloque in (3, 1000):
                    for ascendente in (True, False):
                        verificar(origen, salida, datos, bloque, ascendente)
                        pruebas += 1
        # Validar que errores de entrada no sustituyan resultados existentes.
        anterior = salida.read_bytes()
        for contenido in ('', '1\ntexto\n', '3.5\n'):
            txt.write_text(contenido, encoding='utf-8')
            try:
                OrdenamientoExterno.ordenar(txt, salida, 2)
            except ValueError:
                assert salida.read_bytes() == anterior
                assert not list(carpeta.glob('mezcla_*'))
                pruebas += 1
            else:
                raise AssertionError('Se esperaba un error.')
        for bloque in (0, -1):
            try:
                OrdenamientoExterno.ordenar(txt, salida, bloque)
            except ValueError:
                pruebas += 1
            else:
                raise AssertionError('Bloque invalido aceptado.')
        try:
            OrdenamientoExterno.ordenar(txt, txt)
        except ValueError:
            pruebas += 1
        else:
            raise AssertionError('Se permitio sobrescribir el original.')
        xlsx.write_bytes(b'archivo corrupto')
        try:
            OrdenamientoExterno.ordenar(xlsx, salida)
        except ValueError:
            pruebas += 1
        else:
            raise AssertionError('Se acepto un XLSX dañado.')
    print(f'{pruebas} pruebas de ordenamiento externo correctas.')


if __name__ == '__main__':
    main()
