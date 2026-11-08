# Code review técnico

Revisión del repositorio en el tag `estado-refactorizado`.

## Checklist

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 1 | Cada módulo tiene una sola responsabilidad | ✔ | `modelo`, `validations`, `repository`, `services`, `console` |
| 2 | La lógica no usa `input()` ni `print()` | ✔ | Solo `console.py` |
| 3 | No hay variables globales | ✔ | El estado vive en `ServicioSolicitudes` |
| 4 | Nombres descriptivos | ✔ | Sin `n`, `l`, `t`, `x` |
| 5 | Sin strings ni números mágicos | ✔ | `StrEnum` y `PLAZO_DIAS` |
| 6 | Funciones cortas (≤ 30 líneas) y con pocos parámetros (≤ 5) | ✔ | Máximo 25 líneas y 5 parámetros |
| 7 | Sin código duplicado | ✔ | `_encontrar` y `parsear_*` |
| 8 | Errores con excepciones | ✔ | `ErrorDeAplicacion` |
| 9 | La salida y el `datos.json` son iguales a los de la versión original | ✔ | 10/10 escenarios (tras corregir H1) |
| 10 | Manejo de errores de escritura en disco | ⚠ | `guardar()` no captura `OSError` (H4) |
| 11 | El servicio no expone su estructura interna | ⚠ | Devuelve los diccionarios internos (H5) |

## Hallazgos

| ID | Severidad | Hallazgo | Acción | Estado |
|---|---|---|---|---|
| H1 | Alta | La sangría de la salida cambió de 2 a 1 espacio en el listado de responsables y en el reporte | Restaurar los 2 espacios en `console.py` | Corregido |
| H2 | Media | `.gitignore` vacío: `datos.json` podía subirse al repo | Agregar `datos.json` y `__pycache__/` | Corregido |
| H3 | Media | El README describía el estado inicial | Reescribirlo | Corregido |
| H4 | Baja | `RepositorioJSON.guardar` no maneja `OSError` | Convertirlo en `ErrorPersistencia` | Pendiente |
| H5 | Baja | El servicio devuelve los diccionarios internos | Usar una dataclass `Solicitud` | Pendiente |

## Criterios de aceptación

1. `python docs/comparar_versiones.py` informa 10/10 escenarios idénticos.
2. Hallazgos de severidad alta y media corregidos.
3. Sin variables globales; tipos, prioridades y estados definidos en un solo lugar.
4. README actualizado.

Resultado: **aceptado**, con H4 y H5 como mejoras futuras.
