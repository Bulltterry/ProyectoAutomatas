# combate.py
# Autómata de combate INDEPENDIENTE con transiciones probabilísticas.
#
# Estados: INICIO -> TURNO_JUGADOR -> (EVALUAR_X99) -> TURNO_X99 -> EVALUAR_JUGADOR -> TURNO_JUGADOR ...
# Finales: FIN_VICTORIA, FIN_HUIDA, FIN_DERROTA
#
# Probabilidades (evento -> p):
#   Disparar : impacto 0.75 ; si impacta, crítico 0.20 (daño x2). Soplete: +10 de daño
#   Esquivar : éxito 0.50 (anula el siguiente ataque del X-99)
#   Huir     : éxito 0.30 (termina el combate sin derrotar al X-99)
#   X-99     : impacto 0.70, daño 15-30

import random

PROB_IMPACTO = 0.75
PROB_CRITICO = 0.20
PROB_ESQUIVE = 0.50
PROB_HUIDA = 0.30
PROB_IMPACTO_X99 = 0.70
PROB_EMBOSCADA = 0.20

FINALES_COMBATE = {"FIN_VICTORIA", "FIN_HUIDA", "FIN_DERROTA"}

OPCIONES = {"1": "Disparar rifle de plasma", "2": "Esquivar", "3": "Huir hacia el conducto"}


def combate_forzado(c, estado):
    """El X-99 siempre te espera en el laboratorio C mientras viva."""
    return (not c["alien_derrotado"]) and estado == "laboratorio_c"


def combate_posible(c, estado):
    return (not c["alien_derrotado"]) and estado != "aislado_inicio"


def debe_iniciar(c, estado, rng=random):
    return combate_forzado(c, estado) or (combate_posible(c, estado) and rng.random() < PROB_EMBOSCADA)


def ejecutar_combate(c, entrada=input, rng=random):
    """Corre el autómata. Modifica vida, alien_hp y alien_derrotado. Devuelve el estado final."""
    estado = "INICIO"
    esquiva = False
    while estado not in FINALES_COMBATE:

        if estado == "INICIO":
            print("\n" + "!" * 50 + f"\n¡COMBATE CONTRA EL X-99! (HP X-99: {c['alien_hp']})\n" + "!" * 50)
            estado = "TURNO_JUGADOR"

        elif estado == "TURNO_JUGADOR":
            print(f"\nTu HP: {c['vida']} | HP X-99: {c['alien_hp']}")
            for k, t in OPCIONES.items():
                print(f" [{k}] {t}")
            eleccion = entrada("\nElige una acción: ").strip()
            esquiva = False
            if eleccion == "1":
                if rng.random() < PROB_IMPACTO:
                    dano = rng.randint(15, 25) + (10 if "soplete_plasma" in c["inventario"] else 0)
                    if rng.random() < PROB_CRITICO:
                        dano *= 2
                        print(f"\n¡CRÍTICO! Impacto directo: {dano} de daño.")
                    else:
                        print(f"\nImpactas al X-99: {dano} de daño.")
                    c["alien_hp"] -= dano
                else:
                    print("\nTu disparo falla.")
                estado = "EVALUAR_X99"
            elif eleccion == "2":
                esquiva = rng.random() < PROB_ESQUIVE
                print("\nTe preparas para esquivar..." if esquiva else "\nTe mueves, pero demasiado lento.")
                estado = "TURNO_X99"
            elif eleccion == "3":
                if rng.random() < PROB_HUIDA:
                    print("\nTe escabulles por el conducto y pierdes a la criatura.")
                    estado = "FIN_HUIDA"
                else:
                    print("\nEl conducto está bloqueado, no logras huir.")
                    estado = "TURNO_X99"
            else:
                print("\nAcción no válida en el estado de combate.")

        elif estado == "EVALUAR_X99":
            if c["alien_hp"] <= 0:
                c["alien_derrotado"] = True
                print("\nEl X-99 se desploma, derrotado. El área queda segura.")
                estado = "FIN_VICTORIA"
            else:
                estado = "TURNO_X99"

        elif estado == "TURNO_X99":
            if esquiva:
                print("\n¡Esquivas el zarpazo del X-99 justo a tiempo!")
            elif rng.random() < PROB_IMPACTO_X99:
                dano = rng.randint(15, 30)
                c["vida"] -= dano
                print(f"\nEl X-99 te desgarra con sus garras biónicas: -{dano} HP. HP restante: {c['vida']}")
            else:
                print("\nEl X-99 ataca pero falla.")
            estado = "EVALUAR_JUGADOR"

        elif estado == "EVALUAR_JUGADOR":
            estado = "FIN_DERROTA" if c["vida"] <= 0 else "TURNO_JUGADOR"

    return estado