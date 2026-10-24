import random

ESTADO_INICIAL = "aislado_inicio"

# Texto de la escena q0. Su unica salida es explorar_pasillo: siempre termina en el pasillo.
INTRO = [
    (
        "AISLADO // INICIO",
        "Despiertas dentro de una cápsula de aislamiento médico de la nave Astraea. "
        "Las luces de emergencia parpadean y el silencio es total. "
        "No sabes cuánto tiempo estuviste inconsciente.",
    ),
    (
        "ASTRAEA",
        "[Astraea]: Tripulante, sigo operativa. Hubo una brecha de contención en el "
        "Laboratorio C: la entidad X-99 escapó y el resto de la tripulación no responde. "
        "Los motores, el oxígeno y las comunicaciones están dañados.",
    ),
    (
        "AISLADO // INICIO",
        "El Laboratorio C, Comunicaciones y el Hangar quedaron sellados desde dentro; "
        "solo los ductos de ventilación llegan hasta ellos. Para el resto de la nave "
        "necesitarás una tarjeta de acceso. La compuerta de aislamiento se abre: "
        "el Pasillo Principal te espera.",
    ),
]

ESTADOS_ACEPTACION = {
    "final_a_victoria",
    "final_b_escape",
    "final_c_muerte",
    "final_d_autodestruccion",
}


def siempre(_c):
    return True


def tiene(objeto):
    return lambda c: objeto in c.get("inventario", [])


def puerta_desbloqueada(nombre):
    return lambda c: c.get("puertas_desbloqueadas", {}).get(nombre, False)


def reactor_listo(c):
    pila = c.get("pila_mundo", [])
    sistemas = c.get("sistemas_reparados", {})

    return (
        bool(pila)
        and pila[-1] == "sala_reactor"
        and sistemas.get("motores", 0) == 100
    )


SALAS_DUCTOS = ("laboratorio_c", "comunicaciones", "hangar")


def debajo_del_tope(sala):
    # Simbolo que queda en el tope despues del pop.
    return lambda c: c.get("pila_mundo", [])[-2:-1] == [sala]


def regreso(sala):
    # Volver = deshacer el ultimo paso (por donde se entro): va a la sala debajo del tope.
    al_pasillo = debajo_del_tope("pasillo_principal")

    # Ingenieria y Soporte Vital solo se alcanzan desde el pasillo.
    if sala not in SALAS_DUCTOS:
        return [("pasillo_principal", al_pasillo)]

    return [("pasillo_principal", al_pasillo)] + [
        (otra, debajo_del_tope(otra))
        for otra in SALAS_DUCTOS
        if otra != sala
    ]


def sos_posible(c):
    sistemas = c.get("sistemas_reparados", {})

    return (
        sistemas.get("motores", 0) == 100
        and sistemas.get("comunicaciones", 0) == 100
        and sistemas.get("oxigeno", 0) == 100
        and c.get("alien_derrotado", False)
    )


TRANSICIONES = {
    # Inicio
    ("aislado_inicio", "explorar_pasillo"): [
        ("pasillo_principal", siempre)
    ],

    # La tarjeta solo abre estas dos puertas.
    ("pasillo_principal", "ir_ingenieria"): [
        ("ingenieria", tiene("tarjeta_acceso"))
    ],

    ("pasillo_principal", "ir_soporte_vital"): [
        ("soporte_vital", tiene("tarjeta_acceso"))
    ],

    # Estas puertas deben desbloquearse desde el interior.
    ("pasillo_principal", "ir_comunicaciones"): [
        ("comunicaciones", puerta_desbloqueada("comunicaciones"))
    ],

    ("pasillo_principal", "ir_hangar"): [
        ("hangar", puerta_desbloqueada("hangar"))
    ],

    ("pasillo_principal", "ir_laboratorio"): [
        ("laboratorio_c", puerta_desbloqueada("laboratorio_c"))
    ],

    # La misma decision puede llevar a tres destinos distintos.
    ("pasillo_principal", "entrar_ductos"): [
        ("laboratorio_c", siempre),
        ("comunicaciones", siempre),
        ("hangar", siempre),
    ],

    # Ingenieria -> Sala del reactor (zona anidada del APD)
    ("ingenieria", "entrar_sala_reactor"): [
        ("sala_reactor", tiene("soplete_plasma"))
    ],

    ("sala_reactor", "salir_sala"): [
        ("ingenieria", reactor_listo)
    ],

    # Los ductos conectan los sectores bloqueados entre si: el jugador puede
    ("laboratorio_c", "entrar_ductos"): [
        ("comunicaciones", siempre),
        ("hangar", siempre),
    ],

    ("comunicaciones", "entrar_ductos"): [
        ("laboratorio_c", siempre),
        ("hangar", siempre),
    ],

    ("hangar", "entrar_ductos"): [
        ("laboratorio_c", siempre),
        ("comunicaciones", siempre),
    ],

    # Regresos (POP): el destino lo decide la pila, no la sala actual.
    ("ingenieria", "volver"): regreso("ingenieria"),
    ("soporte_vital", "volver"): regreso("soporte_vital"),
    ("comunicaciones", "volver"): regreso("comunicaciones"),
    ("hangar", "volver"): regreso("hangar"),
    ("laboratorio_c", "volver"): regreso("laboratorio_c"),

    # La puerta da siempre al pasillo, pero solo se abre desde dentro.
    # La pila se desapila hasta el pasillo (mundo.actualizar_pila).
    ("comunicaciones", "salir_puerta"): [
        ("pasillo_principal", puerta_desbloqueada("comunicaciones"))
    ],
    ("hangar", "salir_puerta"): [
        ("pasillo_principal", puerta_desbloqueada("hangar"))
    ],
    ("laboratorio_c", "salir_puerta"): [
        ("pasillo_principal", puerta_desbloqueada("laboratorio_c"))
    ],

    # Final B
    ("hangar", "escapar_capsula"): [
        (
            "final_b_escape",
            lambda c: c.get("sistemas_reparados", {}).get(
                "hangar_minimo", False
            ),
        )
    ],

    # Final A
    ("comunicaciones", "enviar_sos_final"): [
        ("final_a_victoria", sos_posible)
    ],

    # Final D
    ("laboratorio_c", "activar_autodestruccion"): [
        ("final_d_autodestruccion", tiene("llave_maestra"))
    ],
}


def acciones_narrativas(estado):
    return [
        decision
        for (e, decision) in TRANSICIONES
        if e == estado
    ]


def delta(estado, decision, condiciones):
    candidatos = TRANSICIONES.get((estado, decision), [])

    return [
        destino
        for destino, condicion in candidatos
        if condicion(condiciones)
    ]


def verificar_vida(estado, condiciones):
    if condiciones.get("vida", 100) <= 0:
        return "final_c_muerte"

    return estado


def procesar_transicion(
    estado_actual,
    decision,
    condiciones,
    rng=random,
):
    if verificar_vida(estado_actual, condiciones) == "final_c_muerte":
        return "final_c_muerte"

    destinos = delta(
        estado_actual,
        decision,
        condiciones,
    )

    if not destinos:
        return "TRANSICION_RECHAZADA"

    return rng.choice(destinos)


def es_estado_final(estado):
    return estado in ESTADOS_ACEPTACION
