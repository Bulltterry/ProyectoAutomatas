import random
import sys

import combate
import gramatica
import mundo
import narrativa


FINALES = {

    "final_a_victoria":

        (
            "FINAL A: SALVACIÓN TOTAL\n"
            "Reparaste motores, oxígeno "
            "y comunicaciones, eliminaste "
            "al X-99 y enviaste una señal "
            "de auxilio. ¡Sobreviviste!"
        ),


    "final_b_escape":

        (
            "FINAL B: ESCAPE EN CÁPSULA\n"
            "Preparaste la cápsula y "
            "abandonaste la Astraea. "
            "La nave queda a la deriva."
        ),


    "final_c_muerte":

        (
            "FINAL C: DERROTA\n"
            "La entidad X-99 terminó "
            "con tu vida antes de que "
            "pudieras escapar."
        ),


    "final_d_autodestruccion":

        (
            "FINAL D: SACRIFICIO\n"
            "Activaste la autodestrucción. "
            "La Astraea y el X-99 "
            "desaparecen contigo."
        ),
}


def nombre_lista(lista):

    if not lista:

        return "vacío"

    return ", ".join(

        elemento.replace(
            "_",
            " "
        )

        for elemento
        in lista
    )


def imprimir_estado_juego(
    estado,
    c
):

    sistemas = c[
        "sistemas_reparados"
    ]


    print(
        "\n"
        + "=" * 64
    )


    print(
        "UBICACIÓN: "
        + estado.upper().replace(
            "_",
            " "
        )
    )


    print(
        f"HP: "
        f"{c['vida']}"
    )


    print(
        "INVENTARIO: "
        + nombre_lista(
            c["inventario"]
        )
    )


    print(
        "PILA APD: "
        + " > ".join(
            c["pila_mundo"]
        )
    )


    print(
        "SISTEMAS:"
    )


    print(
        f"Motores: "
        f"{sistemas['motores']}%"
    )


    print(
        f"Oxígeno: "
        f"{sistemas['oxigeno']}%"
    )


    print(
        f"Comunicaciones: "
        f"{sistemas['comunicaciones']}%"
    )


    if sistemas[
        "hangar_minimo"
    ]:

        print(
            "Cápsula: LISTA"
        )

    else:

        print(
            "Cápsula: NO LISTA"
        )


    if c[
        "alien_derrotado"
    ]:

        print(
            "X-99: DERROTADO"
        )

    else:

        print(
            f"X-99: "
            f"{c['alien_hp']} HP "
            f"({c.get('alien_estado')})"
        )


    if c.get(
        "mision"
    ):

        print(
            f"MISIÓN: "
            f"{c['mision']}"
        )


    print(
        "=" * 64
    )


def leer_opcion(
    cantidad
):

    try:

        numero = int(
            input(
                "\nElige una opción "
                "(número): "
            ).strip()
        )

    except ValueError:

        return None

    except EOFError:

        raise


    if (
        numero < 1
        or
        numero > cantidad
    ):

        return None


    return numero - 1


def configurar_semilla():

    if len(
        sys.argv
    ) <= 1:

        return


    try:

        random.seed(
            int(
                sys.argv[1]
            )
        )

    except ValueError:

        print(
            "La semilla no es numérica. "
            "Se usará aleatoriedad normal."
        )


def main():

    configurar_semilla()


    print(
        "\nIniciando "
        "PROTOCOLO OMEGA: "
        "FUGA ESPACIAL..."
    )


    c = mundo.nuevo_mundo()

    estado = (
        narrativa.ESTADO_INICIAL
    )


    while True:


        estado = (
            narrativa.verificar_vida(
                estado,
                c
            )
        )


        if narrativa.es_estado_final(
            estado
        ):

            print(
                "\n"
                + "*" * 64
            )

            print(
                FINALES[
                    estado
                ]
            )

            print(
                "*" * 64
            )

            print(
                "Juego terminado."
            )

            return


        imprimir_estado_juego(
            estado,
            c
        )


        opciones = (
            mundo.acciones_mundo(
                estado,
                c
            )
            +
            narrativa.acciones_narrativas(
                estado
            )
        )


        if not opciones:

            print(
                "\nNo existen acciones "
                "disponibles."
            )

            return


        print(
            "\n¿Qué deseas hacer?"
        )


        for i, opcion in enumerate(
            opciones,
            1
        ):

            print(
                f" {i}. "
                f"{opcion.replace('_', ' ').capitalize()}"
            )


        try:

            indice = leer_opcion(
                len(opciones)
            )

        except EOFError:

            return


        if indice is None:

            print(
                "\nEntrada inválida. "
                "Elige un número mostrado "
                "en el menú."
            )

            continue


        decision = opciones[
            indice
        ]


        if decision == "hablar_npc":

            print(
                "\n"
                + gramatica.hablar(
                    c,
                    estado
                )
            )

            continue


        if (
            decision
            in mundo.ACCIONES_MUNDO
        ):

            print(
                "\n> "
                + mundo.procesar_accion_mundo(
                    decision,
                    estado,
                    c
                )
            )

            continue


        nuevo_estado = (
            narrativa.procesar_transicion(
                estado,
                decision,
                c
            )
        )


        if (
            nuevo_estado
            ==
            "TRANSICION_RECHAZADA"
        ):

            print(
                "\n"
                + gramatica.generar_mensaje_ia(
                    "error_transicion"
                )
            )

            continue


        mundo.actualizar_pila(
            c,
            decision,
            nuevo_estado
        )


        estado = nuevo_estado


        if narrativa.es_estado_final(
            estado
        ):

            continue


        if combate.debe_iniciar(
            c,
            estado
        ):

            print(
                "\n"
                + gramatica.generar_mensaje_ia(
                    "alerta_alien"
                )
            )


            try:
                resultado = (
                    combate.ejecutar_combate(
                        c,
                        estado
                    )
                )
            except EOFError:
                return


            if resultado == "FIN_HUIDA":

                print(
                    "\nLograste romper "
                    "el contacto. "
                    "Puedes continuar "
                    "explorando."
                )


            elif resultado == "FIN_VICTORIA":

                print(
                    "\nLa amenaza X-99 "
                    "ha sido neutralizada."
                )


            estado = (
                narrativa.verificar_vida(
                    estado,
                    c
                )
            )


if __name__ == "__main__":

    main()