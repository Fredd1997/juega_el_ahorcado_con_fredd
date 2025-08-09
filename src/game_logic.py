
import random
from config import PALABRAS

def obtener_palabra_aleatoria(idioma, categoria):
    return random.choice(PALABRAS[idioma][categoria])

def ocultar_palabra(palabra):
    return "_ " * len(palabra)

