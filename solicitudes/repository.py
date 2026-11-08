import json


class ErrorPersistencia(Exception):
    pass


def _datos_iniciales():
    return {
        "siguiente_id": 1,
        "estudiantes": [],
        "responsables": [
            {"id": 1, "nombre": "Ana Pérez", "area": "Alumnado"},
            {"id": 2, "nombre": "Luis Gómez", "area": "Secretaría Académica"},
            {"id": 3, "nombre": "Marta Díaz", "area": "Bedelía"},
        ],
        "solicitudes": [],
    }


class RepositorioJSON:
    def __init__(self, ruta):
        self._ruta = ruta

    def cargar(self):
        try:
            with open(self._ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return _datos_iniciales()
        except (json.JSONDecodeError, OSError):
            raise ErrorPersistencia(self._ruta) from None

    def guardar(self, datos):
        with open(self._ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
