## Ejecución

Parado en la carpeta problema_4/, ejecutar en este orden:

    python3 crear_mochila.py     -> genera los .txt de prueba en casos/
    python3 solucion.py          -> resuelve con PuLP y guarda tiempos_pulp.csv
    python3 graficos.py          -> genera graficos/grafico_pulp.png

o

    py crear_mochila.py
    py solucion.py
    py graficos.py

Las carpetas casos/ y graficos/ se crean solas si no existen.

## Notas

- crear_mochila.py genera mochilas al azar: si se vuelve a ejecutar, se reemplazan
  los sets de datos y los tiempos cambian. Para reproducir los resultados del informe,
  usar los archivos que ya están en casos/ y ejecutar solo solucion.py y graficos.py.
- Los tiempos dependen de la computadora: en otra máquina los valores van a ser
  distintos, pero la forma de la curva debería mantenerse.