"""
Problema 3 - Mochila resuelta por Programacion Dinamica
Teoria de Algoritmos - TP1

Planteo TRADICIONAL: maximizar el beneficio para una capacidad fija.

Se arma una tabla dp de (n+1) filas por (capacidad+1) columnas, donde
dp[i][w] = beneficio maximo alcanzable usando unicamente los primeros i
elementos, con una mochila de capacidad w. Se completa fila por fila
(elemento por elemento), reutilizando siempre resultados ya calculados
para subproblemas mas chicos en vez de recalcularlos.
"""

import csv
import os
import time

# Archivos de mochila a procesar, en orden creciente de tamano. Se asume
# que estan en la subcarpeta casos/, generados con crear_mochila.py.
ARCHIVOS_MOCHILA = [
    "mochila100.txt",
    "mochila200.txt",
    "mochila300.txt",
    "mochila400.txt",
    "mochila500.txt",
]

# Carpeta donde vive este script y subcarpeta donde estan los archivos de
# entrada. El CSV de salida se sigue guardando junto al script.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

# Nombre del CSV donde se van a guardar los resultados (uno por archivo
# procesado), para poder comparar despues contra los otros enfoques.
NOMBRE_CSV_SALIDA = "tiempos_pd_tradicional.csv"
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


def reconstruir_solucion(dp, items, capacidad):
    """
    Recorre la tabla dp "hacia atras" para reconstruir que elementos se usaron en la solucion optima: 
    parte de dp[n][capacidad] y para cada elemento se fija si el beneficio cambio al considerarlo o no.

        - Si dp[i][w] == dp[i-1][w]: el elemento i no se uso, se baja una fila con la misma capacidad w.
        - Si dp[i][w] != dp[i-1][w]: el elemento i se uso, se lo agrega a la lista y se descuenta su peso 
                                     de w antes de subir una fila.
    """
    n = len(items)
    elegidos = []
    w = capacidad

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            peso_i, _ = items[i - 1]
            elegidos.append(i - 1)
            w -= peso_i

    elegidos.reverse()
    return elegidos


def mochila_dp_maximizar_beneficio(capacidad, items):
    
    n = len(items)

    # dp[i][w] = beneficio maximo usando los primeros i elementos con capacidad w. 
    # Caso base: sin elementos considerados, o sin capacidad, el beneficio es 0.
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_i, beneficio_i = items[i - 1]
        for w in range(capacidad + 1):
            if peso_i <= w:
                # Se elije el maximo entre no agarrar el objeto o si agarrarlo.
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - peso_i] + beneficio_i)
            else:
                dp[i][w] = dp[i - 1][w]

    mejor_beneficio = dp[n][capacidad]
    mejores_indices = reconstruir_solucion(dp, items, capacidad)
    mejor_peso = sum(items[i][0] for i in mejores_indices)

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
        # algoritmo de programacion dinamica en si mismo.
        capacidad, items = parsear_mochila(ruta_archivo)
        n = len(items)

        inicio = time.perf_counter()
        beneficio_maximo, indices_elegidos, peso_total = mochila_dp_maximizar_beneficio(capacidad, items)
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