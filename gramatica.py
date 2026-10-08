# gramatica.py
# Integrante 3: José — Diseñador de gramática (GLC)
# Generación de diálogos de NPC, alertas y misiones mediante una GLC (BNF).
# Convención: los no terminales van entre <>; todo lo demás es terminal.
# La PRIMERA producción de cada regla recursiva debe ser la no recursiva
# (se usa para cortar la recursión al llegar a MAX_PROF).
#
# Instrucción asociada:
# - Diseñar una gramática libre de contexto en notación BNF.
# - Generar misiones de reparación, oxígeno y comunicaciones.
# - Producir mensajes y diálogos de la nave y personajes.
# - Implementar un generador funcional con ejemplos de derivación válidos.
#
# Archivo principal del entregable: gramatica.py

import random
import re

BNF = r"""
<ERROR_TRANSICION> ::= "[Astraea]:" <SUJETO> <VERBO> <PROBLEMA>
<ALERTA_ALIEN>     ::= "[ALERTA ROJA]:" <SUJETO> <VERBO> <EVENTO>
<SUJETO>   ::= "El sistema central" | "La IA Astraea" | "El monitor de bioseguridad"
<VERBO>    ::= "informa que" | "advierte que" | "detecta que"
<PROBLEMA> ::= "faltan credenciales de acceso" "." | "las puertas están bloqueadas" "."
             | "el protocolo de seguridad lo impide" "."
<EVENTO>   ::= "movimiento en los ductos del techo" "." | "una anomalía térmica acercándose" "."
             | "una brecha de contención cercana" "."

<DIALOGO_ASTRAEA> ::= "[Astraea]:" <SALUDO_IA> <CONSEJOS> "."
<DIALOGO_VOSS>    ::= "[Dra. Voss (holograma)]:" <SALUDO_VOSS> <CONSEJOS> "."
<DIALOGO_UNIDAD7> ::= "[Unidad-7]:" "BIP." <CONSEJOS> "."
<SALUDO_IA>   ::= "Tripulante, sigo operativa." | "Detecto signos vitales débiles." | "Bienvenido de vuelta."
<SALUDO_VOSS> ::= "Si me escuchas, aún queda esperanza." | "Escucha, no tengo mucho tiempo."
<CONSEJOS> ::= <CONSEJO> | <CONSEJO> "y además" <CONSEJOS>          (* recursiva *)
<CONSEJO>  ::= "busca una tarjeta de acceso en el pasillo" | "el soplete de ingeniería repara casi todo"
             | "no entres al laboratorio sin armarte" | "los ductos son un atajo impredecible"
             | "la sala del reactor es la única forma de reactivar los motores"

<MISION>  ::= "recoge" <OBJETO> "para" <NPC>
            | "repara" <SISTEMA> "para" <NPC>
            | "derrota a" <ENEMIGO> "en" <LUGAR>
<OBJETO>  ::= "la tarjeta de acceso" | "el soplete de plasma" | "el botiquín" | "la llave maestra"
<SISTEMA> ::= "los motores" | "la antena de comunicaciones"
<ENEMIGO> ::= "el X-99"
<LUGAR>   ::= "el laboratorio C"
<NPC>     ::= "la Dra. Voss" | "Astraea" | "la Unidad-7"
"""

MAX_PROF = 3

GLC = {
    "<ERROR_TRANSICION>": [["[Astraea]:", "<SUJETO>", "<VERBO>", "<PROBLEMA>"]],
    "<ALERTA_ALIEN>": [["[ALERTA ROJA]:", "<SUJETO>", "<VERBO>", "<EVENTO>"]],
    "<SUJETO>": [["El sistema central"], ["La IA Astraea"], ["El monitor de bioseguridad"]],
    "<VERBO>": [["informa que"], ["advierte que"], ["detecta que"]],
    "<PROBLEMA>": [["faltan credenciales de acceso", "."], ["las puertas están bloqueadas", "."],
                   ["el protocolo de seguridad lo impide", "."]],
    "<EVENTO>": [["movimiento en los ductos del techo", "."], ["una anomalía térmica acercándose", "."],
                 ["una brecha de contención cercana", "."]],
    "<DIALOGO_ASTRAEA>": [["[Astraea]:", "<SALUDO_IA>", "<CONSEJOS>", "."]],
    "<DIALOGO_VOSS>": [["[Dra. Voss (holograma)]:", "<SALUDO_VOSS>", "<CONSEJOS>", "."]],
    "<DIALOGO_UNIDAD7>": [["[Unidad-7]:", "BIP.", "<CONSEJOS>", "."]],
    "<SALUDO_IA>": [["Tripulante, sigo operativa."], ["Detecto signos vitales débiles."], ["Bienvenido de vuelta."]],
    "<SALUDO_VOSS>": [["Si me escuchas, aún queda esperanza."], ["Escucha, no tengo mucho tiempo."]],
    "<CONSEJOS>": [["<CONSEJO>"], ["<CONSEJO>", "y además", "<CONSEJOS>"]],
    "<CONSEJO>": [["busca una tarjeta de acceso en el pasillo"], ["el soplete de ingeniería repara casi todo"],
                  ["no entres al laboratorio sin armarte"], ["los ductos son un atajo impredecible"],
                  ["la sala del reactor es la única forma de reactivar los motores"]],
    "<MISION>": [["recoge", "<OBJETO>", "para", "<NPC>"],
                 ["repara", "<SISTEMA>", "para", "<NPC>"],
                 ["derrota a", "<ENEMIGO>", "en", "<LUGAR>"]],
    "<OBJETO>": [["la tarjeta de acceso"], ["el soplete de plasma"], ["el botiquín"], ["la llave maestra"]],
    "<SISTEMA>": [["los motores"], ["la antena de comunicaciones"]],
    "<ENEMIGO>": [["el X-99"]],
    "<LUGAR>": [["el laboratorio C"]],
    "<NPC>": [["la Dra. Voss"], ["Astraea"], ["la Unidad-7"]],
}

NPC_POR_ESCENA = {
    "pasillo_principal": "<DIALOGO_ASTRAEA>",
    "soporte_vital": "<DIALOGO_VOSS>",
    "laboratorio_c": "<DIALOGO_UNIDAD7>",
}

# Cómo comprobar si una misión generada por la GLC ya se cumplió
VERIFICADORES = {
    "la tarjeta de acceso": lambda c: "tarjeta_acceso" in c["inventario"],
    "el soplete de plasma": lambda c: "soplete_plasma" in c["inventario"],
    "el botiquín": lambda c: "botiquin" in c["inventario"],
    "la llave maestra": lambda c: "llave_maestra" in c["inventario"],
    "los motores": lambda c: c["sistemas_reparados"]["motores"] == 100,
    "la antena de comunicaciones": lambda c: c["sistemas_reparados"]["comunicaciones"] == 100,
    "el X-99": lambda c: c["alien_derrotado"],
}


def _expandir(simbolo, prof, derivacion):
    if simbolo not in GLC:                      # terminal
        return [simbolo]
    producciones = GLC[simbolo]
    prod = producciones[0] if prof >= MAX_PROF else random.choice(producciones)
    if derivacion is not None:
        derivacion.append(f"{simbolo} → {' '.join(prod)}")
    salida = []
    for s in prod:
        salida += _expandir(s, prof + 1, derivacion)
    return salida


def generar(simbolo, derivacion=None):
    """Deriva una cadena del símbolo inicial dado. Si se pasa una lista, guarda la derivación."""
    texto = " ".join(_expandir(simbolo, 0, derivacion))
    texto = re.sub(r"\s+([.,:;!?])", r"\1", texto)
    return re.sub(r"([.:]\s+)([a-záéíóú])", lambda m: m.group(1) + m.group(2).upper(), texto)


def generar_mensaje_ia(contexto):
    simbolo = {"error_transicion": "<ERROR_TRANSICION>", "alerta_alien": "<ALERTA_ALIEN>"}.get(contexto)
    return generar(simbolo) if simbolo else "[Astraea]: Sistemas operando al mínimo."


# ---------- misiones secundarias ----------
def mision_cumplida(mision, c):
    return all(v(c) for k, v in VERIFICADORES.items() if k in mision)


def hablar(c, estado):
    """Diálogo + misión secundaria generada por la GLC. Devuelve el texto a mostrar."""
    simbolo = NPC_POR_ESCENA.get(estado)
    if not simbolo:
        return "Aquí no hay nadie con quien hablar."
    texto = generar(simbolo)
    m = c.get("mision")
    if m and mision_cumplida(m, c):
        c["vida"] = min(100, c["vida"] + 25)
        c["misiones_completadas"] += 1
        c["mision"] = None
        return f"{texto}\n  ✔ Misión cumplida ({m}). Recompensa: +25 HP (HP: {c['vida']})."
    if m:
        return f"{texto}\n  ► Misión activa: {m}."
    for _ in range(20):                          # evita misiones ya cumplidas
        nueva = generar("<MISION>")
        if not mision_cumplida(nueva, c):
            c["mision"] = nueva
            return f"{texto}\n  ► Nueva misión: {nueva}."
    return texto


if __name__ == "__main__":
    print(BNF)
    for s in ("<MISION>", "<DIALOGO_ASTRAEA>", "<ERROR_TRANSICION>"):
        d = []
        print(f"\nCadena: {generar(s, d)}")
        print("Derivación:\n  " + "\n  ".join(d))