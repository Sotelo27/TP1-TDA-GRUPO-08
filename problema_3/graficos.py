"""
Problema 3 - Graficos de Programacion Dinamica
Teoria de Algoritmos - TP1

Genera los graficos pedidos a partir de los CSV que producen
solucion_pd1.py (planteo tradicional) y solucion_pd2.py (planteo
alternativo):

  1) Medido vs teorico - planteo TRADICIONAL:
     el orden teorico es O(n * capacidad), asi que se ajusta una
     constante c tal que tiempo_teorico = c * (n * capacidad) y se
     compara contra el tiempo medido.

  2) Medido vs teorico - planteo ALTERNATIVO:
     el orden teorico es O(n * beneficio_total), donde beneficio_total
     es la suma de los beneficios de TODOS los elementos del caso (no
     el beneficio optimo, que es lo que ya guarda el CSV). Como esa
     suma no se registro en el CSV, se recalcula ac  releyendo los
     mismos archivos de entrada que se usaron para generar los tiempos
     (se asume que el archivo de cada fila es "mochila<n>.txt" dentro
     de la carpeta casos/, siguiendo la convencion usada en los demas
     scripts del TP).

  3) Comparacion entre ambos algoritmos:
     tiempo medido de ambos planteos superpuesto en un mismo grafico,
     en funcion de n, para ver cual escala mejor en la practica.

Los tres graficos se guardan como imagenes dentro de la carpeta
graficos/.
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_GRAFICOS = os.path.join(CARPETA_SCRIPT, "graficos")
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

RUTA_CSV_PD_TRADICIONAL = os.path.join(CARPETA_SCRIPT, "tiempos_pd_tradicional.csv")
RUTA_CSV_PD_ALTERNATIVA = os.path.join(CARPETA_SCRIPT, "tiempos_pd_alternativa.csv")

def parsear_mochila(ruta_archivo):
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

def leer_csv_tiempos(ruta_csv):
    valores_n = []
    valores_capacidad = []
    valores_tiempo = []

    with open(ruta_csv, "r", newline="") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            valores_n.append(int(fila["n"]))
            valores_capacidad.append(int(fila["capacidad"]))
            valores_tiempo.append(float(fila["tiempo_segundos"]))

    orden = np.argsort(valores_n)
    n = np.array(valores_n)[orden]
    capacidad = np.array(valores_capacidad)[orden]
    tiempo = np.array(valores_tiempo)[orden]

    return n, capacidad, tiempo

def obtener_beneficios_totales(valores_n):
    beneficios_totales = []
    for n in valores_n:
        ruta_archivo = os.path.join(CARPETA_CASOS, f"mochila{n}.txt")
        _, items = parsear_mochila(ruta_archivo)
        beneficio_total = sum(beneficio for _, beneficio in items)
        beneficios_totales.append(beneficio_total)

    return np.array(beneficios_totales)

def ajustar_constante(x_teorico, tiempo_medido):
    return np.sum(tiempo_medido * x_teorico) / np.sum(x_teorico ** 2)

def graficar_medido_vs_teorico(n, tiempo_medido, x_teorico, c, etiqueta_teorica, titulo, ruta_salida):
    orden = np.argsort(n)
    n_ordenado = n[orden]
    tiempo_medido_ordenado = tiempo_medido[orden]
    tiempo_teorico_ordenado = c * x_teorico[orden]

    plt.figure()
    plt.plot(n_ordenado, tiempo_medido_ordenado, marker="o", label="Tiempo medido")
    plt.plot(n_ordenado, tiempo_teorico_ordenado, linestyle="--", label=etiqueta_teorica)
    plt.title(titulo)
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()
    plt.savefig(ruta_salida)
    plt.show()


def graficar_comparacion_algoritmos(n_trad, tiempo_trad, n_alt, tiempo_alt, titulo, ruta_salida):
    orden_trad = np.argsort(n_trad)
    orden_alt = np.argsort(n_alt)

    plt.figure()
    plt.plot(n_trad[orden_trad], tiempo_trad[orden_trad], marker="o", label="PD tradicional (maximizar beneficio)")
    plt.plot(n_alt[orden_alt], tiempo_alt[orden_alt], marker="o", label="PD alternativa (minimizar peso)")
    plt.title(titulo)
    plt.xlabel("n = cantidad de elementos")
    plt.ylabel("tiempo (segundos)")
    plt.grid(True)
    plt.legend()
    plt.savefig(ruta_salida)
    plt.show()

if __name__ == "__main__":
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

    # ---------------------------------------------------------------
    # 1) Planteo tradicional: medido vs teorico O(n * capacidad)
    # ---------------------------------------------------------------
    n_trad, capacidad_trad, tiempo_trad = leer_csv_tiempos(RUTA_CSV_PD_TRADICIONAL)
    x_teorico_trad = n_trad * capacidad_trad  # tamano de la tabla dp: (n+1)*(capacidad+1)
    c_trad = ajustar_constante(x_teorico_trad, tiempo_trad)

    print(f"[PD tradicional] constante ajustada c = {c_trad:.3e} (orden: O(n * capacidad))")

    graficar_medido_vs_teorico(
        n_trad,
        tiempo_trad,
        x_teorico_trad,
        c_trad,
        etiqueta_teorica="Tiempo teorico O(n * capacidad)",
        titulo="PD tradicional: tiempo medido vs teorico",
        ruta_salida=os.path.join(CARPETA_GRAFICOS, "pd_tradicional_medido_vs_teorico.png"),
    )

    # ---------------------------------------------------------------
    # 2) Planteo alternativo: medido vs teorico O(n * beneficio_total)
    # ---------------------------------------------------------------
    n_alt, _capacidad_alt, tiempo_alt = leer_csv_tiempos(RUTA_CSV_PD_ALTERNATIVA)
    beneficio_total_alt = obtener_beneficios_totales(n_alt)
    x_teorico_alt = n_alt * beneficio_total_alt  # tamano de la tabla dp: (n+1)*(beneficio_total+1)
    c_alt = ajustar_constante(x_teorico_alt, tiempo_alt)

    print(f"[PD alternativa] constante ajustada c = {c_alt:.3e} (orden: O(n * beneficio_total))")

    graficar_medido_vs_teorico(
        n_alt,
        tiempo_alt,
        x_teorico_alt,
        c_alt,
        etiqueta_teorica="Tiempo teorico O(n * beneficio_total)",
        titulo="PD alternativa: tiempo medido vs teorico",
        ruta_salida=os.path.join(CARPETA_GRAFICOS, "pd_alternativa_medido_vs_teorico.png"),
    )

    # ---------------------------------------------------------------
    # 3) Comparacion entre ambos planteos de programacion dinamica
    # ---------------------------------------------------------------
    graficar_comparacion_algoritmos(
        n_trad,
        tiempo_trad,
        n_alt,
        tiempo_alt,
        titulo="PD tradicional vs PD alternativa: tiempo medido",
        ruta_salida=os.path.join(CARPETA_GRAFICOS, "comparacion_pd_tradicional_vs_alternativa.png"),
    )

    print(f"\nGraficos guardados en {CARPETA_GRAFICOS}")