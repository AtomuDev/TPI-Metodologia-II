# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador (TPI) de **Metodología de Sistemas II**
Tecnicatura Universitaria en Programación a Distancia, UTN.

> **Versión del repositorio:** `estado-inicial` (sistema base, previo al refactoring).
> El estado final del código se publica con el tag `estado-refactorizado`.

## Descripción

Aplicación de consola en Python que permite registrar solicitudes de estudiantes (certificados, equivalencias, bajas, etc.), clasificarlas por tipo, prioridad y estado, asignarles un responsable, consultarlas con filtros y generar un reporte simple.

El sistema fue elegido como caso de trabajo para el TPI: la funcionalidad visible es simple, y el foco del trabajo está en diagnosticar la calidad interna del código, identificar deuda técnica y code smells, aplicar SOLID y Clean Code, y ejecutar refactorings seguros comparando el comportamiento antes y después.


Materia: Metodología de Sistemas II · Comisión: 12 · Fecha: 08/11/26

## Tecnologías

- Python 3.11 o superior
- Módulos de la biblioteca estándar: `json` y `os`
- Persistencia en archivo JSON (`datos.json`)
- Sin dependencias externas

## Instalación y uso

1. Clonar el repositorio:

   ```bash
   git clone <URL-del-repositorio>
   cd <carpeta-del-repositorio>
   ```

2. (Opcional) Ver la versión base:

   ```bash
   git checkout estado-inicial
   ```

3. Ejecutar el programa (ajustar el nombre si el archivo se llama distinto):

   ```bash
   python gestor_solicitudes.py
   ```

Al primer arranque se crea `datos.json` junto al script, con tres responsables precargados. Todos los cambios se guardan automáticamente en ese archivo.

### Menú principal

```
=== Gestión de Solicitudes Académicas ===
1. Registrar solicitud
2. Cambiar estado
3. Asignar responsable
4. Buscar / filtrar
5. Reporte
0. Salir
```

## Funcionalidades

### 1. Registrar solicitud
Pide nombre del estudiante, legajo, tipo, prioridad y descripción. La solicitud se crea en estado `pendiente` y sin responsable.

- Si el legajo ya existe y el nombre coincide, se reutiliza al estudiante.
- Si el legajo existe con otro nombre, se rechaza el registro.
- Los legajos se normalizan (`007` y `7` son el mismo legajo).

### 2. Cambiar estado
Cambia el estado de una solicitud existente.

- No se puede pasar al mismo estado en el que ya está.
- Para pasar a `en_proceso` o `resuelta` debe haber un responsable asignado.
- `rechazada` no exige responsable.
- `resuelta` y `rechazada` son estados finales: una solicitud cerrada no se puede reabrir.

### 3. Asignar responsable
Muestra los responsables disponibles y asigna uno a la solicitud indicada. Se puede reasignar mientras la solicitud no esté cerrada.

### 4. Buscar / filtrar
Lista solicitudes sin filtro o filtrando por estado, prioridad, tipo o legajo. Cada resultado muestra estudiante, tipo, prioridad, estado, responsable y plazo estimado de atención.

### 5. Reporte
Muestra:

- Total de solicitudes.
- Cantidad por estado.
- Cantidad por prioridad, **solo de solicitudes abiertas** (`pendiente` y `en_proceso`).
- Cantidad por responsable y solicitudes sin asignar.
- Solicitudes de prioridad alta sin resolver.

## Reglas de negocio

| Dato | Valores permitidos |
|---|---|
| Tipo | `certificado`, `equivalencia`, `baja`, `otro` |
| Prioridad | `alta`, `media`, `baja` |
| Estado | `pendiente`, `en_proceso`, `resuelta`, `rechazada` |

Plazo estimado de atención según prioridad:

| Prioridad | Plazo |
|---|---|
| alta | 2 días |
| media | 5 días |
| baja | 10 días |

Flujo de estados:

```
pendiente ──► en_proceso ──► resuelta
    │              │
    └──────────────┴──────► rechazada
```

`pendiente` y `en_proceso` pueden alternarse entre sí mientras la solicitud no esté cerrada.

## Modelo de datos

Los datos se guardan en `datos.json` con esta estructura:

```json
{
  "siguiente_id": 1,
  "estudiantes": [
    { "legajo": "1001", "nombre": "Juan Prueba" }
  ],
  "responsables": [
    { "id": 1, "nombre": "Ana Pérez", "area": "Alumnado" }
  ],
  "solicitudes": [
    {
      "id": 1,
      "legajo": "1001",
      "tipo": "certificado",
      "prioridad": "alta",
      "descripcion": "Certificado de alumno regular",
      "estado": "pendiente",
      "responsable_id": null
    }
  ]
}
```

Entidades principales: **Estudiante**, **Responsable** y **Solicitud**.

El sistema no permite eliminar estudiantes ni responsables.

## Manejo de errores

- Todas las entradas se validan y muestran un mensaje de error claro.
- Si `datos.json` está dañado, el programa avisa y termina **sin sobrescribir** el archivo.
- `Ctrl+C` o fin de entrada cierran el programa con un mensaje, sin traceback.

## Datos de prueba

Por indicación de la cátedra, se deben usar **datos sintéticos o anonimizados**. No cargar datos personales reales.

## Estructura del repositorio

```
.
├── main.py   # Código del sistema
├── README.md
└── docs/                   # Checklist de pruebas, code review, evidencias y decisiones técnicas
```

## Hitos del TPI (tags de Git)

| Tag | Contenido |
|---|---|
| `estado-inicial` | Sistema base entregado |
| `etapa-diagnostico` | Diagnóstico de calidad, deuda técnica y code smells |
| `etapa-refactoring` | Refactorings aplicados |
| `etapa-pruebas` | Pruebas y verificación del comportamiento |
| `etapa-docs` | Documentación y code review |
| `estado-refactorizado` | Estado final del código |

## Enlaces

- Informe PDF: _Completar_
- Video de defensa: _Completar_
