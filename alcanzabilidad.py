import copy
import os
import re
from collections import deque

import combate
import mundo
import narrativa


# La pila no tiene limite en el juego; la busqueda se acota a esta altura.
PROF_MAX_PILA = 4


OMITIR = {
    "hablar_npc",
    "usar_botiquin",
}


def clave(estado, c):
    sistemas = c["sistemas_reparados"]
    puertas = c.get("puertas_desbloqueadas", {})

    return (
        estado,
        tuple(sorted(c["inventario"])),
        tuple(sorted(c["recogidos"])),
        tuple(c["pila_mundo"]),
        sistemas["motores"],
        sistemas["comunicaciones"],
        sistemas["oxigeno"],
        sistemas["hangar_minimo"],
        tuple(sorted(puertas.items())),
        c["alien_derrotado"],
        c["alien_hp"],
    )


def sucesores(estado, c):
    acciones = (
        mundo.acciones_mundo(estado, c)
        + narrativa.acciones_narrativas(estado)
    )

    for decision in acciones:
        if decision in OMITIR:
            continue

        if decision in mundo.ACCIONES_MUNDO:
            c2 = copy.deepcopy(c)
            mundo.procesar_accion_mundo(
                decision,
                estado,
                c2,
            )
            yield decision, estado, c2
            continue

        destinos = narrativa.delta(
            estado,
            decision,
            c,
        )

        for destino in destinos:
            # Transicion no determinista: la etiqueta dice a que escena llevo.
            paso = f"{decision} -> {destino}" if len(destinos) > 1 else decision

            c2 = copy.deepcopy(c)

            mundo.actualizar_pila(
                c2,
                decision,
                destino,
            )

            if narrativa.es_estado_final(destino):
                yield paso, destino, c2
                continue

            # Camino sin combate aleatorio.
            if not combate.combate_forzado(c2, destino):
                yield paso, destino, c2

            # Posibles resultados del combate.
            if combate.combate_posible(c2, destino):
                victoria = copy.deepcopy(c2)
                victoria["alien_derrotado"] = True
                victoria["alien_hp"] = 0
                victoria["alien_estado"] = "derrotado"

                yield (
                    paso + " [gana combate]",
                    destino,
                    victoria,
                )

                huida = copy.deepcopy(c2)

                yield (
                    paso + " [huye del combate]",
                    destino,
                    huida,
                )

                derrota = copy.deepcopy(c2)
                derrota["vida"] = 0

                yield (
                    paso + " [muere en combate]",
                    "final_c_muerte",
                    derrota,
                )


def verificar_regreso_por_pila():
    # Misma sala y misma decision 'volver', distinto destino segun la pila.
    c = mundo.nuevo_mundo()
    estado = narrativa.ESTADO_INICIAL
    camino = [
        ("explorar_pasillo", "pasillo_principal"),
        ("entrar_ductos", "hangar"),
        ("entrar_ductos", "laboratorio_c"),
        ("entrar_ductos", "comunicaciones"),
        ("volver", "laboratorio_c"),
    ]

    for decision, esperado in camino:
        assert esperado in narrativa.delta(estado, decision, c), (estado, decision)
        mundo.actualizar_pila(c, decision, esperado)
        estado = esperado

    # Puerta del laboratorio cerrada: no se puede salir por ella.
    assert narrativa.delta(estado, "salir_puerta", c) == []

    # Abierta, la puerta lleva al pasillo y desapila todo lo de encima.
    c["puertas_desbloqueadas"]["laboratorio_c"] = True
    assert narrativa.delta(estado, "salir_puerta", c) == ["pasillo_principal"]
    mundo.actualizar_pila(c, "salir_puerta", "pasillo_principal")
    assert c["pila_mundo"] == ["Z0", "pasillo_principal"], c["pila_mundo"]


def explorar():
    c0 = mundo.nuevo_mundo()
    inicio = narrativa.ESTADO_INICIAL

    cola = deque([(inicio, c0, [])])
    visto = {clave(inicio, c0)}
    escenas = {inicio}
    finales = {}

    while cola:
        estado, c, camino = cola.popleft()
        escenas.add(estado)

        if narrativa.es_estado_final(estado):
            finales.setdefault(estado, camino)
            continue

        if estado != inicio:
            assert c["pila_mundo"][-1] == estado, (
                estado,
                c["pila_mundo"],
            )

        for etiqueta, destino, c2 in sucesores(estado, c):
            k = clave(destino, c2)

            if k not in visto and len(c2["pila_mundo"]) <= PROF_MAX_PILA:
                visto.add(k)
                cola.append(
                    (
                        destino,
                        c2,
                        camino + [etiqueta],
                    )
                )

    return escenas, finales, len(visto)


DIAGRAMA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "01_diagrama_afn.md")


def verificar_diagrama():
    # El PDF exige que el diagrama coincida exactamente con el codigo.
    if not os.path.exists(DIAGRAMA):
        print("(Sin docs/01_diagrama_afn.md: no se compara el diagrama.)")
        return

    texto = open(DIAGRAMA, encoding="utf-8").read()
    mermaid = texto.split("```mermaid", 1)[1].split("```", 1)[0]

    dibujadas = set()

    for origen, destino, etiqueta in re.findall(r"^\s*(\w+) --> (\w+) : (.+)$", mermaid, re.M):
        for parte in etiqueta.split("·"):
            decision = parte.split()[0]
            dibujadas.add((origen, "vida=0" if decision.startswith("[") else decision, destino))

    en_codigo = {
        (estado, decision, destino)
        for (estado, decision), lista in narrativa.TRANSICIONES.items()
        for destino, _ in lista
    }

    # Muerte en combate: desde toda escena no final donde puede haber combate.
    en_codigo |= {
        (estado, "vida=0", "final_c_muerte")
        for estado, _ in narrativa.TRANSICIONES
        if combate.combate_posible(mundo.nuevo_mundo(), estado)
    }

    assert dibujadas == en_codigo, (
        "El diagrama no coincide con narrativa.py. "
        f"Faltan: {sorted(en_codigo - dibujadas)}. Sobran: {sorted(dibujadas - en_codigo)}"
    )

    print(f"Diagrama: {len(en_codigo)} transiciones, coincide con el código.")


if __name__ == "__main__":
    verificar_regreso_por_pila()
    verificar_diagrama()

    escenas, finales, configuraciones = explorar()

    print(
        f"Configuraciones exploradas: {configuraciones}"
    )

    todas = {
        estado
        for estado, _ in narrativa.TRANSICIONES
    } | {
        destino
        for lista in narrativa.TRANSICIONES.values()
        for destino, _ in lista
    }

    inalcanzables = sorted(todas - escenas)

    print(
        "Escenas inalcanzables: "
        f"{inalcanzables or 'ninguna'}"
    )

    print()

    for final in sorted(narrativa.ESTADOS_ACEPTACION):
        if final in finales:
            print(
                f"{final} ({len(finales[final])} decisiones):"
            )

            for i, paso in enumerate(finales[final], 1):
                print(f"   {i}. {paso}")
        else:
            print(f"{final}: INALCANZABLE")

    assert set(finales) == narrativa.ESTADOS_ACEPTACION, (
        "Hay finales inalcanzables"
    )