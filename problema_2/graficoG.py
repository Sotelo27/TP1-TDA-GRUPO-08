"""
Graficos de tiempos
"""
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")

RUTA_CSV_GREEDY = os.path.join(
    CARPETA_SCRIPT,
    "tiemposG.csv"
)

def leer_csv_tiempos(ruta_csv):

    valores_n = []
    valores_tiempo = []

    with open(ruta_csv, "r", newline="") as archivo_csv:
        lector = csv.DictReader(archivo_csv)

        for fila in lector:
            valores_n.append(int(fila["n"]))
            valores_tiempo.append(
                float(fila["tiempo_segundos"])
            )

    orden = np.argsort(valores_n)

    n = np.array(valores_n)[orden]
    tiempo = np.array(valores_tiempo)[orden]

    return n, tiempo


def ajustar_constante(n, tiempo_medido, f):

    valores_f = f(n)

    c = np.sum(
        tiempo_medido * valores_f
    ) / np.sum(
        valores_f ** 2
    )

    return c


def graficar_medido_vs_teorico(
    n,
    tiempo_medido,
    f,
    c,
    etiqueta_teorica,
    titulo,
    ruta_salida
):

    n_ordenado = np.sort(n)

    tiempo_teorico = c * f(n_ordenado)

    plt.figure()

    plt.plot(
        n,
        tiempo_medido,
        marker="o",
        label="Tiempo medido"
    )

    plt.plot(
        n_ordenado,
        tiempo_teorico,
        linestyle="--",
        label=etiqueta_teorica
    )

    plt.title(titulo)
    plt.xlabel("n = cantidad de objetos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()

    plt.savefig(ruta_salida)

    plt.show()


def main():
    os.makedirs(
        CARPETA_GRAFICOS,
        exist_ok=True
    )
    # ---------------------------------------------------------
    # Greedy: complejidad teorica O(n log n)
    # ---------------------------------------------------------
    n_greedy, tiempo_greedy = leer_csv_tiempos(
        RUTA_CSV_GREEDY
    )
    f_greedy = lambda n: n * np.log2(n)
    c_greedy = ajustar_constante(
        n_greedy,
        tiempo_greedy,
        f_greedy
    )
    graficar_medido_vs_teorico(
        n_greedy,
        tiempo_greedy,
        f_greedy,
        c_greedy,
        etiqueta_teorica="Curva teórica ajustada (O(n·log n))",
        titulo="Greedy: tiempo medido vs. curva teórica",
        ruta_salida=os.path.join(
            CARPETA_GRAFICOS,
            "grafico_greedy.png"
        ),
    )

    print(
        f"Constante ajustada greedy "
        f"(tiempo aprox. c * n * log2(n)): "
        f"c = {c_greedy:.6e}"
    )

main()