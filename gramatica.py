import random
import re


BNF = r"""
<ERROR_TRANSICION> ::= "[Astraea]:" <SUJETO> <VERBO> <PROBLEMA>

<ALERTA_ALIEN> ::= "[ALERTA ROJA]:" <SUJETO> <VERBO> <EVENTO>


<SUJETO> ::=
    "El sistema central"
    | "La IA Astraea"
    | "El monitor de bioseguridad"


<VERBO> ::=
    "informa que"
    | "advierte que"
    | "detecta que"


<PROBLEMA> ::=
    "faltan credenciales de acceso" "."
    | "las puertas están bloqueadas" "."
    | "el protocolo de seguridad lo impide" "."


<EVENTO> ::=
    "movimiento en los ductos del techo" "."
    | "una anomalía térmica acercándose" "."
    | "una brecha de contención cercana" "."


<DIALOGO_ASTRAEA> ::=
    "[Astraea]:" <SALUDO_IA> <CONSEJOS> "."


<DIALOGO_VOSS> ::=
    "[Dra. Voss (holograma)]:" <SALUDO_VOSS> <CONSEJOS> "."


<DIALOGO_UNIDAD7> ::=
    "[Unidad-7]:" "BIP." <CONSEJOS> "."


<SALUDO_IA> ::=
    "Tripulante, sigo operativa."
    | "Detecto signos vitales débiles."
    | "Bienvenido de vuelta."


<SALUDO_VOSS> ::=
    "Si me escuchas, aún queda esperanza."
    | "Escucha, no tengo mucho tiempo."


<CONSEJOS> ::=
    <CONSEJO>
    | <CONSEJO> "y además" <CONSEJOS>


<CONSEJO> ::=
    "busca una tarjeta de acceso en el pasillo"
    | "el soplete de ingeniería repara casi todo"
    | "no entres al laboratorio sin armarte"
    | "los ductos son un atajo impredecible"
    | "la sala del reactor es la única forma de reactivar los motores"
    | "restaura el oxígeno antes de enviar el SOS"


<MISION> ::=
    "recoge" <OBJETO> "para" <NPC>
    | "repara" <SISTEMA> "para" <NPC>
    | "derrota a" <ENEMIGO> "en" <LUGAR>


<OBJETO> ::=
    "la tarjeta de acceso"
    | "el soplete de plasma"
    | "el botiquín"
    | "la llave maestra"


<SISTEMA> ::=
    "los motores"
    | "la antena de comunicaciones"
    | "el sistema de oxígeno"


<ENEMIGO> ::= "el X-99"

<LUGAR> ::= "el laboratorio C"

<NPC> ::=
    "la Dra. Voss"
    | "Astraea"
    | "la Unidad-7"
"""


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
            "movimiento en los ductos del techo",
            "."
        ],
        [
            "una anomalía térmica acercándose",
            "."
        ],
        [
            "una brecha de contención cercana",
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
            "derrota a",
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
        ["el X-99"]
    ],

    "<LUGAR>": [
        ["el laboratorio C"]
    ],

    "<NPC>": [
        ["la Dra. Voss"],
        ["Astraea"],
        ["la Unidad-7"]
    ],
}


NPC_POR_ESCENA = {

    "pasillo_principal":
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
        in c.get("inventario", []),

    "el soplete de plasma":
        lambda c:
        "soplete_plasma"
        in c.get("inventario", []),

    "el botiquín":
        lambda c:
        "botiquin"
        in c.get("inventario", []),

    "la llave maestra":
        lambda c:
        "llave_maestra"
        in c.get("inventario", []),

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

    "el X-99":
        lambda c:
        c.get(
            "alien_derrotado",
            False
        ),
}


def expandir(
    simbolo,
    profundidad,
    derivacion,
    rng
):

    if simbolo not in GLC:

        return [
            simbolo
        ]

    producciones = GLC[
        simbolo
    ]

    if profundidad >= MAX_PROF:

        produccion = producciones[0]

    else:

        produccion = rng.choice(
            producciones
        )

    if derivacion is not None:

        derivacion.append(
            f"{simbolo} → "
            f"{' '.join(produccion)}"
        )

    salida = []

    for parte in produccion:

        salida.extend(
            expandir(
                parte,
                profundidad + 1,
                derivacion,
                rng
            )
        )

    return salida


def generar(
    simbolo,
    derivacion=None,
    rng=random
):

    texto = " ".join(
        expandir(
            simbolo,
            0,
            derivacion,
            rng
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
        rng=rng
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
            rng=rng
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