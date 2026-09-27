"""
Problema 3 - Mochila resuelta por Programacion Dinamica
Teoria de Algoritmos - TP1

Planteo ALTERNATIVO: minimizar el peso para un beneficio fijo.

Se arma una tabla dp de (n + 1) filas por (beneficio_total + 1) columnas,
donde dp[i][b] = peso minimo necesario para lograr exactamente un
beneficio b, usando unicamente los primeros i elementos (beneficio_total
es la suma de los beneficios de todos los elementos, el mayor beneficio
que tendria sentido pedir). Se completa fila por fila, igual que en el
planteo tradicional, pero invirtiendo los roles de peso y beneficio en la
recurrencia.
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
NOMBRE_CSV_SALIDA = "tiempos_pd_alternativa.csv"
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, NOMBRE_CSV_SALIDA)

# Se usa infinito para marcar un beneficio inalcanzable.
INFINITO = float("inf")


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


def reconstruir_solucion(dp, items, mejor_beneficio):
    """
    Recorre la tabla dp "hacia atras" para reconstruir que elementos se usaron para lograr mejor_beneficio: 
    parte de dp[n][mejor_beneficio] y para cada elemento se fija si el peso minimo cambio al considerarlo.

        - Si dp[i][b] == dp[i-1][b]: el elemento i no se uso, se baja una fila con el mismo beneficio b.
        - Si dp[i][b] != dp[i-1][b]: el elemento i se uso, se lo agrega a la lista y se descuenta su 
                                     beneficio de b antes de subir fila.
    """
    n = len(items)
    elegidos = []
    b = mejor_beneficio

    for i in range(n, 0, -1):
        if dp[i][b] != dp[i-1][b]:
            _, beneficio_i = items[i-1]
            elegidos.append(i-1)
            b -= beneficio_i

    elegidos.reverse()
    return elegidos


def mochila_dp_minimizar_peso(capacidad, items):

    n = len(items)
    beneficio_total = sum(beneficio for _, beneficio in items)

    # dp[i][b] = peso minimo para lograr el beneficio b usando los primeros i elementos. 
    # Usamos INFINITO para los beneficios inalcanzables con los elementos disponibles.
    dp = [[INFINITO] * (beneficio_total + 1) for _ in range(n + 1)]
    # Caso base: con cero elementos elegidos se logra beneficio 0 a peso 0.
    for i in range(n + 1):
        dp[i][0] = 0

    for i in range(1, n + 1):
        peso_i, beneficio_i = items[i-1]
        for b in range(beneficio_total + 1):
            if beneficio_i <= b:
                # Seleccionamos el minimo entre no agarrar el elemento i o agarrarlo.
                dp[i][b] = min(dp[i-1][b], dp[i-1][b - beneficio_i] + peso_i)
            else:
                dp[i][b] = dp[i-1][b]

    mejor_beneficio = 0
    for b in range(beneficio_total, -1, -1):
        if dp[n][b] <= capacidad:
            mejor_beneficio = b
            break

    mejores_indices = reconstruir_solucion(dp, items, mejor_beneficio)
    mejor_peso = dp[n][mejor_beneficio]

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
        beneficio_maximo, indices_elegidos, peso_total = mochila_dp_minimizar_peso(capacidad, items)
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

    # Se guardan los resultados en un CSV para poder comparar despues
    # estos tiempos contra los de los demas enfoques.
    if filas_csv:
        with open(RUTA_CSV_SALIDA, "w", newline="") as archivo_csv:
            columnas = ["n", "capacidad", "beneficio_maximo", "peso_usado", "tiempo_segundos"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"\nResultados guardados en {RUTA_CSV_SALIDA}")
    else:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")