# Problema 3 - Mochila 0/1: Algoritmo randomizado

> Plantilla: falta implementar la solución, los casos y los gráficos.

## Descripción del problema

Resuelve la mochila 0/1 en forma aproximada con un algoritmo randomizado propio y compara resultado y tiempo con Greedy (Ej 2 del TP1) y Programación Dinámica (Ej 3A del TP1).

## Estructura de archivos y carpetas

| Archivo / carpeta | Descripción |
|---|---|
| `casos/` | Archivos `.txt` con las instancias, generados por `generar_casos.py`. |
| `graficos/` | Gráficos `.png` generados por `graficos.py`. |
| `generar_casos.py` | Genera los casos con la distribución de `crear_mochila.py` de la cátedra. |
| `solucion_randomizado.py` | Lee `casos/`, resuelve cada uno y guarda `tiempos_randomizado.csv`. |
| `graficos.py` | Lee el CSV y genera los gráficos dentro de `graficos/`. |
| `tiempos_randomizado.csv` | Resultados obtenidos para cada set de datos. |
| `informe.md` | Plantilla de esta sección del informe, para pasar a Google Docs. |

## Orden de ejecución

Parado en esta carpeta:

```
1. python generar_casos.py
2. python solucion_randomizado.py
3. python graficos.py
```

## Nota sobre los datos

Sin semilla, volver a ejecutar `generar_casos.py` reemplaza los sets de datos y cambian los tiempos.
