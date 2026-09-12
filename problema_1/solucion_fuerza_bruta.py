"""
Problema 1 - Mochila 0/1 resuelta por Fuerza Bruta
Teoria de Algoritmos - TP1

Este programa resuelve el problema de la mochila 0/1 (cada elemento se
lleva entero o no se lleva, no hay fracciones) probando TODAS las
combinaciones posibles de elementos, es decir, los 2^n subconjuntos que se
pueden formar con n elementos, sin ningun tipo de poda ni optimizacion.

Esto lo convierte en un algoritmo de complejidad temporal exponencial:
O(n * 2^n), ya que por cada uno de los 2^n subconjuntos posibles se
recorren los n elementos para armar el subconjunto y calcular su peso y
beneficio total.

Se implementa asi intencionalmente (sin poda): sirve como base de
comparacion contra la version con backtracking (con poda) que se resuelve
en otro archivo. Por eso mismo, solo es practico para valores de n chicos;
este script procesa los archivos mochila10.txt, mochila13.txt,
mochila16.txt, mochila19.txt y mochila22.txt generados por
crear_mochila.py, y guarda los tiempos obtenidos en un CSV para poder
graficarlos despues.
"""

import csv
import os
import time

# Archivos de mochila a procesar, en orden creciente de tamano. Se asume
# que estan en la misma carpeta que este script, generados con
# crear_mochila.py.
ARCHIVOS_MOCHILA = [
    "mochila10.txt",
    "mochila13.txt",
    "mochila16.txt",
    "mochila19.txt",
    "mochila22.txt",
]

# Carpeta donde vive este script: se usa como base tanto para buscar los
# archivos de entrada como para guardar el CSV de salida.
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Nombre del CSV donde se van a guardar los resultados (uno por archivo
# procesado), para usarlo despues en el grafico de tiempos.
NOMBRE_CSV_SALIDA = "tiempos_fuerza_bruta.csv"
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, NOMBRE_CSV_SALIDA)


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


