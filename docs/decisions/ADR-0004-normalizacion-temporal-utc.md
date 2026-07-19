# ADR-0004 - Normalización temporal UTC

## Contexto

Los artefactos forenses pueden almacenar tiempos en UTC, hora local, FILETIME, Chrome time u otros formatos.

## Decisión

Normalizar la timeline a `timestamp_utc` timezone-aware y rechazar timestamps naive en el correlator.

## Alternativas consideradas

- Mantener timestamps en formato original hasta el reporte.
- Aceptar datetimes naive y resolver zonas horarias al final.

## Justificación

UTC reduce ambigüedades en la correlación y obliga a documentar las conversiones temporales por parser.

## Impacto en el TFM

La normalización temporal se puede defender como control metodológico central para evitar errores de interpretación.
