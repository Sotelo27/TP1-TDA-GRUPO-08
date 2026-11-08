"""
Problema 1 - Cotas superiores y optimo exacto
Teoria de Algoritmos - TP2

Notacion de clase (Martello y Toth, 1990): p = beneficio, w = peso, c =
capacidad, con los elementos ordenados por p/w decreciente. s es el elemento
critico (el primero que no entra) y c_barra la capacidad residual luego de los
elementos anteriores a s.

Las instancias se representan como en los archivos de datos: items es una
lista de tuplas (w, p), es decir (peso, beneficio).

Las dos cotas se calculan en O(n log n) por el ordenamiento y devuelven enteros:
como los beneficios son enteros, el optimo es entero y se puede tomar el piso.
"""

import numpy as np


def _elemento_critico(c, items):
    """
    Ordena por p/w decreciente los elementos con w <= c y busca el critico.
    Filtrar antes asegura que el primero siempre entra, es decir s >= 1 con
    posiciones desde 0, y que por lo tanto existe el elemento s-1.

    Devuelve (ordenados, s, suma_p, c_barra), donde suma_p es la suma de los
    beneficios anteriores a s. Si entran todos no hay critico y s es None.
    """
    ordenados = sorted(
        (item for item in items if item[0] <= c),
        key=lambda item: item[1] / item[0],
        reverse=True,
    )

    suma_p = 0
    c_barra = c
    for s, (w_j, p_j) in enumerate(ordenados):
        if w_j > c_barra:
            return ordenados, s, suma_p, c_barra
        c_barra -= w_j
        suma_p += p_j
    return ordenados, None, suma_p, c_barra


def cota_relajacion_lineal(c, items):
    """
    Cota 1: relajacion lineal. Equivale a la mochila fraccionaria, que corta
    al elemento critico. Devuelve el piso del optimo continuo:

        suma_p + piso(c_barra * p_s / w_s)

    Parametros: c (entero), items (lista de tuplas (w, p)).
    """
    ordenados, s, suma_p, c_barra = _elemento_critico(c, items)
    if s is None:
        return suma_p

    w_s, p_s = ordenados[s]
    return suma_p + c_barra * p_s // w_s


def cota_martello_toth(c, items):
    """
    Cota 2: Martello y Toth (1990). En vez de partir al critico, considera
    las dos alternativas posibles y se queda con la mayor:

        el critico vale 0:  W1 = suma_p + piso(c_barra * p[s+1] / w[s+1])
        el critico vale 1:  W2 = suma_p + piso(p[s] - (w[s] - c_barra) * p[s-1] / w[s-1])
        U2 = max(W1, W2)

    Si el critico es el ultimo no existe s+1 y W1 no tiene termino extra.

    Parametros: c (entero), items (lista de tuplas (w, p)).
    """
    ordenados, s, suma_p, c_barra = _elemento_critico(c, items)
    if s is None:
        return suma_p

    w_s, p_s = ordenados[s]

    W1 = suma_p
    if s + 1 < len(ordenados):
        w_sig, p_sig = ordenados[s + 1]
        W1 += c_barra * p_sig // w_sig

    w_ant, p_ant = ordenados[s - 1]
    W2 = suma_p + (p_s * w_ant - (w_s - c_barra) * p_ant) // w_ant

    U2 = max(W1, W2)
    return U2


def optimo_exacto(c, items):
    """
    Beneficio optimo por Programacion dinamica (Ej 3A del TP1), en O(n * c).
    Usa la misma recurrencia que el TP1. Cada fila se calcula con una operacion
    vectorial de numpy y solo se guarda la anterior, porque interesa el valor.
    """
    fila = np.zeros(c + 1, dtype=np.int64)
    for w_j, p_j in items:
        if w_j <= c:
            fila[w_j:] = np.maximum(fila[w_j:], fila[:-w_j] + p_j)
    return int(fila[c])
