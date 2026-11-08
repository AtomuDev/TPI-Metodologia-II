"""Compara la version original (tag estado-inicial) con la version actual.
Ejecuta las dos con las mismas entradas de teclado y compara lo que se imprime
y el datos.json resultante.

Uso (desde la raiz del repo):  python docs/comparar_versiones.py
"""
import difflib
import os
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG_ORIGINAL = "estado-inicial"

# Cada escenario es una lista de ejecuciones; cada ejecucion, las lineas que se tipean.
REG = ["1", "Nahuel", "123", "baja", "alta", "Solicitud de baja"]
ESCENARIOS = {
    "1 Registrar solicitud valida": [REG + ["0"]],
    "2 Validaciones (nombre, legajo, tipo, prioridad, descripcion)": [
        ["1", "", "1", "baja", "alta", "d",
         "1", "A", "abc", "baja", "alta", "d",
         "1", "A", "1", "xx", "alta", "d",
         "1", "A", "1", "baja", "xx", "d",
         "1", "A", "1", "baja", "alta", "", "0"]],
    "3 Legajo ya usado por otro estudiante": [
        REG + ["1", "Gaston", "123", "baja", "baja", "Otra", "0"]],
    "4 Asignar responsable": [REG + ["3", "1", "1", "0"]],
    "5 Cambiar a en_proceso sin responsable": [REG + ["2", "1", "en_proceso", "0"]],
    "6 Flujo completo y solicitud cerrada": [
        REG + ["3", "1", "2", "2", "1", "en_proceso", "2", "1", "resuelta",
               "2", "1", "pendiente", "0"]],
    "7 Buscar / filtrar": [
        REG + ["4", "ninguno", "4", "estado", "pendiente", "4", "prioridad", "media",
               "4", "legajo", "123", "4", "tipo", "xx", "0"]],
    "8 Reporte": [REG + ["3", "1", "2", "2", "1", "en_proceso", "5", "0"]],
    "9 Persistencia entre ejecuciones": [REG + ["0"], ["4", "ninguno", "0"]],
}


def preparar(carpeta, version):
    if version == "original":
        codigo = subprocess.run(["git", "show", f"{TAG_ORIGINAL}:main.py"], cwd=RAIZ,
                                capture_output=True, check=True).stdout
        with open(os.path.join(carpeta, "main.py"), "wb") as f:
            f.write(codigo)
    else:
        shutil.copy(os.path.join(RAIZ, "main.py"), carpeta)
        shutil.copytree(os.path.join(RAIZ, "solicitudes"), os.path.join(carpeta, "solicitudes"),
                        ignore=shutil.ignore_patterns("__pycache__"))


def ejecutar(version, corridas, datos_previos=None):
    with tempfile.TemporaryDirectory() as carpeta:
        preparar(carpeta, version)
        ruta = os.path.join(carpeta, "datos.json")
        if datos_previos is not None:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(datos_previos)
        salida = []
        for lineas in corridas:
            r = subprocess.run([sys.executable, "main.py"], cwd=carpeta, text=True,
                               input="\n".join(lineas) + "\n", capture_output=True,
                               encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            salida.append(f"[codigo de salida: {r.returncode}]\n{r.stdout}{r.stderr}"
                          .replace(carpeta, "<CARPETA>"))
        datos = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else None
        return "\n".join(salida), datos


def comparar(nombre, corridas, datos_previos=None):
    out_a, json_a = ejecutar("original", corridas, datos_previos)
    out_b, json_b = ejecutar("refactorizada", corridas, datos_previos)
    iguales = out_a == out_b and json_a == json_b
    print(("OK       " if iguales else "DIFIERE  ") + nombre)
    if not iguales:
        for linea in difflib.unified_diff(out_a.splitlines(), out_b.splitlines(),
                                          "original", "refactorizada", lineterm="", n=0):
            print("     " + linea)
    return iguales


def main():
    resultados = [comparar(n, c) for n, c in ESCENARIOS.items()]
    resultados.append(comparar("10 datos.json danado (no se sobrescribe)", [["0"]],
                               datos_previos="{esto no es json"))
    print(f"\n{sum(resultados)}/{len(resultados)} escenarios identicos")
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
