# Problema 1 - Algoritmo aproximado de Sahni (1975)

## 1. Supuestos

Se usa la notación de clase (Martello y Toth, 1990): `p_j` es el beneficio, `w_j` el peso y `c` la capacidad, con los elementos ordenados por `p_j / w_j` decreciente.

- Los pesos `w_j` son enteros positivos, los beneficios `p_j` son enteros no negativos y la capacidad `c` es un entero no negativo.
- Cada elemento se usa como máximo una vez (mochila 0/1).
- Un elemento con `w_j > c` no puede formar parte de ninguna solución, así que se descarta al inicio. Esto no cambia el resultado de `S(k)` y asegura la hipótesis `w_j <= c` que usa la cota de Martello y Toth, porque hace que exista el elemento `s - 1`. En los sets de este trabajo no ocurre: `c = 50n` y `w_j <= 200`.
- El parámetro `k` es un entero no negativo fijado antes de ejecutar. En el peor caso, `S(k)` está a `r = k / (k + 1)` del óptimo. Con `k = 0` es un greedy por densidad sin garantía.
- El algoritmo es determinístico: para una misma instancia y un mismo `k` devuelve siempre el mismo beneficio.
- El costo crece como `n^(k+1)`, lo que limita los valores de `k` utilizables en instancias grandes.

## 2. Diseño

### 2.a Pseudocódigo

Con la lista ya ordenada por `p_j / w_j` decreciente, `GS(M)` agrega sí o sí los elementos de `M` y prueba los restantes igual que greedy:

```
procedure GS(n, c, p, w, M):
    z^g := 0
    ĉ := c − Σ_{j∈M} w_j
    X := ∅
    for j := 1 to n:
        if j ∉ M and w_j ≤ ĉ:
            z^g := z^g + p_j
            ĉ := ĉ − w_j
            X := X ∪ {j}

procedure S(k):
    z^h := 0
    for each M ⊂ {1..n} with |M| ≤ k and Σ_{j∈M} w_j ≤ c:
        call GS(n, c, p, w, M)
        if z^g + Σ_{j∈M} p_j > z^h:
            z^h := z^g + Σ_{j∈M} p_j
            X^h := X ∪ M
```

Cotas superiores. El elemento crítico `s` es el primero que no entra al llenar en orden, y `c̄` es la capacidad residual luego de los `s − 1` primeros:

```
Cota 1 (relajación lineal):
    U1 = ⌊ Σ_{i=1}^{s−1} p_i + c̄ · p_s / w_s ⌋

Cota 2 (Martello y Toth). En vez de partir el crítico, vale 0 o vale 1:
    W1 = Σ_{i=1}^{s−1} p_i + ⌊ c̄ · p_{s+1} / w_{s+1} ⌋              (crítico = 0)
    W2 = Σ_{i=1}^{s−1} p_i + ⌊ p_s − (w_s − c̄) · p_{s−1} / w_{s−1} ⌋  (crítico = 1)
    U2 = max(W1, W2)
```

Casos particulares: si todos los elementos entran no hay crítico y las dos cotas valen la suma de los beneficios. Si el crítico es el último, no existe `s + 1` y `W1` no tiene término extra.

**Relajación lineal.** Se calcula con el método fraccionario, que corta el elemento crítico, y se informa **con piso**: como el óptimo es entero, el piso sigue siendo una cota superior válida. Se comprobó contra el modelo de programación lineal del TP1 con variables continuas en `[0, 1]`, en 172 instancias chicas y medianas: el valor continuo coincidió con el fraccionario, con una diferencia máxima de `4,3e-06` debida al solver. Como el método fraccionario descarta los elementos con `w_j > c`, en esa comparación el modelo se resolvió sobre los mismos elementos; sin descartarlos, la PL podría tomar una fracción de ellos y dar un valor mayor.

**Óptimo exacto.** Se calcula con **Programación dinámica (Ej 3A del TP1)**, en `O(n * c)`. Se comprobó en las 172 instancias que da lo mismo que la implementación de PD del TP1 y que la programación lineal entera del TP1, y en las 162 instancias con `n <= 20` que da lo mismo que fuerza bruta.

### 2.b Estructuras de datos

| Estructura | Uso |
|---|---|
| Lista de tuplas `(w_j, p_j)` | Instancia y elementos ordenados por `p_j / w_j`. |
| Lista `orden` | Traduce cada posición ordenada al índice original del elemento. |
| Tuplas de `itertools.combinations` | Cada conjunto `M` de tamaño a lo sumo `k`. |
| Lista de booleanos `en_M` | Indica en `O(1)` si un elemento pertenece a `M`. |
| Lista `X_h` | Posiciones de la mejor solución encontrada. |
| Arreglo `numpy` de `c + 1` enteros | Fila de la programación dinámica del óptimo exacto. |

## 3. Seguimiento

Instancia: `c = 10`, `k = 1` y cuatro elementos, ya ordenados por `p_j / w_j`:

| j | w_j | p_j | p_j / w_j |
|---:|---:|---:|---:|
| 1 | 6 | 18 | 3,0 |
| 2 | 5 | 14 | 2,8 |
| 3 | 5 | 13 | 2,6 |
| 4 | 2 | 4 | 2,0 |

**Ejecución de `S(1)`.** Se prueban todos los `M` con `|M| <= 1`; los cinco entran en la mochila.

| M | ĉ inicial | Recorrido de GS(M) | z^g | X | z^g + Σ_M p_j | z^h |
|---|---:|---|---:|---|---:|---:|
| ∅ | 10 | j=1 entra (ĉ=4); j=2 y j=3 no entran; j=4 entra (ĉ=2) | 22 | {1, 4} | 22 | 22 |
| {1} | 4 | j=2 y j=3 no entran; j=4 entra (ĉ=2) | 4 | {4} | 4 + 18 = 22 | 22 |
| {2} | 5 | j=1 no entra; j=3 entra (ĉ=0); j=4 no entra | 13 | {3} | 13 + 14 = 27 | **27** |
| {3} | 5 | j=1 no entra; j=2 entra (ĉ=0); j=4 no entra | 14 | {2} | 14 + 13 = 27 | 27 |
| {4} | 8 | j=1 entra (ĉ=2); j=2 y j=3 no entran | 18 | {1} | 18 + 4 = 22 | 27 |

El resultado es `X^h = {2, 3}`, con `z^h = 27` y peso 10. El caso `M = {3}` empata pero no reemplaza a la mejor solución, porque la comparación es estricta. Con `k = 0` solo se evalúa `M = ∅` y el resultado sería 22.

**Elemento crítico.** Al llenar en orden entra `j = 1`, y `j = 2` ya no entra. Entonces `s = 2`, `Σ_{i<s} p_i = 18` y `c̄ = 10 − 6 = 4`.

**Cotas.**

- Relajación lineal: `18 + 4 · 14 / 5 = 29,2`; con piso, `U1 = 29`.
- `W1 = 18 + ⌊4 · 13 / 5⌋ = 18 + 10 = 28`.
- `W2 = 18 + ⌊14 − (5 − 4) · 18 / 6⌋ = 18 + 11 = 29`.
- `U2 = max(28, 29) = 29`.

**Óptimo exacto:** 27. Se cumple `S(1) = 27 <= óptimo = 27 <= U2 = 29 <= relajación lineal = 29`, y `27 >= (1/2) · 27`. Este ejemplo es uno de los casos de `tests/test_base.py`.

## 4. Complejidad temporal

Sea `n` la cantidad de elementos. A partir del pseudocódigo:

- Ordenar la lista por `p_j / w_j`, una sola vez antes de `S(k)`: `O(n log n)`.
- `GS(M)`: calcular `ĉ` cuesta `O(|M|) = O(k)` y el `for` recorre `n` elementos con operaciones `O(1)`, porque la pertenencia a `M` se consulta en `O(1)`. Total: `O(n)`.
- `S(k)`: la cantidad de conjuntos `M` con `|M| <= k` es `Σ_{t=0}^{k} C(n, t) = O(n^k)`, con `k` fijo. Por cada uno se llama a `GS(M)`, y actualizar `X^h` cuesta `O(n)`.

Total: **`O(n log n + n^k · n) = O(n^(k+1))`** para `k >= 1`. El caso `k = 0` queda en `O(n log n)`.

Para `k` fijo el costo es polinomial en `n`, por lo que `S(k)` es un esquema de aproximación polinomial. La **garantía** es que en el peor caso la solución está a `r = k / (k + 1)` del óptimo: al aumentar `k` mejora la garantía, y crece el exponente del costo.

Complejidad espacial: `O(n)`, sin contar la entrada.

Las cotas cuestan `O(n log n)` por el ordenamiento. El óptimo por Programación dinámica (Ej 3A del TP1) cuesta `O(n * c)` en tiempo y `O(c)` en espacio, porque solo se conserva una fila.

## 5. Sets de datos

Los sets están en `casos/` y se generan con `generar_casos.py`. Se usó la distribución de `crear_mochila.py` de la cátedra: pesos en 1-200, beneficios en 1-1000 y capacidad `50 * n`, de manera que aproximadamente la mitad de los elementos entra en la mochila.

Tamaños: `n` = 20, 40, 60, 80, 100, 120, 200, 300, 400, 600, 800 y 1000. Se usa la semilla fija 2026 para que los archivos sean reproducibles.

Criterios:

- Los tamaños chicos, con paso constante, dan varios puntos para `k = 3`, cuyo costo crece como `n^4`.
- Los tamaños mayores muestran el crecimiento de `k = 1` y `k = 2`.
- Cada `k` se corre hasta el mayor `n` con un tiempo razonable: 1000 para `k = 1`, 400 para `k = 2` y 120 para `k = 3`.

## 6. Tiempos de ejecución

Se midió con `time.perf_counter` solo la ejecución del algoritmo, sin la lectura del archivo. Cada valor es el promedio de 5 corridas. Los resultados completos están en `tiempos_sahni.csv`.

| n | k = 1 (s) | k = 2 (s) | k = 3 (s) |
|---:|---:|---:|---:|
| 20 | 0,00022 | 0,00255 | 0,01328 |
| 40 | 0,00066 | 0,01315 | 0,07477 |
| 60 | 0,00040 | 0,01215 | 0,31135 |
| 80 | 0,00076 | 0,03068 | 1,24273 |
| 100 | 0,00128 | 0,10191 | 2,24106 |
| 120 | 0,00149 | 0,09383 | 4,33455 |
| 200 | 0,00405 | 0,45499 | - |
| 300 | 0,01099 | 1,55584 | - |
| 400 | 0,02194 | 3,68648 | - |
| 600 | 0,03965 | - | - |
| 800 | 0,06660 | - | - |
| 1000 | 0,11150 | - | - |

Gráficos: `graficos/grafico_tiempos_k1.png`, `graficos/grafico_tiempos_k2.png` y `graficos/grafico_tiempos_k3.png`.

## 7. Informe de resultados

### Comparación de los cuatro valores

| n | Sahni k = 1 | Sahni k = 2 | Sahni k = 3 | Óptimo | Martello y Toth | Relajación lineal |
|---:|---:|---:|---:|---:|---:|---:|
| 20 | 7781 | 7781 | 7781 | 7781 | 7912 | 7913 |
| 40 | 16471 | 16471 | 16471 | 16471 | 16490 | 16492 |
| 60 | 24908 | 24908 | 24908 | 24908 | 24923 | 24924 |
| 80 | 34035 | 34035 | 34035 | 34038 | 34117 | 34117 |
| 100 | 41903 | 41903 | 41903 | 41903 | 41914 | 41917 |
| 120 | 47875 | 47875 | 47875 | 47875 | 47901 | 47901 |
| 200 | 81529 | 81549 | - | 81549 | 81594 | 81595 |
| 300 | 118616 | 118616 | - | 118616 | 118647 | 118648 |
| 400 | 165551 | 165575 | - | 165575 | 165581 | 165581 |
| 600 | 238888 | - | - | 238900 | 238909 | 238911 |
| 800 | 323271 | - | - | 323271 | 323276 | 323276 |
| 1000 | 414931 | - | - | 414931 | 414937 | 414937 |

En todas las instancias se cumple `Sahni <= Óptimo <= U2 (Martello y Toth) <= Relajación lineal`, y además `Sahni >= k / (k + 1) · Óptimo`. El óptimo se obtuvo con Programación dinámica (Ej 3A del TP1) y la relajación lineal se informa con piso.

- **Sahni** quedó muy por encima de su garantía teórica (1/2 con `k = 1`, 2/3 con `k = 2` y 3/4 con `k = 3`). La mayor distancia observada al óptimo fue de 0,0245 %, con `k = 1` y `n = 200`.
- Con `k = 1`, Sahni alcanzó el óptimo en 8 de 12 instancias. Con `k = 2`, en 8 de 9: la excepción es `n = 80`, donde tampoco lo alcanza `k = 3`. Más `k` nunca empeoró el resultado.
- **Martello y Toth** nunca superó a la relajación lineal, como indica la teoría. La mejora fue muy chica, de 3 unidades como máximo, y en 5 de 12 instancias las dos cotas coincidieron.
- La distancia entre las cotas y el óptimo tiende a bajar al crecer `n`: pasa de 1,7 % en `n = 20` a 0,0014 % en `n = 1000`. Con muchos elementos, un solo elemento fraccionado pesa poco en el total.

El gráfico `graficos/grafico_comparacion_cotas.png` muestra la diferencia porcentual con el óptimo. El eje vertical usa escala logarítmica simétrica porque las diferencias abarcan varios órdenes de magnitud.

### ¿Los tiempos se corresponden con la complejidad determinada inicialmente?

Sí. Se ajustó por cuadrados mínimos la constante de `tiempo(n) = c * n^(k+1)`:

| k | Curva teórica | c | R² |
|---:|---|---:|---:|
| 1 | `c * n^2` | 1,10e-07 | 0,9972 |
| 2 | `c * n^3` | 5,76e-08 | 0,9998 |
| 3 | `c * n^4` | 2,15e-08 | 0,9890 |

La constante baja al aumentar `k`, lo que es coherente con el factor `1/k!` de la cantidad de subconjuntos, `C(n, k) ~ n^k / k!`. El término `n log n` del ordenamiento es despreciable frente al resto en estos tamaños. En los valores más chicos de `n` los tiempos son del orden de microsegundos a milisegundos y tienen más ruido relativo, por lo que algunos puntos se apartan de la curva.

### Conclusión

En esta distribución de instancias, `k = 1` ya da soluciones casi óptimas a un costo muy bajo. Pasar a `k = 2` o `k = 3` multiplica el tiempo y la mejora de beneficio es mínima o nula. Esto no contradice la garantía de peor caso, que es lo único que asegura el algoritmo para cualquier instancia: solo muestra que estas instancias aleatorias están lejos del peor caso.

## Referencias

Martello, S., & Toth, P. (1990). *Knapsack problems: Algorithms and computer implementations*. John Wiley & Sons.

Sahni, S. (1975). Approximate algorithms for the 0/1 knapsack problem. *Journal of the ACM*, *22*(1), 115–124.
