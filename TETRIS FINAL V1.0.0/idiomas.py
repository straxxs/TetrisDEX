import json
import os

IDIOMAS = {
    1: "es",
    2: "en",
    3: "fr",
    4: "pt",
    5: "jp",
    6: "cn",
    7: "it",
    8: "ru",
    9: "de",
    10: "ab"
}


def cargar_idioma(idioma):

    codigo = IDIOMAS.get(idioma, "es")

    ruta = os.path.join("idiomas", f"{codigo}.json")

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)