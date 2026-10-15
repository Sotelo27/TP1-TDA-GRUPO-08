"""
Genera los casos de prueba del Problema 1 dentro de la subcarpeta casos/.

Usa la funcion crear_mochila del script provisto por la catedra
(crear_mochila.py), que se deja SIN MODIFICAR: este script solo la llama
para cada tamaño de mochila que se necesita.

Tamaños generados: n = 10, 11, ..., 22
"""

import os
import sys

VALORES_N = range(10, 23)

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

# crear_mochila escribe el archivo en la carpeta actual, asi que se trabaja
# parado en casos/.
os.makedirs(CARPETA_CASOS, exist_ok=True)
os.chdir(CARPETA_CASOS)

# Al importarlo, crear_mochila.py ejecuta su linea crear_mochila(1000) y deja
# un mochila1000.txt en casos/. Se evita generar __pycache__ junto al script.
sys.dont_write_bytecode = True
from crear_mochila import crear_mochila

for n in VALORES_N:
    crear_mochila(n)

# Si 1000 no es uno de los tamaños de este problema, se borra el archivo que
# genero el import, para que en casos/ queden solo los casos que se usan.
if 1000 not in VALORES_N:
    os.remove("mochila1000.txt")

print(f"Casos generados en {CARPETA_CASOS}: n = {list(VALORES_N)}")
