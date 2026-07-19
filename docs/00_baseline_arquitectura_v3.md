# Baseline Arquitectura v3.1

## Arquitectura modular

La herramienta se organiza por responsabilidades para separar adquisición auxiliar, parsing, normalización, correlación, reporting y validación.

- `core/`: define el contrato `CommonEvent`, conversiones temporales, constantes y excepciones.
- `extractors/`: contiene utilidades de copia de evidencias ya disponibles.
- `parsers/`: encapsula el procesamiento de cada artefacto forense.
- `normalizers/`: centraliza transformaciones hacia el modelo común.
- `correlator/`: construye una timeline ordenada con `pandas`.
- `reporters/`: genera salidas consumibles en CSV, JSON, JSONL y Markdown.
- `validation/`: contiene el esquema de ground truth y helpers de validación.

## Flujo end-to-end

1. La CLI recibe una carpeta de entrada y una carpeta de salida.
2. Se cargan `config/settings.yaml` y `config/artifacts.yaml` si existen.
3. Cada parser configurado procesa su carpeta de artefactos.
4. Los eventos se representan como `CommonEvent`.
5. El correlator convierte los eventos a `DataFrame` y ordena por `timestamp_utc`.
6. Los reporters exportan eventos y timeline.
7. La validación experimental se ejecutará contra `validation/ground_truth.csv` en fases posteriores.

## Artefactos MVP previstos

- EVTX: eventos de seguridad y sistema.
- Prefetch: evidencias de ejecución de programas.
- Registry: claves seleccionadas para actividad de usuario, persistencia y configuración.
- Browser History: visitas, descargas y actividad web básica.

## Salidas

- `events.json`: eventos normalizados como array JSON.
- `events.jsonl`: eventos normalizados como JSON Lines.
- `timeline.csv`: timeline ordenada por UTC.
- `report.md`: resumen preliminar en Markdown.

## Validación mediante ground truth

La validación se basará en escenarios controlados. Cada escenario tendrá eventos esperados en `ground_truth.csv` y se comparará contra la timeline generada. La métrica inicial prevista es cobertura de eventos esperados, desviación temporal y trazabilidad hasta el artefacto original.

## Limitaciones conocidas

- `pandas` carga la timeline en RAM; esto es aceptable para el MVP, pero puede limitar datasets grandes.
- Las zonas horarias requieren tratamiento cuidadoso por artefacto; la baseline normaliza a UTC y rechaza timestamps naive en el correlator.
- Prefetch puede requerir fallback si el formato, versión de Windows o librerías disponibles no permiten parsing completo.
- Los parsers actuales son stubs y no extraen evidencias reales todavía.
