# ADR-0009 - Validador ground truth

## Contexto

El prototipo necesita una forma objetiva de comparar eventos reconstruidos contra acciones esperadas en escenarios controlados. Esta capacidad permite obtener métricas como cobertura, precisión, desviación temporal y trazabilidad, necesarias para evaluar el comportamiento de la herramienta de forma reproducible.

## Decisión

Se implementa un validador basado en `ground_truth.csv` y `events.json`. El validador compara eventos por fuente, objeto esperado y tolerancia temporal, generando resultados CSV, resumen JSON y reporte Markdown.

El motor se ejecuta de forma independiente mediante `python -m validation.validator`, sin alterar el comportamiento por defecto del pipeline principal.

## Alternativas consideradas

- Validación manual de la timeline.
- Validación integrada directamente en `main.py`.
- Validación externa con notebooks o scripts ad hoc.
- Retrasar la validación hasta tener más parsers.

## Justificación

Separar la validación del pipeline principal permite repetir experimentos sin modificar la ejecución de extracción, parsing, normalización y reporting. El validador genera métricas cuantificables, facilita la trazabilidad en la memoria del TFM y evita depender de revisión manual.

La decisión también permite validar escenarios sintéticos controlados, como el historial de navegador, antes de diseñar una evaluación experimental más amplia con múltiples artefactos.

## Limitaciones

El resultado depende de la calidad y granularidad del ground truth. La comparación semántica de objetos es básica y se apoya en coincidencias exactas o parciales sobre `object`, `description` y `raw_evidence`. El cálculo de falsos positivos es conservador y solo se amplía cuando se usa la opción correspondiente.

La validación inicial no sustituye escenarios más amplios y puede requerir tolerancias específicas por tipo de artefacto.

## Impacto en el TFM

El validador permite presentar resultados cuantificados y aporta una base experimental para discutir cobertura, precisión, desviación temporal y trazabilidad. También responde a la necesidad de evaluar la consistencia de la herramienta de forma reproducible.

Esta decisión crea una base para futuras validaciones con EVTX, Prefetch y Registro, así como para comparar resultados por escenario y por artefacto.
