"""
Problema 1 - Mochila 0/1 resuelta por Backtracking
Teoria de Algoritmos - TP1

Este programa resuelve el mismo problema que solucion_fuerza_bruta.py (la
mochila 0/1: cada elemento se lleva entero o no se lleva), pero en vez de
generar y evaluar TODOS los 2^n subconjuntos posibles, arma un arbol de
decision binario (incluir / no incluir cada elemento, en orden de indice)
y lo recorre con backtracking, cortando ramas enteras del arbol cuando se
puede probar que no vale la pena seguir explorandolas.

Se aplican dos podas:

  1) PODA OBLIGATORIA (de factibilidad): jamas se arma un subconjunto que
     ya supera la capacidad. Es la poda minima indispensable para que esto
     sea backtracking y no fuerza bruta disfrazada.

  2) PODA OPCIONAL (cota de beneficio / branch and bound): antes de seguir
     explorando un nodo, se calcula una cota optimista de cuanto beneficio
     se podria llegar a sumar en el mejor de los casos desde ese punto en
     adelante, y si ni en ese mejor caso se puede superar la mejor
     solucion ya encontrada, se corta toda la rama (ambas opciones: ni
     incluir ni excluir el elemento actual).

Este script procesa los mismos archivos que solucion_fuerza_bruta.py
(mochila10.txt ... mochila22.txt) y guarda los tiempos en un CSV aparte
(tiempos_backtracking.csv) para poder comparar ambos enfoques.
"""

import csv
import os
import time

# Archivos de mochila a procesar, en orden creciente de tamano. Se asume
# que estan en la subcarpeta casos/, generados con generar_casos.py.
ARCHIVOS_MOCHILA = [f"mochila{n}.txt" for n in range(10, 23)]

# Cantidad de veces que se resuelve cada archivo. El tiempo que se guarda
# es el promedio de todas las repeticiones, para que una medicion aislada
# afectada por ruido del sistema no distorsione los graficos.
REPETICIONES = 5

# Carpeta donde vive este script y subcarpeta donde estan los archivos de
# entrada. El CSV de salida se sigue guardando junto al script.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

# Nombre del CSV donde se van a guardar los resultados (uno por archivo
# procesado), para poder comparar despues contra tiempos_fuerza_bruta.csv.
NOMBRE_CSV_SALIDA = "tiempos_backtracking.csv"
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, NOMBRE_CSV_SALIDA)


def parsear_mochila(ruta_archivo):
    """
    Lee un archivo de mochila con el siguiente formato:
        linea 1: capacidad de la mochila (entero)
        lineas siguientes: peso,beneficio (uno por elemento, separados por coma)

    Devuelve una tupla (capacidad, items), donde items es una lista de
    tuplas (peso, beneficio), una por cada elemento leido del archivo.

    (Identica a la de solucion_fuerza_bruta.py: se duplica aca a proposito
    para que este archivo sea autocontenido y se pueda correr y corregir
    de forma independiente).
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


def backtrack(i, peso_actual, beneficio_actual, indices_actuales, capacidad, items, beneficio_restante, mejor):
    """
    Decide que hacer con el elemento de indice i (incluirlo o no),
    habiendo ya decidido que pasa con los elementos 0..i-1. Es la funcion
    recursiva que recorre el arbol de decision de mochila_backtracking().

    Parametros que cambian en cada llamada recursiva:
        i: indice del elemento a decidir
        peso_actual, beneficio_actual: peso y beneficio acumulados por las
            decisiones tomadas hasta ahora (elementos 0..i-1)
        indices_actuales: lista de indices incluidos hasta ahora

    Parametros fijos durante toda la busqueda (se pasan tal cual en cada
    llamada, no cambian):
        capacidad: capacidad maxima de la mochila
        items: lista completa de tuplas (peso, beneficio)
        beneficio_restante: beneficio_restante[i] = suma de beneficios de
            items[i:], precalculado en mochila_backtracking()
        mejor: diccionario {"beneficio", "indices", "peso"} con la mejor
            solucion encontrada hasta el momento (se va actualizando)
    """
    # Caso base
    if i == len(items):
        if beneficio_actual > mejor["beneficio"]:
            mejor["beneficio"] = beneficio_actual
            mejor["indices"] = list(indices_actuales)
            mejor["peso"] = peso_actual
        return

    # --- PODA OPCIONAL 
    cota_optimista = beneficio_actual + beneficio_restante[i]
    if cota_optimista <= mejor["beneficio"]:
        return

    peso_i, beneficio_i = items[i]

    # --- PODA OBLIGATORIA
    if peso_actual + peso_i <= capacidad:
        indices_actuales.append(i)
        backtrack(i + 1, peso_actual + peso_i, beneficio_actual + beneficio_i, indices_actuales,
                  capacidad, items, beneficio_restante, mejor)
        indices_actuales.pop()  # se deshace la decision (el "backtrack" propiamente dicho)

    # --- Rama "no incluir el elemento i" ---
    # Esta rama siempre es factible (no agrega peso), asi que siempre se
    # explora.
    backtrack(i + 1, peso_actual, beneficio_actual, indices_actuales,
              capacidad, items, beneficio_restante, mejor)


def mochila_backtracking(capacidad, items):
    """
    Resuelve el problema de la mochila 0/1 con backtracking, recorriendo
    el arbol de decision "incluir / no incluir" elemento por elemento (en
    orden de indice), pero podando las ramas que no pueden llevar a una
    solucion mejor que la ya encontrada. El recorrido en si lo hace la
    funcion backtrack() de arriba.

    Parametros:
        capacidad: capacidad maxima de la mochila (entero)
        items: lista de tuplas (peso, beneficio), una por elemento

    Devuelve una tupla (mejor_beneficio, mejores_indices, mejor_peso), con
    el mismo formato que fuerza_bruta() en solucion_fuerza_bruta.py:
        mejor_beneficio: el beneficio maximo encontrado
        mejores_indices: lista de indices (0-based) de los elementos elegidos
        mejor_peso: peso total de esa seleccion
    """
    n = len(items)

    beneficio_restante = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        beneficio_restante[i] = beneficio_restante[i + 1] + items[i][1]

    mejor = {"beneficio": 0, "indices": [], "peso": 0}

    backtrack(0, 0, 0, [], capacidad, items, beneficio_restante, mejor)

    return mejor["beneficio"], mejor["indices"], mejor["peso"]


if __name__ == "__main__":
    # Filas que se van a escribir en el CSV de salida, una por cada
    # archivo procesado con exito.
    filas_csv = []

    for nombre_archivo in ARCHIVOS_MOCHILA:
        ruta_archivo = os.path.join(CARPETA_CASOS, nombre_archivo)

        if not os.path.isfile(ruta_archivo):
            print(f"No se encontró {nombre_archivo}, corré generar_casos.py primero.")
            continue

        # La lectura y el parseo del archivo NO se incluyen en la
        # medicion de tiempo: solo interesa medir el tiempo que tarda el
        # algoritmo de backtracking en si mismo.
        capacidad, items = parsear_mochila(ruta_archivo)
        n = len(items)

        tiempos = []
        for _ in range(REPETICIONES):
            inicio = time.perf_counter()
            beneficio_maximo, indices_elegidos, peso_total = mochila_backtracking(capacidad, items)
            fin = time.perf_counter()
            tiempos.append(fin - inicio)

        tiempo_ejecucion = sum(tiempos) / REPETICIONES

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
                "tiempo_segundos": round(tiempo_ejecucion, 8),
            }
        )

    # Se guardan los resultados en un CSV para poder comparar despues
    # estos tiempos contra los de tiempos_fuerza_bruta.csv.
    if filas_csv:
        with open(RUTA_CSV_SALIDA, "w", newline="") as archivo_csv:
            columnas = ["n", "capacidad", "beneficio_maximo", "peso_usado", "tiempo_segundos"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"\nResultados guardados en {RUTA_CSV_SALIDA}")
    else:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")
