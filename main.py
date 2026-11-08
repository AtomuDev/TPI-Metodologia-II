import os

from solicitudes.console import ConsolaSolicitudes
from solicitudes.repository import RepositorioJSON, ErrorPersistencia
from solicitudes.services import ServicioSolicitudes

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
