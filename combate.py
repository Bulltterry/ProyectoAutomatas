import random

import gramatica


# =========================================================
# CONFIGURACION
# =========================================================

PROB_IMPACTO = 0.75
PROB_CRITICO = 0.15

PROB_ESQUIVE = 0.60
PROB_HUIDA = 0.35

PROB_IMPACTO_X99 = 0.70
PROB_EMBOSCADA = 0.18


FINALES_COMBATE = {
    "FIN_VICTORIA",
    "FIN_HUIDA",
    "FIN_DERROTA",
}


# =========================================================
# OBJETOS ARROJABLES
# =========================================================

OBJETOS_ARROJABLES = {

    "extintor": {
        "nombre": "Extintor",
        "dano": (8, 12),
        "prob_aturdir": 0.55,
    },

    "bateria_energia": {
        "nombre": "Bateria de energia",
        "dano": (14, 20),
        "prob_aturdir": 0.35,
    },

    "tubo_metalico": {
        "nombre": "Tubo metalico",
        "dano": (10, 16),
        "prob_aturdir": 0.25,
    },
}


# =========================================================
# ENTORNO
# =========================================================

ENTORNOS = {

    "ingenieria": {
        "nombre": "Liberar vapor",
        "dano": (12, 18),
        "prob_aturdir": 0.45,
    },

    "sala_reactor": {
        "nombre": "Abrir valvula de vapor",
        "dano": (16, 22),
        "prob_aturdir": 0.55,
    },

    "soporte_vital": {
        "nombre": "Descarga de presion",
        "dano": (9, 15),
        "prob_aturdir": 0.45,
    },

    "comunicaciones": {
        "nombre": "Sobrecargar panel",
        "dano": (12, 18),
        "prob_aturdir": 0.50,
    },

    "hangar": {
        "nombre": "Cerrar compuerta",
        "dano": (10, 16),
        "prob_aturdir": 0.60,
    },

    "laboratorio_c": {
        "nombre": "Pulso de contencion",
        "dano": (15, 22),
        "prob_aturdir": 0.55,
    },
}


# =========================================================
# DETECCION DE COMBATE
# =========================================================

def combate_forzado(
    c,
    estado_mapa
):
    return (
        not c.get(
            "alien_derrotado",
            False
        )
        and
        # Guarida fija del X-99, o la sala que indica la misión "derrota al X-99 en ...".
        estado_mapa in ("laboratorio_c", gramatica.escena_objetivo(c))
    )


def combate_posible(
    c,
    estado_mapa
):
    return (
        not c.get(
            "alien_derrotado",
            False
        )
        and
        estado_mapa != "aislado_inicio"
    )


def debe_iniciar(
    c,
    estado_mapa,
    rng=random
):
    if combate_forzado(
        c,
        estado_mapa
    ):
        return True

    return (
        combate_posible(
            c,
            estado_mapa
        )
        and
        rng.random()
        < PROB_EMBOSCADA
    )


# =========================================================
# ESTADO DEL X-99
# =========================================================

def actualizar_estado_alien(c):

    hp = c.get(
        "alien_hp",
        0
    )

    if hp <= 0:

        c["alien_hp"] = 0

        c[
            "alien_derrotado"
        ] = True

        c[
            "alien_estado"
        ] = "derrotado"

        return


    if (
        c.get(
            "alien_estado"
        )
        == "aturdido"
    ):
        return


    if hp <= 32:

        c[
            "alien_estado"
        ] = "herido"

    else:

        c[
            "alien_estado"
        ] = "normal"


def aplicar_dano_alien(
    c,
    dano
):
    c["alien_hp"] = max(
        0,
        c.get(
            "alien_hp",
            65
        )
        - dano
    )

    actualizar_estado_alien(
        c
    )


# =========================================================
# COMBATE GRAFICO
# =========================================================

def crear_combate(c):

    c.setdefault(
        "alien_hp",
        65
    )

    c.setdefault(
        "alien_derrotado",
        False
    )

    c.setdefault(
        "alien_estado",
        "normal"
    )

    return {
        "estado": "TURNO_JUGADOR",
        "esquiva": False,
        "entorno_usado": False,
        "mensaje": (
            "El X-99 emerge de las sombras."
        ),
    }


def atacar(
    c,
    combate,
    rng=random
):

    if (
        rng.random()
        >= PROB_IMPACTO
    ):

        combate["mensaje"] = (
            "El disparo falla."
        )

        combate[
            "estado"
        ] = "TURNO_X99"

        return


    dano = rng.randint(
        11,
        18
    )


    if (
        "soplete_plasma"
        in c.get(
            "inventario",
            []
        )
    ):
        dano += 3


    critico = (
        rng.random()
        <
        PROB_CRITICO
    )


    if critico:
        dano *= 2


    aplicar_dano_alien(
        c,
        dano
    )


    if critico:

        combate["mensaje"] = (
            f"¡Golpe critico! "
            f"X-99 recibe {dano} de dano."
        )

    else:

        combate["mensaje"] = (
            f"Impactas al X-99. "
            f"Dano: {dano}."
        )


    if c["alien_derrotado"]:

        combate[
            "estado"
        ] = "FIN_VICTORIA"

    else:

        combate[
            "estado"
        ] = "TURNO_X99"


def defender(
    c,
    combate,
    rng=random
):

    combate["esquiva"] = (
        rng.random()
        <
        PROB_ESQUIVE
    )


    if combate["esquiva"]:

        combate["mensaje"] = (
            "Te preparas para esquivar."
        )

    else:

        combate["mensaje"] = (
            "Intentas defenderte."
        )


    combate[
        "estado"
    ] = "TURNO_X99"


def objetos_disponibles(c):

    return [
        objeto
        for objeto
        in OBJETOS_ARROJABLES

        if objeto
        in c.get(
            "inventario",
            []
        )
    ]


def lanzar_objeto(
    c,
    combate,
    objeto,
    rng=random
):

    if (
        objeto
        not in OBJETOS_ARROJABLES
    ):
        combate[
            "mensaje"
        ] = (
            "Ese objeto no puede lanzarse."
        )

        return


    if objeto not in c.get(
        "inventario",
        []
    ):

        combate[
            "mensaje"
        ] = (
            "No tienes ese objeto."
        )

        return


    datos = (
        OBJETOS_ARROJABLES[
            objeto
        ]
    )


    dano = rng.randint(
        *datos["dano"]
    )


    c["inventario"].remove(
        objeto
    )


    aplicar_dano_alien(
        c,
        dano
    )


    combate["mensaje"] = (
        f"Lanzas {datos['nombre']} "
        f"y causas {dano} de dano."
    )


    if c["alien_derrotado"]:

        combate[
            "estado"
        ] = "FIN_VICTORIA"

        return


    if (
        rng.random()
        <
        datos[
            "prob_aturdir"
        ]
    ):

        c[
            "alien_estado"
        ] = "aturdido"

        combate["mensaje"] += (
            " ¡X-99 queda aturdido!"
        )


    combate[
        "estado"
    ] = "TURNO_X99"


def usar_entorno(
    c,
    combate,
    ubicacion,
    rng=random
):

    if combate[
        "entorno_usado"
    ]:

        combate[
            "mensaje"
        ] = (
            "Ya utilizaste el entorno "
            "de esta habitacion."
        )

        return


    if ubicacion not in ENTORNOS:

        combate[
            "mensaje"
        ] = (
            "No hay nada util "
            "que puedas usar aqui."
        )

        return


    datos = ENTORNOS[
        ubicacion
    ]


    dano = rng.randint(
        *datos["dano"]
    )


    combate[
        "entorno_usado"
    ] = True


    aplicar_dano_alien(
        c,
        dano
    )


    combate["mensaje"] = (
        f"{datos['nombre']}: "
        f"{dano} de dano."
    )


    if c["alien_derrotado"]:

        combate[
            "estado"
        ] = "FIN_VICTORIA"

        return


    if (
        rng.random()
        <
        datos[
            "prob_aturdir"
        ]
    ):

        c[
            "alien_estado"
        ] = "aturdido"

        combate["mensaje"] += (
            " ¡X-99 queda aturdido!"
        )


    combate[
        "estado"
    ] = "TURNO_X99"


def probabilidad_huida(c):

    estado = c.get(
        "alien_estado",
        "normal"
    )


    if estado == "aturdido":
        return 0.90

    if estado == "herido":
        return 0.55

    return PROB_HUIDA


def huir(
    c,
    combate,
    rng=random
):

    prob = probabilidad_huida(
        c
    )


    if rng.random() < prob:

        combate[
            "estado"
        ] = "FIN_HUIDA"

        combate[
            "mensaje"
        ] = (
            "Consigues escapar del X-99."
        )

    else:

        combate[
            "estado"
        ] = "TURNO_X99"

        combate[
            "mensaje"
        ] = (
            "Intentas escapar, "
            "pero X-99 bloquea tu camino."
        )


# =========================================================
# TURNO DEL ALIEN
# =========================================================

def turno_alien(
    c,
    combate,
    rng=random
):

    if (
        combate[
            "estado"
        ]
        != "TURNO_X99"
    ):
        return


    # X-99 aturdido
    if (
        c.get(
            "alien_estado"
        )
        == "aturdido"
    ):

        combate[
            "mensaje"
        ] = (
            "X-99 esta aturdido "
            "y pierde su turno."
        )


        if (
            c.get(
                "alien_hp",
                65
            )
            <= 32
        ):

            c[
                "alien_estado"
            ] = "herido"

        else:

            c[
                "alien_estado"
            ] = "normal"


        combate[
            "estado"
        ] = "TURNO_JUGADOR"

        return


    # Jugador esquiva
    if combate.get(
        "esquiva",
        False
    ):

        combate[
            "esquiva"
        ] = False

        combate[
            "mensaje"
        ] = (
            "¡Esquivas el ataque del X-99!"
        )

        combate[
            "estado"
        ] = "TURNO_JUGADOR"

        return


    # Ataque del alien
    if (
        rng.random()
        <
        PROB_IMPACTO_X99
    ):

        dano = rng.randint(
            14,
            26
        )

        c["vida"] = max(
            0,
            c["vida"] - dano
        )

        combate[
            "mensaje"
        ] = (
            f"X-99 te golpea. "
            f"Pierdes {dano} HP."
        )

    else:

        combate[
            "mensaje"
        ] = (
            "X-99 falla su ataque."
        )


    if c["vida"] <= 0:

        c["vida"] = 0

        combate[
            "estado"
        ] = "FIN_DERROTA"

    else:

        combate[
            "estado"
        ] = "TURNO_JUGADOR"


# =========================================================
# RESULTADO
# =========================================================

def combate_terminado(
    combate
):

    return (
        combate["estado"]
        in FINALES_COMBATE
    )


def resultado_combate(
    combate
):

    if combate_terminado(
        combate
    ):

        return combate[
            "estado"
        ]

    return None

# =========================================================
# COMBATE EN CONSOLA (juego.py)
# =========================================================

def ejecutar_combate(
    c,
    ubicacion,
    rng=random
):

    combate = crear_combate(c)
    print(combate["mensaje"])

    while not combate_terminado(combate):

        print(
            f"\nHP: {c['vida']} | "
            f"X-99: {c['alien_hp']} HP ({c['alien_estado']})"
        )

        acciones = [
            ("Atacar", lambda: atacar(c, combate, rng)),
            ("Defender", lambda: defender(c, combate, rng)),
            ("Huir", lambda: huir(c, combate, rng)),
        ]

        for objeto in objetos_disponibles(c):
            acciones.append((
                f"Lanzar {OBJETOS_ARROJABLES[objeto]['nombre']}",
                lambda o=objeto: lanzar_objeto(c, combate, o, rng),
            ))

        if ubicacion in ENTORNOS and not combate["entorno_usado"]:
            acciones.append((
                ENTORNOS[ubicacion]["nombre"],
                lambda: usar_entorno(c, combate, ubicacion, rng),
            ))

        for i, (texto, _) in enumerate(acciones, 1):
            print(f" {i}. {texto}")

        opcion = input("Acción de combate: ").strip()

        if not opcion.isdigit() or not 1 <= int(opcion) <= len(acciones):
            print("Opción inválida.")
            continue

        acciones[int(opcion) - 1][1]()
        print("> " + combate["mensaje"])

        if combate["estado"] == "TURNO_X99":
            turno_alien(c, combate, rng)
            print("> " + combate["mensaje"])

    return combate["estado"]


if __name__ == "__main__":

    # Auto-chequeo: combates con jugadas al azar siempre terminan
    # en un final del autómata y dejan HP coherentes.
    import builtins
    import contextlib
    import io

    import mundo

    for semilla in range(300):
        rng = random.Random(semilla)
        c = mundo.nuevo_mundo()
        c["inventario"] = ["extintor", "tubo_metalico"]
        builtins.input = lambda _: str(rng.randint(1, 6))

        with contextlib.redirect_stdout(io.StringIO()):
            fin = ejecutar_combate(c, "hangar", rng)

        assert fin in FINALES_COMBATE
        assert (fin == "FIN_DERROTA") == (c["vida"] == 0)
        assert (fin == "FIN_VICTORIA") == c["alien_derrotado"]

    print("OK: 300 combates terminan en un estado final valido.")

