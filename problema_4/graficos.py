"""
Problema 4 - Graficos de tiempos: Programacion Lineal (PuLP + CBC)
Teoria de Algoritmos - TP1

Lee los CSV que genera solucion.py y contrasta los tiempos medidos contra
la complejidad teorica:

    grafico_pulp_teorico_2n.png      -> rango chico: tiempo medido vs. c * 2^n (eje y log)
    grafico_pulp_modelos.png         -> rango grande: tiempo medido vs. c*n, c*n*log n, c*n^2 (log-log)
    grafico_pulp_construccion.png    -> rango grande: construccion del modelo vs. resolucion
    grafico_pulp_dificiles.png       -> extra: instancias de crear_mochila.py vs. dificiles

No corre ningun algoritmo: solo lee los CSV ya generados y grafica.
"""

import csv
import math
import os

import matplotlib.pyplot as plt
import numpy as np

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")

RUTA_CSV_CHICO = os.path.join(CARPETA_SCRIPT, "tiempos_pulp_chico.csv")
RUTA_CSV_GRANDE = os.path.join(CARPETA_SCRIPT, "tiempos_pulp_grande.csv")
RUTA_CSV_DIFICIL = os.path.join(CARPETA_SCRIPT, "tiempos_pulp_dificil.csv")


def leer_csv(ruta_csv):
    """
    Lee un CSV generado por solucion.py y devuelve un diccionario
    {columna: array de numpy} con las columnas numericas, ordenado por n.
    """
    with open(ruta_csv, "r", newline="") as archivo_csv:
        filas = list(csv.DictReader(archivo_csv))
    filas.sort(key=lambda fila: int(fila["n"]))

    datos = {}
    for columna in ["n", "nodos_bb", "tiempo_construccion", "tiempo_resolucion", "tiempo_cbc_interno", "tiempo_total"]:
        datos[columna] = np.array([float(fila[columna]) if fila[columna] != "" else np.nan for fila in filas])
    return datos


def ajustar_constante(n, tiempo_medido, f):
    """
    Ajusta por minimos cuadrados, forzando el ajuste a pasar por el origen,
    la constante c de un modelo teorico tiempo(n) = c * f(n):
        c = sum(tiempo_medido * f(n)) / sum(f(n)**2)
    """
    valores_f = f(n)
    return np.sum(tiempo_medido * valores_f) / np.sum(valores_f ** 2)


def errores_ajuste(tiempo_medido, tiempo_modelo):
    """
    Devuelve (R^2, error relativo medio) de un modelo contra los tiempos
    medidos. R^2 cerca de 1 y error relativo cerca de 0 = buen ajuste.
    """
    ss_res = np.sum((tiempo_medido - tiempo_modelo) ** 2)
    ss_tot = np.sum((tiempo_medido - np.mean(tiempo_medido)) ** 2)
    r2 = 1 - ss_res / ss_tot
    error_relativo = np.mean(np.abs(tiempo_medido - tiempo_modelo) / tiempo_medido)
    return r2, error_relativo


def grafico_teorico_2n(datos):
    """
    Rango chico: tiempo medido contra la curva teorica c * 2^n. La constante
    se ajusta por minimos cuadrados en escala logaritmica, con la pendiente
    fija en log 2:
        log T = log c + n * log 2   =>   log c = promedio(log T - n * log 2)
    Todo se calcula en logaritmos para que 2^n no desborde.
    """
    n = datos["n"]
    tiempo = datos["tiempo_total"]

    log_c = np.mean(np.log(tiempo) - n * math.log(2))
    tiempo_teorico = np.exp(log_c + n * math.log(2))

    # Ajuste exponencial libre (log T = a + b*n): la base empirica e^b
    # indica cuanto se multiplica el tiempo medido por cada elemento extra.
    b, a = np.polyfit(n, np.log(tiempo), 1)
    base_empirica = math.exp(b)

    plt.figure()
    plt.plot(n, tiempo, marker="o", label="Tiempo medido (total)")
    plt.plot(n, tiempo_teorico, linestyle="--", label="Curva teórica ajustada (O(2^n))")
    plt.yscale("log")
    plt.title("PuLP: tiempo medido vs. complejidad teórica O(2^n)")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos, escala logarítmica)")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_pulp_teorico_2n.png"), dpi=150)
    plt.close()

    print("=== Rango chico: contraste contra O(2^n) ===")
    print(f"Constante ajustada c*2^n (en log): c = {math.exp(log_c):.6e}")
    print(f"Tiempo medido: de {tiempo.min():.4f} s a {tiempo.max():.4f} s "
          f"(x{tiempo[-1] / tiempo[0]:.2f} entre n={int(n[0])} y n={int(n[-1])})")
    print(f"La curva 2^n crece x{2.0 ** (n[-1] - n[0]):.3e} en el mismo rango")
    print(f"Base empirica del ajuste exponencial libre: {base_empirica:.4f} por elemento (teorica: 2)")


def grafico_modelos(datos):
    """
    Rango grande, ejes log-log: tiempo medido contra los ajustes c*n,
    c*n*log n y c*n^2. Ademas calcula la pendiente empirica k de la recta
    en log-log (T aprox. c * n^k) y el error de cada modelo.
    """
    n = datos["n"]
    tiempo = datos["tiempo_total"]

    modelos = [
        ("c·n", "c*n", lambda x: x),
        ("c·n·log n", "c*n*log n", lambda x: x * np.log2(x)),
        ("c·n²", "c*n^2", lambda x: x ** 2),
    ]

    k, log_c_k = np.polyfit(np.log(n), np.log(tiempo), 1)

    plt.figure()
    plt.plot(n, tiempo, marker="o", linestyle="none", label="Tiempo medido (total)")

    print("\n=== Rango grande: comparacion de modelos de crecimiento ===")
    print(f"Pendiente en log-log (T aprox. c*n^k): k = {k:.4f}, c = {math.exp(log_c_k):.6e}")

    resultados = []
    for nombre, nombre_consola, f in modelos:
        c = ajustar_constante(n, tiempo, f)
        r2, error_relativo = errores_ajuste(tiempo, c * f(n))
        resultados.append((nombre_consola, c, r2, error_relativo))
        plt.plot(n, c * f(n), linestyle="--", label=f"Ajuste {nombre} (R² = {r2:.3f})")
        print(f"Modelo {nombre_consola:10s}: c = {c:.6e} | R^2 = {r2:.4f} | error relativo medio = {error_relativo * 100:.1f} %")

    mejor = max(resultados, key=lambda r: r[2])
    print(f"Mejor ajuste por R^2: {mejor[0]}")

    # 2^n no se puede dibujar en este rango: 2^1000 ya es del orden de 10^301.
    exponente_10 = n[0] * math.log10(2)
    print(f"La curva c*2^n no se grafica en este rango: 2^{int(n[0])} es del orden de 10^{int(exponente_10)}")

    plt.xscale("log")
    plt.yscale("log")
    plt.title("PuLP: comparación de modelos de crecimiento (log-log)")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True, which="both")
    plt.legend(title=f"pendiente empírica k = {k:.2f}")
    plt.figtext(0.5, 0.01, f"c·2^n no se grafica: 2^{int(n[0])} ≈ 10^{int(exponente_10)}",
                ha="center", fontsize=8)
    plt.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_pulp_modelos.png"), dpi=150)
    plt.close()


def grafico_construccion(datos_chico, datos_grande):
    """
    Rango grande: tiempo de construccion del modelo y de resolucion
    (prob.solve) apilados, mas el tiempo que CBC reporta internamente. La
    diferencia entre resolucion y CBC interno es el costo de PuLP de
    escribir el archivo del modelo, lanzar el ejecutable de CBC y leer la
    solucion.
    """
    n = datos_grande["n"]
    construccion = datos_grande["tiempo_construccion"]
    resolucion = datos_grande["tiempo_resolucion"]
    cbc_interno = datos_grande["tiempo_cbc_interno"]

    ancho = 600
    plt.figure()
    plt.bar(n, construccion, width=ancho, label="Construcción del modelo")
    plt.bar(n, resolucion, width=ancho, bottom=construccion, label="Resolución (prob.solve)")
    plt.plot(n, cbc_interno, marker="o", color="black", label="Tiempo interno de CBC")
    plt.title("PuLP: construcción del modelo vs. resolución")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True, axis="y")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_pulp_construccion.png"), dpi=150)
    plt.close()

    total = datos_grande["tiempo_total"]
    print("\n=== Construccion vs. resolucion ===")
    print(f"Rango grande: construccion = {np.mean(construccion / total) * 100:.1f} % del total, "
          f"resolucion = {np.mean(resolucion / total) * 100:.1f} % (promedio entre instancias)")
    print(f"Rango grande: CBC interno = {np.nanmean(cbc_interno / total) * 100:.1f} % del total")
    print(f"Costo fijo aprox. (tiempo total con n chico): {np.mean(datos_chico['tiempo_total']):.4f} s "
          f"(promedio del rango chico), de los cuales CBC interno = {np.nanmean(datos_chico['tiempo_cbc_interno']):.4f} s")


def grafico_dificiles(datos_chico, datos_dificil):
    """
    Extra: compara en el rango chico las instancias de crear_mochila.py
    contra las instancias fuertemente correlacionadas (beneficio = peso + 20).
    """
    plt.figure()
    plt.plot(datos_chico["n"], datos_chico["tiempo_total"], marker="o", label="crear_mochila.py")
    plt.plot(datos_dificil["n"], datos_dificil["tiempo_total"], marker="o", label="Dificiles (beneficio = peso + 20)")
    plt.yscale("log")
    plt.title("PuLP: instancias aleatorias vs. fuertemente correlacionadas")
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos, escala logarítmica)")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_GRAFICOS, "grafico_pulp_dificiles.png"), dpi=150)
    plt.close()

    print("\n=== Extra: instancias dificiles ===")
    print(f"Nodos de B&B: maximo {int(np.nanmax(datos_dificil['nodos_bb']))} (dificiles) "
          f"vs. {int(np.nanmax(datos_chico['nodos_bb']))} (crear_mochila.py)")


if __name__ == "__main__":
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

    datos_chico = leer_csv(RUTA_CSV_CHICO)
    datos_grande = leer_csv(RUTA_CSV_GRANDE)

    grafico_teorico_2n(datos_chico)
    grafico_modelos(datos_grande)
    grafico_construccion(datos_chico, datos_grande)

    if os.path.isfile(RUTA_CSV_DIFICIL):
        grafico_dificiles(datos_chico, leer_csv(RUTA_CSV_DIFICIL))

    print(f"\nGraficos guardados en {CARPETA_GRAFICOS}")
