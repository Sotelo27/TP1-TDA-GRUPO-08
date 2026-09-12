"""
Problema 1 - Mochila 0/1 resuelta por Fuerza Bruta
Teoria de Algoritmos - TP1

Este programa resuelve el problema de la mochila 0/1 (cada elemento se
lleva entero o no se lleva, no hay fracciones) probando TODAS las
combinaciones posibles de elementos, es decir, los 2^n subconjuntos que se
pueden formar con n elementos, sin ningun tipo de poda ni optimizacion.

Esto lo convierte en un algoritmo de complejidad temporal exponencial:
O(n * 2^n), ya que por cada uno de los 2^n subconjuntos posibles se
recorren los n elementos para armar el subconjunto y calcular su peso y
beneficio total.

Se implementa asi intencionalmente (sin poda): sirve como base de
comparacion contra la version con backtracking (con poda) que se resuelve
en otro archivo. Por eso mismo, solo es practico para valores de n chicos;
este script procesa los archivos mochila10.txt, mochila13.txt,
mochila16.txt, mochila19.txt y mochila22.txt generados por
crear_mochila.py, y guarda los tiempos obtenidos en un CSV para poder
graficarlos despues.
"""

import csv
import os
import time

# Archivos de mochila a procesar, en orden creciente de tamano. Se asume
# que estan en la subcarpeta casos/, generados con crear_mochila.py.
ARCHIVOS_MOCHILA = [
    "mochila10.txt",
    "mochila13.txt",
    "mochila16.txt",
    "mochila19.txt",
    "mochila22.txt",
]

# Carpeta donde vive este script y subcarpeta donde estan los archivos de
# entrada. El CSV de salida se sigue guardando junto al script.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

# Nombre del CSV donde se van a guardar los resultados (uno por archivo
# procesado), para usarlo despues en el grafico de tiempos.
NOMBRE_CSV_SALIDA = "tiempos_fuerza_bruta.csv"
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, NOMBRE_CSV_SALIDA)


def parsear_mochila(ruta_archivo):
    """
    Lee un archivo de mochila con el siguiente formato:
        linea 1: capacidad de la mochila (entero)
        lineas siguientes: peso,beneficio (uno por elemento, separados por coma)

    Devuelve una tupla (capacidad, items), donde items es una lista de
    tuplas (peso, beneficio), una por cada elemento leido del archivo.
    """
    with open(ruta_archivo, "r") as archivo:
        lineas = archivo.read().splitlines()

    capacidad = int(lineas[0])

    items = []
    for linea in lineas[1:]:
        linea = linea.strip()
        if not linea:
            continue
        peso_str, beneficio_str = linea.split(",")
        items.append((int(peso_str), int(beneficio_str)))

    return capacidad, items


def fuerza_bruta(capacidad, items):
    """
    Resuelve el problema de la mochila 0/1 por fuerza bruta pura,
    generando y evaluando TODOS los subconjuntos posibles de elementos.

    Idea del algoritmo:
    Con n elementos existen 2^n subconjuntos posibles, ya que cada
    elemento puede estar incluido (1) o no estar incluido (0) en un
    subconjunto dado. Por lo tanto, cada subconjunto se puede representar
    con un numero binario de n bits (una "mascara"), donde el bit i
    indica si el elemento i forma parte de ese subconjunto o no.

    Se recorren todas las mascaras posibles, de 0 a 2^n - 1, y para cada
    una se arma el subconjunto de elementos correspondiente. No hay
    ninguna poda: siempre se arma el subconjunto COMPLETO (se suman todos
    sus pesos y beneficios) y recien al final se compara su peso contra
    la capacidad para descartarlo o no. La busqueda nunca se corta antes
    de tiempo, ni siquiera cuando ya es evidente que el subconjunto va a
    superar la capacidad.

    Parametros:
        capacidad: capacidad maxima de la mochila (entero)
        items: lista de tuplas (peso, beneficio), una por elemento

    Devuelve una tupla (mejor_beneficio, mejores_indices, mejor_peso):
        mejor_beneficio: el beneficio maximo encontrado entre todos los
            subconjuntos validos (que no superan la capacidad)
        mejores_indices: lista de indices (0-based, sobre "items") de los
            elementos que forman esa solucion optima
        mejor_peso: peso total de esa seleccion de elementos
    """
    n = len(items)

    mejor_beneficio = 0
    mejores_indices = []
    mejor_peso = 0

    # Se recorren los 2^n subconjuntos posibles, representados como los
    # numeros del 0 al 2^n - 1. La representacion binaria de cada numero
    # indica que elementos forman parte de ese subconjunto (bit en 1 =
    # el elemento esta incluido, bit en 0 = no esta incluido).
    for mascara in range(2 ** n):
        peso_subconjunto = 0
        beneficio_subconjunto = 0
        indices_subconjunto = []

        # Se recorren los n bits de la mascara actual para armar el
        # subconjunto de elementos que representa.
        for i in range(n):
            bit_i = (mascara >> i) & 1
            if bit_i == 1:
                peso_i, beneficio_i = items[i]
                peso_subconjunto += peso_i
                beneficio_subconjunto += beneficio_i
                indices_subconjunto.append(i)

        # Recien aca, con el subconjunto ya armado por completo, se
        # verifica si es valido (no supera la capacidad) y si mejora la
        # mejor solucion encontrada hasta el momento. No hay poda: todos
        # los subconjuntos se arman y evaluan enteros, incluso los que
        # claramente van a superar la capacidad.
        if peso_subconjunto <= capacidad and beneficio_subconjunto > mejor_beneficio:
            mejor_beneficio = beneficio_subconjunto
            mejores_indices = indices_subconjunto
            mejor_peso = peso_subconjunto

    return mejor_beneficio, mejores_indices, mejor_peso


if __name__ == "__main__":
    # Filas que se van a escribir en el CSV de salida, una por cada
    # archivo procesado con exito.
    filas_csv = []

    for nombre_archivo in ARCHIVOS_MOCHILA:
        ruta_archivo = os.path.join(CARPETA_CASOS, nombre_archivo)

        if not os.path.isfile(ruta_archivo):
            print(f"No se encontró {nombre_archivo}, corré crear_mochila.py primero.")
            continue

        # La lectura y el parseo del archivo NO se incluyen en la
        # medicion de tiempo: solo interesa medir el tiempo que tarda el
        # algoritmo de fuerza bruta en si mismo.
        capacidad, items = parsear_mochila(ruta_archivo)
        n = len(items)

        inicio = time.perf_counter()
        beneficio_maximo, indices_elegidos, peso_total = fuerza_bruta(capacidad, items)
        fin = time.perf_counter()

        tiempo_ejecucion = fin - inicio

        print(
            f"n={n} | capacidad={capacidad} | beneficio_maximo={beneficio_maximo} "
            f"| peso_usado={peso_total} | tiempo={tiempo_ejecucion:.6f} s"
        )

        filas_csv.append(
            {
                "n": n,
                "capacidad": capacidad,
                "beneficio_maximo": beneficio_maximo,
                "peso_usado": peso_total,
                "tiempo_segundos": round(tiempo_ejecucion, 6),
            }
        )

    # Se guardan los resultados en un CSV para poder graficar despues los
    # tiempos de ejecucion en funcion de n.
    if filas_csv:
        with open(RUTA_CSV_SALIDA, "w", newline="") as archivo_csv:
            columnas = ["n", "capacidad", "beneficio_maximo", "peso_usado", "tiempo_segundos"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"\nResultados guardados en {RUTA_CSV_SALIDA}")
    else:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")
