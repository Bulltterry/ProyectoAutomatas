"""
Motor narrativo = AFN
N = (Q, Sigma, delta, q0, F)

La tarjeta de acceso abre solo Ingenieria y Soporte Vital.
Laboratorio C, Comunicaciones y Hangar permanecen bloqueados desde el pasillo
hasta que el jugador llegue a ellos por los ductos y desbloquee la puerta desde dentro.

La transicion 'entrar_ductos' es no determinista porque puede conducir a varios
estados distintos con la misma entrada.
"""

import random

ESTADO_INICIAL = "aislado_inicio"

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

    # AFN: la misma decision puede llevar a tres destinos distintos.
    # Estos son precisamente los sectores inicialmente bloqueados.
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

    # Regresos normales
    ("ingenieria", "volver_pasillo"): [
        ("pasillo_principal", siempre)
    ],

    ("soporte_vital", "volver_pasillo"): [
        ("pasillo_principal", siempre)
    ],

    # Si se llego por ductos, primero hay que desbloquear la puerta interior.
    ("comunicaciones", "volver_pasillo"): [
        ("pasillo_principal", puerta_desbloqueada("comunicaciones"))
    ],

    ("hangar", "volver_pasillo"): [
        ("pasillo_principal", puerta_desbloqueada("hangar"))
    ],

    ("laboratorio_c", "volver_pasillo"): [
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
