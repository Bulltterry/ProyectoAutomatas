# Protocolo Omega: Fuga Espacial

Proyecto R (RPG narrativo) de Autómatas y Lenguajes Formales.

## Requisitos

- Python 3.12+
- `pip install pygame` (solo para la interfaz gráfica)

## Cómo ejecutar

| Comando | Qué hace |
|---|---|
| `python interfaz.py` | Juego con interfaz gráfica |
| `python main.py` | Juego en consola (menú) |
| `python juego.py 42` | Partida en consola con semilla fija (reproducible) |
| `python alcanzabilidad.py` | Prueba de alcanzabilidad de los 4 finales |
| `python gramatica.py` | Imprime la BNF y derivaciones de ejemplo |
| `python combate.py` | Autoprueba del autómata de combate |

## Arquitectura (4 capas del PDF)

| Capa | Modelo | Archivo |
|---|---|---|
| Motor narrativo | AFN | `narrativa.py` |
| Inventario y mundo | Autómata de pila | `mundo.py` |
| Diálogos y misiones | GLC (BNF) | `gramatica.py` |
| Combate | Autómata probabilístico | `combate.py` |

Documentación formal: carpeta [`docs/`](docs/).
