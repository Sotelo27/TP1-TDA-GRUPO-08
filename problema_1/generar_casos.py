"""
Genera los casos de prueba del Problema 1 dentro de la subcarpeta casos/, con
la distribucion de crear_mochila.py de la catedra.

Los tamanios chicos permiten correr k = 3, cuyo costo crece como n^4; los
grandes muestran el crecimiento de k = 1 y k = 2. La semilla fija hace que
volver a ejecutar este script produzca los mismos archivos.
"""

import os

import utilidades

CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

VALORES_N = [20, 40, 60, 80, 100, 120, 200, 300, 400, 600, 800, 1000]
SEMILLA = 2026

CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")

if __name__ == "__main__":
    utilidades.generar_casos(CARPETA_CASOS, VALORES_N, SEMILLA)
    print(f"Casos generados en {CARPETA_CASOS}: n = {VALORES_N}")
