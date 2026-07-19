# Fase 9.1 - Infraestructura GUI y carga segura de resultados

## Objetivo

La Fase 9.1 implementa la infraestructura mínima de una interfaz local capaz de cargar outputs existentes del prototipo sin modificar evidencias, resultados ni lógica forense. El alcance comprende validación de rutas, catálogo de archivos, loaders robustos, filtros puros, caché de lectura y una pantalla Streamlit de estado y preview.

No incluye dashboard completo, gráficas Plotly, timeline interactiva, explorador avanzado, detalle completo, exportación ni ejecución de `main.run_pipeline()`.

## Compatibilidad y dependencias

La instalación se comprobó efectivamente en `.venv-gui` con:

| Componente | Versión probada |
| --- | --- |
| Python | 3.14.6 |
| pip | 26.1.2 |
| Streamlit | 1.59.2 |
| Plotly | 6.9.0 |
| Pandas | 3.0.3 |

`requirements-gui.txt` contiene únicamente Streamlit y Plotly como dependencias directas fijadas. Las dependencias forenses continúan en `requirements.txt`, por lo que la CLI puede instalarse y probarse sin incorporar el stack gráfico.

## Archivos implementados

- `gui/config.py`: claves canónicas, columnas y constantes de presentación.
- `gui/models.py`: fingerprints, incidencias, resultados de carga, catálogo, escenarios y filtros.
- `gui/services/path_service.py`: resolución y validación segura de rutas.
- `gui/services/output_catalog.py`: detección determinista de outputs conocidos.
- `gui/services/event_repository.py`: carga y validación de `events.json`.
- `gui/services/timeline_repository.py`: carga conservadora de `timeline.csv`.
- `gui/services/validation_repository.py`: carga de todos los escenarios de validación.
- `gui/services/filter_service.py`: filtros y agregados heurísticos independientes de Streamlit.
- `gui/components/load_status.py`: representación compacta del estado de archivos.
- `gui/app.py`: aplicación Streamlit mínima.
- `tests/gui/` y `tests/fixtures/gui/`: pruebas y datos exclusivamente sintéticos.

La estructura compacta difiere del diseño inicial al concentrar los modelos en `gui/models.py` y organizar los tests por servicio. Esta decisión evita módulos vacíos y mantiene una correspondencia directa entre archivo implementado y prueba automatizada.

## Arquitectura implementada

```text
Ruta local
  -> PathService
  -> OutputCatalog
  -> EventRepository / TimelineRepository / ValidationRepository
  -> LoadResult + LoadIssue
  -> caché Streamlit por fingerprint
  -> resumen, estado, preview e incidencias
```

Los repositorios solo leen ficheros. No importan Streamlit, parsers, correlador, validador ni `main.py`. La capa visual consume resultados tipados y no modifica sus fuentes.

## Contratos reales

`events.json` es una lista UTF-8 de objetos producidos por `CommonEvent.to_dict()`. Cada fila debe contener las 16 claves canónicas. Los timestamps se conservan y se añade `_ui_timestamp_utc` para filtros; esta columna es interna y no forma parte de `CommonEvent`.

`timeline.csv` contiene las mismas 16 columnas. `raw_evidence` y `provenance` son cadenas JSON serializadas. El loader preserva cada celda original y añade representaciones `_ui_*` solo cuando el contenido se puede interpretar con seguridad.

Los resultados de validación admiten `correcto`, `parcial`, `no_detectado` y, cuando se activa el cálculo ampliado, `falso_positivo`. Las filas de falso positivo no son obligatorias: el conteo de `validation_summary_*.json` es la fuente principal de esa métrica.

## Carga parcial y errores

Cada loader devuelve registros leídos, aceptados y rechazados, estado general e incidencias con severidad, código, ruta, fila y campo opcionales. En `events.json`, las filas inválidas se rechazan de manera individual y las válidas continúan disponibles. Si no queda ninguna fila válida, el resultado es un error. Los duplicados de `event_id` se detectan y la segunda aparición se rechaza.

Las claves desconocidas se conservan y generan un warning. Un timestamp inválido nunca sustituye al valor original. Los detalles `raw_evidence` y `provenance` permanecen disponibles, pero no se expanden en el preview.

## Caché

Los wrappers `st.cache_data` existen únicamente en `gui/app.py`. Su clave efectiva incluye ruta resuelta, tamaño y `mtime_ns`; un cambio del fichero invalida la carga. El botón **Recargar resultados** limpia solo las cachés de la GUI. No se cachean handles ni evidencias externas.

## Seguridad y privacidad

- servidor local en `127.0.0.1`;
- telemetría de Streamlit desactivada;
- rutas resueltas con `pathlib` y confinadas a la raíz validada;
- ninguna escritura sobre `evidence/` u `output/`;
- ningún `subprocess`, `shell=True` o comando construido desde entrada de usuario;
- ninguna comunicación con servicios externos;
- errores visibles sin traceback en la pantalla;
- preview sin evidencia bruta, procedencia expandida ni rutas completas.

## Filtros

`filter_service.py` ofrece funciones puras para rango temporal UTC, fuente, categoría, acción, parser, escenario, texto libre, presencia de trazabilidad y rango numérico de `confidence`. También obtiene valores disponibles, cuenta eventos trazables y agrupa `confidence` por fuente mediante mediana e intervalos. No calcula una media global ni interpreta el campo como probabilidad calibrada.

## Tests

La suite cubre rutas válidas e inválidas, espacios, permisos, escapes, catálogos vacíos y múltiples, JSON/CSV corruptos, contratos incompletos, columnas extra, timestamps inválidos, duplicados, carga parcial, procedencia vacía, todos los resultados del validador, escenarios huérfanos y múltiples, filtros individuales y combinados, inmutabilidad de DataFrames y smoke tests mediante `streamlit.testing.v1.AppTest`.

El entorno principal omite únicamente los smoke tests que requieren la dependencia opcional Streamlit. El entorno GUI ejecuta toda la suite. La prueba de symlink se omite cuando Windows no permite crear el enlace sin privilegios.

## Prueba de solo lectura con outputs actuales

La carga manual detectó 1.465 eventos válidos y ninguna fila rechazada: 1.458 EVTX, 3 BrowserHistory, 2 Prefetch y 2 Registry. El rango temporal observado fue de `2024-01-10T09:00:00+00:00` a `2026-06-20T16:01:21.765501+00:00`. Se detectaron las validaciones `browser_synthetic`, `prefetch_synthetic`, `registry_synthetic` y `default`, sin incidencias de carga.

Esta comprobación confirma interoperabilidad con outputs existentes; no constituye una nueva validación forense y no alteró los ficheros inspeccionados.

## Limitaciones y trabajo restante

- `events.json` se carga completo en memoria; falta medir decenas de miles de eventos.
- El estado de sesión y los reruns solo cubren el flujo mínimo de carga.
- No hay paginación, timeline ni visualizaciones Plotly en esta fase.
- Los campos pesados se conservan en memoria aunque no se muestren.
- La ruta introducida por el usuario sigue siendo información local sensible y debe enmascararse en capturas.
- El empaquetado y la compatibilidad con futuras versiones de Python requieren reevaluación.
- La Fase 9.2 implementará el dashboard sobre estos servicios sin duplicar contratos ni lógica forense.
