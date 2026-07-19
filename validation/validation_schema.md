# Esquema de Validación

Este documento define el esquema de validación experimental del prototipo. El motor de validación compara los eventos normalizados contra ground truth, genera resultados por evento esperado y calcula métricas cuantificadas de cobertura, precisión, desviación temporal y trazabilidad.

## `ground_truth.csv`

El fichero `ground_truth.csv` describe los eventos esperados en escenarios controlados.

Columnas:

- `gt_id`: identificador único del evento esperado dentro del conjunto de validación.
- `scenario_id`: identificador del escenario experimental.
- `action`: acción esperada, alineada con `event_action` cuando sea posible.
- `expected_object`: objeto esperado asociado a la acción, por ejemplo una URL, ejecutable, clave de registro o identificador de evento.
- `start_time_utc`: marca temporal esperada de inicio en UTC, en formato ISO 8601.
- `tolerance_seconds`: margen temporal permitido para considerar que un evento detectado corresponde al evento esperado.
- `expected_sources`: fuentes o artefactos esperados, separados por `|` si hay más de uno.

Header definitivo:

```csv
gt_id,scenario_id,action,expected_object,start_time_utc,tolerance_seconds,expected_sources
```

## `validation_results.csv`

El fichero `validation_results.csv` recogerá el resultado de comparar la timeline generada contra el ground truth.

Columnas:

- `gt_id`: identificador del evento esperado evaluado.
- `scenario_id`: identificador del escenario experimental.
- `action`: acción evaluada.
- `expected_time_utc`: marca temporal esperada en UTC.
- `expected_object`: objeto esperado definido en el ground truth.
- `expected_sources`: fuentes esperadas definidas en el ground truth.
- `matched_event_id`: identificador `event_id` del evento detectado que se ha emparejado, si existe.
- `detected_time_utc`: marca temporal UTC del evento detectado.
- `time_delta_seconds`: diferencia absoluta o firmada entre el evento esperado y el detectado, según se defina en la implementación.
- `result`: resultado de la comparación.
- `matched_source`: artefacto de origen del evento detectado.
- `notes`: observaciones adicionales sobre el emparejamiento o el fallo de detección.

Header previsto:

```csv
gt_id,scenario_id,action,expected_time_utc,expected_object,expected_sources,matched_event_id,detected_time_utc,time_delta_seconds,result,matched_source,notes
```

## `validation_summary.json`

El fichero `validation_summary.json` resume métricas agregadas de la ejecución del validador.

Campos:

- `ground_truth_total`: número de filas válidas evaluadas del ground truth.
- `correct`: número de eventos esperados detectados correctamente.
- `partial`: número de eventos detectados con coincidencia temporal y de fuente, pero con discrepancia de objeto u otra diferencia menor.
- `not_detected`: número de eventos esperados sin coincidencia.
- `false_positives`: número de eventos detectados no emparejados, calculados de forma conservadora cuando se activa la opción correspondiente.
- `coverage_rate`: proporción `(correct + partial) / ground_truth_total`.
- `correct_rate`: proporción `correct / ground_truth_total`.
- `precision_rate`: proporción `correct / (correct + partial + false_positives)` cuando el denominador es mayor que cero.
- `average_time_delta_seconds`: desviación temporal media de los eventos emparejados.
- `max_time_delta_seconds`: desviación temporal máxima de los eventos emparejados.
- `traceability_rate`: proporción de eventos emparejados que conservan `provenance`.

## Resultados posibles

- `correcto`: el evento esperado se detecta dentro de la tolerancia temporal y con fuente compatible.
- `parcial`: el evento se detecta, pero presenta diferencias relevantes, por ejemplo una fuente inesperada, objeto incompleto o desviación temporal cercana al límite.
- `no_detectado`: no se encuentra un evento que corresponda al ground truth.
- `falso_positivo`: se genera un evento no esperado por el ground truth del escenario.

## Notas de implementación futura

La validación deberá preservar trazabilidad hacia `CommonEvent.event_id`, `traceability_ref`, `source_artifact` y `source_location`. También deberá documentar el criterio de emparejamiento temporal y semántico aplicado para cada familia de artefactos.
