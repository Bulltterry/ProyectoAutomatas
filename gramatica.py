import random
import re


MAX_PROF = 3


GLC = {

    "<ERROR_TRANSICION>": [
        [
            "[Astraea]:",
            "<SUJETO>",
            "<VERBO>",
            "<PROBLEMA>"
        ]
    ],

    "<ALERTA_ALIEN>": [
        [
            "[ALERTA ROJA]:",
            "<SUJETO>",
            "<VERBO>",
            "<EVENTO>"
        ]
    ],

    "<SUJETO>": [
        ["El sistema central"],
        ["La IA Astraea"],
        ["El monitor de bioseguridad"]
    ],

    "<VERBO>": [
        ["informa que"],
        ["advierte que"],
        ["detecta que"]
    ],

    "<PROBLEMA>": [
        [
            "faltan credenciales de acceso",
            "."
        ],
        [
            "las puertas están bloqueadas",
            "."
        ],
        [
            "el protocolo de seguridad lo impide",
            "."
        ],
    ],

    "<EVENTO>": [
        [
            "hay movimiento en los ductos del techo",
            "."
        ],
        [
            "una anomalía térmica se acerca",
            "."
        ],
        [
            "hay una brecha de contención cercana",
            "."
        ],
    ],

    "<DIALOGO_ASTRAEA>": [
        [
            "[Astraea]:",
            "<SALUDO_IA>",
            "<CONSEJOS>",
            "."
        ]
    ],

    "<DIALOGO_VOSS>": [
        [
            "[Dra. Voss (holograma)]:",
            "<SALUDO_VOSS>",
            "<CONSEJOS>",
            "."
        ]
    ],

    "<DIALOGO_UNIDAD7>": [
        [
            "[Unidad-7]:",
            "BIP.",
            "<CONSEJOS>",
            "."
        ]
    ],

    "<SALUDO_IA>": [
        [
            "Tripulante, sigo operativa."
        ],
        [
            "Detecto signos vitales débiles."
        ],
        [
            "Bienvenido de vuelta."
        ],
    ],

    "<SALUDO_VOSS>": [
        [
            "Si me escuchas, aún queda esperanza."
        ],
        [
            "Escucha, no tengo mucho tiempo."
        ],
    ],

    "<CONSEJOS>": [
        [
            "<CONSEJO>"
        ],
        [
            "<CONSEJO>",
            "y además",
            "<CONSEJOS>"
        ]
    ],

    "<CONSEJO>": [
        [
            "busca una tarjeta de acceso en el pasillo"
        ],
        [
            "el soplete de ingeniería repara casi todo"
        ],
        [
            "no entres al laboratorio sin armarte"
        ],
        [
            "los ductos son un atajo impredecible"
        ],
        [
            "la sala del reactor es la única forma "
            "de reactivar los motores"
        ],
        [
            "restaura el oxígeno antes de enviar el SOS"
        ],
    ],

    "<MISION>": [
        [
            "recoge",
            "<OBJETO>",
            "para",
            "<NPC>"
        ],
        [
            "repara",
            "<SISTEMA>",
            "para",
            "<NPC>"
        ],
        [
            "derrota",
            "<ENEMIGO>",
            "en",
            "<LUGAR>"
        ],
    ],

    "<OBJETO>": [
        ["la tarjeta de acceso"],
        ["el soplete de plasma"],
        ["el botiquín"],
        ["la llave maestra"]
    ],

    "<SISTEMA>": [
        ["los motores"],
        ["la antena de comunicaciones"],
        ["el sistema de oxígeno"]
    ],

    "<ENEMIGO>": [
        ["al X-99"]
    ],

    "<LUGAR>": [
        ["el laboratorio C"],
        ["el hangar"],
        ["la sala de comunicaciones"]
    ],

    "<NPC>": [
        ["la Dra. Voss"],
        ["Astraea"],
        ["la Unidad-7"]
    ],
}


# BNF generada desde GLC: el texto entregado siempre coincide con el código.
BNF = "\n".join(
    f"{nt} ::= " + " | ".join(
        " ".join(p if p in GLC else f'"{p}"' for p in prod)
        for prod in producciones
    )
    for nt, producciones in GLC.items()
)


# Cada <LUGAR> es una escena real del AFN: ahí espera el X-99 si la misión lo pide.
ESCENA_POR_LUGAR = {
    "el laboratorio C": "laboratorio_c",
    "el hangar": "hangar",
    "la sala de comunicaciones": "comunicaciones",
}


def escena_objetivo(c):
    mision = c.get("mision") or ""

    if not mision.startswith("derrota"):
        return None

    return ESCENA_POR_LUGAR.get(mision.split(" en ", 1)[-1])


NPC_POR_ESCENA = {

    "pasillo_principal":
        "<DIALOGO_ASTRAEA>",

    "comunicaciones":
        "<DIALOGO_ASTRAEA>",

    "soporte_vital":
        "<DIALOGO_VOSS>",

    "laboratorio_c":
        "<DIALOGO_UNIDAD7>",
}


VERIFICADORES = {

    "la tarjeta de acceso":
        lambda c:
        "tarjeta_acceso"
        in c.get("recogidos", []),

    "el soplete de plasma":
        lambda c:
        "soplete_plasma"
        in c.get("recogidos", []),

    "el botiquín":
        lambda c:
        "botiquin"
        in c.get("recogidos", []),

    "la llave maestra":
        lambda c:
        "llave_maestra"
        in c.get("recogidos", []),

    "los motores":
        lambda c:
        c.get(
            "sistemas_reparados",
            {}
        ).get(
            "motores",
            0
        ) == 100,

    "la antena de comunicaciones":
        lambda c:
        c.get(
            "sistemas_reparados",
            {}
        ).get(
            "comunicaciones",
            0
        ) == 100,

    "el sistema de oxígeno":
        lambda c:
        c.get(
            "sistemas_reparados",
            {}
        ).get(
            "oxigeno",
            0
        ) == 100,

    "al X-99":
        lambda c:
        c.get(
            "alien_derrotado",
            False
        ),
}


# Consejo que ya no hace falta dar cuando se cumple su condicion.
CONSEJO_CUMPLIDO = {
    "busca una tarjeta de acceso en el pasillo": VERIFICADORES["la tarjeta de acceso"],
    "el soplete de ingeniería repara casi todo": VERIFICADORES["el soplete de plasma"],
    "no entres al laboratorio sin armarte": VERIFICADORES["al X-99"],
    "la sala del reactor es la única forma de reactivar los motores": VERIFICADORES["los motores"],
    "restaura el oxígeno antes de enviar el SOS": VERIFICADORES["el sistema de oxígeno"],
}


NPC_DE_DIALOGO = {
    "<DIALOGO_ASTRAEA>": "Astraea",
    "<DIALOGO_VOSS>": "la Dra. Voss",
    "<DIALOGO_UNIDAD7>": "la Unidad-7",
}


def descartes(c, simbolo):
    # Politica del generador: se marcan como "ya usadas" las producciones que no
    # tienen sentido en este momento; la gramatica (BNF) no cambia.
    consejos = [
        p for p in GLC["<CONSEJO>"]
        if p[0] in CONSEJO_CUMPLIDO and CONSEJO_CUMPLIDO[p[0]](c)
    ]
    usadas = {
        "<CONSEJO>": consejos,
        # La mision la pide quien habla.
        "<NPC>": [p for p in GLC["<NPC>"] if p != [NPC_DE_DIALOGO[simbolo]]],
    }

    # Con un solo consejo util no se encadena "y además" (evita repetirlo).
    if len(GLC["<CONSEJO>"]) - len(consejos) < 2:
        usadas["<CONSEJOS>"] = [p for p in GLC["<CONSEJOS>"] if "<CONSEJOS>" in p]

    return usadas


def expandir(
    simbolo,
    profundidad,
    derivacion,
    rng,
    usadas
):

    if simbolo not in GLC:

        return [
            simbolo
        ]

    producciones = GLC[
        simbolo
    ]

    # Politica del generador (la gramatica no cambia): no repetir una
    # produccion en la misma cadena, y al llegar a MAX_PROF solo elegir
    # producciones no recursivas para que la derivacion termine.
    usadas_aqui = usadas.setdefault(simbolo, [])

    candidatas = [
        p for p in producciones
        if p not in usadas_aqui
    ] or producciones

    if profundidad >= MAX_PROF:

        candidatas = [
            p for p in candidatas
            if simbolo not in p
        ] or candidatas

    produccion = rng.choice(
        candidatas
    )

    usadas_aqui.append(
        produccion
    )

    if derivacion is not None:

        derivacion.append(
            f"{simbolo} -> "
            f"{' '.join(produccion)}"
        )

    salida = []

    for parte in produccion:

        salida.extend(
            expandir(
                parte,
                profundidad + 1,
                derivacion,
                rng,
                usadas
            )
        )

    return salida


def generar(
    simbolo,
    derivacion=None,
    rng=random,
    usadas=None
):

    texto = " ".join(
        expandir(
            simbolo,
            0,
            derivacion,
            rng,
            {} if usadas is None else usadas
        )
    )

    texto = re.sub(
        r"\s+([.,:;!?])",
        r"\1",
        texto
    )

    texto = re.sub(
        r"([.:]\s+)([a-záéíóú])",
        lambda m:
        m.group(1)
        + m.group(2).upper(),
        texto
    )

    return texto


def generar_mensaje_ia(
    contexto,
    rng=random
):

    simbolo = {

        "error_transicion":
            "<ERROR_TRANSICION>",

        "alerta_alien":
            "<ALERTA_ALIEN>"

    }.get(
        contexto
    )

    if simbolo:

        return generar(
            simbolo,
            rng=rng
        )

    return (
        "[Astraea]: "
        "Sistemas operando al mínimo."
    )


def mision_cumplida(
    mision,
    c
):

    requisitos = [

        verificar

        for texto, verificar
        in VERIFICADORES.items()

        if texto in mision
    ]

    return (
        bool(requisitos)
        and all(
            verificar(c)
            for verificar
            in requisitos
        )
    )


def hablar(
    c,
    estado,
    rng=random
):

    simbolo = NPC_POR_ESCENA.get(
        estado
    )

    if not simbolo:

        return (
            "Aquí no hay nadie "
            "con quien hablar."
        )

    texto = generar(
        simbolo,
        rng=rng,
        usadas=descartes(c, simbolo)
    )

    mision = c.get(
        "mision"
    )


    if (
        mision
        and mision_cumplida(
            mision,
            c
        )
    ):

        c["vida"] = min(
            100,
            c["vida"] + 25
        )

        c[
            "misiones_completadas"
        ] += 1

        c["mision"] = None

        return (
            f"{texto}\n"
            f"✔ Misión cumplida: "
            f"{mision}\n"
            f"Recompensa: +25 HP. "
            f"HP: {c['vida']}"
        )


    if mision:

        return (
            f"{texto}\n"
            f"► Misión activa: "
            f"{mision}"
        )


    for _ in range(30):

        nueva = generar(
            "<MISION>",
            rng=rng,
            usadas=descartes(c, simbolo)
        )

        if not mision_cumplida(
            nueva,
            c
        ):

            c["mision"] = nueva

            return (
                f"{texto}\n"
                f"► Nueva misión: "
                f"{nueva}"
            )

    return texto


if __name__ == "__main__":

    print(BNF)

    for simbolo in (
        "<MISION>",
        "<DIALOGO_ASTRAEA>",
        "<ERROR_TRANSICION>"
    ):

        derivacion = []

        cadena = generar(
            simbolo,
            derivacion
        )

        print(
            f"\nCadena: "
            f"{cadena}"
        )

        print(
            "Derivación:\n  "
            + "\n  ".join(
                derivacion
            )
        )


    # Auto-chequeo: ningun dialogo repite un consejo y todos aparecen.
    vistos = set()

    for semilla in range(500):
        texto = generar("<DIALOGO_UNIDAD7>", rng=random.Random(semilla))
        consejos = texto.split("BIP. ", 1)[1].rstrip(".").split(" y además ")
        assert len(consejos) == len(set(consejos)), texto
        vistos.update(c.lower() for c in consejos)

    assert len(vistos) == len(GLC["<CONSEJO>"]), vistos
    print("\nOK: 500 dialogos sin consejos repetidos.")

    # Todo <LUGAR> debe ser una escena real, o la misión mandaría a un sitio sin X-99.
    assert set(ESCENA_POR_LUGAR) == {p[0] for p in GLC["<LUGAR>"]}
    print("OK: cada <LUGAR> de las misiones es una escena del AFN.")

    # Auto-chequeo: Voss no aconseja lo ya hecho, no repite consejos y pide
    # misiones para ella; nunca pide recoger algo ya recogido.
    import mundo

    for semilla in range(500):
        rng = random.Random(semilla)
        c = mundo.nuevo_mundo()
        c["recogidos"] = ["tarjeta_acceso", "soplete_plasma", "botiquin"]
        c["sistemas_reparados"]["motores"] = 100
        texto = hablar(c, "soporte_vital", rng)
        dialogo, mision = texto.split("\n► Nueva misión: ")
        dialogo = dialogo.lower()
        assert "tarjeta" not in dialogo and "soplete" not in dialogo and "reactor" not in dialogo, texto
        assert dialogo.count("y además") < 2, texto
        assert "para la Dra. Voss" in mision or mision.startswith("derrota"), mision
        assert not any(o in mision for o in ("la tarjeta", "el soplete", "el botiquín")), mision

    print("OK: dialogos y misiones coherentes con el estado del juego.")
