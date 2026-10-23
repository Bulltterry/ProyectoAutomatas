import random
import re


MAX_PROF = 3


GLC = {

    "<ERROR_TRANSICION>": [
        [
            "[Astraea]:",
            "<SUJETO>",
            "<VERBO>",
            "<PROBLEMA>"
        ]
    ],

    "<ALERTA_ALIEN>": [
        [
            "[ALERTA ROJA]:",
            "<SUJETO>",
            "<VERBO>",
            "<EVENTO>"
        ]
    ],

    "<ALERTA_ALIEN_GRAFICA>": [
        ["Movimiento hostil detectado. La entidad X-99 se aproxima."]
    ],

    "<SUJETO>": [
        ["El sistema central"],
        ["La IA Astraea"],
        ["El monitor de bioseguridad"]
    ],

    "<VERBO>": [
        ["informa que"],
        ["advierte que"],
        ["detecta que"]
    ],

    "<PROBLEMA>": [
        [
            "faltan credenciales de acceso",
            "."
        ],
        [
            "las puertas están bloqueadas",
            "."
        ],
        [
            "el protocolo de seguridad lo impide",
            "."
        ],
    ],

    "<EVENTO>": [
        [
            "movimiento en los ductos del techo",
            "."
        ],
        [
            "una anomalía térmica acercándose",
            "."
        ],
        [
            "una brecha de contención cercana",
            "."
        ],
    ],

    "<MENSAJE_COMBATE>": [
        ["<COMBATE_INICIO>"],
        ["<COMBATE_FALLO_ATAQUE>"],
        ["<COMBATE_GOLPE_CRITICO>"],
        ["<COMBATE_IMPACTO>"],
        ["<COMBATE_ESQUIVA_PREPARADA>"],
        ["<COMBATE_DEFENSA>"],
        ["<COMBATE_OBJETO_INVALIDO>"],
        ["<COMBATE_OBJETO_NO_DISPONIBLE>"],
        ["<COMBATE_LANZAR_OBJETO>"],
        ["<COMBATE_ENTORNO_USADO>"],
        ["<COMBATE_SIN_ENTORNO>"],
        ["<COMBATE_USAR_ENTORNO>"],
        ["<COMBATE_X99_ATURDIDO>"],
        ["<COMBATE_TURNO_PERDIDO>"],
        ["<COMBATE_HUIDA_EXITOSA>"],
        ["<COMBATE_HUIDA_FALLIDA>"],
        ["<COMBATE_ATAQUE_ESQUIVADO>"],
        ["<COMBATE_ATAQUE_X99>"],
        ["<COMBATE_FALLO_X99>"],
        ["<COMBATE_OPCION_INVALIDA>"],
        ["<COMBATE_SIN_OBJETOS>"],
        ["<COMBATE_RESULTADO_HUIDA>"],
        ["<COMBATE_RESULTADO_VICTORIA>"],
        ["<COMBATE_RESULTADO_HUIDA_GRAFICA>"],
        ["<COMBATE_RESULTADO_VICTORIA_GRAFICA>"],
    ],

    "<COMBATE_INICIO>": [
        ["El X-99 emerge de las sombras."]
    ],
    "<COMBATE_FALLO_ATAQUE>": [
        ["El disparo falla."]
    ],
    "<COMBATE_GOLPE_CRITICO>": [
        ["¡Golpe crítico! X-99 recibe", "{dano}", "de daño."]
    ],
    "<COMBATE_IMPACTO>": [
        ["Impactas al X-99. Daño:", "{dano}", "."]
    ],
    "<COMBATE_ESQUIVA_PREPARADA>": [
        ["Te preparas para esquivar."]
    ],
    "<COMBATE_DEFENSA>": [
        ["Intentas defenderte."]
    ],
    "<COMBATE_OBJETO_INVALIDO>": [
        ["Ese objeto no puede lanzarse."]
    ],
    "<COMBATE_OBJETO_NO_DISPONIBLE>": [
        ["No tienes ese objeto."]
    ],
    "<COMBATE_LANZAR_OBJETO>": [
        ["Lanzas", "{objeto}", "y causas", "{dano}", "de daño."]
    ],
    "<COMBATE_ENTORNO_USADO>": [
        ["Ya utilizaste el entorno de esta habitación."]
    ],
    "<COMBATE_SIN_ENTORNO>": [
        ["No hay nada útil que puedas usar aquí."]
    ],
    "<COMBATE_USAR_ENTORNO>": [
        ["{entorno}:", "{dano}", "de daño."]
    ],
    "<COMBATE_X99_ATURDIDO>": [
        ["¡X-99 queda aturdido!"]
    ],
    "<COMBATE_TURNO_PERDIDO>": [
        ["X-99 está aturdido y pierde su turno."]
    ],
    "<COMBATE_HUIDA_EXITOSA>": [
        ["Consigues escapar del X-99."]
    ],
    "<COMBATE_HUIDA_FALLIDA>": [
        ["Intentas escapar, pero X-99 bloquea tu camino."]
    ],
    "<COMBATE_ATAQUE_ESQUIVADO>": [
        ["¡Esquivas el ataque del X-99!"]
    ],
    "<COMBATE_ATAQUE_X99>": [
        ["X-99 te golpea. Pierdes", "{dano}", "HP."]
    ],
    "<COMBATE_FALLO_X99>": [
        ["X-99 falla su ataque."]
    ],
    "<COMBATE_OPCION_INVALIDA>": [
        ["Opción inválida."]
    ],
    "<COMBATE_SIN_OBJETOS>": [
        ["No tienes objetos arrojables."]
    ],
    "<COMBATE_RESULTADO_HUIDA>": [
        ["Lograste romper el contacto. Puedes continuar explorando."]
    ],
    "<COMBATE_RESULTADO_VICTORIA>": [
        ["La amenaza X-99 ha sido neutralizada."]
    ],
    "<COMBATE_RESULTADO_HUIDA_GRAFICA>": [
        ["Escapaste del X-99."]
    ],
    "<COMBATE_RESULTADO_VICTORIA_GRAFICA>": [
        ["X-99 ha sido neutralizado."]
    ],
