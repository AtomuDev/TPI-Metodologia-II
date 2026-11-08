# Sistema de Gestión de Solicitudes Académicas

TPI de **Metodología de Sistemas II** · UTN, Tecnicatura Universitaria en Programación a Distancia · Comisión 12

> Esta es la versión **refactorizada** (tag `estado-refactorizado`). El sistema original está en el tag `estado-inicial`.

## Qué hace

Aplicación de consola en Python para registrar solicitudes de estudiantes (certificados, equivalencias, bajas, otros), cambiar su estado, asignarles un responsable, buscarlas y sacar un reporte. Los datos se guardan en `datos.json`.

El TPI se centra en la calidad interna: se mejoró el diseño del código sin cambiar su comportamiento.

## Uso

Requiere Python 3.11 o superior. No tiene dependencias externas.

```bash
python main.py
```

Menú: 1 Registrar solicitud · 2 Cambiar estado · 3 Asignar responsable · 4 Buscar / filtrar · 5 Reporte · 0 Salir.

## Reglas de negocio

- **Tipos:** certificado, equivalencia, baja, otro.
- **Prioridades y plazo estimado:** alta (2 días), media (5 días), baja (10 días).
- **Estados:** pendiente, en_proceso, resuelta, rechazada. Resuelta y rechazada son finales: una solicitud cerrada no se reabre.
- Para pasar a `en_proceso` o `resuelta` hace falta un responsable asignado.
- Un legajo no puede registrarse con dos nombres distintos.

## Estructura

```
main.py                  # Arma las piezas e inicia el programa
solicitudes/
  modelo.py              # Enums, reglas y excepciones
  validations.py         # Validación de lo que escribe el usuario
  repository.py          # Lectura y escritura de datos.json
  services.py            # Lógica de negocio y reporte
  console.py             # Menú, input() y print()
docs/
  comparar_versiones.py  # Compara la versión original con la actual
  code-review.md         # Checklist y hallazgos del code review
```

Para agregar un tipo nuevo (por ejemplo `constancia`) alcanza con sumarlo al enum `Tipo` en `modelo.py`.

## Verificación

```bash
python docs/comparar_versiones.py
```

Ejecuta la versión original (tag `estado-inicial`) y la actual con las mismas entradas, y compara lo que se imprime y el `datos.json` resultante. Resultado esperado: `10/10 escenarios identicos`. Requiere `git`.

## Manejo de errores

- Las entradas se validan con mensajes como `Error: el nombre es obligatorio`.
- Si `datos.json` está dañado, el programa avisa y termina sin sobrescribirlo.
- `Ctrl+C` cierra el programa sin mostrar errores técnicos.

## Tags de Git

| Tag | Contenido |
|---|---|
| `estado-inicial` | Sistema base |
| `etapa-refactoring` | Refactorings aplicados |
| `etapa-docs` | Code review y documentación |
