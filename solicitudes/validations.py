from .modelo import Tipo, Prioridad, NuevaSolicitud, ErrorDeValidacion


def parsear_entero_positivo(texto, mensaje_error):
    if not texto.isdecimal() or int(texto) <= 0:
        raise ErrorDeValidacion(mensaje_error)
    return int(texto)


def parsear_legajo(texto):
    return str(parsear_entero_positivo(texto, "el legajo debe ser un número positivo"))


def parsear_enum(clase, texto, mensaje_error):
    try:
        return clase(texto)
    except ValueError:
        raise ErrorDeValidacion(mensaje_error) from None


def construir_nueva_solicitud(nombre, legajo, tipo, prioridad, descripcion):
    if nombre == "":
        raise ErrorDeValidacion("el nombre es obligatorio")
    legajo = parsear_legajo(legajo)
    tipo = parsear_enum(Tipo, tipo, "tipo inválido")
    prioridad = parsear_enum(Prioridad, prioridad, "prioridad inválida")
    if descripcion == "":
        raise ErrorDeValidacion("la descripción es obligatoria")
    return NuevaSolicitud(nombre, legajo, tipo, prioridad, descripcion)
