# Problema 2 - Mochila 0/1: Algoritmo Greedy

## Descripción del problema

El problema consiste en resolver la **mochila 0/1** utilizando un algoritmo **Greedy**.

Cada elemento tiene:

- un peso;
- un beneficio.

La mochila tiene una capacidad máxima y cada elemento puede ser seleccionado como máximo una vez.

La estrategia utilizada consiste en ordenar los elementos según su relación:

$$
\frac{beneficio}{peso}
$$

de mayor a menor, e ir agregando los elementos en ese orden mientras haya capacidad disponible.

Además, para obtener una **garantía de calidad de 1/2**, se compara la solución obtenida por Greedy con la solución formada por el **mejor elemento individual que pueda entrar en la mochila**, y se conserva la de mayor beneficio.

---

## Orden de ejecución

Los archivos deben ejecutarse en el siguiente orden:

```text
1. python crear_mochila.py
2. python solucionG.py
3. python graficos.py
```
---

# Funcionamiento del algoritmo Greedy

El algoritmo utiliza la relación beneficio/peso para decidir qué elemento considerar primero.

Para cada elemento se calcula:

$$
\frac{beneficio_i}{peso_i}
$$

Luego los elementos se ordenan de mayor a menor según este valor.

Después se recorren los elementos ordenados:

- si el elemento entra en la capacidad restante, se agrega;
- si no entra, se continúa con el siguiente elemento.

De esta forma se intenta aprovechar la capacidad de la mochila seleccionando primero los elementos que ofrecen mayor beneficio por unidad de peso.

Finalmente, se compara esta solución con el mejor elemento individual que entra en la mochila.

La solución final es:

$$
\max(G,M)
$$

donde:

- $G$ es el beneficio obtenido por Greedy;
- $M$ es el beneficio del mejor elemento individual que entra en la mochila.

---

# ¿Por qué esto tiene garantía 1/2?

- El elemento crítico es el primero que queda afuera, entonces sabemos que:

$$
W_1 < W,\qquad W_2 < W\qquad \text{y}\qquad W_1+W_2>W
$$

- Los elementos están ordenados por el coeficiente en forma descendente, entonces:

$$
\frac{P_1}{W_1} > \frac{P_2}{W_2}
$$

Entonces, sabemos que:

- Los elementos de $P_1+P_2$ son los que mejor aprovechan el espacio disponible.
- Por lo menos una de las dos soluciones $(W_1,W_2)$ ocupa más de la mitad de la mochila.

$$
\Rightarrow \text{La solución obtenida es por lo menos la mitad de la solución óptima}
$$

Por lo tanto, si $OPT$ representa el beneficio de una solución óptima y $ALG$ representa el beneficio obtenido por nuestro algoritmo:

$$
ALG \geq \frac{OPT}{2}
$$

Es decir, el algoritmo tiene una **garantía de calidad de 1/2**.

---

# Mochila creada manualmente

Además de los casos generados automáticamente para medir los tiempos, se creó una instancia manual en el archivo:

```text
mochila_manual.txt
```

Este caso no se utiliza para la comparación de tiempos, sino para mostrar experimentalmente cómo puede actuar la garantía de calidad.

La instancia utilizada es:

```text
100
51,52
50,50
50,50
```

La capacidad de la mochila es:

$$
W=100
$$

Los elementos son:

| Elemento | Peso | Beneficio | Beneficio/Peso |
|---|---:|---:|---:|
| 1 | 51 | 52 | 1,0196 |
| 2 | 50 | 50 | 1 |
| 3 | 50 | 50 | 1 |

El primer elemento tiene la mayor relación beneficio/peso, por lo que Greedy lo selecciona primero.

Luego queda:

$$
100-51=49
$$

Los dos elementos restantes pesan 50, por lo que ninguno puede entrar.

Por lo tanto, Greedy obtiene:

$$
G=52
$$

Sin embargo, la solución formada por los elementos 2 y 3 es:

$$
50+50=100
$$

y tiene beneficio:

$$
OPT=50+50=100
$$

Entonces:

$$
\frac{G}{OPT}
=
\frac{52}{100}
=
0,52
$$

Por lo tanto, en este caso la solución obtenida por Greedy representa el:

$$
52\%
$$

del valor óptimo.

Esto muestra un caso en el que el resultado queda cercano a la garantía teórica:

$$
\frac{1}{2}=0,5
$$

y permite observar experimentalmente por qué la solución Greedy no necesariamente coincide con la solución óptima.

---

# Resumen de ejecución

Desde la carpeta `problema_2`, ejecutar:

```bash
py crear_mochila.py
py solucionG.py
py graficos.py
```

El flujo completo es:

```text
crear_mochila.py
        ↓
genera los casos en casos/
        ↓
solucionG.py
        ↓
ejecuta Greedy y mide tiempos
        ↓
tiemposG.csv
        ↓
graficos.py
        ↓
gráficos en graficos/
```

El archivo `mochila_manual.txt` se utiliza aparte para analizar el caso construido manualmente y mostrar experimentalmente la garantía de calidad de 1/2.