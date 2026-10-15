## Ejecución

Requiere **PuLP 3.x** (`pip install "pulp<4"`): la versión 4.0 cambió la forma de crear
variables y no es compatible con el código. También usa `numpy` y `matplotlib` para los gráficos.

Parado en la carpeta problema_4/, ejecutar en este orden:

    python3 generar_casos.py           -> genera los .txt de prueba en casos/ (y los difíciles en casos/dificiles/)
    python3 solucion.py                -> resuelve con PuLP y guarda los tres CSV de tiempos
    python3 graficos.py                -> genera los gráficos en graficos/ e imprime los ajustes

o

    py generar_casos.py
    py solucion.py
    py graficos.py

Las carpetas casos/ y graficos/ se crean solas si no existen. La corrida completa de
solucion.py tarda alrededor de 25 segundos.

`crear_mochila.py` es el script provisto por la cátedra y se deja sin modificar; `generar_casos.py` lo llama para cada tamaño de mochila.

## Experimentos

| Experimento | Casos | CSV |
|---|---|---|
| Rango chico | n = 10, 15, 20, 25, 30, 35, 40 (crear_mochila.py) | `tiempos_pulp_chico.csv` |
| Rango grande | n = 1000, 2000, 5000, 10000, 15000, 20000 (crear_mochila.py) | `tiempos_pulp_grande.csv` |
| Extra: instancias difíciles | n = 10, 20, 30, 40, beneficio = peso + 20 (función propia en generar_casos.py) | `tiempos_pulp_dificil.csv` |

Cada instancia se resuelve 5 veces (`REPETICIONES` en solucion.py) y se guarda el promedio.
Columnas de los CSV:

- `estado`: estado que devuelve el solver (tiene que ser `Optimal`).
- `beneficio_maximo`, `peso_usado`: solución encontrada.
- `nodos_bb`: nodos de Branch and Bound explorados por CBC (se lee de su log).
- `tiempo_construccion`: armado del modelo (variables, función objetivo y restricción).
- `tiempo_resolucion`: `prob.solve`, incluye escribir el modelo, lanzar CBC y leer la solución.
- `tiempo_cbc_interno`: tiempo que reporta el propio CBC en su log (resolución de 0.01 s).
- `tiempo_total`: construcción + resolución.

## Gráficos

- `grafico_pulp_teorico_2n.png`: rango chico, tiempo medido vs. curva teórica c·2^n (eje y logarítmico).
- `grafico_pulp_modelos.png`: rango grande, tiempo medido vs. ajustes c·n, c·n·log n y c·n² (log-log),
  con la pendiente empírica k. La curva 2^n no se puede dibujar en este rango.
- `grafico_pulp_construccion.png`: rango grande, construcción del modelo vs. resolución.
- `grafico_pulp_dificiles.png`: extra, instancias de crear_mochila.py vs. instancias difíciles.

`graficos.py` imprime en consola las constantes ajustadas, el R² y el error relativo de cada modelo.

## Notas

- generar_casos.py genera mochilas al azar: si se vuelve a ejecutar, se reemplazan
  los sets de datos y los tiempos cambian. Para reproducir los resultados del informe,
  usar los archivos que ya están en casos/ y ejecutar solo solucion.py y graficos.py.
- Los tiempos dependen de la computadora: en otra máquina los valores van a ser
  distintos, pero la forma de la curva debería mantenerse.
