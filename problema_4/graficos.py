import csv
import os

import matplotlib.pyplot as plt
import numpy as np

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_SCRIPT, "tiempos_pulp.csv")
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")

def leer_tiempos():
    with open(RUTA_CSV, "r") as archivo_csv:
        filas = list(csv.DictReader(archivo_csv))
    n = np.array([int(fila["n"]) for fila in filas], dtype=float)
    tiempos = np.array([float(fila["tiempo_segundos"]) for fila in filas])
    return n, tiempos

if __name__ == "__main__":
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    n, tiempos = leer_tiempos()

    A = (n * np.log2(n))[:, None]
    c = np.linalg.lstsq(A, tiempos, rcond=None)[0][0]
    xs = np.linspace(n.min(), n.max(), 400)

    plt.figure(figsize=(7, 4.5))
    plt.plot(n, tiempos, "o-", label="Tiempo medido")
    plt.plot(xs, c * xs * np.log2(xs), "--", label="Curva de ajuste (c·n·log n)")
    plt.title("Programación Lineal (PuLP): tiempo medido vs. curva de ajuste")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_pulp.png"), dpi=150)
    plt.close()
    print(f"Ajuste: c = {c:.3e}")

    print(f"Graficos guardados en {CARPETA_GRAFICOS}")