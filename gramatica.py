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

    "<ALERTA_ALIEN_GRAFICA>": [
        ["Movimiento hostil detectado. La entidad X-99 se aproxima."]
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

    "<MENSAJE_COMBATE>": [
        ["<COMBATE_INICIO>"],
        ["<COMBATE_FALLO_ATAQUE>"],
        ["<COMBATE_GOLPE_CRITICO>"],
        ["<COMBATE_IMPACTO>"],
        ["<COMBATE_ESQUIVA_PREPARADA>"],
        ["<COMBATE_DEFENSA>"],
        ["<COMBATE_OBJETO_INVALIDO>"],
        ["<COMBATE_OBJETO_NO_DISPONIBLE>"],
        ["<COMBATE_LANZAR_OBJETO>"],
        ["<COMBATE_ENTORNO_USADO>"],
        ["<COMBATE_SIN_ENTORNO>"],
        ["<COMBATE_USAR_ENTORNO>"],
        ["<COMBATE_X99_ATURDIDO>"],
        ["<COMBATE_TURNO_PERDIDO>"],
        ["<COMBATE_HUIDA_EXITOSA>"],
        ["<COMBATE_HUIDA_FALLIDA>"],
        ["<COMBATE_ATAQUE_ESQUIVADO>"],
        ["<COMBATE_ATAQUE_X99>"],
        ["<COMBATE_FALLO_X99>"],
        ["<COMBATE_OPCION_INVALIDA>"],
        ["<COMBATE_SIN_OBJETOS>"],
        ["<COMBATE_RESULTADO_HUIDA>"],
        ["<COMBATE_RESULTADO_VICTORIA>"],
        ["<COMBATE_RESULTADO_HUIDA_GRAFICA>"],
        ["<COMBATE_RESULTADO_VICTORIA_GRAFICA>"],
    ],

    "<COMBATE_INICIO>": [
        ["El X-99 emerge de las sombras."]
    ],
    "<COMBATE_FALLO_ATAQUE>": [
        ["El disparo falla."]
    ],
    "<COMBATE_GOLPE_CRITICO>": [
        ["¡Golpe crítico! X-99 recibe", "{dano}", "de daño."]
    ],
    "<COMBATE_IMPACTO>": [
        ["Impactas al X-99. Daño:", "{dano}", "."]
    ],
    "<COMBATE_ESQUIVA_PREPARADA>": [
        ["Te preparas para esquivar."]
    ],
    "<COMBATE_DEFENSA>": [
        ["Intentas defenderte."]
    ],
    "<COMBATE_OBJETO_INVALIDO>": [
        ["Ese objeto no puede lanzarse."]
    ],
    "<COMBATE_OBJETO_NO_DISPONIBLE>": [
        ["No tienes ese objeto."]
    ],
    "<COMBATE_LANZAR_OBJETO>": [
        ["Lanzas", "{objeto}", "y causas", "{dano}", "de daño."]
    ],
    "<COMBATE_ENTORNO_USADO>": [
        ["Ya utilizaste el entorno de esta habitación."]
    ],
    "<COMBATE_SIN_ENTORNO>": [
        ["No hay nada útil que puedas usar aquí."]
    ],
    "<COMBATE_USAR_ENTORNO>": [
        ["{entorno}:", "{dano}", "de daño."]
    ],
    "<COMBATE_X99_ATURDIDO>": [
        ["¡X-99 queda aturdido!"]
    ],
    "<COMBATE_TURNO_PERDIDO>": [
        ["X-99 está aturdido y pierde su turno."]
    ],
    "<COMBATE_HUIDA_EXITOSA>": [
        ["Consigues escapar del X-99."]
    ],
    "<COMBATE_HUIDA_FALLIDA>": [
        ["Intentas escapar, pero X-99 bloquea tu camino."]
    ],
    "<COMBATE_ATAQUE_ESQUIVADO>": [
        ["¡Esquivas el ataque del X-99!"]
    ],
    "<COMBATE_ATAQUE_X99>": [
        ["X-99 te golpea. Pierdes", "{dano}", "HP."]
    ],
    "<COMBATE_FALLO_X99>": [
        ["X-99 falla su ataque."]
    ],
    "<COMBATE_OPCION_INVALIDA>": [
        ["Opción inválida."]
    ],
    "<COMBATE_SIN_OBJETOS>": [
        ["No tienes objetos arrojables."]
    ],
    "<COMBATE_RESULTADO_HUIDA>": [
        ["Lograste romper el contacto. Puedes continuar explorando."]
    ],
    "<COMBATE_RESULTADO_VICTORIA>": [
        ["La amenaza X-99 ha sido neutralizada."]
    ],
    "<COMBATE_RESULTADO_HUIDA_GRAFICA>": [
        ["Escapaste del X-99."]
    ],
    "<COMBATE_RESULTADO_VICTORIA_GRAFICA>": [
        ["X-99 ha sido neutralizado."]
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
        ["los ductos de ventilación"]
    ],

    "<NPC>": [
        ["la Dra. Voss"],
        ["Astraea"],
        ["la Unidad-7"]
    ],
}

BNF = "\n".join(
    f"{nt} ::= " + " | ".join(
        " ".join(p if p in GLC else f'"{p}"' for p in prod)
        for prod in producciones
    )
    for nt, producciones in GLC.items()
)

EVENTOS_COMBATE = {
    "inicio": "<COMBATE_INICIO>",
    "disparo_falla": "<COMBATE_FALLO_ATAQUE>",
    "golpe_critico": "<COMBATE_GOLPE_CRITICO>",
    "impacto": "<COMBATE_IMPACTO>",
    "esquiva_preparada": "<COMBATE_ESQUIVA_PREPARADA>",
    "defensa": "<COMBATE_DEFENSA>",
    "objeto_invalido": "<COMBATE_OBJETO_INVALIDO>",
    "objeto_no_disponible": "<COMBATE_OBJETO_NO_DISPONIBLE>",
    "lanzar_objeto": "<COMBATE_LANZAR_OBJETO>",
    "entorno_usado": "<COMBATE_ENTORNO_USADO>",
    "sin_entorno": "<COMBATE_SIN_ENTORNO>",
    "usar_entorno": "<COMBATE_USAR_ENTORNO>",
    "x99_aturdido": "<COMBATE_X99_ATURDIDO>",
    "turno_perdido": "<COMBATE_TURNO_PERDIDO>",
    "huida_exitosa": "<COMBATE_HUIDA_EXITOSA>",
    "huida_fallida": "<COMBATE_HUIDA_FALLIDA>",
    "ataque_esquivado": "<COMBATE_ATAQUE_ESQUIVADO>",
    "ataque_x99": "<COMBATE_ATAQUE_X99>",
    "fallo_x99": "<COMBATE_FALLO_X99>",
    "opcion_invalida": "<COMBATE_OPCION_INVALIDA>",
    "sin_objetos": "<COMBATE_SIN_OBJETOS>",
    "resultado_huida": "<COMBATE_RESULTADO_HUIDA>",
    "resultado_victoria": "<COMBATE_RESULTADO_VICTORIA>",
    "resultado_huida_grafica": "<COMBATE_RESULTADO_HUIDA_GRAFICA>",
    "resultado_victoria_grafica": "<COMBATE_RESULTADO_VICTORIA_GRAFICA>",
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

    "al X-99":
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
    rng=random
):

    texto = " ".join(
        expandir(
            simbolo,
            0,
            derivacion,
            rng,
            {}
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


def generar_mensaje_combate(evento, **valores):

    simbolo = EVENTOS_COMBATE.get(evento)

    if simbolo is None:
        raise ValueError(
            f"Evento de combate desconocido: {evento}"
        )

    texto = generar(
        simbolo,
        rng=random.Random()
    )

    try:
        return texto.format(**valores)
    except KeyError as error:
        raise ValueError(
            f"Falta el valor {error.args[0]!r} para el evento {evento!r}"
        ) from error


def generar_mensaje_ia(
    contexto,
    rng=random
):

    simbolo = {

        "error_transicion":
            "<ERROR_TRANSICION>",

        "alerta_alien":
            "<ALERTA_ALIEN>",

        "alerta_alien_grafica":
            "<ALERTA_ALIEN_GRAFICA>"

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


