# Problema 3 - Mochila 0/1: Planteo Tradicional vs Planteo Alternativo

## Descripción del problema

Se resuelve el problema de la mochila 0/1 mediante Programacion Dinamica con dos enfoques distintos:

1. **Planteo Tradicional**: Maximiza el beneficio para una capacidad fija.
2. **Planteo Alternativo**: Minimiza el peso necesario para alcanzar un beneficio fijo. 

Ambos enfoques llegan exactamente al mismo resultado óptimo; lo que cambia es el tiempo que tardan en encontrarlo.

## Estructura de archivos y carpetas

| Archivo / carpeta | Descripción |
|---|---|
| `casos/` | Archivos `.txt` con las instancias de mochila a resolver, generados por `crear_mochila.py`. |
| `graficos/` | Gráficos `.png` generados por `graficos.py`. |
| `crear_mochila.py` | Genera los casos de prueba (`mochila100.txt`, `mochila200.txt`, `mochila300.txt`, `mochila400.txt`, `mochila500.txt`) dentro de `casos/`. |
| `solucion_pd1.py` | Lee los casos de `casos/`, resuelve cada uno por programacion dinamica (version tradicional) y guarda los tiempos en `tiempos_pd_tradicional.csv`. |
| `solucion_pd2.py` | Lee los mismos casos de `casos/`, los resuelve por programacion dinamica (version alternativa) y guarda los tiempos en `tiempos_alternativa.csv`. |
| `graficos.py` | Lee ambos CSV y genera los tres gráficos comparativos dentro de `graficos/`. |
| `tiempos_pd_tradicional.csv` | Resultados (n, capacidad, beneficio máximo, peso usado, tiempo)
| `tiempos_alternativa.csv` | Resultados (n, capacidad, beneficio máximo, peso usado, tiempo)

## Orden de ejecución

Los scripts tienen dependencias entre sí, así que hay que correrlos en este orden:

```
1. python crear_mochila.py
2. python solucion_pd1.py
3. python solucion_pd2.py
4. python graficos.py
```

El orden importa: sin correr `crear_mochila.py` primero no hay archivos para leer en `casos/`, y sin correr ambas soluciones no hay CSV para que `graficos.py` pueda graficar.

**OPCIONAL:** Si se desea ver la reconstruccion del resultado (objetos elegidos), debemos descomentar el print de la linea 136 (`tiempos_pd_tradicional.csv`) o linea 149 (`tiempos_alternativa.csv`).

## Nota sobre los datos

`crear_mochila.py` no usa una semilla fija, así que los datos generados (y por lo tanto los tiempos exactos medidos) van a variar levemente entre corridas.

## Requerimientos

- Python 3.14+
- `numpy`
- `matplotlib`

(Los módulos `csv` y `time` son de la biblioteca estándar de Python y no requieren instalación aparte).