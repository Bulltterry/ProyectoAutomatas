import os

BASE = os.path.dirname(
    os.path.abspath(__file__)
)

archivo = os.path.join(
    BASE,
    "assets",
    "sonidos",
    "puerta.wav"
)

with open(archivo, "rb") as f:
    datos = f.read(20)

print("Primeros bytes:")
print(datos)