from random import randint
import os
CARPETA_CASOS = "casos"
def crear_mochila(n):
    nombre = os.path.join(CARPETA_CASOS, "mochila" + str(n) + ".txt")

    with open(nombre, "w") as arch:
        capacidad = n * 50
        arch.write(str(capacidad) + "\n")

        for i in range(n):
            peso = randint(1, 200)
            beneficio = randint(1, 1000)

            arch.write(str(peso) + "," + str(beneficio) + "\n")


os.makedirs(CARPETA_CASOS, exist_ok=True)

for n in [100, 200, 500, 1000, 2000, 5000]:
    crear_mochila(n)
	
# Esta función crea una mochila con una lista del tamaño indicado como parámetro
# Los beneficios están en el rango 1-1000
# Los pesos están en el rango 1-200
# La capacidad de la mochila es tamaño * 50: aprox, la mitad de los elementos cabrán en la mochila
#
# Se genera un archivo cuya primera línea es la capacidad de la mochila
# Las líneas siguientes son pares ordenados (peso, beneficio) de cada elemento.
