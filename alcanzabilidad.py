# alcanzabilidad.py
# Prueba de alcanzabilidad: BFS sobre configuraciones (estado AFN, mundo/pila).
# Usa las MISMAS tablas y funciones del juego (narrativa, mundo, combate).
# El combate se modela como no determinista: puede no ocurrir, ganarse o perderse.
# Salida: secuencia MÍNIMA de decisiones para cada final.

import copy
from collections import deque

import combate
import mundo
import narrativa

OMITIR = {"hablar_npc", "usar_botiquin"}   # no cambian la alcanzabilidad


def clave(estado, c):
    s = c["sistemas_reparados"]
    return (estado, tuple(sorted(c["inventario"])), tuple(c["pila_mundo"]),
            s["motores"], s["comunicaciones"], s["hangar_minimo"], c["alien_derrotado"])


def sucesores(estado, c):
    for decision in mundo.acciones_mundo(estado, c) + narrativa.acciones_narrativas(estado):
        if decision in OMITIR:
            continue
        if decision in mundo.ACCIONES_MUNDO:
            c2 = copy.deepcopy(c)
            mundo.procesar_accion_mundo(decision, estado, c2)
            yield decision, estado, c2
            continue
        for dest in narrativa.delta(estado, decision, c):
            c2 = copy.deepcopy(c)
            mundo.actualizar_pila(c2, decision, dest)
            if narrativa.es_estado_final(dest):
                yield decision, dest, c2
                continue
            if not combate.combate_forzado(c2, dest):
                yield decision, dest, c2                          # sin combate
            if combate.combate_posible(c2, dest):
                cv = copy.deepcopy(c2)
                cv["alien_derrotado"], cv["alien_hp"] = True, 0
                yield decision + " [gana combate]", dest, cv      # victoria
                yield decision + " [muere en combate]", "final_c_muerte", c2


def explorar():
    c0 = mundo.nuevo_mundo()
    inicio = narrativa.ESTADO_INICIAL
    cola = deque([(inicio, c0, [])])
    visto = {clave(inicio, c0)}
    escenas, finales = {inicio}, {}
    while cola:
        estado, c, camino = cola.popleft()
        escenas.add(estado)
        if narrativa.es_estado_final(estado):
            finales.setdefault(estado, camino)
            continue
        if estado != inicio:    # invariante del APD: el tope de la pila es la escena actual
            assert c["pila_mundo"][-1] == estado, (estado, c["pila_mundo"])
        for etiqueta, dest, c2 in sucesores(estado, c):
            k = clave(dest, c2)
            if k not in visto:
                visto.add(k)
                cola.append((dest, c2, camino + [etiqueta]))
    return escenas, finales, len(visto)


if __name__ == "__main__":
    escenas, finales, n = explorar()
    print(f"Configuraciones exploradas: {n}")
    todas = {e for (e, _) in narrativa.TRANSICIONES} | {
        d for lst in narrativa.TRANSICIONES.values() for d, _ in lst}
    print(f"Escenas inalcanzables: {sorted(todas - escenas) or 'ninguna'}\n")
    for f in sorted(narrativa.ESTADOS_ACEPTACION):
        if f in finales:
            print(f"{f}  ({len(finales[f])} decisiones):")
            for i, paso in enumerate(finales[f], 1):
                print(f"   {i}. {paso}")
        else:
            print(f"{f}: INALCANZABLE")
    assert set(finales) == narrativa.ESTADOS_ACEPTACION, "Hay finales inalcanzables"
    print("\nOK: los 4 finales son alcanzables y el invariante de la pila se cumple.")
