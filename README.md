# Trabajo Práctico 1 - Teoría de Algoritmos (2° Cuatrimestre 2026)

## Descripción General

Este repositorio contiene la resolución completa del **Trabajo Práctico 1** de la materia **Teoría de Algoritmos (TB024 - Curso Echevarría)** de la **Facultad de Ingeniería, UBA**.

El trabajo aborda el **problema de la mochila (Knapsack Problem)** resuelto mediante distintas estrategias algorítmicas. Cada problema se encuentra desarrollado en su propia carpeta, con su correspondiente análisis (supuestos, diseño, pseudocódigo, complejidad), implementación, sets de datos, pruebas y gráficos de tiempos de ejecución.

---

## Contenido por Problema

### Problema 1 – Fuerza Bruta vs. Backtracking
Implementación del problema de la mochila mediante **fuerza bruta**, y luego mediante **backtracking** para llegar al mismo resultado en menos tiempo.
- Contiene el código fuente y los tests asociados de ambas variantes.
- Cálculo del orden de complejidad temporal de ambos algoritmos.
- `graficos.py` compara la curva de tiempos de ejecución teórica y real de ambos algoritmos.
- Incluye las instrucciones de ejecución en el `README.md` interno.

---

### Problema 2 – Algoritmo Greedy
Resolución del problema de la mochila mediante un enfoque **Greedy**, con garantía de calidad 1/2.
- Archivo `solucion.py` contiene la resolución.
- `graficos.py` genera los gráficos de tiempos de ejecución teórica vs. real.
- Incluye un set de datos creado manualmente para evidenciar el caso donde actúa la garantía de calidad.
- Incluye sets de datos y tests automáticos.

---

### Problema 3 – Programación Dinámica
Dos algoritmos de **Programación Dinámica** para el problema de la mochila:
- Planteo **tradicional**: maximizar el beneficio para una capacidad fija.
- Planteo **alternativo**: minimizar el peso para un beneficio fijo.
- Cálculo del orden de complejidad temporal de ambos algoritmos.
- `graficos.py` genera los gráficos comparativos (teórico vs. real, y entre ambos algoritmos).

---

### Problema 4 – Programación Lineal
Algoritmo que resuelve el problema de la mochila 0/1 mediante **Programación Lineal Entera**, utilizando la biblioteca **PuLP** (con el solver CBC, incluido en la biblioteca).
- `generar_casos.py` genera los sets de datos en `casos/` usando `crear_mochila.py`: un rango chico (n = 10 a 40) y un rango grande (n = 1000 a 20000), más instancias difíciles extra en `casos/dificiles/`.
- `solucion.py` arma el modelo (variables binarias Yi, función objetivo y restricción de capacidad), lo resuelve con PuLP y guarda los resultados, tiempos y nodos de Branch and Bound en `tiempos_pulp_chico.csv`, `tiempos_pulp_grande.csv` y `tiempos_pulp_dificil.csv`.
- `graficos.py` contrasta los tiempos medidos contra la complejidad teórica O(2^n) y contra modelos polinomiales, y guarda los gráficos en `graficos/`.
- Incluye las instrucciones de ejecución en el `README.md` interno.
- **Requiere PuLP 3.x** (`pip install "pulp<4"`): la versión 4.0 cambió la forma de crear variables y no es compatible con el código.

---

### Conclusión
Comparación, en los rangos en que sea posible, de los tiempos obtenidos para los mismos sets de datos por los 6 algoritmos desarrollados (fuerza bruta, backtracking, greedy, programación dinámica tradicional, programación dinámica alternativa y programación lineal). Análisis de los resultados obtenidos.

---

## Generación de Sets de Datos

Los sets de datos utilizados en los distintos problemas se generan a partir del script provisto por la cátedra `crear_mochila.py`, con tamaños adecuados para poder comparar la curva de tiempos de ejecución teórica y real de cada algoritmo.

---

## Ejecución

Cada carpeta de problema contiene un archivo `README.md` con instrucciones detalladas para:
- Ejecutar las soluciones (`python solucion_X.py`)
- Correr los tests (`pytest`)
- Generar gráficos (`python graficos.py`)

---

## Requerimientos

- **Lenguaje:** Python 3.14+ (última versión estable disponible)
- **Bibliotecas:** *(a completar a medida que se desarrolle el TP)*
  - `matplotlib`
  - `numpy`
  - `pulp`
  - `pytest`

Instalación de todas las bibliotecas:

    pip install "pulp<4" numpy matplotlib pytest


## Informe

El informe completo (carátula, índice, supuestos, diseño, pseudocódigo, seguimiento, complejidad, sets de datos, tiempos de ejecución e informe de resultados de cada problema) se encuentra en la carpeta `informe`, en formato PDF.