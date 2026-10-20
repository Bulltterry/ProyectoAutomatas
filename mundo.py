"""
Subsistema de mundo = Autómata de Pila (APD).

La pila representa la anidación de zonas de la nave:
- PUSH al entrar/explorar una zona.
- POP al volver/salir de una zona.
- Z0 es el símbolo inicial.

Además mantiene inventario, sistemas reparados y el estado de las puertas.
"""

PREFIJOS_PUSH = (
    "ir_",
    "entrar_",
    "explorar_",
)

PREFIJOS_POP = (
    "volver",
    "salir_",
)

PUERTAS_INTERIORES = {
    "laboratorio_c",
    "comunicaciones",
    "hangar",
}

ACCIONES_MUNDO = {
    "buscar_objetos",
    "reparar_sistemas",
    "usar_botiquin",
    "hablar_npc",
    "desbloquear_puerta",
}

ACCIONES_BASE = {
    "pasillo_principal": [
        "buscar_objetos",
        "hablar_npc",
    ],
    "ingenieria": [
        "buscar_objetos",
    ],
    "sala_reactor": [
        "reparar_sistemas",
    ],
    "soporte_vital": [
        "buscar_objetos",
        "reparar_sistemas",
        "hablar_npc",
    ],
    "comunicaciones": [
        "reparar_sistemas",
    ],
    "hangar": [
        "buscar_objetos",
        "reparar_sistemas",
    ],
    "laboratorio_c": [
        "buscar_objetos",
        "hablar_npc",
    ],
}

OBJETOS_POR_SALA = {
    "pasillo_principal": [
        (
            "tarjeta_acceso",
            "¡Encontraste una Tarjeta de Acceso en el suelo del pasillo!",
        ),
    ],
    "ingenieria": [
        (
            "soplete_plasma",
            "Recogiste un Soplete de Plasma de la caja de herramientas.",
        ),
    ],
    "soporte_vital": [
        (
            "botiquin",
            "Encontraste un Botiquín médico en un casillero.",
        ),
        (
            "extintor",
            "Encontraste un Extintor presurizado. Puede servir como arma improvisada.",
        ),
    ],
    "hangar": [
        (
            "tubo_metalico",
            "Recogiste un Tubo Metálico pesado del área de mantenimiento.",
        ),
    ],
    "laboratorio_c": [
        (
            "llave_maestra",
            "Tomaste la Llave Maestra del cadáver de un científico.",
        ),
        (
            "bateria_energia",
            "Encontraste una Batería de Energía todavía cargada.",
        ),
    ],
}


def nuevo_mundo():
    return {
        "vida": 100,
        "inventario": [],
        "pila_mundo": ["Z0"],
        "sistemas_reparados": {
            "motores": 0,
            "comunicaciones": 0,
            "oxigeno": 0,
            "hangar_minimo": False,
        },
        "puertas_desbloqueadas": {
            "laboratorio_c": False,
            "comunicaciones": False,
            "hangar": False,
        },
        "alien_derrotado": False,
        "alien_hp": 65,
        "alien_estado": "normal",
        "mision": None,
        "misiones_completadas": 0,
    }


def tope(c):
    return c["pila_mundo"][-1]


def actualizar_pila(c, decision, nuevo_estado):
    if decision.startswith(PREFIJOS_PUSH):
        c["pila_mundo"].append(nuevo_estado)

    elif decision.startswith(PREFIJOS_POP) and len(c["pila_mundo"]) > 1:
        c["pila_mundo"].pop()


def puerta_desbloqueada(c, estado):
    return c.get("puertas_desbloqueadas", {}).get(estado, False)


def acciones_mundo(estado, c):
    acciones = list(
        ACCIONES_BASE.get(
            estado,
            [],
        )
    )

    if (
        "botiquin" in c.get("inventario", [])
        and estado in ACCIONES_BASE
    ):
        acciones.append("usar_botiquin")

    if (
        estado in PUERTAS_INTERIORES
        and not puerta_desbloqueada(c, estado)
    ):
        acciones.append("desbloquear_puerta")

    return acciones


def buscar_objeto(estado_actual, c):
    objetos = OBJETOS_POR_SALA.get(
        estado_actual,
        [],
    )

    for objeto, texto in objetos:
        if objeto not in c["inventario"]:
            c["inventario"].append(objeto)
            return texto

    return "Exploraste el área, pero no encontraste nada útil."


def procesar_accion_mundo(accion, estado_actual, c):
    if accion == "buscar_objetos":
        return buscar_objeto(
            estado_actual,
            c,
        )

    if accion == "usar_botiquin":
        if "botiquin" in c["inventario"]:
            c["inventario"].remove("botiquin")
            c["vida"] = min(
                100,
                c["vida"] + 40,
            )
            return f"Usas el botiquín. HP: {c['vida']}."

        return "No tienes botiquín."

    if accion == "desbloquear_puerta":
        if estado_actual not in PUERTAS_INTERIORES:
            return "Esta zona no tiene una puerta bloqueada de ese tipo."

        if puerta_desbloqueada(c, estado_actual):
            return "La puerta ya estaba desbloqueada."

        c["puertas_desbloqueadas"][estado_actual] = True

        return (
            "Desbloqueaste la puerta desde el interior. "
            "Ahora podrás entrar normalmente desde el pasillo."
        )

    if accion == "reparar_sistemas":
        if estado_actual == "sala_reactor":
            if "soplete_plasma" in c["inventario"]:
                c["sistemas_reparados"]["motores"] = 100
                return (
                    "Has reparado los motores principales al 100%. "
                    "Ya puedes salir de la sala del reactor."
                )

            return "Necesitas un Soplete de Plasma para reparar los motores."

        if estado_actual == "soporte_vital":
            c["sistemas_reparados"]["oxigeno"] = 100
            return "Sistema de oxígeno restaurado al 100%. Soporte vital estable."

        if estado_actual == "comunicaciones":
            c["sistemas_reparados"]["comunicaciones"] = 100
            return "Sistemas de comunicación restaurados. Antena en línea."

        if estado_actual == "hangar":
            c["sistemas_reparados"]["hangar_minimo"] = True
            return "Has preparado la cápsula de escape de emergencia."

        return "No hay sistemas que puedas reparar aquí."

    if accion == "hablar_npc":
        return "La conversación se procesa mediante la GLC."

    return "Acción de mundo no reconocida."
