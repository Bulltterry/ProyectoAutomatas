import os
import pygame


pygame.init()

print("Pygame iniciado")


try:
    pygame.mixer.init()

    print(
        "Mixer iniciado correctamente:"
    )

    print(
        pygame.mixer.get_init()
    )

except Exception as error:

    print(
        "ERROR AL INICIAR EL MIXER:"
    )

    print(
        error
    )

    input(
        "Presiona ENTER..."
    )

    raise SystemExit


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


RUTA_SONIDOS = os.path.join(
    BASE_DIR,
    "assets",
    "sonidos"
)


print(
    "\nCarpeta de sonidos:"
)

print(
    RUTA_SONIDOS
)


print(
    "\n¿Existe la carpeta?"
)

print(
    os.path.exists(
        RUTA_SONIDOS
    )
)


archivo = os.path.join(
    RUTA_SONIDOS,
    "menu.ogg"
)


print(
    "\nArchivo a probar:"
)

print(
    archivo
)


print(
    "\n¿Existe menu.ogg?"
)

print(
    os.path.exists(
        archivo
    )
)


try:

    pygame.mixer.music.load(
        archivo
    )

    pygame.mixer.music.set_volume(
        1.0
    )

    pygame.mixer.music.play()

    print(
        "\nREPRODUCIENDO menu.ogg..."
    )

    print(
        "Deberías escuchar música durante 8 segundos."
    )


    pygame.time.wait(
        8000
    )


except Exception as error:

    print(
        "\nERROR AL REPRODUCIR:"
    )

    print(
        error
    )


pygame.mixer.music.stop()

pygame.quit()


input(
    "\nPrueba terminada. Presiona ENTER..."
)