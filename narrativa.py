# narrativa.py
# Motor narrativo = AFN  N = (Q, Σ, δ, q0, F)
#   Q  : escenas (estados)
#   Σ  : decisiones del jugador
#   δ  : TRANSICIONES  (estado, decisión) -> LISTA de (destino, condición)
#        Si hay varios destinos válidos para la misma entrada => no determinismo real.
#   q0 : "aislado_inicio"
#   F  : ESTADOS_ACEPTACION (los 4 finales)
#
# Las condiciones leen el estado del mundo (APD en mundo.py), por ejemplo el
# TOPE de la pila: así la transición depende de más memoria que el estado actual.

import random

ESTADO_INICIAL = "aislado_inicio"
ESTADOS_ACEPTACION = {
    "final_a_victoria",
    "final_b_escape",
    "final_c_muerte",
    "final_d_autodestruccion",
}

# ---------- condiciones ----------
SIEMPRE = lambda c: True


def _tiene(objeto):
    return lambda c: objeto in c.get("inventario", [])


def _reactor_listo(c):
    # Solo se sale de la sala anidada si el TOPE de la pila es la sala y está resuelta
    return c["pila_mundo"][-1] == "sala_reactor" and c["sistemas_reparados"]["motores"] == 100


def _sos_posible(c):
    s = c["sistemas_reparados"]
    return s["motores"] == 100 and s["comunicaciones"] == 100 and c["alien_derrotado"]


# ---------- función de transición δ ----------
TRANSICIONES = {
    ("aislado_inicio", "explorar_pasillo"): [("pasillo_principal", SIEMPRE)],

    # Movimiento desde el pasillo (requieren tarjeta)
    ("pasillo_principal", "ir_ingenieria"): [("ingenieria", _tiene("tarjeta_acceso"))],
    ("pasillo_principal", "ir_soporte_vital"): [("soporte_vital", _tiene("tarjeta_acceso"))],
    ("pasillo_principal", "ir_comunicaciones"): [("comunicaciones", _tiene("tarjeta_acceso"))],
    ("pasillo_principal", "ir_hangar"): [("hangar", _tiene("tarjeta_acceso"))],
    ("pasillo_principal", "ir_laboratorio"): [("laboratorio_c", _tiene("tarjeta_acceso"))],

    # NO DETERMINISMO: los ductos no piden tarjeta pero no controlas dónde sales
    ("pasillo_principal", "entrar_ductos"): [
        ("ingenieria", SIEMPRE),
        ("soporte_vital", SIEMPRE),
        ("laboratorio_c", SIEMPRE),
    ],

    # Sala anidada (apila una sala dentro de otra)
    ("ingenieria", "entrar_sala_reactor"): [("sala_reactor", _tiene("soplete_plasma"))],
    ("sala_reactor", "salir_sala"): [("ingenieria", _reactor_listo)],

    # Retornos (pop)
    ("ingenieria", "volver_pasillo"): [("pasillo_principal", SIEMPRE)],
    ("soporte_vital", "volver_pasillo"): [("pasillo_principal", SIEMPRE)],
    ("comunicaciones", "volver_pasillo"): [("pasillo_principal", SIEMPRE)],
    ("hangar", "volver_pasillo"): [("pasillo_principal", SIEMPRE)],
    ("laboratorio_c", "volver_pasillo"): [("pasillo_principal", SIEMPRE)],

    # Transiciones a estados de aceptación
    ("hangar", "escapar_capsula"): [
        ("final_b_escape", lambda c: c["sistemas_reparados"]["hangar_minimo"])],
    ("comunicaciones", "enviar_sos_final"): [("final_a_victoria", _sos_posible)],
    ("laboratorio_c", "activar_autodestruccion"): [
        ("final_d_autodestruccion", _tiene("llave_maestra"))],
}


def acciones_narrativas(estado):
    """Decisiones que existen en δ para este estado (así menú == diagrama)."""
    return [d for (e, d) in TRANSICIONES if e == estado]


def delta(estado, decision, condiciones):
    """Conjunto de destinos posibles (puede tener más de uno => AFN)."""
    candidatos = TRANSICIONES.get((estado, decision), [])
    return [destino for destino, cond in candidatos if cond(condiciones)]


def verificar_vida(estado, condiciones):
    """Transición de máxima prioridad hacia el Final C."""
    return "final_c_muerte" if condiciones.get("vida", 100) <= 0 else estado


def procesar_transicion(estado_actual, decision, condiciones):
    """Devuelve el nuevo estado (elegido al azar entre los válidos) o TRANSICION_RECHAZADA."""
    if verificar_vida(estado_actual, condiciones) == "final_c_muerte":
        return "final_c_muerte"
    destinos = delta(estado_actual, decision, condiciones)
    if not destinos:
        return "TRANSICION_RECHAZADA"
    return random.choice(destinos)


def es_estado_final(estado):
    return estado in ESTADOS_ACEPTACION