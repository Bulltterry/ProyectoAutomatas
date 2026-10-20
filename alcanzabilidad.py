import copy
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
        ("volver", "hangar"),
    ]

    for decision, esperado in camino:
        assert esperado in narrativa.delta(estado, decision, c), (estado, decision)
        mundo.actualizar_pila(c, decision, esperado)
        estado = esperado

    # Puerta del hangar cerrada: no se puede volver al pasillo todavia.
    assert narrativa.delta(estado, "volver", c) == []

    c["puertas_desbloqueadas"]["hangar"] = True
    assert narrativa.delta(estado, "volver", c) == ["pasillo_principal"]


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


if __name__ == "__main__":
    verificar_regreso_por_pila()

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
