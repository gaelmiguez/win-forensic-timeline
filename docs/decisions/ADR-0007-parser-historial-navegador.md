# ADR-0007 - Parser de historial de navegador

## Contexto

La baseline inicial estableció la arquitectura y los puntos de extensión para parsers forenses, pero aún no generaba eventos reales. Para avanzar hacia una validación práctica era necesario incorporar un artefacto accesible, reproducible y con estructura suficientemente estable.

## Decisión

Implementar un parser funcional de historiales de navegador Chrome/Edge basados en SQLite. El parser procesa ficheros `History`, valida la existencia de las tablas `urls` y `visits`, convierte `visits.visit_time` con `chrome_time_to_utc` y genera eventos `CommonEvent` con `source_artifact` igual a `BrowserHistory`.

## Alternativas consideradas

- Empezar por EVTX, que tiene alto valor forense pero mayor complejidad técnica y semántica.
- Empezar por Prefetch, que requiere tratamiento cuidadoso de versiones y posibles librerías específicas.
- Mantener todos los parsers como stubs hasta disponer de una imagen Windows real.

## Justificación

BrowserHistory se incluye como artefacto práctico adicional para validar escenarios de navegación por su disponibilidad, estructura SQLite, facilidad de generación sintética y posibilidad de contraste mediante ground truth. Además, permite probar de extremo a extremo el modelo de eventos, la normalización temporal, la correlación y los reporters sin añadir dependencias externas.

## Impacto en el TFM

La herramienta deja de ser únicamente arquitectónica y pasa a producir eventos reales en un escenario controlado. Esto mejora la demostrabilidad del prototipo y aporta una base experimental inicial para validar navegación web antes de abordar EVTX, Prefetch y Registro.
