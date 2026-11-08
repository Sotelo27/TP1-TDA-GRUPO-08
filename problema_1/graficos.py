"""
Problema 1 - Graficos: Algoritmo aproximado de Sahni (1975)
Teoria de Algoritmos - TP2

Lee tiempos_sahni.csv y genera, sin correr ningun algoritmo:
- por cada k, el tiempo medido contra la curva teorica c * n^(k+1);
- la distancia al optimo de Sahni y de las dos cotas superiores.
"""

import csv
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")
RUTA_CSV = os.path.join(CARPETA_SCRIPT, "tiempos_sahni.csv")

K_COMPARACION = 2

COLOR_MEDIDO = "#2a78d6"
COLOR_TEORICO = "#eb6834"
COLOR_CATEGORIAS = {
    "Relajación lineal": "#2a78d6",
    "Martello y Toth": "#eb6834",
    f"Sahni (k = {K_COMPARACION})": "#1baf7a",
}
COLOR_TEXTO = "#0b0b0b"
COLOR_TEXTO_SECUNDARIO = "#52514e"
COLOR_GRILLA = "#e4e3df"
COLOR_FONDO = "#fcfcfb"


def leer_filas():
    """Devuelve las filas del CSV con todos sus valores numericos."""
    with open(RUTA_CSV, newline="") as archivo:
        return [
            {clave: float(valor) for clave, valor in fila.items()}
            for fila in csv.DictReader(archivo)
        ]


def ajustar_constante(tiempo, curva):
    """Constante c de tiempo = c * curva, por minimos cuadrados."""
    return float(np.dot(tiempo, curva) / np.dot(curva, curva))


def coeficiente_r2(medido, modelo):
    """Coeficiente de determinacion del modelo contra lo medido."""
    residuo = np.sum((medido - modelo) ** 2)
    total = np.sum((medido - np.mean(medido)) ** 2)
    return 1 - residuo / total


def preparar_ejes(ax, titulo, etiqueta_y):
    ax.set_facecolor(COLOR_FONDO)
    ax.set_title(titulo, color=COLOR_TEXTO, loc="left", fontsize=13, pad=12)
    ax.set_xlabel("n (cantidad de elementos)", color=COLOR_TEXTO_SECUNDARIO)
    ax.set_ylabel(etiqueta_y, color=COLOR_TEXTO_SECUNDARIO)
    ax.grid(axis="y", color=COLOR_GRILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=COLOR_TEXTO_SECUNDARIO, length=0)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(COLOR_GRILLA)


def guardar(fig, nombre):
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    ruta = os.path.join(CARPETA_GRAFICOS, nombre)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150, facecolor=COLOR_FONDO)
    plt.close(fig)
    print(f"Grafico guardado en {ruta}")


def graficar_tiempos(filas, k):
    """Grafica tiempo medido y curva teorica c * n^(k+1) para un k."""
    filas_k = sorted((f for f in filas if f["k"] == k), key=lambda f: f["n"])
    n = np.array([f["n"] for f in filas_k])
    medido = np.array([f["tiempo_segundos"] for f in filas_k])

    exponente = k + 1
    c = ajustar_constante(medido, n**exponente)
    r2 = coeficiente_r2(medido, c * n**exponente)
    print(f"k={k}: c={c:.3e}, R2={r2:.5f}")

    n_curva = np.linspace(n.min(), n.max(), 300)

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_FONDO)
    preparar_ejes(ax, f"Sahni con k = {k}: tiempo medido y curva teórica", "Tiempo (segundos)")
    ax.plot(
        n_curva, c * n_curva**exponente, color=COLOR_TEORICO, linewidth=2,
        label=f"Teórica: {c:.2e} · n^{exponente}  (R² = {r2:.4f})",
    )
    ax.plot(
        n, medido, linestyle="none", marker="o", markersize=8, color=COLOR_MEDIDO,
        markeredgecolor=COLOR_FONDO, markeredgewidth=1.5, label="Medido",
    )
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, labelcolor=COLOR_TEXTO_SECUNDARIO, loc="upper left")
    guardar(fig, f"grafico_tiempos_k{k}.png")


def graficar_comparacion(filas):
    """Grafica la distancia porcentual al optimo de Sahni y de las cotas."""
    filas_k = sorted((f for f in filas if f["k"] == K_COMPARACION), key=lambda f: f["n"])
    n = np.array([f["n"] for f in filas_k])
    optimo = np.array([f["optimo"] for f in filas_k])

    series = {
        "Relajación lineal": "cota_relajacion_lineal",
        "Martello y Toth": "cota_martello_toth",
        f"Sahni (k = {K_COMPARACION})": "beneficio_sahni",
    }
    marcadores = {"Relajación lineal": "o", "Martello y Toth": "s"}

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_FONDO)
    preparar_ejes(ax, "Distancia al óptimo exacto", "Diferencia con el óptimo (%)")
    ax.axhline(0, color=COLOR_TEXTO_SECUNDARIO, linewidth=1.2, label="Óptimo exacto")

    for nombre, columna in series.items():
        valores = np.array([f[columna] for f in filas_k])
        ax.plot(
            n, 100 * (valores - optimo) / optimo, color=COLOR_CATEGORIAS[nombre], linewidth=2,
            marker=marcadores.get(nombre, "^"), markersize=8,
            markeredgecolor=COLOR_FONDO, markeredgewidth=1.5, label=nombre,
        )

    # Las diferencias van de 0,001 % a casi 2 %: una escala lineal oculta las chicas.
    ax.set_yscale("symlog", linthresh=0.01)
    ax.set_yticks([-0.1, -0.01, 0, 0.01, 0.1, 1])
    ax.set_yticklabels(["-0,1", "-0,01", "0", "0,01", "0,1", "1"])
    ax.set_ylim(-0.1, 3)

    ax.legend(frameon=False, labelcolor=COLOR_TEXTO_SECUNDARIO, loc="upper right")
    guardar(fig, "grafico_comparacion_cotas.png")


def main():
    filas = leer_filas()
    for k in sorted({int(fila["k"]) for fila in filas}):
        graficar_tiempos(filas, k)
    graficar_comparacion(filas)


if __name__ == "__main__":
    main()
