import os
import math
import random
import wave
import struct


# =========================================================
# CONFIGURACION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CARPETA = os.path.join(
    BASE_DIR,
    "assets",
    "sonidos"
)

FRECUENCIA = 44100
VOLUMEN = 0.35

os.makedirs(
    CARPETA,
    exist_ok=True
)


# =========================================================
# GUARDAR WAV
# =========================================================

def guardar_wav(
    nombre,
    muestras
):

    ruta = os.path.join(
        CARPETA,
        nombre
    )

    with wave.open(
        ruta,
        "w"
    ) as archivo:

        archivo.setnchannels(
            2
        )

        archivo.setsampwidth(
            2
        )

        archivo.setframerate(
            FRECUENCIA
        )

        for muestra in muestras:

            muestra = max(
                -1.0,
                min(
                    1.0,
                    muestra
                )
            )

            valor = int(
                muestra
                *
                32767
            )

            datos = struct.pack(
                "<hh",
                valor,
                valor
            )

            archivo.writeframesraw(
                datos
            )

    print(
        "Creado:",
        ruta
    )


# =========================================================
# TONO
# =========================================================

def tono(
    frecuencia,
    duracion,
    volumen=VOLUMEN,
    vibrato=0
):

    total = int(
        FRECUENCIA
        *
        duracion
    )

    muestras = []

    for i in range(
        total
    ):

        t = (
            i
            /
            FRECUENCIA
        )

        frecuencia_actual = (
            frecuencia
            +
            math.sin(
                2
                *
                math.pi
                *
                5
                *
                t
            )
            *
            vibrato
        )

        valor = (
            math.sin(
                2
                *
                math.pi
                *
                frecuencia_actual
                *
                t
            )
            *
            volumen
        )

        muestras.append(
            valor
        )

    return muestras


# =========================================================
# SILENCIO
# =========================================================

def silencio(
    duracion
):

    return [
        0.0
        for _
        in range(
            int(
                FRECUENCIA
                *
                duracion
            )
        )
    ]


# =========================================================
# RUIDO
# =========================================================

def ruido(
    duracion,
    volumen=0.2
):

    return [

        random.uniform(
            -volumen,
            volumen
        )

        for _
        in range(
            int(
                FRECUENCIA
                *
                duracion
            )
        )
    ]


# =========================================================
# FUNDIDO
# =========================================================

def fundido(
    muestras
):

    total = len(
        muestras
    )

    resultado = []

    for i, valor in enumerate(
        muestras
    ):

        posicion = (
            i
            /
            total
        )

        if posicion < 0.1:

            factor = (
                posicion
                /
                0.1
            )

        elif posicion > 0.9:

            factor = (
                1
                -
                posicion
            ) / 0.1

        else:

            factor = 1

        resultado.append(
            valor
            *
            factor
        )

    return resultado


# =========================================================
# MEZCLAR
# =========================================================

def mezclar(
    *pistas
):

    longitud = max(
        len(
            pista
        )
        for pista
        in pistas
    )

    resultado = []

    for i in range(
        longitud
    ):

        valor = 0

        for pista in pistas:

            if i < len(
                pista
            ):

                valor += pista[
                    i
                ]

        valor /= len(
            pistas
        )

        resultado.append(
            valor
        )

    return resultado


# =========================================================
# EFECTO: RECOGER
# =========================================================

recoger = (
    tono(
        700,
        0.08,
        0.4
    )
    +
    tono(
        950,
        0.10,
        0.4
    )
    +
    tono(
        1250,
        0.12,
        0.35
    )
)

guardar_wav(
    "recoger.wav",
    recoger
)


# =========================================================
# EFECTO: PUERTA
# =========================================================

puerta = mezclar(

    fundido(
        tono(
            120,
            0.55,
            0.45
        )
    ),

    fundido(
        ruido(
            0.55,
            0.20
        )
    )
)

guardar_wav(
    "puerta.wav",
    puerta
)


# =========================================================
# EFECTO: TERMINAL
# =========================================================

terminal = (
    tono(
        880,
        0.08,
        0.35
    )
    +
    silencio(
        0.04
    )
    +
    tono(
        1100,
        0.08,
        0.35
    )
)

guardar_wav(
    "terminal.wav",
    terminal
)


# =========================================================
# EFECTO: GOLPE
# =========================================================

golpe = mezclar(

    fundido(
        tono(
            90,
            0.25,
            0.6
        )
    ),

    fundido(
        ruido(
            0.25,
            0.50
        )
    )
)

guardar_wav(
    "golpe.wav",
    golpe
)


# =========================================================
# EFECTO: ALIEN
# =========================================================

alien = mezclar(

    fundido(
        tono(
            65,
            0.8,
            0.50,
            8
        )
    ),

    fundido(
        ruido(
            0.8,
            0.25
        )
    )
)

guardar_wav(
    "alien.wav",
    alien
)


# =========================================================
# EFECTO: ALARMA
# =========================================================

alarma = []

for _ in range(
    4
):

    alarma += tono(
        850,
        0.25,
        0.4
    )

    alarma += silencio(
        0.12
    )

    alarma += tono(
        650,
        0.25,
        0.4
    )

    alarma += silencio(
        0.12
    )

guardar_wav(
    "alarma.wav",
    alarma
)


# =========================================================
# EFECTO: REACTOR
# =========================================================

reactor = mezclar(

    fundido(
        tono(
            100,
            1.4,
            0.40,
            3
        )
    ),

    fundido(
        tono(
            200,
            1.4,
            0.15
        )
    )
)

guardar_wav(
    "reactor.wav",
    reactor
)


# =========================================================
# EFECTO: VICTORIA
# =========================================================

victoria = (

    tono(
        523,
        0.22,
        0.35
    )

    +

    tono(
        659,
        0.22,
        0.35
    )

    +

    tono(
        784,
        0.22,
        0.35
    )

    +

    tono(
        1046,
        0.60,
        0.40
    )
)

guardar_wav(
    "victoria.wav",
    victoria
)


# =========================================================
# MUSICA MENU
# =========================================================

menu = []

notas_menu = [

    220,
    277,
    330,
    277,

    220,
    330,
    415,
    330,
]

for _ in range(
    4
):

    for nota in notas_menu:

        menu += fundido(
            tono(
                nota,
                0.35,
                0.18
            )
        )

guardar_wav(
    "menu.wav",
    menu
)


# =========================================================
# MUSICA NAVE
# =========================================================

nave_base = []

for _ in range(
    12
):

    nave_base += fundido(
        tono(
            110,
            0.45,
            0.15,
            2
        )
    )

    nave_base += fundido(
        tono(
            165,
            0.45,
            0.10
        )
    )

guardar_wav(
    "nave.wav",
    nave_base
)


# =========================================================
# MUSICA COMBATE
# =========================================================

combate_musica = []

notas_combate = [

    110,
    110,
    147,
    110,

    165,
    147,
    110,
    98,
]

for _ in range(
    6
):

    for nota in notas_combate:

        parte = mezclar(

            tono(
                nota,
                0.20,
                0.30
            ),

            ruido(
                0.20,
                0.08
            )
        )

        combate_musica += parte

guardar_wav(
    "combate.wav",
    combate_musica
)


print()
print(
    "=" * 50
)

print(
    "TODOS LOS SONIDOS FUERON GENERADOS"
)

print(
    "=" * 50
)