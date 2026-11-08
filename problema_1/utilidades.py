"""
Problema 1 - Lectura y generacion de instancias, medicion de tiempos y CSV
Teoria de Algoritmos - TP2

Una instancia es (capacidad, items), con items una lista de tuplas
(peso, beneficio). El formato de archivo es el de crear_mochila.py de la
catedra: la primera linea es la capacidad y cada linea siguiente "peso,beneficio".
"""

import csv
import os
import random
import re
import time

PESO_MAXIMO = 200
BENEFICIO_MAXIMO = 1000
CAPACIDAD_POR_ITEM = 50

REPETICIONES = 5


def parsear_mochila(ruta_archivo):
    """Lee un archivo de mochila y devuelve (capacidad, items)."""
    with open(ruta_archivo) as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    capacidad = int(lineas[0])
    items = []
    for linea in lineas[1:]:
        peso, beneficio = linea.split(",")
        items.append((int(peso), int(beneficio)))
    return capacidad, items


def crear_mochila(ruta_archivo, n, generador=random):
    """
    Escribe una instancia de n items con la misma distribucion que el script
    de la catedra: pesos en 1-200, beneficios en 1-1000 y capacidad n * 50.
    """
    with open(ruta_archivo, "w") as archivo:
        archivo.write(f"{n * CAPACIDAD_POR_ITEM}\n")
        for _ in range(n):
            peso = generador.randint(1, PESO_MAXIMO)
            beneficio = generador.randint(1, BENEFICIO_MAXIMO)
            archivo.write(f"{peso},{beneficio}\n")


def generar_casos(carpeta_casos, valores_n, semilla=None):
    """
    Genera mochila<n>.txt en carpeta_casos por cada n de valores_n. Con una
    semilla, volver a generar los casos produce exactamente los mismos archivos.
    """
    os.makedirs(carpeta_casos, exist_ok=True)
    generador = random.Random(semilla)
    for n in valores_n:
        crear_mochila(os.path.join(carpeta_casos, f"mochila{n}.txt"), n, generador)


def listar_casos(carpeta_casos):
    """Devuelve las rutas de los mochila*.txt de la carpeta, ordenadas por n."""
    if not os.path.isdir(carpeta_casos):
        return []

    nombres = [
        nombre
        for nombre in os.listdir(carpeta_casos)
        if nombre.startswith("mochila") and nombre.endswith(".txt")
    ]
    nombres.sort(key=lambda nombre: [int(numero) for numero in re.findall(r"\d+", nombre)])
    return [os.path.join(carpeta_casos, nombre) for nombre in nombres]


def medir(algoritmo, capacidad, items, repeticiones=REPETICIONES):
    """
    Corre algoritmo(capacidad, items) "repeticiones" veces y devuelve
    (resultado de la ultima corrida, tiempo promedio en segundos).
    """
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = algoritmo(capacidad, items)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    return resultado, sum(tiempos) / repeticiones


def guardar_csv(ruta_csv, columnas, filas):
    """Guarda las filas (lista de diccionarios) en un CSV."""
    if not filas:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")
        return

    with open(ruta_csv, "w", newline="") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"\nResultados guardados en {ruta_csv}")
