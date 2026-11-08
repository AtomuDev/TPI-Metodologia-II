import os

from solicitudes.consola import ConsolaSolicitudes
from solicitudes.repositorio import RepositorioJSON, ErrorPersistencia
from solicitudes.servicio import ServicioSolicitudes

RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.json")


def main():
    try:
        servicio = ServicioSolicitudes(RepositorioJSON(RUTA_DATOS))
    except ErrorPersistencia:
        print("Error: no se pudo leer " + RUTA_DATOS + " (archivo dañado o inaccesible).")
        print("Revise o elimine el archivo manualmente y vuelva a ejecutar.")
        raise SystemExit(1)
    ConsolaSolicitudes(servicio).ejecutar()


if __name__ == "__main__":
    main()
