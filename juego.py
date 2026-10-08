# main.py
# Coordinador principal - Protocolo Omega: Fuga Espacial
# Uso:  python main.py [semilla]

import random
import sys

import combate
import gramatica
import mundo
import narrativa

FINALES = {
    "final_a_victoria": "FINAL A: REPARASTE LA NAVE, ELIMINASTE AL X-99 Y PEDISTE AYUDA. ¡SOBREVIVISTE!",
    "final_b_escape": "FINAL B: LOGRASTE ESCAPAR EN LA CÁPSULA. LA NAVE QUEDA A LA DERIVA.",
    "final_c_muerte": "FINAL C: LA ENTIDAD X-99 TE HA ANIQUILADO. ESTÁS MUERTO.",
    "final_d_autodestruccion": "FINAL D: ACTIVASTE LA AUTODESTRUCCIÓN. LA NAVE Y EL X-99 ESTALLAN CONTIGO DENTRO.",
}


def imprimir_estado_juego(estado, c):
    print("\n" + "=" * 60)
    print(f"UBICACIÓN: {estado.upper().replace('_', ' ')}")
    print(f"HP: {c['vida']} | INVENTARIO: {c['inventario']}")
    print(f"PILA: {' > '.join(c['pila_mundo'])}")
    if c["mision"]:
        print(f"MISIÓN: {c['mision']}")
    print("=" * 60)


def main():
    if len(sys.argv) > 1:
        random.seed(int(sys.argv[1]))
    print("Iniciando PROTOCOLO OMEGA: FUGA ESPACIAL...")

    c = mundo.nuevo_mundo()
    estado = narrativa.ESTADO_INICIAL

    while True:
        if narrativa.es_estado_final(estado):
            print("\n" + "*" * 60 + f"\n{FINALES[estado]}\n" + "*" * 60 + "\nJuego Terminado.")
            return

        imprimir_estado_juego(estado, c)
        # El menú sale de las tablas: mundo (APD) + narrativa (AFN)
        opciones = mundo.acciones_mundo(estado, c) + narrativa.acciones_narrativas(estado)
        print("\n¿Qué deseas hacer?")
        for i, opt in enumerate(opciones, 1):
            print(f" {i}. {opt.replace('_', ' ').capitalize()}")

        try:
            decision = opciones[int(input("\nElige una opción (número): ")) - 1]
        except (ValueError, IndexError):
            print("\nEntrada inválida. Intenta de nuevo.")
            continue
        except EOFError:
            return

        if decision == "hablar_npc":                         # GLC
            print("\n" + gramatica.hablar(c, estado))
        elif decision in mundo.ACCIONES_MUNDO:               # APD / inventario
            print(f"\n> {mundo.procesar_accion_mundo(decision, estado, c)}")
        else:                                                # AFN
            nuevo = narrativa.procesar_transicion(estado, decision, c)
            if nuevo == "TRANSICION_RECHAZADA":
                print("\n" + gramatica.generar_mensaje_ia("error_transicion"))
                continue
            mundo.actualizar_pila(c, decision, nuevo)
            estado = nuevo
            if not narrativa.es_estado_final(estado) and combate.debe_iniciar(c, estado):
                print("\n" + gramatica.generar_mensaje_ia("alerta_alien"))
                combate.ejecutar_combate(c)
                estado = narrativa.verificar_vida(estado, c)  # ¿murió en combate?


if __name__ == "__main__":
    main()