import juego


TITULO = "PROTOCOLO OMEGA: FUGA ESPACIAL"


def mostrar_menu():
    print("\n" + "=" * 42)
    print(f"{TITULO:^42}")
    print("=" * 42)
    print("1. Iniciar")
    print("2. Integrantes")
    print("3. Créditos")
    print("4. Salir")


def iniciar_partida():
    juego.main()


def mostrar_integrantes():
    print("\n--- INTEGRANTES ---")
    print("Daniel")
    print("Marlyn")
    print("Josue")
    print("Danna")
    print("Dylan")
    input("\nPresiona Enter para volver al menú...")


def mostrar_creditos():
    print("\n--- CRÉDITOS ---")
    print("Proyecto de Autómatas y Lenguajes Formales.")
    print("Desarrollado en Python.")
    print()
    print("Narrativa y AFN: Daniel")
    print("Inventario y mundo (APD): Marlyn")
    print("Gramática y misiones (GLC): Josue")
    print("Historia y combate: Danna")
    print("Integración, documentación y pruebas: Dylan")
    input("\nPresiona Enter para volver al menú...")


def main():
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            iniciar_partida()

        elif opcion == "2":
            mostrar_integrantes()

        elif opcion == "3":
            mostrar_creditos()

        elif opcion == "4":
            print("\nGracias por jugar. ¡Hasta pronto!")
            break

        else:
            print("\nOpción inválida. Escribe un número del 1 al 4.")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()