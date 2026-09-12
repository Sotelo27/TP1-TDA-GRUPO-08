"""
Problema 1 - Graficos de tiempos: Fuerza Bruta vs Backtracking
Teoria de Algoritmos - TP1

Este script lee los tiempos medidos que generaron solucion_fuerza_bruta.py
(tiempos_fuerza_bruta.csv) y solucion_backtracking.py (tiempos_backtracking.csv),
ajusta una curva teorica a cada conjunto de mediciones segun la complejidad
esperada de cada algoritmo, y genera tres graficos en PNG para usar en el
informe:

    grafico_fuerza_bruta.png   -> tiempo medido vs curva teorica c * n * 2^n
    grafico_backtracking.png   -> tiempo medido vs curva teorica c * 2^n
    grafico_comparativo.png    -> ambos tiempos medidos superpuestos (log)

No corre ningun algoritmo: solo lee los CSV ya generados y grafica.
"""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")

RUTA_CSV_FUERZA_BRUTA = os.path.join(CARPETA_SCRIPT, "tiempos_fuerza_bruta.csv")
RUTA_CSV_BACKTRACKING = os.path.join(CARPETA_SCRIPT, "tiempos_backtracking.csv")


def leer_csv_tiempos(ruta_csv):
    """
    Lee un CSV con columnas n,capacidad,beneficio_maximo,peso_usado,tiempo_segundos
    (el formato que generan solucion_fuerza_bruta.py y solucion_backtracking.py) y
    devuelve dos arrays de numpy: los valores de n y los tiempos en segundos,
    ordenados por n.
    """
    valores_n = []
    valores_tiempo = []

    with open(ruta_csv, "r", newline="") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            valores_n.append(int(fila["n"]))
            valores_tiempo.append(float(fila["tiempo_segundos"]))

   
    orden = np.argsort(valores_n)
    n = np.array(valores_n)[orden]
    tiempo = np.array(valores_tiempo)[orden]

    return n, tiempo


def ajustar_constante(n, tiempo_medido, f):
    """
    Ajusta por minimos cuadrados, forzando el ajuste a pasar por el origen,
    la constante c de un modelo teorico tiempo(n) = c * f(n).

    Minimizar sum((tiempo_medido - c*f(n))**2) respecto de c da:
        c = sum(tiempo_medido * f(n)) / sum(f(n)**2)

    Esta c es justamente la constante que hay que citar en el informe de
    resultados como "constante del modelo teorico ajustado" para cada
    algoritmo.
    """
    valores_f = f(n)
    c = np.sum(tiempo_medido * valores_f) / np.sum(valores_f ** 2)
    return c


def graficar_medido_vs_teorico(n, tiempo_medido, f, c, etiqueta_teorica, titulo, ruta_salida):
    """
    Genera y guarda un grafico con dos curvas: los tiempos medidos (con
    marcadores) y la curva teorica c*f(n) (punteada), para un mismo n.
    """
    n_ordenado = np.sort(n)
    tiempo_teorico = c * f(n_ordenado)

    plt.figure()
    plt.plot(n, tiempo_medido, marker="o", label="Tiempo medido")
    plt.plot(n_ordenado, tiempo_teorico, linestyle="--", label=etiqueta_teorica)
    plt.title(titulo)
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()
    plt.savefig(ruta_salida)
    plt.show()


if __name__ == "__main__":
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

    # --- Fuerza bruta: complejidad teorica O(n * 2^n) ---
    n_fb, tiempo_fb = leer_csv_tiempos(RUTA_CSV_FUERZA_BRUTA)
    f_fuerza_bruta = lambda n: n * 2.0 ** n
    c_fuerza_bruta = ajustar_constante(n_fb, tiempo_fb, f_fuerza_bruta)

    graficar_medido_vs_teorico(
        n_fb,
        tiempo_fb,
        f_fuerza_bruta,
        c_fuerza_bruta,
        etiqueta_teorica="Curva teórica ajustada (O(n·2^n))",
        titulo="Fuerza bruta: tiempo medido vs. curva teórica",
        ruta_salida=os.path.join(CARPETA_GRAFICOS, "grafico_fuerza_bruta.png"),
    )

    # --- Backtracking: complejidad teorica en el peor caso O(2^n) ---
    n_bt, tiempo_bt = leer_csv_tiempos(RUTA_CSV_BACKTRACKING)
    g_backtracking = lambda n: 2.0 ** n
    c_backtracking = ajustar_constante(n_bt, tiempo_bt, g_backtracking)

    graficar_medido_vs_teorico(
        n_bt,
        tiempo_bt,
        g_backtracking,
        c_backtracking,
        etiqueta_teorica="Curva teórica ajustada (O(2^n))",
        titulo="Backtracking: tiempo medido vs. curva teórica",
        ruta_salida=os.path.join(CARPETA_GRAFICOS, "grafico_backtracking.png"),
    )

    # --- Comparativo: ambos tiempos medidos superpuestos, en escala log ---
    # Se usa escala logaritmica en el eje y porque los tiempos de
    # backtracking son ordenes de magnitud menores que los de fuerza
    # bruta, y en escala lineal la curva de backtracking se veria
    # practicamente pegada al eje x.
    plt.figure()
    plt.plot(n_fb, tiempo_fb, marker="o", label="Fuerza bruta")
    plt.plot(n_bt, tiempo_bt, marker="o", label="Backtracking")
    plt.yscale("log")
    plt.title("Comparación fuerza bruta vs. backtracking (escala logarítmica)")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_comparativo.png"))
    plt.show()

    # Constantes ajustadas: son las que van citadas en el informe de
    # resultados para justificar el modelo teorico de cada algoritmo.
    print(f"Constante ajustada fuerza bruta  (tiempo aprox. c * n * 2^n): c = {c_fuerza_bruta:.6e}")
    print(f"Constante ajustada backtracking (tiempo aprox. c * 2^n):     c = {c_backtracking:.6e}")
