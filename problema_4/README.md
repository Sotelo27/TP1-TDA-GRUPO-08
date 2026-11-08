# Problema 4 - Mochila 0/1: Conclusiones

> Plantilla: falta implementar la solución, los casos y los gráficos.

## Descripción del problema

Compara, en los rangos en que sea posible, los tiempos de fuerza bruta, backtracking, greedy, programación dinámica tradicional, programación lineal, aproximado 1, aproximado 2 (épsilon fijo) y randomizado. Para los aproximados incluye las cotas de la relajación lineal y de Martello y Toth.

## Estructura de archivos y carpetas

| Archivo / carpeta | Descripción |
|---|---|
| `casos/` | Archivos `.txt` con las instancias, generados por `generar_casos.py`. |
| `graficos/` | Gráficos `.png` generados por `graficos.py`. |
| `generar_casos.py` | Genera los casos con la distribución de `crear_mochila.py` de la cátedra. |
| `solucion.py` | Lee `casos/`, resuelve cada uno y guarda `tiempos_todos.csv`. |
| `graficos.py` | Lee el CSV y genera los gráficos dentro de `graficos/`. |
| `tiempos_todos.csv` | Resultados obtenidos para cada set de datos. |
| `informe.md` | Plantilla de esta sección del informe, para pasar a Google Docs. |

## Orden de ejecución

Parado en esta carpeta:

```
1. python generar_casos.py
2. python solucion.py
3. python graficos.py
```

## Nota sobre los datos

Sin semilla, volver a ejecutar `generar_casos.py` reemplaza los sets de datos y cambian los tiempos.
