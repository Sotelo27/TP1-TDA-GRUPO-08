"""
Verificacion del Problema 1 y de las plantillas. Se corre con
"python tests/test_base.py" o con pytest, parado en la raiz del repositorio.
"""

import importlib.util
import itertools
import os
import random
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "problema_1"))

import cotas
import solucion_sahni
import utilidades


def cargar(ruta_relativa, nombre):
    ruta = os.path.join(RAIZ, *ruta_relativa.split("/"))
    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


def optimo_fuerza_bruta(capacidad, items):
    mejor = 0
    for eleccion in itertools.product((0, 1), repeat=len(items)):
        peso = sum(e * p for e, (p, _) in zip(eleccion, items))
        if peso <= capacidad:
            mejor = max(mejor, sum(e * b for e, (_, b) in zip(eleccion, items)))
    return mejor


def instancias_aleatorias(cantidad=400):
    generador = random.Random(7)
    for _ in range(cantidad):
        n = generador.randint(1, 10)
        items = [(generador.randint(1, 30), generador.randint(1, 60)) for _ in range(n)]
        yield generador.randint(1, 80), items


def test_ejemplo_del_informe():
    capacidad, items = 10, [(6, 18), (5, 14), (5, 13), (2, 4)]
    assert solucion_sahni.mochila_sahni(capacidad, items, 0) == (22, [0, 3], 8)
    assert solucion_sahni.mochila_sahni(capacidad, items, 1) == (27, [1, 2], 10)
    assert cotas.optimo_exacto(capacidad, items) == 27
    assert cotas.cota_relajacion_lineal(capacidad, items) == 29
    assert cotas.cota_martello_toth(capacidad, items) == 29


def test_optimo_coincide_con_fuerza_bruta():
    for capacidad, items in instancias_aleatorias():
        assert cotas.optimo_exacto(capacidad, items) == optimo_fuerza_bruta(capacidad, items)


def test_orden_de_las_cuatro_magnitudes():
    for capacidad, items in instancias_aleatorias():
        optimo = cotas.optimo_exacto(capacidad, items)
        martello_toth = cotas.cota_martello_toth(capacidad, items)
        relajacion = cotas.cota_relajacion_lineal(capacidad, items)
        for k in (1, 2, 3):
            beneficio = solucion_sahni.mochila_sahni(capacidad, items, k)[0]
            assert beneficio <= optimo <= martello_toth <= relajacion


def test_garantia_de_sahni():
    for capacidad, items in instancias_aleatorias():
        optimo = cotas.optimo_exacto(capacidad, items)
        for k in (1, 2, 3):
            assert (k + 1) * solucion_sahni.mochila_sahni(capacidad, items, k)[0] >= k * optimo


def test_seleccion_consistente():
    for capacidad, items in instancias_aleatorias():
        beneficio, indices, peso = solucion_sahni.mochila_sahni(capacidad, items, 2)
        assert len(indices) == len(set(indices))
        assert peso == sum(items[i][0] for i in indices) <= capacidad
        assert beneficio == sum(items[i][1] for i in indices)


def test_mas_k_no_empeora():
    for capacidad, items in instancias_aleatorias():
        beneficios = [solucion_sahni.mochila_sahni(capacidad, items, k)[0] for k in range(4)]
        assert beneficios == sorted(beneficios)


def test_casos_borde():
    assert solucion_sahni.mochila_sahni(5, [], 2) == (0, [], 0)
    assert solucion_sahni.mochila_sahni(5, [(9, 9)], 2) == (0, [], 0)
    assert cotas.cota_relajacion_lineal(5, [(9, 9)]) == 0
    assert cotas.cota_martello_toth(5, [(9, 9)]) == 0
    assert cotas.cota_martello_toth(9, [(2, 3), (3, 4)]) == 7


def sahni_literal_de_clase(c, items, k):
    """S(k) y GS(M) tal como figuran en las diapositivas, sin filtrar elementos."""
    L = sorted(items, key=lambda item: item[1] / item[0], reverse=True)
    n = len(L)
    z_h = 0
    for tamanio in range(k + 1):
        for M in itertools.combinations(range(n), tamanio):
            if sum(L[j][0] for j in M) > c:
                continue
            z_g = 0
            c_gorro = c - sum(L[j][0] for j in M)
            for j in range(n):
                if j not in M and L[j][0] <= c_gorro:
                    z_g += L[j][1]
                    c_gorro -= L[j][0]
            z_h = max(z_h, z_g + sum(L[j][1] for j in M))
    return z_h


def test_sahni_coincide_con_el_pseudocodigo_de_clase():
    for capacidad, items in instancias_aleatorias():
        for k in range(4):
            esperado = sahni_literal_de_clase(capacidad, items, k)
            assert solucion_sahni.mochila_sahni(capacidad, items, k)[0] == esperado


def test_borde_peso_mayor_que_capacidad():
    # El item de mayor densidad no entra: debe filtrarse antes de buscar el critico.
    capacidad, items = 10, [(50, 5000), (6, 12), (6, 6)]
    assert cotas.cota_relajacion_lineal(capacidad, items) == 16
    assert cotas.cota_martello_toth(capacidad, items) == 14  # W1 = 12, W2 = 14
    assert cotas.optimo_exacto(capacidad, items) == 12
    assert solucion_sahni.mochila_sahni(capacidad, items, 1) == (12, [1], 6)


def test_borde_todos_entran():
    capacidad, items = 100, [(2, 3), (3, 4), (5, 50)]
    assert cotas.cota_relajacion_lineal(capacidad, items) == 57
    assert cotas.cota_martello_toth(capacidad, items) == 57
    assert cotas.optimo_exacto(capacidad, items) == 57
    assert solucion_sahni.mochila_sahni(capacidad, items, 1) == (57, [0, 1, 2], 10)


def test_borde_critico_es_el_ultimo():
    # No existe s+1: W1 = 9 sin termino extra, W2 = 9 + piso(8 - 2 * 9 / 3) = 11.
    capacidad, items = 5, [(3, 9), (4, 8)]
    assert cotas.cota_relajacion_lineal(capacidad, items) == 13
    assert cotas.cota_martello_toth(capacidad, items) == 11
    assert cotas.optimo_exacto(capacidad, items) == 9


def test_borde_capacidad_cero_e_instancia_vacia():
    for capacidad, items in ((0, [(1, 5), (2, 9)]), (0, []), (10, [])):
        assert cotas.cota_relajacion_lineal(capacidad, items) == 0
        assert cotas.cota_martello_toth(capacidad, items) == 0
        assert cotas.optimo_exacto(capacidad, items) == 0
        assert solucion_sahni.mochila_sahni(capacidad, items, 2) == (0, [], 0)


def test_borde_empates_en_densidad():
    # Misma densidad en todos: critico con residual 0, W1 = W2 = 20.
    capacidad, items = 10, [(5, 10), (5, 10), (4, 8), (3, 6)]
    assert cotas.cota_relajacion_lineal(capacidad, items) == 20
    assert cotas.cota_martello_toth(capacidad, items) == 20
    assert cotas.optimo_exacto(capacidad, items) == 20

    # El orden de entrada no debe invalidar las desigualdades.
    generador = random.Random(11)
    for _ in range(200):
        items = [(w, 3 * w) for w in (generador.randint(1, 12) for _ in range(8))]
        items += [(w, 2 * w) for w in (generador.randint(1, 12) for _ in range(2))]
        generador.shuffle(items)
        capacidad = generador.randint(1, 50)
        optimo = cotas.optimo_exacto(capacidad, items)
        assert solucion_sahni.mochila_sahni(capacidad, items, 2)[0] <= optimo
        assert optimo <= cotas.cota_martello_toth(capacidad, items)
        assert cotas.cota_martello_toth(capacidad, items) <= cotas.cota_relajacion_lineal(capacidad, items)


def test_generacion_y_lectura_de_casos():
    with tempfile.TemporaryDirectory() as carpeta:
        utilidades.generar_casos(carpeta, [100, 20], semilla=1)
        rutas = utilidades.listar_casos(carpeta)
        assert [os.path.basename(r) for r in rutas] == ["mochila20.txt", "mochila100.txt"]
        capacidad, items = utilidades.parsear_mochila(rutas[1])
        assert capacidad == 5000 and len(items) == 100
        assert all(1 <= p <= 200 and 1 <= b <= 1000 for p, b in items)


def test_plantillas_sin_implementar():
    fptas = cargar("problema_2/solucion_fptas.py", "p2_fptas")
    randomizado = cargar("problema_3/solucion_randomizado.py", "p3_randomizado")
    conclusiones = cargar("problema_4/solucion.py", "p4_conclusiones")
    pendientes = [
        lambda: fptas.mochila_fptas(10, [(1, 1)], 0.1),
        lambda: randomizado.mochila_randomizada(10, [(1, 1)]),
        conclusiones.main,
    ]
    for pendiente in pendientes:
        try:
            pendiente()
        except NotImplementedError:
            continue
        raise AssertionError("La plantilla deberia lanzar NotImplementedError")


if __name__ == "__main__":
    pruebas = [(nombre, f) for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for nombre, prueba in pruebas:
        prueba()
        print(f"OK  {nombre}")
    print(f"\n{len(pruebas)} pruebas OK")
