# Contratos de datos de la GUI

## Principios

- Los loaders validan antes de mostrar.
- Un fichero inválido no invalida otros outputs compatibles.
- Los errores indican fichero y campo, sin volcar evidencia completa.
- Las rutas de evidencia se tratan como datos sensibles.

## `events.json`

Tipo raíz: lista JSON de eventos.

`CommonEvent.to_dict()` serializa siempre las 16 claves. La obligatoriedad siguiente se refiere a la presencia de la clave; solo algunos valores admiten `null`.

| Campo | Tipo serializado | Clave obligatoria | `null` permitido | Tratamiento del loader |
| --- | --- | --- | --- | --- |
| `event_id` | string no vacío | Sí | No | fila inválida si falta o está vacío |
| `timestamp_utc` | ISO 8601 con zona | Sí | No | conservar valor para diagnóstico; excluir la fila de vistas temporales si es naive o inválido |
| `timestamp_local` | ISO 8601 con zona | Sí | Sí | mostrar `N/D` si es null; advertir sin corregir si es inválido |
| `timestamp_type` | string no vacío | Sí | No | fila inválida; no inventar `unknown` |
| `source_artifact` | string no vacío | Sí | No | fila inválida; no inventar una fuente |
| `source_location` | string no vacío | Sí | No | fila inválida y warning de trazabilidad |
| `event_category` | string no vacío | Sí | No | fila inválida; no recategorizar |
| `event_action` | string no vacío | Sí | No | fila inválida; no inventar acción |
| `object` | string | Sí | Sí | mostrar `N/D` si es null |
| `description` | string no vacío | Sí | No | fila inválida; no generar descripción |
| `raw_evidence` | objeto, lista, escalar o null | Sí | Sí | mostrar bajo demanda; no sustituir el valor original |
| `parser_module` | string no vacío | Sí | No | fila inválida |
| `traceability_ref` | string no vacío | Sí | No | fila inválida y warning de trazabilidad |
| `confidence` | número entre 0 y 1 | Sí | No | fila inválida si falta, es booleano o queda fuera de rango |
| `provenance` | objeto | Sí | No | fila inválida si no es objeto; objeto vacío produce warning |
| `scenario_id` | string | Sí | Sí | mostrar `N/D` si es null |

Los campos forenses no se corrigen ni completan silenciosamente. Las filas que incumplen el contrato se separan del dataset canónico y aparecen en el informe de calidad de carga. Las columnas desconocidas se toleran y preservan como extensiones, pero no se usan en filtros o métricas hasta que exista un mapeo explícito. `CommonEvent` no contiene `is_synthetic`: la interfaz solo distingue contexto experimental mediante `scenario_id` o metadata de validación disponible.

## `timeline.csv`

Usa las mismas 16 columnas obligatorias. `raw_evidence` y `provenance` son strings JSON. El loader intenta parsearlos solo al solicitar detalle. `timestamp_utc` se convierte con formato mixto, UTC y error controlado; los valores naive o inválidos no se incorporan a vistas temporales. Se preserva el valor textual para diagnóstico.

Preferencia: cargar `events.json` como fuente canónica de detalle y usar `timeline.csv` para interoperabilidad o fallback. Si ambos existen, se compara recuento y conjunto de `event_id`; una discrepancia genera warning.

## `validation_summary_*.json`

Campos requeridos: `ground_truth_total`, `correct`, `partial`, `not_detected`, `false_positives`, `coverage_rate`, `correct_rate`, `precision_rate`, `average_time_delta_seconds`, `max_time_delta_seconds`, `traceability_rate`.

Los conteos son enteros no negativos; tasas están entre 0 y 1; deltas son números o null. Campos ausentes se muestran como `N/D`, sin recalcular salvo acción explícita del servicio.

## `validation_results_*.csv`

Header esperado:

```csv
gt_id,scenario_id,action,expected_time_utc,expected_object,expected_sources,matched_event_id,detected_time_utc,time_delta_seconds,result,matched_source,notes
```

En la ejecución por defecto, `result` admite `correcto`, `parcial` y `no_detectado`. Cuando se activa `--include-false-positives`, el validador actual también puede añadir filas `falso_positivo` y refleja su conteo agregado en `validation_summary_*.json`. La GUI usa siempre el resumen para el conteo y acepta las filas adicionales solo cuando están presentes; no las exige para cargar un resultado válido. `matched_event_id` es opcional y enlaza con `events.json`. Una referencia inexistente se muestra como match huérfano.

## `ground_truth_*.csv`

Header esperado:

```csv
gt_id,scenario_id,action,expected_object,start_time_utc,tolerance_seconds,expected_sources
```

La GUI lo trata como entrada de validación de solo lectura. `expected_sources` se divide por `|`; tolerancia debe ser no negativa; timestamp debe incluir zona. Filas inválidas se listan separadamente.

## Huella e invalidación

Cada carga registra ruta resuelta, tamaño y `mtime` de los outputs, no de las evidencias como timestamp forense. La cache se invalida si cambia cualquiera de esos valores o la versión del loader.

## Contrato de servicios

- `PipelineService.run(input_root, output_root) -> PipelineRunResult` es el contrato futuro de alto nivel de la GUI. Encapsulará `main.run_pipeline(input_root: str | Path, output_root: str | Path) -> dict` y traducirá su diccionario de resultados a un modelo de servicio estable.
- `EventRepository.load(output_root) -> EventDataset`.
- `EventRepository.filter(dataset, FilterState) -> EventView`.
- `ValidationRepository.discover/load(output_root) -> ValidationDataset`.
- `ExportService.export(view, format, destination, manifest) -> ExportResult`.

Los resultados incluyen warnings estructurados y nunca excepciones sin traducir a nivel de página.
