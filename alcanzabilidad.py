import copy
from collections import deque

import combate
import mundo
import narrativa


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
            c2 = copy.deepcopy(c)

            mundo.actualizar_pila(
                c2,
                decision,
                destino,
            )

            if narrativa.es_estado_final(destino):
                yield decision, destino, c2
                continue

            # Camino sin combate aleatorio.
            if not combate.combate_forzado(c2, destino):
                yield decision, destino, c2

            # Posibles resultados del combate.
            if combate.combate_posible(c2, destino):
                victoria = copy.deepcopy(c2)
                victoria["alien_derrotado"] = True
                victoria["alien_hp"] = 0
                victoria["alien_estado"] = "derrotado"

                yield (
                    decision + " [gana combate]",
                    destino,
                    victoria,
                )

                huida = copy.deepcopy(c2)

                yield (
                    decision + " [huye del combate]",
                    destino,
                    huida,
                )

                derrota = copy.deepcopy(c2)
                derrota["vida"] = 0

                yield (
                    decision + " [muere en combate]",
                    "final_c_muerte",
                    derrota,
                )


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

            if k not in visto:
                visto.add(k)
                cola.append(
                    (
                        destino,
                        c2,
                        camino + [etiqueta],
                    )
                )

    return escenas, finales, len(visto)


if __name__ == "__main__":
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

    print(
        "\nOK: los 4 finales son alcanzables y "
        "el invariante del APD se cumple."
    )
