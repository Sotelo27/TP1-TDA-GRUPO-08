# Problema 1 - Mochila 0/1: Algoritmo aproximado de Sahni (1975)

## Descripción del problema

Resuelve la mochila 0/1 en forma aproximada con el algoritmo de Sahni, para k = 1, 2 y 3, y compara cuatro valores por instancia: resultado de Sahni, cota de la relajación lineal, cota de Martello y Toth y óptimo exacto (programación dinámica).

## Estructura de archivos y carpetas

| Archivo / carpeta | Descripción |
|---|---|
| `casos/` | Archivos `.txt` con las instancias, generados por `generar_casos.py`. |
| `graficos/` | Gráficos `.png` generados por `graficos.py`. |
| `generar_casos.py` | Genera los casos con la distribución de `crear_mochila.py` de la cátedra. |
| `solucion_sahni.py` | Lee `casos/`, resuelve cada uno y guarda `tiempos_sahni.csv`. |
| `cotas.py` | Cota de la relajación lineal, cota de Martello y Toth y óptimo exacto. |
| `utilidades.py` | Lectura y generación de instancias, medición de tiempos y guardado de CSV. |
| `graficos.py` | Lee el CSV y genera los gráficos dentro de `graficos/`. |
| `tiempos_sahni.csv` | Resultados obtenidos para cada set de datos. |
| `informe.md` | Esta sección del informe, para pasar a Google Docs. |

## Orden de ejecución

Parado en esta carpeta:

```
1. python generar_casos.py
2. python solucion_sahni.py
3. python graficos.py
```

## Nota sobre los datos

`generar_casos.py` usa una semilla fija: al volver a ejecutarlo se obtienen los mismos sets de datos. Los tiempos sí cambian entre corridas y entre máquinas.
