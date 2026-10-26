"""
Problema 4 - Mochila resuelta por Programacion Lineal (biblioteca PuLP)
Teoria de Algoritmos - TP1

Se plantea la mochila 0/1 como un problema de Programacion Lineal Entera:

    Variables:    Yi en {0, 1}  (1 = el elemento i entra en la mochila)
    Objetivo:     MAX  suma(beneficio_i * Yi)
    Restriccion:  suma(peso_i * Yi) <= capacidad

PuLP le pasa el modelo al solver CBC (incluido con la biblioteca), que lo
resuelve con el metodo Simplex y Branch and Bound.

Se corren tres experimentos, cada uno con su propio CSV (los casos los
genera generar_casos.py, que usa los mismos valores de n):
    - rango chico  (n = 10, 12, ..., 40)          -> tiempos_pulp_chico.csv
    - rango grande (n = 1000, 2000, ..., 20000)   -> tiempos_pulp_grande.csv
      (5 mochilas distintas por cada n, se promedian sus tiempos)
    - instancias dificiles (extra, n = 10, 12, ..., 40) -> tiempos_pulp_dificil.csv
"""

import csv
import os
import re
import tempfile
import time

import pulp

# Carpeta donde vive este script y subcarpeta donde estan los archivos de
# entrada. Los CSV de salida se guardan junto al script.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")
CARPETA_CASOS_DIFICILES = os.path.join(CARPETA_CASOS, "dificiles")

# Cantidad de mochilas distintas por cada n en el rango grande (tiene que
# coincidir con INSTANCIAS_POR_N de generar_casos.py).
INSTANCIAS_POR_N = 5

# Experimentos a correr: (nombre, grupos de archivos, CSV de salida, repeticiones).
# Cada grupo es la lista de archivos de un mismo n; si tiene varios archivos,
# se promedian sus resultados en una sola fila del CSV.
#   - Rango chico y dificiles: 1 archivo por n, resuelto 5 veces (se promedia
#     para reducir el ruido de la maquina).
#   - Rango grande: 5 mochilas distintas por n, cada una resuelta 1 vez. Aca
#     el ruido principal no es la maquina sino la mochila: CBC tarda distinto
#     segun la instancia, asi que se promedian instancias distintas.
EXPERIMENTOS = [
    (
        "rango chico",
        [[os.path.join(CARPETA_CASOS, f"mochila{n}.txt")] for n in range(10, 41, 2)],
        "tiempos_pulp_chico.csv",
        5,
    ),
    (
        "rango grande",
        [
            [os.path.join(CARPETA_CASOS, f"mochila{n}_{k}.txt") for k in range(1, INSTANCIAS_POR_N + 1)]
            for n in range(1000, 20001, 1000)
        ],
        "tiempos_pulp_grande.csv",
        1,
    ),
    (
        "instancias dificiles",
        [[os.path.join(CARPETA_CASOS_DIFICILES, f"mochila_dificil{n}.txt")] for n in range(10, 41, 2)],
        "tiempos_pulp_dificil.csv",
        5,
    ),
]

# Archivo temporal donde CBC escribe su log, del que se extrae la cantidad de
# nodos de Branch and Bound y el tiempo que tardo CBC internamente.
RUTA_LOG_CBC = os.path.join(tempfile.gettempdir(), "tda_tp1_cbc.log")

COLUMNAS_CSV = [
    "n",
    "capacidad",
    "estado",
    "beneficio_maximo",
    "peso_usado",
    "nodos_bb",
    "tiempo_construccion",
    "tiempo_resolucion",
    "tiempo_cbc_interno",
    "tiempo_total",
]


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

def construir_modelo(capacidad, items):

    n = len(items)

    # Se crea el problema de maximizacion.
    problema = pulp.LpProblem("Mochila", pulp.LpMaximize)

    # Variables de decision bivalentes: y[i] = 1 si el elemento i entra en la mochila, 0 si no.
    y = [pulp.LpVariable(f"y_{i}", cat=pulp.LpBinary) for i in range(n)]

    # Funcion objetivo: maximizar la suma de los beneficios de los elementos elegidos.
    problema += pulp.lpSum(items[i][1] * y[i] for i in range(n))

    # Restriccion: la suma de los pesos de los elementos elegidos no puede superar la capacidad.
    problema += pulp.lpSum(items[i][0] * y[i] for i in range(n)) <= capacidad

    return problema, y

def resolver_modelo(problema, y, items, ruta_log=None):

    # Se resuelve con el solver CBC (msg=False para que no imprima su log;
    # si se pasa ruta_log, CBC lo escribe en ese archivo).
    problema.solve(pulp.PULP_CBC_CMD(msg=False, logPath=ruta_log))

    # Se leen los elementos cuya variable quedo en 1.
    mejores_indices = [i for i in range(len(items)) if round(y[i].value()) == 1]
    mejor_beneficio = sum(items[i][1] for i in mejores_indices)
    mejor_peso = sum(items[i][0] for i in mejores_indices)

    return mejor_beneficio, mejores_indices, mejor_peso

def mochila_pulp(capacidad, items):
    problema, y = construir_modelo(capacidad, items)
    return resolver_modelo(problema, y, items)

def leer_log_cbc(ruta_log):
    """
    Extrae del log de CBC la cantidad de nodos de Branch and Bound
    explorados ("Enumerated nodes") y el tiempo total que tardo CBC
    internamente, medido por el propio CBC ("Total time ... Wallclock").
    Si no encuentra alguno de los dos datos, devuelve None en su lugar.
    """
    with open(ruta_log, "r", errors="ignore") as archivo:
        texto = archivo.read()

    nodos = re.findall(r"Enumerated nodes:\s+(\d+)", texto)
    tiempo = re.findall(r"Total time \(CPU seconds\):\s+[\d.]+\s+\(Wallclock seconds\):\s+([\d.]+)", texto)

    nodos_bb = int(nodos[-1]) if nodos else None
    tiempo_cbc = float(tiempo[-1]) if tiempo else None
    return nodos_bb, tiempo_cbc

def medir_instancia(capacidad, items, repeticiones):
    """
    Resuelve la instancia "repeticiones" veces y devuelve un diccionario con
    los resultados y los tiempos promedio de construccion del modelo, de
    resolucion (prob.solve) y total, mas los datos extraidos del log de CBC.
    """
    tiempos_construccion = []
    tiempos_resolucion = []
    tiempos_cbc = []

    for _ in range(repeticiones):
        if os.path.exists(RUTA_LOG_CBC):
            os.remove(RUTA_LOG_CBC)

        inicio = time.perf_counter()
        problema, y = construir_modelo(capacidad, items)
        medio = time.perf_counter()
        beneficio_maximo, indices_elegidos, peso_total = resolver_modelo(problema, y, items, RUTA_LOG_CBC)
        fin = time.perf_counter()

        tiempos_construccion.append(medio - inicio)
        tiempos_resolucion.append(fin - medio)

        nodos_bb, tiempo_cbc = leer_log_cbc(RUTA_LOG_CBC)
        if tiempo_cbc is not None:
            tiempos_cbc.append(tiempo_cbc)

    tiempo_construccion = sum(tiempos_construccion) / repeticiones
    tiempo_resolucion = sum(tiempos_resolucion) / repeticiones

    return {
        "n": len(items),
        "capacidad": capacidad,
        "estado": pulp.LpStatus[problema.status],
        "beneficio_maximo": beneficio_maximo,
        "peso_usado": peso_total,
        "nodos_bb": nodos_bb,
        "tiempo_construccion": round(tiempo_construccion, 8),
        "tiempo_resolucion": round(tiempo_resolucion, 8),
        "tiempo_cbc_interno": round(sum(tiempos_cbc) / len(tiempos_cbc), 8) if tiempos_cbc else None,
        "tiempo_total": round(tiempo_construccion + tiempo_resolucion, 8),
    }

def promediar_filas(filas):
    """
    Junta en una sola fila los resultados de varias mochilas del mismo n:
    promedia los valores numericos y deja estado = Optimal solo si todas
    las mochilas terminaron en Optimal.
    """
    if len(filas) == 1:
        return filas[0]

    promedio = {"n": filas[0]["n"], "capacidad": filas[0]["capacidad"]}
    estados = {fila["estado"] for fila in filas}
    promedio["estado"] = "Optimal" if estados == {"Optimal"} else "/".join(sorted(estados))

    for columna in COLUMNAS_CSV:
        if columna in promedio:
            continue
        valores = [fila[columna] for fila in filas if fila[columna] is not None]
        promedio[columna] = round(sum(valores) / len(valores), 8) if valores else None
    return promedio

def correr_experimento(nombre, grupos_archivos, nombre_csv, repeticiones):
    print(f"\n=== Experimento: {nombre} ===")

    filas_csv = []
    for rutas_archivos in grupos_archivos:
        filas_grupo = []
        for ruta_archivo in rutas_archivos:
            if not os.path.isfile(ruta_archivo):
                print(f"No se encontró {os.path.basename(ruta_archivo)}, corré generar_casos.py primero.")
                continue

            # La lectura y el parseo del archivo NO se incluyen en la medicion.
            capacidad, items = parsear_mochila(ruta_archivo)
            filas_grupo.append(medir_instancia(capacidad, items, repeticiones))

        if not filas_grupo:
            continue
        fila = promediar_filas(filas_grupo)

        print(
            f"n={fila['n']} | mochilas={len(filas_grupo)} | estado={fila['estado']} "
            f"| beneficio_maximo={fila['beneficio_maximo']} | peso_usado={fila['peso_usado']} "
            f"| nodos_bb={fila['nodos_bb']} | construccion={fila['tiempo_construccion']:.6f} s "
            f"| resolucion={fila['tiempo_resolucion']:.6f} s | total={fila['tiempo_total']:.6f} s"
        )
        filas_csv.append(fila)

    # Se guardan los resultados en un CSV para poder graficarlos despues
    if filas_csv:
        ruta_csv = os.path.join(CARPETA_SCRIPT, nombre_csv)
        with open(ruta_csv, "w", newline="") as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"Resultados guardados en {ruta_csv}")
    else:
        print("No se proceso ningun archivo, no se genero el CSV.")

if __name__ == "__main__":

    # Calentamiento: la primera resolución con PuLP es más lenta que las demás
    # porque el sistema todavía no tiene en memoria el ejecutable del solver CBC
    # (y PuLP termina de inicializarse). Se resuelve una mochila chica SIN medir
    # el tiempo, para que ese costo de "arranque en frío" no se sume a la
    # primera mochila medida.
    mochila_pulp(50, [(10, 60), (20, 100), (30, 120)])

    inicio_corrida = time.perf_counter()
    for nombre, grupos_archivos, nombre_csv, repeticiones in EXPERIMENTOS:
        correr_experimento(nombre, grupos_archivos, nombre_csv, repeticiones)

    print(f"\nCorrida completa: {time.perf_counter() - inicio_corrida:.1f} s")