# mundo.py
# Subsistema de mundo = AUTÓMATA DE PILA  M = (Q, Σ, Γ, δ, q0, Z0, F)
#   Γ  : {Z0} ∪ salas de la nave
#   Z0 : símbolo inicial de la pila
#   push al entrar a una sala ("ir_*", "entrar_*", "explorar_*")
#   pop  al salir ("volver_*", "salir_*"), solo si lo autoriza la AFN
#        (p. ej. salir de sala_reactor exige que ese TOPE esté resuelto).
# Se usa pila (y no Máquina de Turing) porque la memoria que crece es la
# anidación de salas (LIFO): solo se toca el tope. Los objetos son un conjunto
# finito (4) cuyo estado cabe en el control finito. Ver DOCUMENTACION.md.

PREFIJOS_PUSH = ("ir_", "entrar_", "explorar_")
PREFIJOS_POP = ("volver_", "salir_")

ACCIONES_MUNDO = {"buscar_objetos", "reparar_sistemas", "usar_botiquin", "hablar_npc"}

ACCIONES_BASE = {
    "pasillo_principal": ["buscar_objetos", "hablar_npc"],
    "ingenieria": ["buscar_objetos"],
    "sala_reactor": ["reparar_sistemas"],
    "soporte_vital": ["buscar_objetos", "hablar_npc"],
    "comunicaciones": ["reparar_sistemas"],
    "hangar": ["reparar_sistemas"],
    "laboratorio_c": ["buscar_objetos", "hablar_npc"],
}

OBJETOS_POR_SALA = {
    "pasillo_principal": ("tarjeta_acceso", "¡Encontraste una Tarjeta de Acceso en el suelo del pasillo!"),
    "ingenieria": ("soplete_plasma", "Recogiste un Soplete de Plasma de la caja de herramientas."),
    "soporte_vital": ("botiquin", "Encontraste un Botiquín médico en un casillero."),
    "laboratorio_c": ("llave_maestra", "Tomaste la Llave Maestra del cadáver de un científico."),
}


def nuevo_mundo():
    return {
        "vida": 100,
        "inventario": [],
        "pila_mundo": ["Z0"],
        "sistemas_reparados": {"motores": 0, "comunicaciones": 0, "hangar_minimo": False},
        "alien_derrotado": False,
        "alien_hp": 60,
        "mision": None,
        "misiones_completadas": 0,
    }


# ---------- operaciones de pila ----------
def tope(c):
    return c["pila_mundo"][-1]


def actualizar_pila(c, decision, nuevo_estado):
    """Aplica push/pop según el tipo de decisión ya aprobada por el AFN."""
    if decision.startswith(PREFIJOS_PUSH):
        c["pila_mundo"].append(nuevo_estado)
    elif decision.startswith(PREFIJOS_POP) and len(c["pila_mundo"]) > 1:
        c["pila_mundo"].pop()


def acciones_mundo(estado, c):
    acc = list(ACCIONES_BASE.get(estado, []))
    if "botiquin" in c["inventario"] and estado in ACCIONES_BASE:
        acc.append("usar_botiquin")
    return acc


def procesar_accion_mundo(accion, estado_actual, c):
    if accion == "buscar_objetos":
        objeto, texto = OBJETOS_POR_SALA.get(estado_actual, (None, None))
        if objeto and objeto not in c["inventario"]:
            c["inventario"].append(objeto)
            return texto
        return "Exploraste el área, pero no encontraste nada útil."

    if accion == "usar_botiquin":
        if "botiquin" in c["inventario"]:
            c["inventario"].remove("botiquin")
            c["vida"] = min(100, c["vida"] + 40)
            return f"Usas el botiquín. HP: {c['vida']}."
        return "No tienes botiquín."

    if accion == "reparar_sistemas":
        if estado_actual == "sala_reactor":
            if "soplete_plasma" in c["inventario"]:
                c["sistemas_reparados"]["motores"] = 100
                return "Has reparado los motores principales al 100%. Ya puedes salir de la sala."
            return "Necesitas un Soplete de Plasma para reparar los motores."
        if estado_actual == "comunicaciones":
            c["sistemas_reparados"]["comunicaciones"] = 100
            return "Sistemas de comunicación restaurados. Antena en línea."
        if estado_actual == "hangar":
            c["sistemas_reparados"]["hangar_minimo"] = True
            return "Has preparado la cápsula de escape de emergencia."
        return "No hay sistemas que puedas reparar aquí."

    return "Acción de mundo no reconocida."