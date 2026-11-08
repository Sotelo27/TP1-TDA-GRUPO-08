# Trabajo Práctico 2 - Teoría de Algoritmos (2° Cuatrimestre 2026)

## Descripción General

Resolución del **Trabajo Práctico 2** de **Teoría de Algoritmos (TB024 - Curso Echevarría)**, Facultad de Ingeniería, UBA. Aborda el **problema de la mochila 0/1** con algoritmos aproximados y randomizados.

> Estado actual: el Problema 1 está resuelto. Los Problemas 2, 3 y 4 son plantillas por implementar.

---

## Contenido por Problema

- **Problema 1 - Algoritmo aproximado de Sahni:** comparación contra las cotas de relajación lineal y de Martello y Toth y contra el óptimo exacto.
- **Problema 2 - Algoritmo arbitrariamente bueno:** épsilon parametrizable.
- **Problema 3 - Algoritmo randomizado:** comparación con Greedy y Programación Dinámica del TP1.
- **Problema 4 - Conclusiones:** comparación de tiempos de todos los algoritmos de los TPs 1 y 2.

---

## Estructura

| Carpeta / archivo | Descripción |
|---|---|
| `problema_N/` | Casos, gráficos, scripts, resultados, README e `informe.md` de cada problema. |
| `informe/` | Plantilla del informe general y PDF final. |
| `tests/test_base.py` | Verificación del Problema 1 y de las plantillas. |

---

## Requerimientos

- **Lenguaje:** Python 3.14+
- **Bibliotecas:** `matplotlib`, `numpy`

Instalación:

    pip install numpy matplotlib

---

## Ejecución

Parado en cada carpeta `problema_N/`, en este orden (el nombre de la solución de cada problema está en su `README.md` interno):

    python generar_casos.py    -> genera los sets de datos en casos/
    python solucion_X.py       -> resuelve, mide y guarda el CSV de resultados
    python graficos.py         -> genera los gráficos en graficos/

Verificación, parado en la raíz del repositorio:

    python tests/test_base.py

---

## Informe

El informe se escribe en Google Docs a partir de `informe/plantilla_general.md` y de cada `problema_N/informe.md`. Se exporta como `informe/TP2_Informe_Grupo08.pdf`.
