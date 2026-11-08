from dataclasses import dataclass
from enum import StrEnum


class Tipo(StrEnum):
    CERTIFICADO = "certificado"
    EQUIVALENCIA = "equivalencia"
    BAJA = "baja"
    OTRO = "otro"


class Prioridad(StrEnum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Estado(StrEnum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    RECHAZADA = "rechazada"


ESTADOS_FINALES = (Estado.RESUELTA, Estado.RECHAZADA)
ESTADOS_ABIERTOS = (Estado.PENDIENTE, Estado.EN_PROCESO)
ESTADOS_CON_RESPONSABLE = (Estado.EN_PROCESO, Estado.RESUELTA)
PLAZO_DIAS = {Prioridad.ALTA: 2, Prioridad.MEDIA: 5, Prioridad.BAJA: 10}


@dataclass(frozen=True)
class NuevaSolicitud:
    nombre: str
    legajo: str
    tipo: Tipo
    prioridad: Prioridad
    descripcion: str


class ErrorDeAplicacion(Exception):
    pass


class ErrorDeValidacion(ErrorDeAplicacion):
    pass


class ErrorDeNegocio(ErrorDeAplicacion):
    pass
