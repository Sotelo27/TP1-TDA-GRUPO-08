"""
Resuelve el problema de la mochila 0/1 utilizando un algoritmo greedy
que selecciona los elementos según su relacion beneficio/peso.

Para garantizar una calidad de al menos 1/2, se compara la solucion
obtenida por greedy con el mejor elemento individual que entra en la
mochila.

Guarda los tiempos de ejecucion en tiemposG.csv.
"""
import csv
import os
import time
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_CASOS = os.path.join(CARPETA_SCRIPT, "casos")
RUTA_CSV = os.path.join(CARPETA_SCRIPT, "tiemposG.csv")
RUTA_CASO_MANUAL = os.path.join(CARPETA_SCRIPT, "mochila_manual.txt")
"""
    Lee una instancia de mochila.
    El archivo tiene:
        primera linea: capacidad
        siguientes lineas: peso,beneficio
    Devuelve:
        capacidad, objetos
    """
def leer_mochila(ruta):

    objetos = []

    with open(ruta, "r") as archivo:
        capacidad = int(archivo.readline())

        for linea in archivo:
            peso, beneficio = map(
                int,
                linea.strip().split(",")
            )

            objetos.append((peso, beneficio))

    return capacidad, objetos

"""
Ordena los objetos de mayor a menor segun su relacion
beneficio/peso.
"""
def ordenar(objetos):
    return sorted(objetos,key=lambda objeto: objeto[1] / objeto[0],reverse=True)

def greedy(objetos, capacidad):
    objetosOrd = ordenar(objetos)
    pesoT=0
    valorT=0
    for peso,valor in objetosOrd:
        if pesoT + peso <= capacidad:
            pesoT+=peso
            valorT+=valor
    return valorT, pesoT

"""
Busca el objeto individual de mayor beneficio que pueda
entrar en la mochila.
"""
def mejor_elemento(objetos, capacidad):


    mejor_beneficio = 0
    mejor_peso = 0

    for peso, beneficio in objetos:

        if peso <= capacidad and beneficio > mejor_beneficio:
            mejor_beneficio = beneficio
            mejor_peso = peso

    return mejor_beneficio, mejor_peso

"""
Compara la solucion greedy con el mejor elemento individual.
Esta comparacion permite obtener la garantia de calidad 1/2.
"""
def mochila_greedy(objetos, capacidad):

    beneficio_greedy, peso_greedy = greedy(
        objetos,
        capacidad
    )

    beneficio_individual, peso_individual = mejor_elemento(
        objetos,
        capacidad
    )

    if beneficio_greedy >= beneficio_individual:
        return beneficio_greedy, peso_greedy

    return beneficio_individual, peso_individual

"""
Extrae n del nombre mochila<n>.txt.

Por ejemplo:
    mochila1000.txt -> 1000
"""
def obtener_n(nombre):
    nombre_sin_extension = os.path.splitext(nombre)[0]

    return int(
        nombre_sin_extension.replace("mochila", "")
    )

def probar_caso_manual():
    print("\n--- CASO MANUAL ---") 
    capacidad, objetos = leer_mochila(RUTA_CASO_MANUAL) 
    beneficio, peso = mochila_greedy( objetos, capacidad ) 
    print(f"Capacidad: {capacidad}") 
    print(f"Beneficio obtenido por greedy: {beneficio}") 
    print(f"Peso utilizado: {peso}")
def main():

    archivos = [
        nombre
        for nombre in os.listdir(CARPETA_CASOS)
        if nombre.startswith("mochila")
        and nombre.endswith(".txt")
    ]

    archivos.sort(key=obtener_n)

    resultados = []

    for nombre in archivos:

        ruta = os.path.join(
            CARPETA_CASOS,
            nombre
        )

        capacidad, objetos = leer_mochila(ruta)

        inicio = time.perf_counter()

        beneficio, peso = mochila_greedy(
            objetos,
            capacidad
        )

        fin = time.perf_counter()

        tiempo = fin - inicio

        n = len(objetos)

        print(
            f"n={n} | "
            f"capacidad={capacidad} | "
            f"beneficio={beneficio} | "
            f"peso={peso} | "
            f"tiempo={tiempo:.9f} s"
        )

        resultados.append([
            n,
            capacidad,
            beneficio,
            peso,
            tiempo
        ])

    with open(
        RUTA_CSV,
        "w",
        newline=""
    ) as archivo_csv:

        escritor = csv.writer(archivo_csv)

        escritor.writerow([
            "n",
            "capacidad",
            "beneficio_maximo",
            "peso_usado",
            "tiempo_segundos"
        ])

        escritor.writerows(resultados)

    probar_caso_manual()

main()