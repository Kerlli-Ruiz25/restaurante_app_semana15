import json
from pathlib import Path

class ArchivoServicio:
    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def leer(self):
        if not self.ruta.exists():
            return []
        with self.ruta.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar(self, datos):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
