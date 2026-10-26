"""
Genera los casos de prueba del Problema 4 dentro de la subcarpeta casos/.

Usa la funcion crear_mochila del script provisto por la catedra
(crear_mochila.py), este script solo la llama para cada tamaño de mochila que se necesita.

    - rango chico  (n = 10, 12, ..., 40): para contrastar contra O(2^n)
    - rango grande (n = 1000, 2000, ..., 20000): para ver la tendencia real del tiempo
      (5 mochilas distintas por cada n: mochila<n>_1.txt ... mochila<n>_5.txt)
    - extra: instancias dificiles (casos/dificiles/), con su propia funcion
"""

import os
import sys
from random import randint

VALORES_N_CHICO = list(range(10, 41, 2))
VALORES_N_GRANDE = list(range(1000, 20001, 1000))
VALORES_N_DIFICIL = list(range(10, 41, 2))

# En el rango grande el tiempo de CBC varia mucho de una mochila a otra del
# mismo tamaño, asi que para cada n se generan varias mochilas distintas y
# despues se promedian sus tiempos.
INSTANCIAS_POR_N = 5

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")
CARPETA_CASOS_DIFICILES = os.path.join(CARPETA_CASOS, "dificiles")


def crear_mochila_dificil(n):
    """
    Experimento extra: instancia "fuertemente correlacionada". Mismo formato,
    rango de pesos y capacidad que crear_mochila, pero el beneficio de cada
    elemento es su peso + 20 (un decimo del rango de pesos). Como todos los
    elementos tienen casi la misma relacion beneficio/peso, la relajacion
    lineal da cotas muy parecidas en todas las ramas y a Branch and Bound le
    cuesta mas podar.
    """
    nombre = os.path.join(CARPETA_CASOS_DIFICILES, "mochila_dificil" + str(n) + ".txt")
    with open(nombre, "w") as arch:
        arch.write(str(n * 50) + "\n")
        for i in range(n):
            peso = randint(1, 200)
            arch.write(str(peso) + "," + str(peso + 20) + "\n")


# crear_mochila escribe el archivo en la carpeta actual, asi que se trabaja
# parado en casos/.
os.makedirs(CARPETA_CASOS_DIFICILES, exist_ok=True)
os.chdir(CARPETA_CASOS)

# Al importarlo, crear_mochila.py ejecuta su linea crear_mochila(1000) y deja
# un mochila1000.txt en casos/; el loop del rango grande lo pisa y lo
# renombra. Se evita generar __pycache__ junto al script.
sys.dont_write_bytecode = True
from crear_mochila import crear_mochila

for n in VALORES_N_CHICO:
    crear_mochila(n)

# Rango grande: se generan INSTANCIAS_POR_N mochilas distintas para cada n.
# crear_mochila siempre escribe "mochila<n>.txt", asi que despues de cada
# llamada se renombra el archivo a "mochila<n>_<k>.txt".
for n in VALORES_N_GRANDE:
    for k in range(1, INSTANCIAS_POR_N + 1):
        crear_mochila(n)
        os.replace(f"mochila{n}.txt", f"mochila{n}_{k}.txt")

for n in VALORES_N_DIFICIL:
    crear_mochila_dificil(n)

print(f"Casos generados en {CARPETA_CASOS}")
print(f"  rango chico:  n = {VALORES_N_CHICO}")
print(f"  rango grande: n = {VALORES_N_GRANDE} ({INSTANCIAS_POR_N} mochilas por cada n)")
print(f"  dificiles:    n = {VALORES_N_DIFICIL} (en casos/dificiles/)")