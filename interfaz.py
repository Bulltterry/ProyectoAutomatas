import os
import sys
import pygame

import narrativa
import mundo
import gramatica
import combate


# =========================================================
# INICIALIZACION
# =========================================================

pygame.mixer.pre_init(
    44100,
    -16,
    2,
    512
)

pygame.init()

try:

    if pygame.mixer.get_init() is None:

        pygame.mixer.init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512
        )

    AUDIO_DISPONIBLE = True

    print(
        "Audio iniciado:",
        pygame.mixer.get_init()
    )

except Exception as error:

    AUDIO_DISPONIBLE = False

    print(
        "No se pudo iniciar el audio:",
        error
    )


# =========================================================
# CONFIGURACION
# =========================================================

ANCHO = 960
ALTO = 660
FPS = 60

pantalla = pygame.display.set_mode(
    (
        ANCHO,
        ALTO
    )
)

pygame.display.set_caption(
    "Protocolo Omega: Fuga Espacial"
)

reloj = pygame.time.Clock()


# =========================================================
# COLORES
# =========================================================

NEGRO = (
    8,
    12,
    20
)

AZUL_OSCURO = (
    13,
    28,
    46
)

AZUL = (
    65,
    180,
    255
)

BLANCO = (
    235,
    240,
    245
)

ROJO = (
    230,
    55,
    65
)

ROJO_OSCURO = (
    80,
    25,
    25
)

GRIS = (
    75,
    85,
    100
)

GRIS_CLARO = (
    130,
    140,
    155
)

VERDE = (
    65,
    210,
    120
)

MORADO = (
    180,
    70,
    180
)

AMARILLO = (
    240,
    210,
    60
)

NARANJA = (
    240,
    140,
    50
)

CIAN = (
    40,
    210,
    210
)

PISO = (
    28,
    38,
    48
)

LINEA_PISO = (
    45,
    55,
    65
)


# =========================================================
# FUENTES
# =========================================================

fuente_titulo = pygame.font.SysFont(
    "consolas",
    46,
    bold=True
)

fuente_subtitulo = pygame.font.SysFont(
    "consolas",
    30,
    bold=True
)

fuente_menu = pygame.font.SysFont(
    "consolas",
    26,
    bold=True
)

fuente_normal = pygame.font.SysFont(
    "consolas",
    22
)

fuente_pequena = pygame.font.SysFont(
    "consolas",
    17
)

fuente_mini = pygame.font.SysFont(
    "consolas",
    15
)


# =========================================================
# AUDIO
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RUTA_SONIDOS = os.path.join(
    BASE_DIR,
    "assets",
    "sonidos"
)


def ruta_audio(
    nombre
):

    return os.path.join(
        RUTA_SONIDOS,
        nombre
    )


def cargar_sonido(
    nombre,
    volumen=0.60
):

    if not AUDIO_DISPONIBLE:

        return None

    ruta = ruta_audio(
        nombre
    )

    try:

        sonido = pygame.mixer.Sound(
            ruta
        )

        sonido.set_volume(
            volumen
        )

        print(
            "Sonido cargado:",
            nombre
        )

        return sonido

    except Exception as error:

        print(
            "No se pudo cargar",
            nombre,
            ":",
            error
        )

        return None


def reproducir_sonido(
    sonido
):

    if (
        AUDIO_DISPONIBLE
        and
        sonido is not None
    ):

        sonido.play()


def reproducir_musica(
    nombre,
    volumen=0.35
):

    if not AUDIO_DISPONIBLE:

        return

    ruta = ruta_audio(
        nombre
    )

    try:

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            ruta
        )

        pygame.mixer.music.set_volume(
            volumen
        )

        pygame.mixer.music.play(
            -1
        )

        print(
            "Musica:",
            nombre
        )

    except Exception as error:

        print(
            "ERROR reproduciendo",
            nombre,
            ":",
            error
        )


def detener_musica():

    if AUDIO_DISPONIBLE:

        pygame.mixer.music.stop()


# EFECTOS

sonido_recoger = cargar_sonido(
    "recoger.wav"
)

sonido_puerta = cargar_sonido(
    "puerta.wav"
)

sonido_terminal = cargar_sonido(
    "terminal.wav"
)

sonido_golpe = cargar_sonido(
    "golpe.wav"
)

sonido_alien = cargar_sonido(
    "alien.wav"
)

sonido_alarma = cargar_sonido(
    "alarma.wav"
)

sonido_reactor = cargar_sonido(
    "reactor.wav"
)

sonido_victoria = cargar_sonido(
    "victoria.wav"
)


# =========================================================
# INVENTARIO
# =========================================================

INVENTARIO_INFO = {

    "tarjeta_acceso": {

        "nombre":
            "TARJETA DE ACCESO",

        "descripcion":
            (
                "Objeto clave. Permite abrir "
                "Ingeniería y Soporte Vital."
            ),

        "tipo":
            "clave"
    },


    "soplete_plasma": {

        "nombre":
            "SOPLETE DE PLASMA",

        "descripcion":
            (
                "Herramienta necesaria para entrar "
                "a la Sala del Reactor."
            ),

        "tipo":
            "clave"
    },


    "llave_maestra": {

        "nombre":
            "LLAVE MAESTRA",

        "descripcion":
            (
                "Permite activar el "
                "Protocolo Omega."
            ),

        "tipo":
            "clave"
    },


    "botiquin": {

        "nombre":
            "BOTIQUÍN",

        "descripcion":
            (
                "Recupera hasta 40 puntos "
                "de vida."
            ),

        "tipo":
            "consumible"
    },


    "extintor": {

        "nombre":
            "EXTINTOR",

        "descripcion":
            (
                "Puede lanzarse contra X-99 "
                "y posiblemente aturdirlo."
            ),

        "tipo":
            "combate"
    },


    "bateria_energia": {

        "nombre":
            "BATERÍA DE ENERGÍA",

        "descripcion":
            (
                "Objeto de combate que provoca "
                "daño eléctrico."
            ),

        "tipo":
            "combate"
    },


    "tubo_metalico": {

        "nombre":
            "TUBO METÁLICO",

        "descripcion":
            (
                "Arma improvisada para "
                "combatir al X-99."
            ),

        "tipo":
            "combate"
    }
}


# =========================================================
# NPC
# =========================================================

NPCS = {

    "soporte_vital":
        "DRA. VOSS",

    "laboratorio_c":
        "UNIDAD-7",

    "comunicaciones":
        "ASTRAEA"
}


# =========================================================
# POSICIONES DE LAS SALAS
# =========================================================

CONFIG_SALAS = {

    "ingenieria": {

        "objeto":
            pygame.Rect(
                180,
                300,
                135,
                60
            ),

        "terminal":
            pygame.Rect(
                385,
                175,
                160,
                60
            ),

        "reactor":
            pygame.Rect(
                700,
                250,
                110,
                80
            ),

        "salida":
            pygame.Rect(
                410,
                450,
                140,
                20
            )
    },


    "soporte_vital": {

        "objeto":
            pygame.Rect(
                175,
                305,
                135,
                60
            ),

        "npc":
            pygame.Rect(
                365,
                250,
                150,
                65
            ),

        "terminal":
            pygame.Rect(
                600,
                175,
                160,
                60
            ),

        "salida":
            pygame.Rect(
                410,
                450,
                140,
                20
            )
    },


    "laboratorio_c": {

        "objeto":
            pygame.Rect(
                175,
                280,
                135,
                60
            ),

        "npc":
            pygame.Rect(
                350,
                185,
                150,
                65
            ),

        "terminal":
            pygame.Rect(
                570,
                175,
                160,
                60
            ),

        "accion_final":
            pygame.Rect(
                565,
                320,
                190,
                60
            ),

        "ducto":
            pygame.Rect(
                175,
                380,
                90,
                55
            ),

        "salida":
            pygame.Rect(
                410,
                450,
                140,
                20
            )
    },


    "hangar": {

        "objeto":
            pygame.Rect(
                175,
                310,
                135,
                60
            ),

        "terminal":
            pygame.Rect(
                555,
                170,
                170,
                60
            ),

        "accion_final":
            pygame.Rect(
                565,
                310,
                180,
                60
            ),

        "ducto":
            pygame.Rect(
                175,
                385,
                90,
                55
            ),

        "salida":
            pygame.Rect(
                410,
                450,
                140,
                20
            )
    },


    "comunicaciones": {

        "objeto":
            pygame.Rect(
                175,
                305,
                135,
                60
            ),

        "terminal":
            pygame.Rect(
                555,
                170,
                170,
                60
            ),

        "accion_final":
            pygame.Rect(
                565,
                315,
                190,
                60
            ),

        "ducto":
            pygame.Rect(
                175,
                385,
                90,
                55
            ),

        "salida":
            pygame.Rect(
                410,
                450,
                140,
                20
            )
    }
}


# =========================================================
# TEXTO
# =========================================================

def corregir_texto_visible(
    texto
):

    texto = str(
        texto
    )

    cambios = {

        "dano":
            "daño",

        "Dano":
            "Daño",

        "DANO":
            "DAÑO",

        "mision":
            "misión",

        "Mision":
            "Misión",

        "MISION":
            "MISIÓN",

        "senal":
            "señal",

        "Senal":
            "Señal",

        "SENAL":
            "SEÑAL",

        "capsula":
            "cápsula",

        "Capsula":
            "Cápsula",

        "CAPSULA":
            "CÁPSULA",

        "oxigeno":
            "oxígeno",

        "Oxigeno":
            "Oxígeno",

        "OXIGENO":
            "OXÍGENO",

        "ingenieria":
            "ingeniería",

        "Ingenieria":
            "Ingeniería",

        "INGENIERIA":
            "INGENIERÍA",

        "autodestruccion":
            "autodestrucción",

        "Autodestruccion":
            "Autodestrucción",

        "AUTODESTRUCCION":
            "AUTODESTRUCCIÓN",

        "transmision":
            "transmisión",

        "Transmision":
            "Transmisión",

        "TRANSMISION":
            "TRANSMISIÓN",

        "descripcion":
            "descripción",

        "Descripcion":
            "Descripción",

        "DESCRIPCION":
            "DESCRIPCIÓN",

        "automaticamente":
            "automáticamente",

        "AUTOMATICO":
            "AUTOMÁTICO",

        "maximo":
            "máximo",

        "aqui":
            "aquí",

        "utiles":
            "útiles",

        "rapidamente":
            "rápidamente",

        "menu":
            "menú",

        "CREDITOS":
            "CRÉDITOS",

        "Automatas":
            "Autómatas",

        "Gramatica":
            "Gramática",

        "Integracion":
            "Integración"
    }


    for original, nuevo in cambios.items():

        texto = texto.replace(
            original,
            nuevo
        )


    return texto


def escribir(
    texto,
    fuente,
    color,
    x,
    y
):

    imagen = fuente.render(
        corregir_texto_visible(
            texto
        ),
        True,
        color
    )

    pantalla.blit(
        imagen,
        (
            x,
            y
        )
    )


def envolver_texto(
    texto,
    fuente,
    ancho_maximo
):

    palabras = corregir_texto_visible(
        texto
    ).split()


    if not palabras:

        return [""]


    lineas = []

    actual = palabras[0]


    for palabra in palabras[
        1:
    ]:

        prueba = (
            actual
            +
            " "
            +
            palabra
        )


        if (
            fuente.size(
                prueba
            )[0]
            <=
            ancho_maximo
        ):

            actual = prueba

        else:

            lineas.append(
                actual
            )

            actual = palabra


    lineas.append(
        actual
    )

    return lineas


def dibujar_texto_ajustado(
    texto,
    fuente,
    color,
    x,
    y,
    ancho,
    max_lineas=3,
    separacion=20
):

    lineas = envolver_texto(
        texto,
        fuente,
        ancho
    )[:max_lineas]


    for numero, linea in enumerate(
        lineas
    ):

        escribir(
            linea,
            fuente,
            color,
            x,
            y + numero * separacion
        )


# =========================================================
# FUNCIONES GENERALES
# =========================================================

def cerca(
    jugador,
    objeto,
    distancia=45
):

    return jugador.colliderect(
        objeto.inflate(
            distancia,
            distancia
        )
    )


def nombre_legible(
    texto
):

    return corregir_texto_visible(
        str(
            texto
        ).replace(
            "_",
            " "
        ).upper()
    )


def resumir_inventario(
    c,
    max_objetos=2
):

    objetos = c.get(
        "inventario",
        []
    )


    if not objetos:

        return "VACÍO"


    resultado = ", ".join(

        nombre_legible(
            objeto
        ).title()

        for objeto
        in objetos[
            :max_objetos
        ]
    )


    if (
        len(objetos)
        >
        max_objetos
    ):

        resultado += (
            f" +{len(objetos) - max_objetos}"
        )


    return resultado


def texto_mision(c):

    mision = c.get(
        "mision"
    )


    if not mision:

        return (
            "Sin misión activa"
        )


    if isinstance(
        mision,
        str
    ):

        return mision


    if isinstance(
        mision,
        dict
    ):

        for clave in (

            "texto",
            "descripcion",
            "mision",
            "objetivo"

        ):

            if clave in mision:

                return str(
                    mision[
                        clave
                    ]
                )


    return str(
        mision
    )


# =========================================================
# SISTEMAS
# =========================================================

def sistema_completo(
    c,
    clave
):

    valor = c.get(
        "sistemas_reparados",
        {}
    ).get(
        clave,
        False
    )


    if isinstance(
        valor,
        bool
    ):

        return valor


    if isinstance(
        valor,
        (
            int,
            float
        )
    ):

        return (
            valor >= 100
        )


    return bool(
        valor
    )


def obtener_porcentaje_sistema(
    c,
    clave
):

    valor = c.get(
        "sistemas_reparados",
        {}
    ).get(
        clave,
        0
    )


    if isinstance(
        valor,
        bool
    ):

        return (
            100
            if valor
            else 0
        )


    if isinstance(
        valor,
        (
            int,
            float
        )
    ):

        return max(
            0,
            min(
                100,
                int(
                    valor
                )
            )
        )


    return 0


def condiciones_sos(c):

    faltan = []


    if not sistema_completo(
        c,
        "motores"
    ):

        faltan.append(
            "motores"
        )


    if not sistema_completo(
        c,
        "comunicaciones"
    ):

        faltan.append(
            "comunicaciones"
        )


    if not sistema_completo(
        c,
        "oxigeno"
    ):

        faltan.append(
            "oxígeno"
        )


    if not c.get(
        "alien_derrotado",
        False
    ):

        faltan.append(
            "X-99"
        )


    return faltan


def sos_disponible(c):

    return (
        len(
            condiciones_sos(
                c
            )
        )
        ==
        0
    )


# =========================================================
# TRANSICIONES DEL AFN
# =========================================================

def procesar_transicion_compatible(
    estado,
    decisiones,
    c
):

    for decision in decisiones:

        resultado = narrativa.procesar_transicion(
            estado,
            decision,
            c
        )


        if (
            resultado
            !=
            "TRANSICION_RECHAZADA"
        ):

            return (
                resultado,
                decision
            )


    return (
        "TRANSICION_RECHAZADA",
        None
    )


# =========================================================
# DIALOGOS GLC
# =========================================================

def obtener_dialogo_glc(c, estado):
    return gramatica.hablar(c, estado)


# =========================================================
# GRAFICOS GENERALES
# =========================================================

def dibujar_cuadricula(
    x,
    y,
    ancho,
    alto
):

    for px in range(
        x,
        x + ancho,
        40
    ):

        pygame.draw.line(
            pantalla,
            LINEA_PISO,
            (
                px,
                y
            ),
            (
                px,
                y + alto
            )
        )


    for py in range(
        y,
        y + alto,
        40
    ):

        pygame.draw.line(
            pantalla,
            LINEA_PISO,
            (
                x,
                py
            ),
            (
                x + ancho,
                py
            )
        )


def dibujar_jugador(
    jugador
):

    x = jugador.x
    y = jugador.y


    pygame.draw.ellipse(
        pantalla,
        (
            10,
            15,
            20
        ),
        (
            x + 3,
            y + 25,
            27,
            9
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            45,
            60
        ),
        (
            x + 8,
            y + 23,
            6,
            8
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            45,
            60
        ),
        (
            x + 19,
            y + 23,
            6,
            8
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            220,
            225,
            235
        ),
        (
            x + 7,
            y + 13,
            19,
            13
        )
    )


    pygame.draw.rect(
        pantalla,
        AZUL,
        (
            x + 10,
            y + 16,
            13,
            6
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            225,
            185,
            145
        ),
        (
            x + 10,
            y + 5,
            13,
            10
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            40,
            50
        ),
        (
            x + 9,
            y + 3,
            15,
            5
        )
    )


    pygame.draw.rect(
        pantalla,
        CIAN,
        (
            x + 17,
            y + 8,
            5,
            3
        )
    )


def dibujar_rejilla_ducto(
    rect
):

    pygame.draw.rect(
        pantalla,
        (
            55,
            65,
            80
        ),
        rect
    )


    pygame.draw.rect(
        pantalla,
        GRIS_CLARO,
        rect,
        3
    )


    for x in range(
        rect.x + 10,
        rect.right - 5,
        15
    ):

        pygame.draw.line(
            pantalla,
            GRIS_CLARO,
            (
                x,
                rect.y + 6
            ),
            (
                x,
                rect.bottom - 6
            ),
            2
        )


def dibujar_terminal_retro(
    rect,
    activa=True
):

    color = (
        CIAN
        if activa
        else ROJO
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            45,
            55
        ),
        rect,
        border_radius=4
    )


    pygame.draw.rect(
        pantalla,
        GRIS_CLARO,
        rect,
        2,
        border_radius=4
    )


    pantalla_terminal = pygame.Rect(
        rect.x + 18,
        rect.y + 10,
        rect.width - 36,
        22
    )


    pygame.draw.rect(
        pantalla,
        (
            5,
            20,
            25
        ),
        pantalla_terminal
    )


    pygame.draw.rect(
        pantalla,
        color,
        pantalla_terminal,
        2
    )


    pygame.draw.rect(
        pantalla,
        VERDE,
        (
            rect.x + 25,
            rect.bottom - 18,
            10,
            6
        )
    )


    pygame.draw.rect(
        pantalla,
        AMARILLO,
        (
            rect.x + 42,
            rect.bottom - 18,
            10,
            6
        )
    )


    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            rect.x + 59,
            rect.bottom - 18,
            10,
            6
        )
    )


    escribir(
        "TERMINAL",
        fuente_mini,
        BLANCO,
        rect.centerx - 35,
        rect.y + 38
    )


def dibujar_caja_objetos(
    rect
):

    pygame.draw.rect(
        pantalla,
        (
            85,
            68,
            30
        ),
        rect
    )


    pygame.draw.rect(
        pantalla,
        AMARILLO,
        rect,
        2
    )


    pygame.draw.line(
        pantalla,
        (
            40,
            35,
            20
        ),
        rect.topleft,
        rect.bottomright,
        4
    )


    pygame.draw.line(
        pantalla,
        (
            40,
            35,
            20
        ),
        rect.topright,
        rect.bottomleft,
        4
    )


    escribir(
        "OBJETOS",
        fuente_mini,
        BLANCO,
        rect.x + 35,
        rect.y + 22
    )


def dibujar_barra_sistema(
    x,
    y,
    porcentaje,
    nombre
):

    escribir(
        nombre,
        fuente_mini,
        BLANCO,
        x,
        y - 22
    )


    pygame.draw.rect(
        pantalla,
        GRIS,
        (
            x,
            y,
            220,
            18
        )
    )


    color = (
        VERDE
        if porcentaje >= 100
        else ROJO
    )


    ancho = int(
        220
        *
        min(
            porcentaje,
            100
        )
        /
        100
    )


    pygame.draw.rect(
        pantalla,
        color,
        (
            x,
            y,
            ancho,
            18
        )
    )


    escribir(
        f"{porcentaje}%",
        fuente_mini,
        BLANCO,
        x + 90,
        y + 1
    )


# =========================================================
# MENU - FONDO
# =========================================================

def dibujar_fondo_menu():

    pantalla.fill(
        NEGRO
    )


    pygame.draw.rect(
        pantalla,
        AZUL_OSCURO,
        (
            70,
            50,
            820,
            550
        ),
        border_radius=10
    )


    pygame.draw.rect(
        pantalla,
        AZUL,
        (
            70,
            50,
            820,
            550
        ),
        2,
        border_radius=10
    )


    estrellas = [

        (100, 90),
        (170, 150),
        (280, 90),
        (760, 100),
        (850, 170),

        (120, 300),
        (830, 330),
        (700, 210),
        (540, 90),
        (400, 180),

        (220, 420),
        (700, 450)
    ]


    for punto in estrellas:

        pygame.draw.circle(
            pantalla,
            BLANCO,
            punto,
            2
        )


# =========================================================
# PASILLO
# =========================================================

def dibujar_piso_pasillo():

    pygame.draw.rect(
        pantalla,
        (
            25,
            33,
            43
        ),
        (
            100,
            80,
            760,
            400
        )
    )


    for fila, y in enumerate(
        range(
            80,
            480,
            40
        )
    ):

        for columna, x in enumerate(
            range(
                100,
                860,
                40
            )
        ):

            color = (

                (
                    32,
                    42,
                    54
                )

                if (
                    fila + columna
                ) % 2 == 0

                else

                (
                    28,
                    37,
                    48
                )
            )


            pygame.draw.rect(
                pantalla,
                color,
                (
                    x,
                    y,
                    40,
                    40
                )
            )


            pygame.draw.rect(
                pantalla,
                (
                    42,
                    54,
                    66
                ),
                (
                    x,
                    y,
                    40,
                    40
                ),
                1
            )


    pygame.draw.rect(
        pantalla,
        (
            40,
            49,
            59
        ),
        (
            300,
            120,
            360,
            300
        )
    )


def dibujar_puerta(
    rect,
    nombre,
    abierta
):

    color_estado = (
        VERDE
        if abierta
        else ROJO
    )


    marco = rect.inflate(
        12,
        12
    )


    pygame.draw.rect(
        pantalla,
        (
            20,
            27,
            35
        ),
        marco
    )


    pygame.draw.rect(
        pantalla,
        GRIS_CLARO,
        marco,
        2
    )


    pygame.draw.rect(
        pantalla,
        (
            45,
            55,
            65
        ),
        rect
    )


    pygame.draw.rect(
        pantalla,
        color_estado,
        (
            rect.x + 4,
            rect.y + 4,
            7,
            7
        )
    )


    if (
        rect.width
        >
        rect.height
    ):

        escribir(
            nombre,
            fuente_mini,
            BLANCO,
            rect.centerx - 45,
            rect.y + 27
        )

    else:

        escribir(
            nombre,
            fuente_mini,
            BLANCO,
            rect.x + 25,
            rect.centery - 8
        )


# =========================================================
# INGENIERIA
# =========================================================

def dibujar_ingenieria():

    pygame.draw.rect(
        pantalla,
        (
            26,
            35,
            43
        ),
        (
            120,
            110,
            720,
            360
        )
    )


    dibujar_cuadricula(
        120,
        110,
        720,
        360
    )


    pygame.draw.rect(
        pantalla,
        (
            90,
            110,
            120
        ),
        (
            120,
            110,
            720,
            360
        ),
        3
    )


    pygame.draw.line(
        pantalla,
        (
            85,
            95,
            105
        ),
        (
            145,
            150
        ),
        (
            145,
            370
        ),
        10
    )


    pygame.draw.line(
        pantalla,
        CIAN,
        (
            150,
            150
        ),
        (
            150,
            370
        ),
        3
    )


    pygame.draw.line(
        pantalla,
        (
            100,
            110,
            120
        ),
        (
            250,
            135
        ),
        (
            690,
            135
        ),
        8
    )


    pygame.draw.circle(
        pantalla,
        ROJO,
        (
            150,
            240
        ),
        12,
        3
    )


def dibujar_puerta_reactor(
    rect,
    reparado
):

    color = (
        VERDE
        if reparado
        else ROJO
    )


    marco = rect.inflate(
        14,
        14
    )


    pygame.draw.rect(
        pantalla,
        (
            25,
            30,
            35
        ),
        marco
    )


    pygame.draw.rect(
        pantalla,
        color,
        marco,
        3
    )


    pygame.draw.rect(
        pantalla,
        (
            50,
            55,
            60
        ),
        rect
    )


    pygame.draw.line(
        pantalla,
        (
            15,
            20,
            25
        ),
        (
            rect.centerx,
            rect.top
        ),
        (
            rect.centerx,
            rect.bottom
        ),
        3
    )


    pygame.draw.circle(
        pantalla,
        color,
        (
            rect.x + 15,
            rect.y + 15
        ),
        5
    )


    escribir(
        "REACTOR",
        fuente_mini,
        BLANCO,
        rect.x + 18,
        rect.y + 37
    )


# =========================================================
# SOPORTE VITAL
# =========================================================

def dibujar_tanque_oxigeno(
    x,
    y,
    lleno
):

    color = (
        VERDE
        if lleno
        else ROJO
    )


    pygame.draw.rect(
        pantalla,
        (
            105,
            120,
            130
        ),
        (
            x,
            y + 10,
            48,
            65
        ),
        border_radius=10
    )


    pygame.draw.rect(
        pantalla,
        color,
        (
            x,
            y + 10,
            48,
            65
        ),
        3,
        border_radius=10
    )


    pygame.draw.rect(
        pantalla,
        (
            70,
            80,
            90
        ),
        (
            x + 14,
            y,
            20,
            15
        )
    )


    pygame.draw.circle(
        pantalla,
        color,
        (
            x + 24,
            y + 38
        ),
        7
    )


def dibujar_dra_voss(
    rect
):

    x = rect.centerx - 18
    y = rect.centery - 25


    pygame.draw.rect(
        pantalla,
        (
            40,
            55,
            70
        ),
        (
            x + 8,
            y + 35,
            7,
            17
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            40,
            55,
            70
        ),
        (
            x + 23,
            y + 35,
            7,
            17
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            220,
            230,
            235
        ),
        (
            x + 5,
            y + 18,
            29,
            24
        )
    )


    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            x + 17,
            y + 22,
            5,
            14
        )
    )


    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            x + 12,
            y + 27,
            15,
            5
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            225,
            185,
            150
        ),
        (
            x + 10,
            y + 5,
            18,
            15
        )
    )


def dibujar_soporte_vital(c):

    oxigeno = obtener_porcentaje_sistema(
        c,
        "oxigeno"
    )


    reparado = (
        oxigeno >= 100
    )


    pygame.draw.rect(
        pantalla,
        (
            24,
            38,
            42
        ),
        (
            120,
            110,
            720,
            360
        )
    )


    dibujar_cuadricula(
        120,
        110,
        720,
        360
    )


    pygame.draw.rect(
        pantalla,
        (
            65,
            160,
            140
        ),
        (
            120,
            110,
            720,
            360
        ),
        3
    )


    pygame.draw.line(
        pantalla,
        (
            85,
            105,
            105
        ),
        (
            145,
            140
        ),
        (
            810,
            140
        ),
        9
    )


    pygame.draw.line(
        pantalla,
        (
            VERDE
            if reparado
            else ROJO
        ),
        (
            145,
            145
        ),
        (
            810,
            145
        ),
        3
    )


    dibujar_tanque_oxigeno(
        735,
        270,
        reparado
    )


    dibujar_tanque_oxigeno(
        675,
        270,
        reparado
    )


    dibujar_barra_sistema(
        360,
        155,
        oxigeno,
        "OXÍGENO"
    )


    if reparado:

        escribir(
            "ATMÓSFERA ESTABLE",
            fuente_pequena,
            VERDE,
            390,
            195
        )

    else:

        escribir(
            "ALERTA: OXÍGENO CRÍTICO",
            fuente_pequena,
            ROJO,
            375,
            195
        )


# =========================================================
# LABORATORIO
# =========================================================

def dibujar_unidad7(
    rect
):

    x = rect.centerx - 20
    y = rect.centery - 28


    pygame.draw.rect(
        pantalla,
        (
            90,
            100,
            110
        ),
        (
            x + 7,
            y + 38,
            8,
            18
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            90,
            100,
            110
        ),
        (
            x + 27,
            y + 38,
            8,
            18
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            70,
            85,
            100
        ),
        (
            x + 4,
            y + 18,
            34,
            25
        ),
        border_radius=4
    )


    pygame.draw.rect(
        pantalla,
        CIAN,
        (
            x + 4,
            y + 18,
            34,
            25
        ),
        2
    )


    pygame.draw.circle(
        pantalla,
        CIAN,
        (
            x + 21,
            y + 30
        ),
        5
    )


    pygame.draw.rect(
        pantalla,
        (
            100,
            115,
            125
        ),
        (
            x + 9,
            y + 2,
            24,
            18
        )
    )


    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            x + 14,
            y + 8,
            14,
            4
        )
    )


def dibujar_laboratorio(c):

    derrotado = c.get(
        "alien_derrotado",
        False
    )


    pygame.draw.rect(
        pantalla,
        (
            25,
            28,
            38
        ),
        (
            120,
            110,
            720,
            360
        )
    )


    dibujar_cuadricula(
        120,
        110,
        720,
        360
    )


    pygame.draw.rect(
        pantalla,
        MORADO,
        (
            120,
            110,
            720,
            360
        ),
        3
    )


    for x in (
        160,
        300,
        440,
        580,
        720
    ):

        pygame.draw.rect(
            pantalla,
            (
                VERDE
                if derrotado
                else ROJO
            ),
            (
                x,
                123,
                65,
                4
            )
        )


    # Cápsula rota

    capsula = pygame.Rect(
        700,
        240,
        100,
        125
    )


    pygame.draw.rect(
        pantalla,
        (
            20,
            50,
            60
        ),
        capsula,
        border_radius=18
    )


    pygame.draw.rect(
        pantalla,
        ROJO,
        capsula,
        3,
        border_radius=18
    )


    pygame.draw.ellipse(
        pantalla,
        (
            10,
            25,
            30
        ),
        (
            722,
            265,
            56,
            75
        )
    )


    escribir(
        "X-99",
        fuente_mini,
        ROJO,
        733,
        300
    )


    if derrotado:

        escribir(
            "X-99 NEUTRALIZADO",
            fuente_pequena,
            VERDE,
            370,
            120
        )

    else:

        escribir(
            "ALERTA: CONTENCIÓN FALLIDA",
            fuente_pequena,
            ROJO,
            355,
            120
        )


# =========================================================
# HANGAR
# =========================================================

def dibujar_caja_carga(
    x,
    y,
    ancho=60,
    alto=45
):

    pygame.draw.rect(
        pantalla,
        (
            85,
            70,
            40
        ),
        (
            x,
            y,
            ancho,
            alto
        )
    )


    pygame.draw.rect(
        pantalla,
        AMARILLO,
        (
            x,
            y,
            ancho,
            alto
        ),
        2
    )


    pygame.draw.line(
        pantalla,
        (
            45,
            38,
            25
        ),
        (
            x,
            y
        ),
        (
            x + ancho,
            y + alto
        ),
        3
    )


def dibujar_hangar(c):

    preparado = sistema_completo(
        c,
        "hangar_minimo"
    )


    pygame.draw.rect(
        pantalla,
        (
            27,
            31,
            38
        ),
        (
            120,
            110,
            720,
            360
        )
    )


    dibujar_cuadricula(
        120,
        110,
        720,
        360
    )


    pygame.draw.rect(
        pantalla,
        GRIS_CLARO,
        (
            120,
            110,
            720,
            360
        ),
        3
    )


    dibujar_caja_carga(
        145,
        155,
        75,
        55
    )


    dibujar_caja_carga(
        230,
        170
    )


    dibujar_caja_carga(
        155,
        230
    )


    if preparado:

        escribir(
            "CÁPSULA LISTA PARA LANZAMIENTO",
            fuente_pequena,
            VERDE,
            335,
            140
        )

    else:

        escribir(
            "CÁPSULA FUERA DE SERVICIO",
            fuente_pequena,
            ROJO,
            355,
            140
        )


def dibujar_capsula_escape(
    rect,
    preparada
):

    color = (
        VERDE
        if preparada
        else ROJO
    )


    pygame.draw.ellipse(
        pantalla,
        (
            90,
            100,
            110
        ),
        rect
    )


    pygame.draw.ellipse(
        pantalla,
        color,
        rect,
        4
    )


    ventana = pygame.Rect(
        rect.x + 35,
        rect.y + 25,
        rect.width - 70,
        45
    )


    pygame.draw.ellipse(
        pantalla,
        (
            10,
            35,
            45
        ),
        ventana
    )


    pygame.draw.ellipse(
        pantalla,
        CIAN,
        ventana,
        3
    )


    pygame.draw.circle(
        pantalla,
        color,
        (
            rect.centerx,
            rect.bottom - 20
        ),
        7
    )


# =========================================================
# COMUNICACIONES
# =========================================================

def dibujar_monitor_senal(
    x,
    y,
    activa
):

    color = (
        VERDE
        if activa
        else ROJO
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            45,
            55
        ),
        (
            x,
            y,
            115,
            70
        )
    )


    pygame.draw.rect(
        pantalla,
        color,
        (
            x,
            y,
            115,
            70
        ),
        2
    )


    pygame.draw.rect(
        pantalla,
        (
            5,
            18,
            23
        ),
        (
            x + 10,
            y + 10,
            95,
            40
        )
    )


    puntos = [

        (
            x + 15,
            y + 35
        ),

        (
            x + 30,
            y + 35
        ),

        (
            x + 37,
            y + 20
        ),

        (
            x + 46,
            y + 45
        ),

        (
            x + 57,
            y + 30
        ),

        (
            x + 70,
            y + 30
        ),

        (
            x + 80,
            y + 18
        ),

        (
            x + 90,
            y + 40
        ),

        (
            x + 103,
            y + 30
        )
    ]


    pygame.draw.lines(
        pantalla,
        color,
        False,
        puntos,
        2
    )


def dibujar_comunicaciones(c):

    reparado = sistema_completo(
        c,
        "comunicaciones"
    )


    pygame.draw.rect(
        pantalla,
        (
            20,
            30,
            42
        ),
        (
            120,
            110,
            720,
            360
        )
    )


    dibujar_cuadricula(
        120,
        110,
        720,
        360
    )


    pygame.draw.rect(
        pantalla,
        CIAN,
        (
            120,
            110,
            720,
            360
        ),
        3
    )


    dibujar_monitor_senal(
        155,
        155,
        reparado
    )


    dibujar_monitor_senal(
        285,
        155,
        reparado
    )


    # Antena

    pygame.draw.line(
        pantalla,
        GRIS_CLARO,
        (
            720,
            200
        ),
        (
            720,
            280
        ),
        5
    )


    pygame.draw.arc(
        pantalla,
        (
            VERDE
            if reparado
            else ROJO
        ),
        (
            680,
            165,
            80,
            60
        ),
        0.2,
        2.9,
        5
    )


    if reparado:

        escribir(
            "COMUNICACIONES OPERATIVAS",
            fuente_pequena,
            VERDE,
            350,
            120
        )

    else:

        escribir(
            "ERROR: ENLACE EXTERNO CAÍDO",
            fuente_pequena,
            ROJO,
            350,
            120
        )


# =========================================================
# TERMINAL OMEGA / SOS
# =========================================================

def dibujar_terminal_especial(
    rect,
    texto,
    habilitada
):

    color = (
        VERDE
        if habilitada
        else ROJO
    )


    pygame.draw.rect(
        pantalla,
        (
            35,
            30,
            40
        ),
        rect,
        border_radius=5
    )


    pygame.draw.rect(
        pantalla,
        color,
        rect,
        3,
        border_radius=5
    )


    pygame.draw.rect(
        pantalla,
        (
            5,
            20,
            25
        ),
        (
            rect.x + 15,
            rect.y + 8,
            rect.width - 30,
            25
        )
    )


    escribir(
        texto,
        fuente_mini,
        color,
        rect.centerx - 35,
        rect.y + 12
    )


    pygame.draw.circle(
        pantalla,
        color,
        (
            rect.centerx,
            rect.bottom - 14
        ),
        8
    )


# =========================================================
# X-99
# =========================================================

def dibujar_x99(
    x,
    y,
    estado
):

    if estado == "aturdido":

        visor = AMARILLO

    elif estado == "herido":

        visor = NARANJA

    elif estado == "derrotado":

        visor = GRIS

    else:

        visor = ROJO


    pygame.draw.ellipse(
        pantalla,
        (
            5,
            8,
            10
        ),
        (
            x - 10,
            y + 135,
            120,
            25
        )
    )


    # Piernas

    pygame.draw.rect(
        pantalla,
        (
            45,
            55,
            45
        ),
        (
            x + 15,
            y + 100,
            22,
            45
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            45,
            55,
            45
        ),
        (
            x + 65,
            y + 100,
            22,
            45
        )
    )


    # Torso

    pygame.draw.polygon(
        pantalla,
        (
            55,
            70,
            55
        ),
        [

            (
                x + 20,
                y + 50
            ),

            (
                x + 80,
                y + 50
            ),

            (
                x + 95,
                y + 105
            ),

            (
                x + 10,
                y + 105
            )
        ]
    )


    # Brazos

    pygame.draw.rect(
        pantalla,
        (
            50,
            65,
            50
        ),
        (
            x - 3,
            y + 58,
            18,
            55
        )
    )


    pygame.draw.rect(
        pantalla,
        (
            50,
            65,
            50
        ),
        (
            x + 85,
            y + 58,
            18,
            55
        )
    )


    # Cabeza

    pygame.draw.polygon(
        pantalla,
        (
            70,
            85,
            65
        ),
        [

            (
                x + 25,
                y + 18
            ),

            (
                x + 75,
                y + 18
            ),

            (
                x + 82,
                y + 45
            ),

            (
                x + 68,
                y + 58
            ),

            (
                x + 32,
                y + 58
            ),

            (
                x + 18,
                y + 45
            )
        ]
    )


    pygame.draw.rect(
        pantalla,
        (
            95,
            105,
            95
        ),
        (
            x + 30,
            y + 28,
            40,
            22
        )
    )


    pygame.draw.rect(
        pantalla,
        visor,
        (
            x + 35,
            y + 33,
            30,
            5
        )
    )


    pygame.draw.circle(
        pantalla,
        visor,
        (
            x + 50,
            y + 78
        ),
        6
    )


    if estado == "aturdido":

        escribir(
            "* * *",
            fuente_pequena,
            AMARILLO,
            x + 30,
            y - 10
        )


# =========================================================
# HUD
# =========================================================

def dibujar_hud(
    c,
    ubicacion,
    mensaje
):

    pygame.draw.rect(
        pantalla,
        AZUL_OSCURO,
        (
            100,
            515,
            760,
            125
        )
    )


    pygame.draw.rect(
        pantalla,
        AZUL,
        (
            100,
            515,
            760,
            125
        ),
        2
    )


    pygame.draw.line(
        pantalla,
        (
            55,
            95,
            125
        ),
        (
            455,
            525
        ),
        (
            455,
            630
        ),
        1
    )


    escribir(
        f"VIDA: {c['vida']}/100",
        fuente_pequena,
        VERDE,
        120,
        530
    )


    escribir(
        "UBICACIÓN:",
        fuente_mini,
        BLANCO,
        120,
        557
    )


    escribir(
        nombre_legible(
            ubicacion
        ),
        fuente_mini,
        CIAN,
        220,
        557
    )


    escribir(
        "INVENTARIO:",
        fuente_mini,
        BLANCO,
        120,
        584
    )


    dibujar_texto_ajustado(
        resumir_inventario(
            c
        ),
        fuente_mini,
        BLANCO,
        220,
        584,
        215,
        2
    )


    escribir(
        "[I] INVENTARIO",
        fuente_mini,
        GRIS_CLARO,
        120,
        615
    )


    escribir(
        "MISIÓN ACTUAL:",
        fuente_mini,
        AMARILLO,
        475,
        530
    )


    dibujar_texto_ajustado(
        texto_mision(
            c
        ),
        fuente_mini,
        BLANCO,
        475,
        552,
        355,
        2
    )


    dibujar_texto_ajustado(
        mensaje,
        fuente_mini,
        AMARILLO,
        475,
        594,
        355,
        2
    )


# =========================================================
# DIALOGOS
# =========================================================

def mostrar_dialogo(
    texto,
    titulo="TRANSMISIÓN"
):

    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (

                evento.type
                ==
                pygame.KEYDOWN

                and

                evento.key in (

                    pygame.K_RETURN,
                    pygame.K_e,
                    pygame.K_ESCAPE

                )
            ):

                return


        sombra = pygame.Surface(
            (
                ANCHO,
                ALTO
            ),
            pygame.SRCALPHA
        )


        sombra.fill(
            (
                0,
                0,
                0,
                170
            )
        )


        pantalla.blit(
            sombra,
            (
                0,
                0
            )
        )


        caja = pygame.Rect(
            120,
            360,
            720,
            235
        )


        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            caja,
            border_radius=8
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            caja,
            3,
            border_radius=8
        )


        escribir(
            titulo,
            fuente_normal,
            CIAN,
            145,
            382
        )


        lineas = envolver_texto(
            texto,
            fuente_mini,
            650
        )


        for numero, linea in enumerate(
            lineas[:7]
        ):

            escribir(
                linea,
                fuente_mini,
                BLANCO,
                145,
                425 + numero * 21
            )


        escribir(
            "E / ENTER - CONTINUAR",
            fuente_mini,
            GRIS_CLARO,
            610,
            565
        )


        pygame.display.flip()


# =========================================================
# INVENTARIO GRAFICO
# =========================================================

def pantalla_inventario(c):

    seleccionado = 0

    mensaje = (
        "Selecciona un objeto."
    )


    while True:

        reloj.tick(
            FPS
        )


        objetos = c.get(
            "inventario",
            []
        )


        if objetos:

            seleccionado = max(
                0,
                min(
                    seleccionado,
                    len(objetos) - 1
                )
            )

        else:

            seleccionado = 0


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key in (

                    pygame.K_ESCAPE,
                    pygame.K_i

                ):

                    return


                elif (

                    evento.key
                    ==
                    pygame.K_UP

                    and

                    objetos
                ):

                    seleccionado = (
                        seleccionado - 1
                    ) % len(objetos)


                elif (

                    evento.key
                    ==
                    pygame.K_DOWN

                    and

                    objetos
                ):

                    seleccionado = (
                        seleccionado + 1
                    ) % len(objetos)


                elif evento.key in (

                    pygame.K_e,
                    pygame.K_RETURN

                ):

                    if not objetos:

                        mensaje = (
                            "El inventario está vacío."
                        )

                        continue


                    objeto = objetos[
                        seleccionado
                    ]


                    datos = INVENTARIO_INFO.get(

                        objeto,

                        {

                            "nombre":
                                nombre_legible(
                                    objeto
                                ),

                            "descripcion":
                                "Objeto sin descripción.",

                            "tipo":
                                "desconocido"
                        }
                    )


                    if objeto == "botiquin":

                        if (
                            c["vida"]
                            >=
                            100
                        ):

                            mensaje = (
                                "Tu vida ya está al máximo."
                            )

                        else:

                            try:

                                mensaje = mundo.procesar_accion_mundo(
                                    "usar_botiquin",
                                    "inventario",
                                    c
                                )

                            except Exception:

                                vida_anterior = c[
                                    "vida"
                                ]


                                c["vida"] = min(
                                    100,
                                    c["vida"] + 40
                                )


                                if (
                                    "botiquin"
                                    in
                                    c["inventario"]
                                ):

                                    c[
                                        "inventario"
                                    ].remove(
                                        "botiquin"
                                    )


                                mensaje = (
                                    f"Recuperaste "
                                    f"{c['vida'] - vida_anterior} HP."
                                )


                    elif (
                        datos["tipo"]
                        ==
                        "clave"
                    ):

                        mensaje = (
                            datos["nombre"]
                            +
                            " se utiliza automáticamente."
                        )


                    elif (
                        datos["tipo"]
                        ==
                        "combate"
                    ):

                        mensaje = (
                            datos["nombre"]
                            +
                            " se utiliza en combate."
                        )


        pantalla.fill(
            NEGRO
        )


        escribir(
            "INVENTARIO",
            fuente_titulo,
            AZUL,
            350,
            50
        )


        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                100,
                120,
                350,
                400
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                100,
                120,
                350,
                400
            ),
            2
        )


        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                480,
                120,
                380,
                400
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                480,
                120,
                380,
                400
            ),
            2
        )


        escribir(
            "OBJETOS",
            fuente_normal,
            BLANCO,
            125,
            145
        )


        if not objetos:

            escribir(
                "Inventario vacío",
                fuente_pequena,
                GRIS,
                125,
                200
            )


        for indice, objeto in enumerate(
            objetos[:7]
        ):

            y = (
                195
                +
                indice * 43
            )


            datos = INVENTARIO_INFO.get(

                objeto,

                {
                    "nombre":
                        nombre_legible(
                            objeto
                        )
                }
            )


            if (
                indice
                ==
                seleccionado
            ):

                pygame.draw.rect(
                    pantalla,
                    AZUL,
                    (
                        120,
                        y - 7,
                        305,
                        34
                    )
                )


                color = NEGRO

                escribir(
                    ">",
                    fuente_pequena,
                    NEGRO,
                    130,
                    y
                )

            else:

                color = BLANCO


            escribir(
                datos[
                    "nombre"
                ],
                fuente_mini,
                color,
                160,
                y
            )


        if objetos:

            objeto = objetos[
                seleccionado
            ]


            datos = INVENTARIO_INFO.get(

                objeto,

                {

                    "nombre":
                        nombre_legible(
                            objeto
                        ),

                    "descripcion":
                        "Sin descripción.",

                    "tipo":
                        "desconocido"
                }
            )


            escribir(
                datos[
                    "nombre"
                ],
                fuente_normal,
                AMARILLO,
                510,
                150
            )


            escribir(
                "TIPO:",
                fuente_mini,
                BLANCO,
                510,
                195
            )


            escribir(
                datos[
                    "tipo"
                ].upper(),
                fuente_mini,
                CIAN,
                575,
                195
            )


            escribir(
                "DESCRIPCIÓN:",
                fuente_mini,
                BLANCO,
                510,
                235
            )


            dibujar_texto_ajustado(
                datos[
                    "descripcion"
                ],
                fuente_mini,
                BLANCO,
                510,
                265,
                310,
                6
            )


            if objeto == "botiquin":

                escribir(
                    f"VIDA: {c['vida']}/100",
                    fuente_pequena,
                    VERDE,
                    510,
                    405
                )


                escribir(
                    "E / ENTER - USAR",
                    fuente_pequena,
                    AMARILLO,
                    510,
                    445
                )


        pygame.draw.rect(
            pantalla,
            (
                20,
                35,
                50
            ),
            (
                100,
                545,
                760,
                70
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                100,
                545,
                760,
                70
            ),
            2
        )


        dibujar_texto_ajustado(
            mensaje,
            fuente_mini,
            AMARILLO,
            120,
            560,
            720,
            2
        )


        escribir(
            "FLECHAS seleccionar | E usar | I/ESC cerrar",
            fuente_mini,
            GRIS_CLARO,
            285,
            625
        )


        pygame.display.flip()


# =========================================================
# SELECTOR OBJETOS COMBATE
# =========================================================

def pantalla_objetos_combate(c):

    objetos = combate.objetos_disponibles(
        c
    )


    if not objetos:

        mostrar_dialogo(
            "No tienes objetos arrojables.",
            "INVENTARIO"
        )

        return None


    seleccionado = 0


    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key == pygame.K_ESCAPE:

                    return None


                elif evento.key == pygame.K_UP:

                    seleccionado = (
                        seleccionado - 1
                    ) % len(objetos)


                elif evento.key == pygame.K_DOWN:

                    seleccionado = (
                        seleccionado + 1
                    ) % len(objetos)


                elif evento.key in (

                    pygame.K_e,
                    pygame.K_RETURN

                ):

                    return objetos[
                        seleccionado
                    ]


        pantalla.fill(
            NEGRO
        )


        escribir(
            "LANZAR OBJETO",
            fuente_titulo,
            AMARILLO,
            315,
            70
        )


        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                210,
                160,
                540,
                330
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                210,
                160,
                540,
                330
            ),
            2
        )


        for indice, objeto in enumerate(
            objetos
        ):

            y = (
                210
                +
                indice * 65
            )


            datos = combate.OBJETOS_ARROJABLES[
                objeto
            ]


            if (
                indice
                ==
                seleccionado
            ):

                pygame.draw.rect(
                    pantalla,
                    AZUL,
                    (
                        250,
                        y - 10,
                        460,
                        45
                    )
                )

                color = NEGRO

            else:

                color = BLANCO


            escribir(
                datos[
                    "nombre"
                ].upper(),
                fuente_normal,
                color,
                290,
                y
            )


        pygame.display.flip()


# =========================================================
# COMBATE X-99
# =========================================================

def pantalla_combate(
    c,
    ubicacion
):

    datos = combate.crear_combate(
        c
    )


    seleccionado = 0

    flash = 0


    opciones = [

        "ATACAR",

        "DEFENDER",

        "LANZAR OBJETO",

        "USAR ENTORNO",

        "ESCAPAR"
    ]


    posiciones = [

        (
            130,
            465
        ),

        (
            455,
            465
        ),

        (
            130,
            510
        ),

        (
            455,
            510
        ),

        (
            130,
            555
        )
    ]


    def turno_alien():

        if (
            datos[
                "estado"
            ]
            !=
            "TURNO_X99"
        ):

            return


        vida_antes = c[
            "vida"
        ]

        mensaje_jugador = datos[
            "mensaje"
        ]


        combate.turno_alien(
            c,
            datos
        )


        mensaje_alien = datos[
            "mensaje"
        ]


        if (
            c["vida"]
            <
            vida_antes
        ):

            reproducir_sonido(
                sonido_alien
            )


        if (
            mensaje_alien
            !=
            mensaje_jugador
        ):

            datos[
                "mensaje"
            ] = (
                mensaje_jugador
                +
                "  "
                +
                mensaje_alien
            )


    while True:

        reloj.tick(
            FPS
        )


        resultado = combate.resultado_combate(
            datos
        )


        if resultado:

            mostrar_dialogo(
                datos[
                    "mensaje"
                ],
                "RESULTADO DEL COMBATE"
            )

            return resultado


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key in (

                    pygame.K_UP,
                    pygame.K_LEFT

                ):

                    seleccionado = (
                        seleccionado - 1
                    ) % len(opciones)


                elif evento.key in (

                    pygame.K_DOWN,
                    pygame.K_RIGHT

                ):

                    seleccionado = (
                        seleccionado + 1
                    ) % len(opciones)


                elif evento.key in (

                    pygame.K_e,
                    pygame.K_RETURN

                ):


                    if seleccionado == 0:

                        hp_antes = c.get(
                            "alien_hp",
                            65
                        )


                        combate.atacar(
                            c,
                            datos
                        )


                        if (
                            c.get(
                                "alien_hp",
                                65
                            )
                            <
                            hp_antes
                        ):

                            reproducir_sonido(
                                sonido_golpe
                            )

                            flash = 8


                        turno_alien()


                    elif seleccionado == 1:

                        combate.defender(
                            c,
                            datos
                        )

                        turno_alien()


                    elif seleccionado == 2:

                        objeto = pantalla_objetos_combate(
                            c
                        )


                        if objeto:

                            combate.lanzar_objeto(
                                c,
                                datos,
                                objeto
                            )

                            reproducir_sonido(
                                sonido_golpe
                            )

                            flash = 8

                            turno_alien()


                    elif seleccionado == 3:

                        combate.usar_entorno(
                            c,
                            datos,
                            ubicacion
                        )

                        reproducir_sonido(
                            sonido_golpe
                        )

                        flash = 8

                        turno_alien()


                    elif seleccionado == 4:

                        combate.huir(
                            c,
                            datos
                        )

                        turno_alien()


        # FONDO

        pantalla.fill(
            (
                7,
                10,
                15
            )
        )


        pygame.draw.rect(
            pantalla,
            (
                22,
                27,
                35
            ),
            (
                40,
                90,
                880,
                330
            )
        )


        pygame.draw.rect(
            pantalla,
            ROJO_OSCURO,
            (
                40,
                90,
                880,
                330
            ),
            3
        )


        estado_alien = c.get(
            "alien_estado",
            "normal"
        )


        if estado_alien == "aturdido":

            titulo = (
                "X-99 ATURDIDO"
            )

        elif estado_alien == "herido":

            titulo = (
                "X-99 HERIDO"
            )

        else:

            titulo = (
                "ENCUENTRO HOSTIL"
            )


        escribir(
            titulo,
            fuente_titulo,
            ROJO,
            275,
            35
        )


        # JUGADOR

        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                90,
                135,
                350,
                260
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                90,
                135,
                350,
                260
            ),
            2
        )


        escribir(
            "TRIPULANTE",
            fuente_normal,
            CIAN,
            125,
            155
        )


        pygame.draw.rect(
            pantalla,
            GRIS,
            (
                125,
                205,
                260,
                24
            )
        )


        pygame.draw.rect(
            pantalla,
            VERDE,
            (
                125,
                205,
                int(
                    260
                    *
                    max(
                        0,
                        c["vida"]
                        /
                        100
                    )
                ),
                24
            )
        )


        escribir(
            f"HP: {c['vida']}/100",
            fuente_mini,
            BLANCO,
            210,
            208
        )


        dibujar_texto_ajustado(
            datos[
                "mensaje"
            ],
            fuente_mini,
            AMARILLO,
            125,
            265,
            270,
            5
        )


        # X99

        dibujar_x99(
            620,
            150,
            estado_alien
        )


        escribir(
            "X-99",
            fuente_normal,
            ROJO,
            650,
            320
        )


        escribir(
            (
                "ESTADO: "
                +
                estado_alien.upper()
            ),
            fuente_mini,
            AMARILLO,
            600,
            350
        )


        hp_alien = c.get(
            "alien_hp",
            65
        )


        pygame.draw.rect(
            pantalla,
            GRIS,
            (
                535,
                380,
                250,
                22
            )
        )


        pygame.draw.rect(
            pantalla,
            ROJO,
            (
                535,
                380,
                int(
                    250
                    *
                    max(
                        0,
                        hp_alien
                        /
                        65
                    )
                ),
                22
            )
        )


        escribir(
            f"X-99: {hp_alien}/65",
            fuente_mini,
            BLANCO,
            600,
            382
        )


        # MENU

        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                90,
                430,
                700,
                185
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                90,
                430,
                700,
                185
            ),
            2
        )


        for indice, opcion in enumerate(
            opciones
        ):

            x, y = posiciones[
                indice
            ]


            if (
                indice
                ==
                seleccionado
            ):

                pygame.draw.rect(
                    pantalla,
                    AZUL,
                    (
                        x - 12,
                        y - 7,
                        285,
                        35
                    )
                )


                color = NEGRO

                escribir(
                    ">",
                    fuente_pequena,
                    NEGRO,
                    x,
                    y
                )


                texto_x = (
                    x + 25
                )

            else:

                color = BLANCO

                texto_x = x


            escribir(
                opcion,
                fuente_pequena,
                color,
                texto_x,
                y
            )


        if flash > 0:

            capa = pygame.Surface(
                (
                    ANCHO,
                    ALTO
                ),
                pygame.SRCALPHA
            )


            capa.fill(
                (
                    255,
                    40,
                    40,
                    35
                )
            )


            pantalla.blit(
                capa,
                (
                    0,
                    0
                )
            )


            flash -= 1


        pygame.display.flip()


# =========================================================
# TRANSICION DE ZONA
# =========================================================

def transicion_zona(
    nombre,
    subtitulo="ASTRAEA"
):

    inicio = pygame.time.get_ticks()


    while (
        pygame.time.get_ticks()
        -
        inicio
        <
        650
    ):

        pantalla.fill(
            NEGRO
        )


        texto = fuente_titulo.render(
            nombre_legible(
                nombre
            ),
            True,
            BLANCO
        )


        pantalla.blit(
            texto,
            (
                ANCHO // 2
                -
                texto.get_width() // 2,
                285
            )
        )


        sub = fuente_mini.render(
            subtitulo,
            True,
            CIAN
        )


        pantalla.blit(
            sub,
            (
                ANCHO // 2
                -
                sub.get_width() // 2,
                350
            )
        )


        pygame.display.flip()

        reloj.tick(
            FPS
        )


# =========================================================
# REACTOR PRINCIPAL
# =========================================================

def pantalla_reactor(
    estado,
    c
):

    jugador = pygame.Rect(
        450,
        380,
        32,
        32
    )


    velocidad = 4


    mensaje = (
        "El reactor principal está "
        "fuera de servicio."
    )


    reactor_rect = pygame.Rect(
        350,
        155,
        260,
        130
    )


    consola_rect = pygame.Rect(
        390,
        330,
        180,
        55
    )


    salida_rect = pygame.Rect(
        410,
        450,
        140,
        20
    )


    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key == pygame.K_i:

                    pantalla_inventario(
                        c
                    )


                elif evento.key == pygame.K_e:


                    if cerca(
                        jugador,
                        consola_rect,
                        55
                    ):

                        reproducir_sonido(
                            sonido_terminal
                        )


                        mensaje = mundo.procesar_accion_mundo(
                            "reparar_sistemas",
                            estado,
                            c
                        )


                        reproducir_sonido(
                            sonido_reactor
                        )


                    elif cerca(
                        jugador,
                        salida_rect,
                        55
                    ):

                        resultado = narrativa.procesar_transicion(
                            estado,
                            "salir_sala",
                            c
                        )


                        if (
                            resultado
                            ==
                            "TRANSICION_RECHAZADA"
                        ):

                            mensaje = (
                                "Debes reparar "
                                "los motores."
                            )

                        else:

                            reproducir_sonido(
                                sonido_puerta
                            )


                            mundo.actualizar_pila(
                                c,
                                "salir_sala",
                                resultado
                            )


                            return resultado


                elif evento.key == pygame.K_ESCAPE:

                    resultado = narrativa.procesar_transicion(
                        estado,
                        "salir_sala",
                        c
                    )


                    if (
                        resultado
                        !=
                        "TRANSICION_RECHAZADA"
                    ):

                        mundo.actualizar_pila(
                            c,
                            "salir_sala",
                            resultado
                        )

                        return resultado


        teclas = pygame.key.get_pressed()


        if teclas[
            pygame.K_w
        ] or teclas[
            pygame.K_UP
        ]:

            jugador.y -= velocidad


        if teclas[
            pygame.K_s
        ] or teclas[
            pygame.K_DOWN
        ]:

            jugador.y += velocidad


        if teclas[
            pygame.K_a
        ] or teclas[
            pygame.K_LEFT
        ]:

            jugador.x -= velocidad


        if teclas[
            pygame.K_d
        ] or teclas[
            pygame.K_RIGHT
        ]:

            jugador.x += velocidad


        jugador.x = max(
            130,
            min(
                jugador.x,
                790
            )
        )


        jugador.y = max(
            120,
            min(
                jugador.y,
                420
            )
        )


        pantalla.fill(
            NEGRO
        )


        escribir(
            "SALA DEL REACTOR",
            fuente_titulo,
            ROJO,
            285,
            40
        )


        dibujar_ingenieria()


        motores = obtener_porcentaje_sistema(
            c,
            "motores"
        )


        color_reactor = (
            VERDE
            if motores >= 100
            else ROJO
        )


        pygame.draw.rect(
            pantalla,
            (
                25,
                30,
                35
            ),
            reactor_rect,
            border_radius=15
        )


        pygame.draw.rect(
            pantalla,
            color_reactor,
            reactor_rect,
            4,
            border_radius=15
        )


        pygame.draw.circle(
            pantalla,
            color_reactor,
            reactor_rect.center,
            30
        )


        pygame.draw.circle(
            pantalla,
            BLANCO,
            reactor_rect.center,
            10
        )


        escribir(
            "REACTOR PRINCIPAL",
            fuente_normal,
            BLANCO,
            380,
            185
        )


        dibujar_barra_sistema(
            370,
            295,
            motores,
            "ESTADO DE MOTORES"
        )


        dibujar_terminal_retro(
            consola_rect,
            motores >= 100
        )


        pygame.draw.rect(
            pantalla,
            color_reactor,
            salida_rect
        )


        escribir(
            "SALIDA",
            fuente_mini,
            BLANCO,
            salida_rect.x + 42,
            salida_rect.y - 25
        )


        dibujar_jugador(
            jugador
        )


        # APD

        pygame.draw.rect(
            pantalla,
            AZUL_OSCURO,
            (
                120,
                500,
                720,
                135
            )
        )


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                120,
                500,
                720,
                135
            ),
            2
        )


        escribir(
            "PILA APD:",
            fuente_mini,
            BLANCO,
            145,
            540
        )


        dibujar_texto_ajustado(
            " > ".join(
                c.get(
                    "pila_mundo",
                    []
                )
            ),
            fuente_mini,
            CIAN,
            245,
            540,
            550,
            2
        )


        dibujar_texto_ajustado(
            mensaje,
            fuente_mini,
            AMARILLO,
            145,
            585,
            650,
            2
        )


        pygame.display.flip()


# =========================================================
# HABITACIONES
# =========================================================

def pantalla_habitacion(
    estado,
    c,
    entrada_por_ducto=False
):

    if entrada_por_ducto:

        jugador = pygame.Rect(
            690,
            330,
            32,
            32
        )

        mensaje = (
            "Entraste por los ductos."
        )

    else:

        jugador = pygame.Rect(
            450,
            330,
            32,
            32
        )

        mensaje = (
            "Explora la habitación."
        )


    velocidad = 4

    combate_realizado = False


    config = CONFIG_SALAS.get(
        estado,
        {}
    )


    objeto_rect = config.get(
        "objeto",
        pygame.Rect(
            175,
            290,
            135,
            60
        )
    )


    terminal_rect = config.get(
        "terminal",
        pygame.Rect(
            590,
            175,
            160,
            60
        )
    )


    npc_rect = config.get(
        "npc",
        pygame.Rect(
            370,
            220,
            150,
            65
        )
    )


    salida_rect = config.get(
        "salida",
        pygame.Rect(
            410,
            450,
            140,
            20
        )
    )


    ducto_rect = config.get(
        "ducto",
        pygame.Rect(
            175,
            385,
            90,
            55
        )
    )


    reactor_rect = config.get(
        "reactor",
        pygame.Rect(
            700,
            250,
            110,
            80
        )
    )


    final_rect = config.get(
        "accion_final",
        pygame.Rect(
            565,
            315,
            190,
            60
        )
    )


    def puerta_bloqueada():

        return (

            estado
            in
            mundo.PUERTAS_INTERIORES

            and

            not mundo.puerta_desbloqueada(
                c,
                estado
            )
        )


    def salir():

        nonlocal mensaje

        # POP: el AFN regresa a la sala que queda debajo del tope de la pila.
        resultado = narrativa.procesar_transicion(
            estado,
            "volver",
            c
        )

        if resultado == "TRANSICION_RECHAZADA":
            mensaje = (
                "Desbloquea la puerta desde este lado."
                if puerta_bloqueada()
                else "La salida está bloqueada."
            )
            return None

        reproducir_sonido(
            sonido_puerta
        )

        mundo.actualizar_pila(
            c,
            "volver",
            resultado
        )

        return resultado


    while True:

        reloj.tick(
            FPS
        )


        # X99

        if (

            estado == "laboratorio_c"

            and

            not c.get(
                "alien_derrotado",
                False
            )

            and

            not combate_realizado
        ):

            combate_realizado = True


            mostrar_dialogo(
                (
                    "Movimiento hostil detectado. "
                    "La entidad X-99 se aproxima."
                ),
                "ALERTA ROJA"
            )


            detener_musica()

            reproducir_sonido(
                sonido_alarma
            )


            reproducir_musica(
                "combate.wav",
                0.45
            )


            resultado_combate = pantalla_combate(
                c,
                estado
            )


            if resultado_combate == "FIN_DERROTA":

                return (
                    "final_c_muerte"
                )


            elif resultado_combate == "FIN_VICTORIA":

                detener_musica()

                reproducir_sonido(
                    sonido_victoria
                )

                reproducir_musica(
                    "nave.wav",
                    0.30
                )

                mensaje = (
                    "X-99 ha sido neutralizado."
                )


            elif resultado_combate == "FIN_HUIDA":

                reproducir_musica(
                    "nave.wav",
                    0.30
                )

                mensaje = (
                    "Escapaste del X-99."
                )


        # EVENTOS

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key == pygame.K_ESCAPE:

                    resultado = salir()


                    if resultado is not None:

                        return resultado


                elif evento.key == pygame.K_i:

                    pantalla_inventario(
                        c
                    )


                elif evento.key == pygame.K_e:


                    # REACTOR

                    # DUCTO (PUSH): la sala nueva se abre encima de esta.
                    if (
                        estado in narrativa.SALAS_DUCTOS
                        and cerca(jugador, ducto_rect, 55)
                    ):
                        nuevo = narrativa.procesar_transicion(
                            estado,
                            "entrar_ductos",
                            c
                        )

                        if nuevo == "TRANSICION_RECHAZADA":
                            mensaje = "No puedes entrar al sistema de ductos."
                        else:
                            mundo.actualizar_pila(c, "entrar_ductos", nuevo)
                            transicion_zona(nuevo, "ACCESO POR DUCTOS")
                            salida = pantalla_habitacion(nuevo, c, True)

                            # La sala anidada regresa aqui (POP) o a un final.
                            if salida != estado:
                                return salida

                            mensaje = "Regresaste por los ductos."

                    elif (

                        estado == "ingenieria"

                        and

                        cerca(
                            jugador,
                            reactor_rect,
                            55
                        )
                    ):

                        nuevo = narrativa.procesar_transicion(
                            estado,
                            "entrar_sala_reactor",
                            c
                        )


                        if (
                            nuevo
                            ==
                            "TRANSICION_RECHAZADA"
                        ):

                            mensaje = (
                                "Necesitas el "
                                "Soplete de Plasma."
                            )

                        else:

                            reproducir_sonido(
                                sonido_puerta
                            )


                            mundo.actualizar_pila(
                                c,
                                "entrar_sala_reactor",
                                nuevo
                            )


                            transicion_zona(
                                "SALA DEL REACTOR",
                                "INGENIERÍA"
                            )


                            resultado = pantalla_reactor(
                                nuevo,
                                c
                            )


                            if resultado == "ingenieria":

                                mensaje = (
                                    "Regresaste del reactor."
                                )


                    # SOS

                    elif (

                        estado
                        ==
                        "comunicaciones"

                        and

                        cerca(
                            jugador,
                            final_rect,
                            55
                        )
                    ):

                        faltan = condiciones_sos(
                            c
                        )


                        if faltan:

                            mensaje = (
                                "SOS bloqueada. Falta: "
                                +
                                ", ".join(
                                    faltan
                                )
                            )

                        else:

                            resultado, decision = procesar_transicion_compatible(

                                estado,

                                ["enviar_sos_final"],

                                c
                            )


                            if (
                                resultado
                                !=
                                "TRANSICION_RECHAZADA"
                            ):

                                mundo.actualizar_pila(
                                    c,
                                    decision,
                                    resultado
                                )

                                return resultado


                    # CAPSULA

                    elif (

                        estado
                        ==
                        "hangar"

                        and

                        cerca(
                            jugador,
                            final_rect,
                            55
                        )
                    ):

                        if not sistema_completo(
                            c,
                            "hangar_minimo"
                        ):

                            mensaje = (
                                "La cápsula no está preparada."
                            )

                        else:

                            resultado, decision = procesar_transicion_compatible(

                                estado,

                                ["escapar_capsula"],

                                c
                            )


                            if (
                                resultado
                                !=
                                "TRANSICION_RECHAZADA"
                            ):

                                mundo.actualizar_pila(
                                    c,
                                    decision,
                                    resultado
                                )

                                return resultado


                    # OMEGA

                    elif (

                        estado
                        ==
                        "laboratorio_c"

                        and

                        cerca(
                            jugador,
                            final_rect,
                            55
                        )
                    ):

                        if (
                            "llave_maestra"
                            not in
                            c.get(
                                "inventario",
                                []
                            )
                        ):

                            mensaje = (
                                "Necesitas la Llave Maestra."
                            )

                        else:

                            resultado, decision = procesar_transicion_compatible(

                                estado,

                                ["activar_autodestruccion"],

                                c
                            )


                            if (
                                resultado
                                !=
                                "TRANSICION_RECHAZADA"
                            ):

                                mundo.actualizar_pila(
                                    c,
                                    decision,
                                    resultado
                                )

                                return resultado


                    # NPC

                    elif (

                        estado in NPCS

                        and

                        cerca(
                            jugador,
                            npc_rect,
                            55
                        )
                    ):

                        dialogo = obtener_dialogo_glc(
                            c,
                            estado
                        )


                        mostrar_dialogo(
                            dialogo,
                            NPCS[
                                estado
                            ]
                        )


                        mensaje = (
                            "Transmisión finalizada."
                        )


                    # SALIDA

                    elif cerca(
                        jugador,
                        salida_rect,
                        55
                    ):

                        if puerta_bloqueada():

                            reproducir_sonido(
                                sonido_terminal
                            )


                            mensaje = mundo.procesar_accion_mundo(
                                "desbloquear_puerta",
                                estado,
                                c
                            )

                        else:

                            resultado = salir()


                            if resultado is not None:

                                return resultado


                    # OBJETOS

                    elif cerca(
                        jugador,
                        objeto_rect,
                        55
                    ):

                        acciones = mundo.acciones_mundo(
                            estado,
                            c
                        )


                        if (
                            "buscar_objetos"
                            in acciones
                        ):

                            antes = len(
                                c.get(
                                    "inventario",
                                    []
                                )
                            )


                            mensaje = mundo.procesar_accion_mundo(
                                "buscar_objetos",
                                estado,
                                c
                            )


                            despues = len(
                                c.get(
                                    "inventario",
                                    []
                                )
                            )


                            if despues > antes:

                                reproducir_sonido(
                                    sonido_recoger
                                )


                    # TERMINAL

                    elif cerca(
                        jugador,
                        terminal_rect,
                        55
                    ):

                        reproducir_sonido(
                            sonido_terminal
                        )


                        acciones = mundo.acciones_mundo(
                            estado,
                            c
                        )


                        if (
                            "reparar_sistemas"
                            in acciones
                        ):

                            mensaje = mundo.procesar_accion_mundo(
                                "reparar_sistemas",
                                estado,
                                c
                            )

                        else:

                            mensaje = (
                                "La terminal no tiene "
                                "funciones disponibles."
                            )


        # MOVIMIENTO

        teclas = pygame.key.get_pressed()


        if teclas[
            pygame.K_w
        ] or teclas[
            pygame.K_UP
        ]:

            jugador.y -= velocidad


        if teclas[
            pygame.K_s
        ] or teclas[
            pygame.K_DOWN
        ]:

            jugador.y += velocidad


        if teclas[
            pygame.K_a
        ] or teclas[
            pygame.K_LEFT
        ]:

            jugador.x -= velocidad


        if teclas[
            pygame.K_d
        ] or teclas[
            pygame.K_RIGHT
        ]:

            jugador.x += velocidad


        jugador.x = max(
            130,
            min(
                jugador.x,
                790
            )
        )


        jugador.y = max(
            120,
            min(
                jugador.y,
                420
            )
        )


        # DIBUJO

        pantalla.fill(
            NEGRO
        )


        escribir(
            nombre_legible(
                estado
            ),
            fuente_titulo,
            AZUL,
            280,
            40
        )


        if estado == "ingenieria":

            dibujar_ingenieria()


        elif estado == "soporte_vital":

            dibujar_soporte_vital(
                c
            )


        elif estado == "laboratorio_c":

            dibujar_laboratorio(
                c
            )


        elif estado == "hangar":

            dibujar_hangar(
                c
            )


        elif estado == "comunicaciones":

            dibujar_comunicaciones(
                c
            )


        else:

            pygame.draw.rect(
                pantalla,
                PISO,
                (
                    120,
                    110,
                    720,
                    360
                )
            )


            dibujar_cuadricula(
                120,
                110,
                720,
                360
            )


        dibujar_caja_objetos(
            objeto_rect
        )


        # TERMINAL NORMAL

        if estado == "soporte_vital":

            terminal_activa = sistema_completo(
                c,
                "oxigeno"
            )


        elif estado == "hangar":

            terminal_activa = sistema_completo(
                c,
                "hangar_minimo"
            )


        elif estado == "comunicaciones":

            terminal_activa = sistema_completo(
                c,
                "comunicaciones"
            )


        else:

            terminal_activa = True


        dibujar_terminal_retro(
            terminal_rect,
            terminal_activa
        )


        # NPC

        if estado == "soporte_vital":

            dibujar_dra_voss(
                npc_rect
            )


            escribir(
                "DRA. VOSS",
                fuente_mini,
                CIAN,
                npc_rect.x + 35,
                npc_rect.bottom + 5
            )


        elif estado == "laboratorio_c":

            dibujar_unidad7(
                npc_rect
            )


            escribir(
                "UNIDAD-7",
                fuente_mini,
                CIAN,
                npc_rect.x + 37,
                npc_rect.bottom + 5
            )


        elif estado == "comunicaciones":

            pygame.draw.rect(
                pantalla,
                (
                    35,
                    100,
                    130
                ),
                npc_rect,
                border_radius=5
            )


            escribir(
                "ASTRAEA",
                fuente_mini,
                BLANCO,
                npc_rect.x + 35,
                npc_rect.y + 20
            )


        # DUCTO

        if estado in narrativa.SALAS_DUCTOS:

            dibujar_rejilla_ducto(
                ducto_rect
            )


        # ELEMENTOS ESPECIALES

        if estado == "ingenieria":

            dibujar_puerta_reactor(
                reactor_rect,
                sistema_completo(
                    c,
                    "motores"
                )
            )


        elif estado == "comunicaciones":

            dibujar_terminal_especial(
                final_rect,
                "S.O.S.",
                sos_disponible(
                    c
                )
            )


        elif estado == "laboratorio_c":

            dibujar_terminal_especial(
                final_rect,
                "OMEGA",
                (
                    "llave_maestra"
                    in
                    c.get(
                        "inventario",
                        []
                    )
                )
            )


        elif estado == "hangar":

            capsula = pygame.Rect(
                final_rect.x - 10,
                final_rect.y - 55,
                final_rect.width + 20,
                120
            )


            dibujar_capsula_escape(
                capsula,
                sistema_completo(
                    c,
                    "hangar_minimo"
                )
            )


        # SALIDA

        bloqueada = puerta_bloqueada()


        pygame.draw.rect(
            pantalla,
            (
                ROJO
                if bloqueada
                else VERDE
            ),
            salida_rect
        )


        escribir(
            (
                "BLOQUEADA"
                if bloqueada
                else "SALIDA"
            ),
            fuente_mini,
            BLANCO,
            salida_rect.x + 30,
            salida_rect.y - 25
        )


        dibujar_jugador(
            jugador
        )


        # MENSAJE DE INTERACCION

        if (

            estado == "ingenieria"

            and

            cerca(
                jugador,
                reactor_rect,
                55
            )
        ):

            escribir(
                "E - ENTRAR AL REACTOR",
                fuente_mini,
                AMARILLO,
                370,
                82
            )


        elif (

            estado == "comunicaciones"

            and

            cerca(
                jugador,
                final_rect,
                55
            )
        ):

            faltan = condiciones_sos(
                c
            )


            if faltan:

                escribir(
                    (
                        "FALTA: "
                        +
                        ", ".join(
                            faltan
                        ).upper()
                    ),
                    fuente_mini,
                    ROJO,
                    325,
                    82
                )

            else:

                escribir(
                    "E - TRANSMITIR SEÑAL SOS",
                    fuente_mini,
                    VERDE,
                    355,
                    82
                )


        elif (

            estado == "hangar"

            and

            cerca(
                jugador,
                final_rect,
                55
            )
        ):

            escribir(
                (
                    "E - LANZAR CÁPSULA"
                    if sistema_completo(
                        c,
                        "hangar_minimo"
                    )
                    else
                    "CÁPSULA NO PREPARADA"
                ),
                fuente_mini,
                (
                    VERDE
                    if sistema_completo(
                        c,
                        "hangar_minimo"
                    )
                    else ROJO
                ),
                370,
                82
            )


        elif (

            estado == "laboratorio_c"

            and

            cerca(
                jugador,
                final_rect,
                55
            )
        ):

            escribir(
                (
                    "E - ACTIVAR PROTOCOLO OMEGA"
                    if (
                        "llave_maestra"
                        in c.get(
                            "inventario",
                            []
                        )
                    )
                    else
                    "REQUIERE LLAVE MAESTRA"
                ),
                fuente_mini,
                AMARILLO,
                350,
                82
            )


        elif (

            estado in NPCS

            and

            cerca(
                jugador,
                npc_rect,
                55
            )
        ):

            escribir(
                "E - HABLAR",
                fuente_pequena,
                AMARILLO,
                410,
                82
            )


        elif cerca(
            jugador,
            salida_rect,
            55
        ):

            escribir(
                (
                    "E - DESBLOQUEAR PUERTA"
                    if bloqueada
                    else
                    "E - VOLVER AL PASILLO"
                ),
                fuente_mini,
                AMARILLO,
                365,
                82
            )


        elif cerca(
            jugador,
            objeto_rect,
            55
        ):

            escribir(
                "E - BUSCAR OBJETOS",
                fuente_mini,
                AMARILLO,
                380,
                82
            )


        elif cerca(
            jugador,
            terminal_rect,
            55
        ):

            escribir(
                "E - USAR TERMINAL",
                fuente_mini,
                AMARILLO,
                385,
                82
            )


        dibujar_hud(
            c,
            estado,
            mensaje
        )


        pygame.display.flip()


# =========================================================
# FINAL
# =========================================================

def pantalla_final(
    estado
):

    datos = {

        "final_a_victoria": (

            "FINAL A - RESCATE",

            (
                "La señal SOS fue recibida. "
                "Una nave de rescate se aproxima "
                "a Astraea."
            ),

            VERDE
        ),


        "final_b_escape": (

            "FINAL B - CÁPSULA",

            (
                "Escapaste de Astraea utilizando "
                "la cápsula de emergencia."
            ),

            CIAN
        ),


        "final_c_muerte": (

            "FINAL C - MUERTE",

            (
                "X-99 logró acabar con "
                "el último tripulante."
            ),

            ROJO
        ),


        "final_d_autodestruccion": (

            "FINAL D - AUTODESTRUCCIÓN",

            (
                "El Protocolo Omega fue activado. "
                "Astraea desaparece junto al X-99."
            ),

            NARANJA
        )
    }


    titulo, descripcion, color = datos.get(

        estado,

        (
            "FINAL",
            nombre_legible(
                estado
            ),
            BLANCO
        )
    )


    detener_musica()


    if estado in (

        "final_a_victoria",
        "final_b_escape"

    ):

        reproducir_sonido(
            sonido_victoria
        )


    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (

                evento.type
                ==
                pygame.KEYDOWN

                and

                evento.key in (

                    pygame.K_RETURN,
                    pygame.K_ESCAPE

                )
            ):

                return


        dibujar_fondo_menu()


        escribir(
            titulo,
            fuente_titulo,
            color,
            190,
            175
        )


        dibujar_texto_ajustado(
            descripcion,
            fuente_normal,
            BLANCO,
            220,
            290,
            530,
            5,
            28
        )


        escribir(
            "ESTADO DE ACEPTACIÓN DEL AFN",
            fuente_mini,
            AMARILLO,
            340,
            455
        )


        escribir(
            "ENTER / ESC - VOLVER",
            fuente_pequena,
            GRIS_CLARO,
            370,
            515
        )


        pygame.display.flip()


# =========================================================
# JUEGO PRINCIPAL
# =========================================================

def jugar():

    reproducir_musica(
        "nave.wav",
        0.30
    )


    c = mundo.nuevo_mundo()


    estado = narrativa.ESTADO_INICIAL


    resultado = narrativa.procesar_transicion(
        estado,
        "explorar_pasillo",
        c
    )


    if (
        resultado
        !=
        "TRANSICION_RECHAZADA"
    ):

        mundo.actualizar_pila(
            c,
            "explorar_pasillo",
            resultado
        )

        estado = resultado


    jugador = pygame.Rect(
        450,
        310,
        32,
        32
    )


    velocidad = 4


    mensaje = (
        "Busca la tarjeta. "
        "Abre Ingeniería y Soporte Vital."
    )


    puerta_ingenieria = pygame.Rect(
        360,
        80,
        110,
        22
    )


    puerta_hangar = pygame.Rect(
        680,
        80,
        100,
        22
    )


    puerta_soporte = pygame.Rect(
        100,
        250,
        22,
        100
    )


    puerta_lab = pygame.Rect(
        838,
        250,
        22,
        100
    )


    puerta_comunicaciones = pygame.Rect(
        520,
        458,
        140,
        22
    )


    tarjeta_rect = pygame.Rect(
        245,
        335,
        25,
        16
    )


    ducto_rect = pygame.Rect(
        175,
        400,
        105,
        45
    )


    puertas = [

        (
            puerta_ingenieria,
            "ir_ingenieria",
            "Ingeniería"
        ),

        (
            puerta_soporte,
            "ir_soporte_vital",
            "Soporte Vital"
        ),

        (
            puerta_lab,
            "ir_laboratorio",
            "Laboratorio C"
        ),

        (
            puerta_hangar,
            "ir_hangar",
            "Hangar"
        ),

        (
            puerta_comunicaciones,
            "ir_comunicaciones",
            "Comunicaciones"
        )
    ]


    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key == pygame.K_ESCAPE:

                    return


                elif evento.key == pygame.K_i:

                    pantalla_inventario(
                        c
                    )


                elif evento.key == pygame.K_e:


                    # TARJETA

                    if (

                        "tarjeta_acceso"
                        not in
                        c[
                            "inventario"
                        ]

                        and

                        cerca(
                            jugador,
                            tarjeta_rect
                        )
                    ):

                        mensaje = mundo.buscar_objeto(
                            "pasillo_principal",
                            c
                        )


                        reproducir_sonido(
                            sonido_recoger
                        )


                        continue


                    # DUCTO

                    if cerca(
                        jugador,
                        ducto_rect,
                        45
                    ):

                        nuevo = narrativa.procesar_transicion(
                            estado,
                            "entrar_ductos",
                            c
                        )


                        if (
                            nuevo
                            ==
                            "TRANSICION_RECHAZADA"
                        ):

                            mensaje = (
                                "No puedes entrar "
                                "al sistema de ductos."
                            )

                        else:

                            mundo.actualizar_pila(
                                c,
                                "entrar_ductos",
                                nuevo
                            )


                            transicion_zona(
                                nuevo,
                                "ACCESO POR DUCTOS"
                            )


                            salida = pantalla_habitacion(
                                nuevo,
                                c,
                                True
                            )


                            if (
                                salida
                                and
                                str(
                                    salida
                                ).startswith(
                                    "final_"
                                )
                            ):

                                pantalla_final(
                                    salida
                                )

                                return


                            estado = (
                                salida
                                if salida
                                else
                                "pasillo_principal"
                            )


                            jugador.center = (
                                460,
                                300
                            )


                            mensaje = (
                                "Regresaste al Pasillo Principal."
                            )


                        continue


                    # PUERTAS

                    usada = False


                    for (
                        rect,
                        decision,
                        nombre
                    ) in puertas:


                        if not cerca(
                            jugador,
                            rect
                        ):

                            continue


                        usada = True


                        nuevo = narrativa.procesar_transicion(
                            estado,
                            decision,
                            c
                        )


                        if (
                            nuevo
                            ==
                            "TRANSICION_RECHAZADA"
                        ):

                            if decision in (

                                "ir_ingenieria",
                                "ir_soporte_vital"

                            ):

                                mensaje = (
                                    nombre
                                    +
                                    " requiere la Tarjeta de Acceso."
                                )

                            else:

                                mensaje = (
                                    nombre
                                    +
                                    " está bloqueado. "
                                    "Usa los ductos."
                                )

                        else:

                            reproducir_sonido(
                                sonido_puerta
                            )


                            mundo.actualizar_pila(
                                c,
                                decision,
                                nuevo
                            )


                            transicion_zona(
                                nuevo
                            )


                            salida = pantalla_habitacion(
                                nuevo,
                                c,
                                False
                            )


                            if (
                                salida
                                and
                                str(
                                    salida
                                ).startswith(
                                    "final_"
                                )
                            ):

                                pantalla_final(
                                    salida
                                )

                                return


                            estado = (
                                salida
                                if salida
                                else
                                "pasillo_principal"
                            )


                            jugador.center = (
                                460,
                                300
                            )


                            mensaje = (
                                "Regresaste al Pasillo Principal."
                            )


                        break


                    if not usada:

                        mensaje = (
                            "No hay nada cerca "
                            "con lo que interactuar."
                        )


        # MOVIMIENTO

        teclas = pygame.key.get_pressed()


        if teclas[
            pygame.K_w
        ] or teclas[
            pygame.K_UP
        ]:

            jugador.y -= velocidad


        if teclas[
            pygame.K_s
        ] or teclas[
            pygame.K_DOWN
        ]:

            jugador.y += velocidad


        if teclas[
            pygame.K_a
        ] or teclas[
            pygame.K_LEFT
        ]:

            jugador.x -= velocidad


        if teclas[
            pygame.K_d
        ] or teclas[
            pygame.K_RIGHT
        ]:

            jugador.x += velocidad


        jugador.x = max(
            110,
            min(
                jugador.x,
                818
            )
        )


        jugador.y = max(
            100,
            min(
                jugador.y,
                438
            )
        )


        # DIBUJO

        pantalla.fill(
            NEGRO
        )


        escribir(
            "ASTRAEA // PASILLO PRINCIPAL",
            fuente_pequena,
            CIAN,
            110,
            40
        )


        dibujar_piso_pasillo()


        pygame.draw.rect(
            pantalla,
            AZUL,
            (
                100,
                80,
                760,
                400
            ),
            3
        )


        tiene_tarjeta = (
            "tarjeta_acceso"
            in
            c[
                "inventario"
            ]
        )


        lab_abierto = mundo.puerta_desbloqueada(
            c,
            "laboratorio_c"
        )


        hangar_abierto = mundo.puerta_desbloqueada(
            c,
            "hangar"
        )


        comunicaciones_abierto = mundo.puerta_desbloqueada(
            c,
            "comunicaciones"
        )


        dibujar_puerta(
            puerta_ingenieria,
            "INGENIERÍA",
            tiene_tarjeta
        )


        dibujar_puerta(
            puerta_soporte,
            "SOPORTE",
            tiene_tarjeta
        )


        dibujar_puerta(
            puerta_hangar,
            "HANGAR",
            hangar_abierto
        )


        dibujar_puerta(
            puerta_lab,
            "LAB C",
            lab_abierto
        )


        dibujar_puerta(
            puerta_comunicaciones,
            "COMUNICACIONES",
            comunicaciones_abierto
        )


        dibujar_rejilla_ducto(
            ducto_rect
        )


        escribir(
            "DUCTO",
            fuente_mini,
            BLANCO,
            197,
            377
        )


        if not tiene_tarjeta:

            pygame.draw.rect(
                pantalla,
                AMARILLO,
                tarjeta_rect
            )


            escribir(
                "TARJETA",
                fuente_mini,
                AMARILLO,
                220,
                357
            )


        dibujar_jugador(
            jugador
        )


        if (

            not tiene_tarjeta

            and

            cerca(
                jugador,
                tarjeta_rect
            )
        ):

            escribir(
                "E - RECOGER TARJETA",
                fuente_pequena,
                AMARILLO,
                360,
                55
            )


        elif cerca(
            jugador,
            ducto_rect,
            45
        ):

            escribir(
                "E - ENTRAR A LOS DUCTOS (AFN)",
                fuente_pequena,
                AMARILLO,
                330,
                55
            )


        elif any(

            cerca(
                jugador,
                rect
            )

            for (
                rect,
                _,
                _
            )

            in puertas
        ):

            escribir(
                "E - INTERACTUAR CON PUERTA",
                fuente_pequena,
                AMARILLO,
                345,
                55
            )


        dibujar_hud(
            c,
            "pasillo_principal",
            mensaje
        )


        pygame.display.flip()


# =========================================================
# INTEGRANTES
# =========================================================

def pantalla_integrantes():

    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (

                evento.type
                ==
                pygame.KEYDOWN

                and

                evento.key in (

                    pygame.K_ESCAPE,
                    pygame.K_RETURN

                )
            ):

                return


        dibujar_fondo_menu()


        escribir(
            "INTEGRANTES",
            fuente_titulo,
            AZUL,
            330,
            100
        )


        integrantes = [

            "Daniel - AFN narrativo",

            "Marlyn - APD e inventario",

            "Josue - Gramática GLC",

            "Danna - Mundo y combate",

            "Dylan - Integración y QA"
        ]


        for indice, nombre in enumerate(
            integrantes
        ):

            escribir(
                nombre,
                fuente_normal,
                BLANCO,
                250,
                220 + indice * 50
            )


        pygame.display.flip()


# =========================================================
# CREDITOS
# =========================================================

def pantalla_creditos():

    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (

                evento.type
                ==
                pygame.KEYDOWN

                and

                evento.key in (

                    pygame.K_ESCAPE,
                    pygame.K_RETURN

                )
            ):

                return


        dibujar_fondo_menu()


        escribir(
            "CRÉDITOS",
            fuente_titulo,
            AZUL,
            365,
            100
        )


        escribir(
            "Proyecto Final",
            fuente_normal,
            BLANCO,
            390,
            210
        )


        escribir(
            "Autómatas y Lenguajes Formales",
            fuente_normal,
            BLANCO,
            280,
            255
        )


        escribir(
            "Python + pygame-ce",
            fuente_normal,
            VERDE,
            350,
            320
        )


        escribir(
            "AFN + APD + GLC + Combate",
            fuente_normal,
            AMARILLO,
            300,
            365
        )


        pygame.display.flip()


# =========================================================
# MENU PRINCIPAL
# =========================================================

def pantalla_inicio():

    reproducir_musica(
        "menu.wav",
        0.40
    )


    opciones = [

        "INICIAR",

        "INTEGRANTES",

        "CRÉDITOS",

        "SALIR"
    ]


    seleccionado = 0


    while True:

        reloj.tick(
            FPS
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if evento.type == pygame.KEYDOWN:


                if evento.key == pygame.K_DOWN:

                    seleccionado = (
                        seleccionado + 1
                    ) % len(opciones)


                elif evento.key == pygame.K_UP:

                    seleccionado = (
                        seleccionado - 1
                    ) % len(opciones)


                elif evento.key == pygame.K_RETURN:


                    if seleccionado == 0:

                        jugar()


                        reproducir_musica(
                            "menu.wav",
                            0.40
                        )


                    elif seleccionado == 1:

                        pantalla_integrantes()


                    elif seleccionado == 2:

                        pantalla_creditos()


                    elif seleccionado == 3:

                        pygame.quit()

                        sys.exit()


        dibujar_fondo_menu()


        escribir(
            "PROTOCOLO OMEGA",
            fuente_titulo,
            AZUL,
            270,
            110
        )


        escribir(
            "FUGA ESPACIAL",
            fuente_titulo,
            ROJO,
            300,
            170
        )


        for indice, opcion in enumerate(
            opciones
        ):

            y = (
                300
                +
                indice * 55
            )


            if (
                indice
                ==
                seleccionado
            ):

                pygame.draw.rect(
                    pantalla,
                    AZUL,
                    (
                        300,
                        y - 7,
                        360,
                        43
                    ),
                    border_radius=5
                )


                color = NEGRO


                escribir(
                    ">",
                    fuente_menu,
                    NEGRO,
                    320,
                    y
                )

            else:

                pygame.draw.rect(
                    pantalla,
                    GRIS,
                    (
                        300,
                        y - 7,
                        360,
                        43
                    ),
                    1,
                    border_radius=5
                )


                color = BLANCO


            escribir(
                opcion,
                fuente_menu,
                color,
                370,
                y
            )


        escribir(
            "FLECHAS: mover menú     ENTER: seleccionar",
            fuente_pequena,
            BLANCO,
            280,
            555
        )


        pygame.display.flip()


# =========================================================
# INICIO
# =========================================================

if __name__ == "__main__":

    pantalla_inicio()