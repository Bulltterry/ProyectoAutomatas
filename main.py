def mostrar_menu():
    print("\n================================")
    print("          FUGA ESPACIAL")
    print("================================")
    print("1. Iniciar")
    print("2. Integrantes")
    print("3. Créditos")
    print("4. Salir")


def iniciar_partida():
    print("\n--- INICIAR PARTIDA ---")
    print("El juego todavía está en desarrollo.")
    input("\nPresiona Enter para volver al menú...")


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
    print("Inventario y mundo: Marlyn")
    print("Gramática y misiones: Josue")
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