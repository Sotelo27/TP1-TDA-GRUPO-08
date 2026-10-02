"""
Problema 4 - Mochila resuelta por Programacion Lineal (biblioteca PuLP)
Teoria de Algoritmos - TP1

Se plantea la mochila 0/1 como un problema de Programacion Lineal Entera:

    Variables:    Yi en {0, 1}  (1 = el elemento i entra en la mochila)
    Objetivo:     MAX  suma(beneficio_i * Yi)
    Restriccion:  suma(peso_i * Yi) <= capacidad

PuLP le pasa el modelo al solver CBC (incluido con la biblioteca), que lo
resuelve con el metodo Simplex y Branch and Bound.
"""

import csv
import os
import time

import pulp

# Archivos de mochila a procesar, en orden creciente de tamano. Se asume
# que estan en la subcarpeta casos/, generados con crear_mochila.py.
ARCHIVOS_MOCHILA = [
    "mochila1000.txt",
    "mochila2000.txt",
    "mochila5000.txt",
    "mochila10000.txt",
    "mochila20000.txt",
]

# Carpeta donde vive este script y subcarpeta donde estan los archivos de
# entrada. El CSV de salida se guarda junto al script.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

# Nombre del CSV donde se van a guardar los resultados (uno por archivo
# procesado), para poder comparar despues contra los otros enfoques.
NOMBRE_CSV_SALIDA = "tiempos_pulp.csv"
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

def mochila_pulp(capacidad, items):

    n = len(items)

    # Se crea el problema de maximizacion.
    problema = pulp.LpProblem("Mochila", pulp.LpMaximize)

    # Variables de decision bivalentes: y[i] = 1 si el elemento i entra en la mochila, 0 si no.
    y = [pulp.LpVariable(f"y_{i}", cat=pulp.LpBinary) for i in range(n)]

    # Funcion objetivo: maximizar la suma de los beneficios de los elementos elegidos.
    problema += pulp.lpSum(items[i][1] * y[i] for i in range(n))

    # Restriccion: la suma de los pesos de los elementos elegidos no puede superar la capacidad.
    problema += pulp.lpSum(items[i][0] * y[i] for i in range(n)) <= capacidad

    # Se resuelve con el solver CBC (msg=False para que no imprima su log).
    problema.solve(pulp.PULP_CBC_CMD(msg=False))

    # Se leen los elementos cuya variable quedo en 1.
    mejores_indices = [i for i in range(n) if round(y[i].value()) == 1]
    mejor_beneficio = sum(items[i][1] for i in mejores_indices)
    mejor_peso = sum(items[i][0] for i in mejores_indices)

    return mejor_beneficio, mejores_indices, mejor_peso

if __name__ == "__main__":
    # Filas que se van a escribir en el CSV de salida, una por cada
    # archivo procesado con exito.
    filas_csv = []

    # Calentamiento: la primera vez que se usa PuLP, el sistema tiene que cargar
    # el solver CBC desde el disco, y eso tarda bastante mas que una resolucion
    # normal. Se resuelve una mochila chica SIN medir el tiempo, para que ese
    # costo no quede sumado a la primera mochila medida.
    mochila_pulp(50, [(10, 60), (20, 100), (30, 120)])

    for nombre_archivo in ARCHIVOS_MOCHILA:
        ruta_archivo = os.path.join(CARPETA_CASOS, nombre_archivo)

        if not os.path.isfile(ruta_archivo):
            print(f"No se encontró {nombre_archivo}, corré crear_mochila.py primero.")
            continue

        # La lectura y el parseo del archivo NO se incluyen en la
        # medicion de tiempo: solo interesa medir el tiempo que tarda en
        # armarse y resolverse el modelo de programacion lineal.
        capacidad, items = parsear_mochila(ruta_archivo)
        n = len(items)

        inicio = time.perf_counter()
        beneficio_maximo, indices_elegidos, peso_total = mochila_pulp(capacidad, items)
        fin = time.perf_counter()

        tiempo_ejecucion = fin - inicio

        print(
            f"n={n} | capacidad={capacidad} | beneficio_maximo={beneficio_maximo} "
            f"| peso_usado={peso_total} | tiempo={tiempo_ejecucion:.6f} s"
        )
        # DESCOMENTAR SI SE QUIERE VER LOS ELEMENTOS ELEGIDOS
        # print(f"  Elementos elegidos: {indices_elegidos}")

        filas_csv.append(
            {
                "n": n,
                "capacidad": capacidad,
                "beneficio_maximo": beneficio_maximo,
                "peso_usado": peso_total,
                "tiempo_segundos": round(tiempo_ejecucion, 4),
            }
        )

    # Se guardan los resultados en un CSV para poder comparar
    if filas_csv:
        with open(RUTA_CSV_SALIDA, "w", newline="") as archivo_csv:
            columnas = ["n", "capacidad", "beneficio_maximo", "peso_usado", "tiempo_segundos"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"\nResultados guardados en {RUTA_CSV_SALIDA}")
    else:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")