from .modelo import Tipo, Prioridad, Estado, ErrorDeAplicacion, ErrorDeValidacion
from .validaciones import (parsear_entero_positivo, parsear_legajo, parsear_enum,
                           construir_nueva_solicitud)

CRITERIOS = ("estado", "prioridad", "tipo", "legajo")
_ENUM_POR_CRITERIO = {
    "estado": (Estado, "estado inválido"),
    "prioridad": (Prioridad, "prioridad inválida"),
    "tipo": (Tipo, "tipo inválido"),
}


class ConsolaSolicitudes:
    def __init__(self, servicio):
        self._servicio = servicio

    def ejecutar(self):
        acciones = {"1": self._registrar, "2": self._cambiar_estado,
                    "3": self._asignar, "4": self._buscar, "5": self._reporte}
        while True:
            print("")
            print("=== Gestión de Solicitudes Académicas ===")
            print("1. Registrar solicitud")
            print("2. Cambiar estado")
            print("3. Asignar responsable")
            print("4. Buscar / filtrar")
            print("5. Reporte")
            print("0. Salir")
            try:
                opcion = input("Opción: ").strip()
                if opcion == "0":
                    print("Hasta luego")
                    break
                accion = acciones.get(opcion)
                if accion is None:
                    print("Opción inválida")
                else:
                    accion()
            except (KeyboardInterrupt, EOFError):
                print("\nEntrada interrumpida. Hasta luego")
                break

    def _registrar(self):
        nombre = input("Nombre del estudiante: ").strip()
        legajo = input("Legajo: ").strip()
        tipo = input(f"Tipo ({'/'.join(Tipo)}): ").strip().lower()
        prioridad = input(f"Prioridad ({'/'.join(Prioridad)}): ").strip().lower()
        descripcion = input("Descripción: ").strip()
        try:
            nueva = construir_nueva_solicitud(nombre, legajo, tipo, prioridad, descripcion)
            nuevo_id = self._servicio.registrar_solicitud(nueva)
        except ErrorDeAplicacion as error:
            print(f"Error: {error}")
            return
        print(f"Solicitud #{nuevo_id} registrada")

    def _pedir_solicitud_abierta(self, mensaje_id_invalido):
        texto = input("ID de solicitud: ").strip()
        id_solicitud = parsear_entero_positivo(texto, mensaje_id_invalido)
        return self._servicio.obtener_solicitud_abierta(id_solicitud)

    def _cambiar_estado(self):
        try:
            solicitud = self._pedir_solicitud_abierta("ID inválido")
            print(f"Estado actual: {solicitud['estado']}")
            texto = input(f"Nuevo estado ({'/'.join(Estado)}): ").strip().lower()
            nuevo_estado = parsear_enum(Estado, texto, "estado inválido")
            self._servicio.cambiar_estado(solicitud["id"], nuevo_estado)
        except ErrorDeAplicacion as error:
            print(f"Error: {error}")
            return
        print(f"Solicitud #{solicitud['id']} ahora está {nuevo_estado}")

    def _asignar(self):
        if not self._servicio.hay_solicitudes():
            print("Error: no hay solicitudes registradas")
            return
        print("Responsables disponibles:")
        for r in self._servicio.listar_responsables():
            print(f" {r['id']} - {r['nombre']} ({r['area']})")
        try:
            solicitud = self._pedir_solicitud_abierta("ID de solicitud inválido")
            texto = input("ID de responsable: ").strip()
            id_responsable = parsear_entero_positivo(texto, "ID de responsable inválido")
            responsable = self._servicio.asignar_responsable(solicitud["id"], id_responsable)
        except ErrorDeAplicacion as error:
            print(f"Error: {error}")
            return
        print(f"Solicitud #{solicitud['id']} asignada a {responsable['nombre']}")

    def _pedir_criterio(self):
        opciones = "/".join(CRITERIOS + ("ninguno",))
        texto = input(f"Filtrar por ({opciones}): ").strip().lower()
        if texto == "ninguno":
            return None
        if texto not in CRITERIOS:
            raise ErrorDeValidacion("criterio inválido")
        return texto

    def _pedir_valor(self, criterio):
        valor = input("Valor: ").strip().lower()
        if valor == "":
            raise ErrorDeValidacion("debe ingresar un valor")
        if criterio == "legajo":
            return parsear_legajo(valor)
        clase, mensaje = _ENUM_POR_CRITERIO[criterio]
        return parsear_enum(clase, valor, mensaje)

    def _buscar(self):
        try:
            criterio = self._pedir_criterio()
            valor = None if criterio is None else self._pedir_valor(criterio)
        except ErrorDeAplicacion as error:
            print(f"Error: {error}")
            return
        solicitudes = self._servicio.filtrar(criterio, valor)
        if not solicitudes:
            print("No se encontraron solicitudes")
            return
        for solicitud in solicitudes:
            print(self._formatear_solicitud(solicitud))

    def _formatear_solicitud(self, s):
        estudiante = self._servicio.nombre_estudiante(s["legajo"])
        responsable = self._servicio.nombre_responsable(s["responsable_id"])
        plazo = self._servicio.plazo_dias(s)
        return (f"#{s['id']} | {estudiante} ({s['legajo']}) | {s['tipo']} | {s['prioridad']} | "
                f"{s['estado']} | Responsable: {responsable} | Plazo: {plazo} días | "
                f"{s['descripcion']}")

    def _reporte(self):
        r = self._servicio.generar_reporte()
        print("--- Reporte ---")
        print(f"Total de solicitudes: {r.total}")
        print("Por estado:")
        for estado, cantidad in r.por_estado.items():
            print(f" {estado}: {cantidad}")
        print("Por prioridad (solo abiertas):")
        for prioridad, cantidad in r.por_prioridad_abiertas.items():
            print(f" {prioridad}: {cantidad}")
        print("Por responsable:")
        for nombre, cantidad in r.por_responsable:
            print(f" {nombre}: {cantidad}")
        print(f" sin asignar: {r.sin_asignar}")
        print(f"Solicitudes de prioridad alta sin resolver: {r.alta_sin_resolver}")
