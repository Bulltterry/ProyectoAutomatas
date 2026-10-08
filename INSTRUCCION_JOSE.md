# Integrante 3 — José

## Rol
Diseñador de gramática — GLC

## Contexto del proyecto
José desarrollará el sistema que genera las misiones de reparación y los diálogos de los personajes.

## ¿Qué debe realizar?
- Diseñar una gramática libre de contexto en notación BNF.
- Crear reglas para generar misiones como reparar el reactor, restablecer el oxígeno y activar las comunicaciones.
- Generar mensajes y diálogos de la computadora de la nave.
- Implementar un generador que aplique las producciones gramaticales.
- Documentar ejemplos de derivaciones válidas.

## Archivo principal
- `gramatica.py`

## Entregable
Gramática BNF, generador funcional de misiones y diálogos, y ejemplos de derivaciones.

## Conexión con este proyecto
Este módulo ya forma parte del sistema narrativo del juego `Astrea`, donde la gramática permite:
- crear misiones secundarias,
- generar mensajes de error y alertas,
- producir diálogos de NPCs,
- validar combinaciones de frases coherentes con la historia.

La implementación actual en `gramatica.py` cumple esta instrucción, y queda conectada directamente con `narrativa.py`, `mundo.py` y `main.py` para sostener la lógica del juego.
