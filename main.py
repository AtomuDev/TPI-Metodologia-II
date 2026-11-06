import json
import os


ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")

datos = {}


class GestorSolicitudes:

    def __init__(self):
        global datos

        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except FileNotFoundError:
            datos = {
                "siguiente_id": 1,
                "estudiantes": [],
                "responsables": [
                    {"id": 1, "nombre": "Ana Pérez", "area": "Alumnado"},
                    {"id": 2, "nombre": "Luis Gómez", "area": "Secretaría Académica"},
                    {"id": 3, "nombre": "Marta Díaz", "area": "Bedelía"},
                ],
                "solicitudes": [],
            }
        except (json.JSONDecodeError, OSError):
            print("Error: no se pudo leer " + ARCHIVO + " (archivo dañado o inaccesible).")
            print("Revise o elimine el archivo manualmente y vuelva a ejecutar.")
            raise SystemExit(1)

    def guardar(self):
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def crear_solicitud(self, n, l, t, p, d, e, r):
        est = None

        for x in datos["estudiantes"]:
            if x["legajo"] == l:
                est = x

        if est is None:
            datos["estudiantes"].append({"legajo": l, "nombre": n})

        s = {
            "id": datos["siguiente_id"],
            "legajo": l,
            "tipo": t,
            "prioridad": p,
            "descripcion": d,
            "estado": e,
            "responsable_id": r,
        }

        datos["siguiente_id"] = datos["siguiente_id"] + 1
        datos["solicitudes"].append(s)

        self.guardar()

        return s["id"]

    def registrar(self):
        n = input("Nombre del estudiante: ").strip()
        l = input("Legajo: ").strip()
        t = input("Tipo (certificado/equivalencia/baja/otro): ").strip().lower()
        p = input("Prioridad (alta/media/baja): ").strip().lower()
        d = input("Descripción: ").strip()

        if n == "":
            print("Error: el nombre es obligatorio")
            return None

        if not l.isdecimal() or int(l) <= 0:
            print("Error: el legajo debe ser un número positivo")
            return None

        l = str(int(l))

        if t != "certificado" and t != "equivalencia" and t != "baja" and t != "otro":
            print("Error: tipo inválido")
            return None

        if p != "alta" and p != "media" and p != "baja":
            print("Error: prioridad inválida")
            return None

        if d == "":
            print("Error: la descripción es obligatoria")
            return None

        existente = None

        for a in datos["estudiantes"]:
            if a["legajo"] == l:
                existente = a

        if existente is not None and existente["nombre"].lower() != n.lower():
            print("Error: el legajo " + l + " ya está registrado a nombre de " + existente["nombre"])
            return None

        nuevo_id = self.crear_solicitud(n, l, t, p, d, "pendiente", None)

        print("Solicitud #" + str(nuevo_id) + " registrada")

        return nuevo_id

    def cambiar_estado(self):
        i = input("ID de solicitud: ").strip()

        if not i.isdecimal() or int(i) <= 0:
            print("Error: ID inválido")
            return False

        s = None

        for x in datos["solicitudes"]:
            if x["id"] == int(i):
                s = x

        if s is None:
            print("Error: solicitud no encontrada")
            return False

        if s["estado"] == "resuelta" or s["estado"] == "rechazada":
            print("Error: la solicitud ya está cerrada")
            return False

        print("Estado actual: " + s["estado"])
        ne = input("Nuevo estado (pendiente/en_proceso/resuelta/rechazada): ").strip().lower()

        if ne != "pendiente" and ne != "en_proceso" and ne != "resuelta" and ne != "rechazada":
            print("Error: estado inválido")
            return False

        if ne == s["estado"]:
            print("Error: la solicitud ya está en ese estado")
            return False

        if (ne == "en_proceso" or ne == "resuelta") and s["responsable_id"] is None:
            print("Error: debe asignar un responsable antes de pasar a " + ne)
            return False

        s["estado"] = ne

        self.guardar()

        print("Solicitud #" + str(s["id"]) + " ahora está " + ne)

        return True

    def asignar(self):
        if len(datos["solicitudes"]) == 0:
            print("Error: no hay solicitudes registradas")
            return False

        print("Responsables disponibles:")

        for r in datos["responsables"]:
            print("  " + str(r["id"]) + " - " + r["nombre"] + " (" + r["area"] + ")")

        i = input("ID de solicitud: ").strip()

        if not i.isdecimal() or int(i) <= 0:
            print("Error: ID de solicitud inválido")
            return False

        s = None

        for x in datos["solicitudes"]:
            if x["id"] == int(i):
                s = x

        if s is None:
            print("Error: solicitud no encontrada")
            return False

        if s["estado"] == "resuelta" or s["estado"] == "rechazada":
            print("Error: la solicitud ya está cerrada")
            return False

        ri = input("ID de responsable: ").strip()

        if not ri.isdecimal() or int(ri) <= 0:
            print("Error: ID de responsable inválido")
            return False

        resp = None

        for r in datos["responsables"]:
            if r["id"] == int(ri):
                resp = r

        if resp is None:
            print("Error: responsable no encontrado")
            return False

        s["responsable_id"] = resp["id"]

        self.guardar()

        print("Solicitud #" + str(s["id"]) + " asignada a " + resp["nombre"])

        return True

    def buscar(self):
        c = input("Filtrar por (estado/prioridad/tipo/legajo/ninguno): ").strip().lower()

        if c != "estado" and c != "prioridad" and c != "tipo" and c != "legajo" and c != "ninguno":
            print("Error: criterio inválido")
            return None

        v = ""

        if c != "ninguno":
            v = input("Valor: ").strip().lower()

            if v == "":
                print("Error: debe ingresar un valor")
                return None

            if c == "estado" and v not in ["pendiente", "en_proceso", "resuelta", "rechazada"]:
                print("Error: estado inválido")
                return None

            if c == "prioridad" and v not in ["alta", "media", "baja"]:
                print("Error: prioridad inválida")
                return None

            if c == "tipo" and v not in ["certificado", "equivalencia", "baja", "otro"]:
                print("Error: tipo inválido")
                return None

            if c == "legajo":
                if not v.isdecimal() or int(v) <= 0:
                    print("Error: el legajo debe ser un número positivo")
                    return None

                v = str(int(v))

        lst = []

        for x in datos["solicitudes"]:
            if c == "ninguno":
                lst.append(x)
            elif c == "estado" and x["estado"] == v:
                lst.append(x)
            elif c == "prioridad" and x["prioridad"] == v:
                lst.append(x)
            elif c == "tipo" and x["tipo"] == v:
                lst.append(x)
            elif c == "legajo" and x["legajo"] == v:
                lst.append(x)

        if len(lst) == 0:
            print("No se encontraron solicitudes")
            return lst

        for x in lst:
            nombre = ""

            for e in datos["estudiantes"]:
                if e["legajo"] == x["legajo"]:
                    nombre = e["nombre"]

            resp = "sin asignar"

            for r in datos["responsables"]:
                if r["id"] == x["responsable_id"]:
                    resp = r["nombre"]

            if x["prioridad"] == "alta":
                plazo = 2
            elif x["prioridad"] == "media":
                plazo = 5
            else:
                plazo = 10

            print("#" + str(x["id"]) + " | " + nombre + " (" + x["legajo"] + ") | " + x["tipo"] + " | "
                  + x["prioridad"] + " | " + x["estado"] + " | Responsable: " + resp
                  + " | Plazo: " + str(plazo) + " días | " + x["descripcion"])

        return lst

    def reporte(self):
        print("--- Reporte ---")
        print("Total de solicitudes: " + str(len(datos["solicitudes"])))

        print("Por estado:")

        for e in ["pendiente", "en_proceso", "resuelta", "rechazada"]:
            c = 0

            for x in datos["solicitudes"]:
                if x["estado"] == e:
                    c = c + 1

            print("  " + e + ": " + str(c))

        print("Por prioridad (solo abiertas):")

        for p in ["alta", "media", "baja"]:
            c = 0

            for x in datos["solicitudes"]:
                if x["prioridad"] == p and (x["estado"] == "pendiente" or x["estado"] == "en_proceso"):
                    c = c + 1

            print("  " + p + ": " + str(c))

        print("Por responsable:")

        for r in datos["responsables"]:
            c = 0

            for x in datos["solicitudes"]:
                if x["responsable_id"] == r["id"]:
                    c = c + 1

            print("  " + r["nombre"] + ": " + str(c))

        c = 0

        for x in datos["solicitudes"]:
            if x["responsable_id"] is None:
                c = c + 1

        print("  sin asignar: " + str(c))

        c = 0

        for x in datos["solicitudes"]:
            if x["prioridad"] == "alta" and (x["estado"] == "pendiente" or x["estado"] == "en_proceso"):
                c = c + 1

        print("Solicitudes de prioridad alta sin resolver: " + str(c))


def menu():
    g = GestorSolicitudes()

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
            op = input("Opción: ").strip()

            if op == "1":
                g.registrar()
            elif op == "2":
                g.cambiar_estado()
            elif op == "3":
                g.asignar()
            elif op == "4":
                g.buscar()
            elif op == "5":
                g.reporte()
            elif op == "0":
                print("Hasta luego")
                break
            else:
                print("Opción inválida")
        except (KeyboardInterrupt, EOFError):
            print("\nEntrada interrumpida. Hasta luego")
            break


if __name__ == "__main__":
    menu()