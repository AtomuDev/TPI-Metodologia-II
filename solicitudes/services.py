from dataclasses import dataclass

from .modelo import (Estado, Prioridad, ESTADOS_FINALES, ESTADOS_ABIERTOS,
                     ESTADOS_CON_RESPONSABLE, PLAZO_DIAS, ErrorDeNegocio)


def _encontrar(coleccion, clave, valor):
    for elemento in coleccion:
        if elemento[clave] == valor:
            return elemento
    return None


@dataclass
class Reporte:
    total: int
    por_estado: dict
    por_prioridad_abiertas: dict
    por_responsable: list
    sin_asignar: int
    alta_sin_resolver: int


class ServicioSolicitudes:
    def __init__(self, repositorio):
        self._repositorio = repositorio
        self._datos = repositorio.cargar()

    # --- consultas ---
    def hay_solicitudes(self):
        return len(self._datos["solicitudes"]) > 0

    def listar_responsables(self):
        return list(self._datos["responsables"])

    def obtener_solicitud(self, id_solicitud):
        solicitud = _encontrar(self._datos["solicitudes"], "id", id_solicitud)
        if solicitud is None:
            raise ErrorDeNegocio("solicitud no encontrada")
        return solicitud

    def obtener_solicitud_abierta(self, id_solicitud):
        solicitud = self.obtener_solicitud(id_solicitud)
        if solicitud["estado"] in ESTADOS_FINALES:
            raise ErrorDeNegocio("la solicitud ya está cerrada")
        return solicitud

    def obtener_responsable(self, id_responsable):
        responsable = _encontrar(self._datos["responsables"], "id", id_responsable)
        if responsable is None:
            raise ErrorDeNegocio("responsable no encontrado")
        return responsable

    def nombre_estudiante(self, legajo):
        estudiante = _encontrar(self._datos["estudiantes"], "legajo", legajo)
        return "" if estudiante is None else estudiante["nombre"]

    def nombre_responsable(self, id_responsable):
        responsable = _encontrar(self._datos["responsables"], "id", id_responsable)
        return "sin asignar" if responsable is None else responsable["nombre"]

    def plazo_dias(self, solicitud):
        return PLAZO_DIAS[solicitud["prioridad"]]

    def filtrar(self, criterio, valor):
        if criterio is None:
            return list(self._datos["solicitudes"])
        return [s for s in self._datos["solicitudes"] if s[criterio] == valor]

    # --- comandos ---
    def registrar_solicitud(self, nueva):
        estudiante = _encontrar(self._datos["estudiantes"], "legajo", nueva.legajo)
        if estudiante is not None and estudiante["nombre"].lower() != nueva.nombre.lower():
            raise ErrorDeNegocio(
                f"el legajo {nueva.legajo} ya está registrado a nombre de {estudiante['nombre']}")
        if estudiante is None:
            self._datos["estudiantes"].append({"legajo": nueva.legajo, "nombre": nueva.nombre})
        solicitud = {
            "id": self._datos["siguiente_id"],
            "legajo": nueva.legajo,
            "tipo": nueva.tipo,
            "prioridad": nueva.prioridad,
            "descripcion": nueva.descripcion,
            "estado": Estado.PENDIENTE,
            "responsable_id": None,
        }
        self._datos["siguiente_id"] += 1
        self._datos["solicitudes"].append(solicitud)
        self._repositorio.guardar(self._datos)
        return solicitud["id"]

    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.obtener_solicitud_abierta(id_solicitud)
        if nuevo_estado == solicitud["estado"]:
            raise ErrorDeNegocio("la solicitud ya está en ese estado")
        if nuevo_estado in ESTADOS_CON_RESPONSABLE and solicitud["responsable_id"] is None:
            raise ErrorDeNegocio(f"debe asignar un responsable antes de pasar a {nuevo_estado}")
        solicitud["estado"] = nuevo_estado
        self._repositorio.guardar(self._datos)

    def asignar_responsable(self, id_solicitud, id_responsable):
        solicitud = self.obtener_solicitud_abierta(id_solicitud)
        responsable = self.obtener_responsable(id_responsable)
        solicitud["responsable_id"] = responsable["id"]
        self._repositorio.guardar(self._datos)
        return responsable

    def generar_reporte(self):
        solicitudes = self._datos["solicitudes"]
        abiertas = [s for s in solicitudes if s["estado"] in ESTADOS_ABIERTOS]
        por_prioridad = {p: sum(1 for s in abiertas if s["prioridad"] == p) for p in Prioridad}
        return Reporte(
            total=len(solicitudes),
            por_estado={e: sum(1 for s in solicitudes if s["estado"] == e) for e in Estado},
            por_prioridad_abiertas=por_prioridad,
            por_responsable=[
                (r["nombre"], sum(1 for s in solicitudes if s["responsable_id"] == r["id"]))
                for r in self._datos["responsables"]],
            sin_asignar=sum(1 for s in solicitudes if s["responsable_id"] is None),
            alta_sin_resolver=por_prioridad[Prioridad.ALTA],
        )
