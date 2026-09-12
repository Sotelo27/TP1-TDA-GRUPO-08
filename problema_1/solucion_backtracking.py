"""
Problema 1 - Mochila 0/1 resuelta por Backtracking
Teoria de Algoritmos - TP1

Este programa resuelve el mismo problema que solucion_fuerza_bruta.py (la
mochila 0/1: cada elemento se lleva entero o no se lleva), pero en vez de
generar y evaluar TODOS los 2^n subconjuntos posibles, arma un arbol de
decision binario (incluir / no incluir cada elemento, en orden de indice)
y lo recorre con backtracking, cortando ramas enteras del arbol cuando se
puede probar que no vale la pena seguir explorandolas.

Se aplican dos podas:

  1) PODA OBLIGATORIA (de factibilidad): jamas se arma un subconjunto que
     ya supera la capacidad. Es la poda minima indispensable para que esto
     sea backtracking y no fuerza bruta disfrazada.

  2) PODA OPCIONAL (cota de beneficio / branch and bound): antes de seguir
     explorando un nodo, se calcula una cota optimista de cuanto beneficio
     se podria llegar a sumar en el mejor de los casos desde ese punto en
     adelante, y si ni en ese mejor caso se puede superar la mejor
     solucion ya encontrada, se corta toda la rama (ambas opciones: ni
     incluir ni excluir el elemento actual).

Gracias a estas podas, backtracking recorre en la practica una fraccion
mucho menor de los 2^n subconjuntos que la fuerza bruta (en el peor caso
sigue siendo exponencial, pero el caso promedio mejora muchisimo), y sin
embargo llega exactamente al mismo resultado optimo, porque nunca se
descarta una rama que pudiera contener la solucion optima.

Este script procesa los mismos archivos que solucion_fuerza_bruta.py
(mochila10.txt ... mochila22.txt) y guarda los tiempos en un CSV aparte
(tiempos_backtracking.csv) para poder comparar ambos enfoques.
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
# procesado), para poder comparar despues contra tiempos_fuerza_bruta.csv.
NOMBRE_CSV_SALIDA = "tiempos_backtracking.csv"
RUTA_CSV_SALIDA = os.path.join(CARPETA_SCRIPT, NOMBRE_CSV_SALIDA)


def parsear_mochila(ruta_archivo):
    """
    Lee un archivo de mochila con el siguiente formato:
        linea 1: capacidad de la mochila (entero)
        lineas siguientes: peso,beneficio (uno por elemento, separados por coma)

    Devuelve una tupla (capacidad, items), donde items es una lista de
    tuplas (peso, beneficio), una por cada elemento leido del archivo.

    (Identica a la de solucion_fuerza_bruta.py: se duplica aca a proposito
    para que este archivo sea autocontenido y se pueda correr y corregir
    de forma independiente).
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


def mochila_backtracking(capacidad, items):
    """
    Resuelve el problema de la mochila 0/1 con backtracking, recorriendo
    el arbol de decision "incluir / no incluir" elemento por elemento (en
    orden de indice), pero podando las ramas que no pueden llevar a una
    solucion mejor que la ya encontrada.

    Parametros:
        capacidad: capacidad maxima de la mochila (entero)
        items: lista de tuplas (peso, beneficio), una por elemento

    Devuelve una tupla (mejor_beneficio, mejores_indices, mejor_peso), con
    el mismo formato que fuerza_bruta() en solucion_fuerza_bruta.py:
        mejor_beneficio: el beneficio maximo encontrado
        mejores_indices: lista de indices (0-based) de los elementos elegidos
        mejor_peso: peso total de esa seleccion
    """
    n = len(items)

    # beneficio_restante[i] = suma de los beneficios de items[i], items[i+1],
    # ..., items[n-1]. Se precalcula una sola vez, recorriendo la lista de
    # atras para adelante, para poder consultar en O(1) "cuanto beneficio
    # queda por delante" en cada nodo del arbol, en vez de tener que sumar
    # la lista restante de items cada vez que se evalua la poda opcional.
    beneficio_restante = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        beneficio_restante[i] = beneficio_restante[i + 1] + items[i][1]

    # Registro de la mejor solucion encontrada hasta el momento. Se usa un
    # diccionario (en vez de variables globales sueltas) para que la
    # funcion recursiva interna pueda leerlo y modificarlo sin necesidad
    # de declarar "nonlocal" por cada campo.
    mejor = {"beneficio": 0, "indices": [], "peso": 0}

    def backtrack(i, peso_actual, beneficio_actual, indices_actuales):
        """
        Decide que hacer con el elemento de indice i (incluirlo o no),
        habiendo ya decidido que pasa con los elementos 0..i-1.

        peso_actual y beneficio_actual son el peso y beneficio acumulados
        por las decisiones tomadas hasta ahora (elementos 0..i-1).
        indices_actuales es la lista de indices incluidos hasta ahora.
        """
        # Caso base: ya se decidio (incluir o no) sobre los n elementos,
        # asi que indices_actuales representa un subconjunto completo,
        # igual que una mascara de bits completa en la version de fuerza
        # bruta. Si es mejor que el mejor encontrado hasta ahora, se
        # guarda como nueva mejor solucion.
        if i == n:
            if beneficio_actual > mejor["beneficio"]:
                mejor["beneficio"] = beneficio_actual
                mejor["indices"] = list(indices_actuales)
                mejor["peso"] = peso_actual
            return

        # --- PODA OPCIONAL: cota de beneficio (branch and bound) ---
        # beneficio_restante[i] es la suma de los beneficios de TODOS los
        # elementos que todavia no se visitaron (items[i:]), es decir, el
        # mejor de los casos posibles: como si se pudieran llevar todos
        # sin importar el peso que ocupen. Si ni sumando esa cota optimista
        # al beneficio ya acumulado se supera la mejor solucion encontrada
        # hasta el momento, no tiene sentido seguir explorando desde este
        # nodo: se corta la rama completa (no se prueba ni incluir ni
        # excluir el elemento actual). Esta poda es opcional en el sentido
        # de que el algoritmo sigue siendo correcto sin ella (solo mas
        # lento): si se quisiera sacar, alcanza con borrar este bloque.
        cota_optimista = beneficio_actual + beneficio_restante[i]
        if cota_optimista <= mejor["beneficio"]:
            return

        peso_i, beneficio_i = items[i]

        # --- Rama "incluir el elemento i" ---
        # --- PODA OBLIGATORIA: factibilidad de peso ---
        # Solo se explora esta rama si el elemento entra en la capacidad
        # restante. Si incluirlo ya supera la capacidad, ni siquiera se
        # llama a la recursion con esa opcion: esa rama entera del arbol
        # (y todo lo que colgaria de ella) queda descartada de antemano,
        # sin necesidad de terminar de decidir sobre el resto de los
        # elementos para darse cuenta de que es invalida. Esta es la poda
        # que distingue al backtracking de la fuerza bruta pura.
        if peso_actual + peso_i <= capacidad:
            indices_actuales.append(i)
            backtrack(i + 1, peso_actual + peso_i, beneficio_actual + beneficio_i, indices_actuales)
            indices_actuales.pop()  # se deshace la decision (el "backtrack" propiamente dicho)

        # --- Rama "no incluir el elemento i" ---
        # Esta rama siempre es factible (no agrega peso), asi que siempre
        # se explora.
        backtrack(i + 1, peso_actual, beneficio_actual, indices_actuales)

    backtrack(0, 0, 0, [])

    return mejor["beneficio"], mejor["indices"], mejor["peso"]


if __name__ == "__main__":
    # Filas que se van a escribir en el CSV de salida, una por cada
    # archivo procesado con exito.
    filas_csv = []

    for nombre_archivo in ARCHIVOS_MOCHILA:
        ruta_archivo = os.path.join(CARPETA_SCRIPT, nombre_archivo)

        if not os.path.isfile(ruta_archivo):
            print(f"No se encontró {nombre_archivo}, corré crear_mochila.py primero.")
            continue

        # La lectura y el parseo del archivo NO se incluyen en la
        # medicion de tiempo: solo interesa medir el tiempo que tarda el
        # algoritmo de backtracking en si mismo.
        capacidad, items = parsear_mochila(ruta_archivo)
        n = len(items)

        inicio = time.perf_counter()
        beneficio_maximo, indices_elegidos, peso_total = mochila_backtracking(capacidad, items)
        fin = time.perf_counter()

        tiempo_ejecucion = fin - inicio

        print(
            f"n={n} | capacidad={capacidad} | beneficio_maximo={beneficio_maximo} "
            f"| peso_usado={peso_total} | tiempo={tiempo_ejecucion:.6f} s"
        )

        filas_csv.append(
            {
                "n": n,
                "capacidad": capacidad,
                "beneficio_maximo": beneficio_maximo,
                "peso_usado": peso_total,
                "tiempo_segundos": round(tiempo_ejecucion, 4),
            }
        )

    # Se guardan los resultados en un CSV para poder comparar despues
    # estos tiempos contra los de tiempos_fuerza_bruta.csv.
    if filas_csv:
        with open(RUTA_CSV_SALIDA, "w", newline="") as archivo_csv:
            columnas = ["n", "capacidad", "beneficio_maximo", "peso_usado", "tiempo_segundos"]
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas_csv)

        print(f"\nResultados guardados en {RUTA_CSV_SALIDA}")
    else:
        print("\nNo se proceso ningun archivo, no se genero el CSV.")
