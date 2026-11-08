"""
Problema 1 - Algoritmo aproximado de Sahni (1975)
Teoria de Algoritmos - TP2

Para cada caso de casos/ y cada k compara cuatro valores: resultado de Sahni,
cota de la relajacion lineal, cota de Martello y Toth y optimo exacto.
"""

import os
from itertools import combinations

import cotas
import utilidades

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

K_POR_DEFECTO = 2

# Mayor n en que se corre cada k: el costo crece como n^(k+1).
N_MAXIMO_POR_K = {1: 1000, 2: 400, 3: 120}

CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, "tiempos_sahni.csv")
COLUMNAS_CSV = [
    "n", "capacidad", "k", "beneficio_sahni", "peso_usado",
    "cota_relajacion_lineal", "cota_martello_toth", "optimo", "tiempo_segundos",
]


def _greedy_gs(items, en_M, c_gorro):
    """
    GS(M): parte de la lista ya ordenada por p/w, con los elementos de M ya
    agregados, y prueba los restantes igual que greedy.

    Parametros: items (lista ordenada de tuplas (w, p)), en_M (marca de cada
    posicion) y c_gorro (capacidad que queda luego de M).
    Devuelve (z_g, capacidad que sobra, X).
    """
    z_g = 0
    X = []
    for j, (w_j, p_j) in enumerate(items):
        if not en_M[j] and w_j <= c_gorro:
            z_g += p_j
            c_gorro -= w_j
            X.append(j)
    return z_g, c_gorro, X


def mochila_sahni(c, items, k=K_POR_DEFECTO):
    """
    S(k), algoritmo de Sahni (1975): llama a GS(M) por cada M con |M| <= k cuyo
    peso entre en la mochila y se queda con la mejor solucion. Es O(n^(k+1)) y
    en el peor caso esta a k / (k + 1) del optimo.

    Los elementos con w > c se descartan al inicio: no cambia el resultado,
    porque ningun M que los contenga entra y GS nunca los agregaria.

    Parametros: c (entero), items (lista de tuplas (w, p)), k (entero no negativo).
    Devuelve (beneficio, indices, peso), con indices en la numeracion original.
    """
    orden = sorted(
        (i for i, (w_i, _) in enumerate(items) if w_i <= c),
        key=lambda i: items[i][1] / items[i][0],
        reverse=True,
    )
    ordenados = [items[i] for i in orden]
    en_M = [False] * len(ordenados)

    z_h = 0
    peso_h = 0
    X_h = []

    for tamanio in range(k + 1):
        for M in combinations(range(len(ordenados)), tamanio):
            peso_M = sum(ordenados[j][0] for j in M)
            if peso_M > c:
                continue

            for j in M:
                en_M[j] = True

            z_g, sobrante, X = _greedy_gs(ordenados, en_M, c - peso_M)
            beneficio = z_g + sum(ordenados[j][1] for j in M)

            for j in M:
                en_M[j] = False

            if beneficio > z_h:
                z_h = beneficio
                peso_h = c - sobrante
                X_h = X + list(M)

    indices = sorted(orden[j] for j in X_h)
    return z_h, indices, peso_h


def main():
    filas_csv = []

    for ruta_archivo in utilidades.listar_casos(CARPETA_CASOS):
        capacidad, items = utilidades.parsear_mochila(ruta_archivo)
        n = len(items)
        relajacion = cotas.cota_relajacion_lineal(capacidad, items)
        martello_toth = cotas.cota_martello_toth(capacidad, items)
        optimo = cotas.optimo_exacto(capacidad, items)

        for k, n_maximo in N_MAXIMO_POR_K.items():
            if n > n_maximo:
                continue

            (beneficio, _, peso), tiempo = utilidades.medir(
                lambda c, i: mochila_sahni(c, i, k), capacidad, items
            )
            print(f"n={n:5d} k={k} sahni={beneficio} optimo={optimo} t={tiempo:.4f}s")

            filas_csv.append(
                {
                    "n": n,
                    "capacidad": capacidad,
                    "k": k,
                    "beneficio_sahni": beneficio,
                    "peso_usado": peso,
                    "cota_relajacion_lineal": relajacion,
                    "cota_martello_toth": martello_toth,
                    "optimo": optimo,
                    "tiempo_segundos": round(tiempo, 8),
                }
            )

    utilidades.guardar_csv(RUTA_CSV_SALIDA, COLUMNAS_CSV, filas_csv)


if __name__ == "__main__":
    main()
