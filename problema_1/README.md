# Problema 1 - Mochila 0/1: Fuerza Bruta vs. Backtracking

## Descripción del problema

Se resuelve el problema de la mochila 0/1 (cada elemento se lleva entero o no se lleva, no hay fracciones) con dos enfoques distintos:

1. **Fuerza bruta**: prueba todos los subconjuntos posibles de elementos (los `2^n` subconjuntos que se pueden formar con `n` elementos) y se queda con el de mayor beneficio que no supere la capacidad. Complejidad `O(n·2^n)`.
2. **Backtracking**: recorre el mismo árbol de decisiones (incluir / excluir cada elemento), pero podando ramas que no pueden mejorar la solución encontrada hasta el momento, mediante dos podas:
   - **Poda por factibilidad de peso (obligatoria)**: no se explora la rama "incluir" si el elemento hace superar la capacidad.
   - **Poda por cota optimista de beneficio (opcional)**: se corta la rama completa si, en el mejor de los casos, no se puede superar la mejor solución ya encontrada.

Ambos enfoques llegan exactamente al mismo resultado óptimo; lo que cambia es el tiempo que tardan en encontrarlo.

## Estructura de archivos y carpetas

| Archivo / carpeta | Descripción |
|---|---|
| `casos/` | Archivos `.txt` con las instancias de mochila a resolver, generados por `crear_mochila.py`. |
| `graficos/` | Gráficos `.png` generados por `graficos.py`. |
| `crear_mochila.py` | Genera los casos de prueba (`mochila10.txt`, `mochila13.txt`, `mochila16.txt`, `mochila19.txt`, `mochila22.txt`) dentro de `casos/`. |
| `solucion_fuerza_bruta.py` | Lee los casos de `casos/`, resuelve cada uno por fuerza bruta y guarda los tiempos en `tiempos_fuerza_bruta.csv`. |
| `solucion_backtracking.py` | Lee los mismos casos de `casos/`, los resuelve por backtracking y guarda los tiempos en `tiempos_backtracking.csv`. |
| `graficos.py` | Lee ambos CSV y genera los tres gráficos comparativos dentro de `graficos/`. |
| `tiempos_fuerza_bruta.csv` | Resultados (n, capacidad, beneficio máximo, peso usado, tiempo) de la corrida de fuerza bruta. |
| `tiempos_backtracking.csv` | Resultados (n, capacidad, beneficio máximo, peso usado, tiempo) de la corrida de backtracking. |

## Orden de ejecución

Los scripts tienen dependencias entre sí, así que hay que correrlos en este orden:

```
1. python crear_mochila.py           # genera mochila10.txt ... mochila22.txt dentro de casos/
2. python solucion_fuerza_bruta.py   # lee casos/, corre fuerza bruta, imprime resultados y guarda tiempos_fuerza_bruta.csv
3. python solucion_backtracking.py   # lee casos/, corre backtracking, imprime resultados y guarda tiempos_backtracking.csv
4. python graficos.py                # lee ambos CSV y genera grafico_fuerza_bruta.png, grafico_backtracking.png y grafico_comparativo.png dentro de graficos/
```

El orden importa: sin correr `crear_mochila.py` primero no hay archivos para leer en `casos/`, y sin correr ambas soluciones no hay CSV para que `graficos.py` pueda graficar.

## Nota sobre los datos

`crear_mochila.py` no usa una semilla fija, así que los datos generados (y por lo tanto los tiempos exactos medidos) van a variar levemente entre corridas. El análisis de por qué el tiempo de backtracking no es estrictamente creciente con `n` (depende de qué tan efectiva resulta la poda para cada instancia particular, no solo del tamaño) se desarrolla en el informe, no en este README.

## Requerimientos

- Python 3.14+
- `numpy`
- `matplotlib`

(Los módulos `csv` y `time` son de la biblioteca estándar de Python y no requieren instalación aparte).
