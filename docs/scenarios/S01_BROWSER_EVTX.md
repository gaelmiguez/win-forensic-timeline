# S01_BROWSER_EVTX

## Objetivo

El escenario `S01_BROWSER_EVTX` prepara una validación controlada que combina actividad de navegador sintética y, cuando el entorno lo permite, eventos controlados del registro Windows Event Log `Application`.

El objetivo es disponer de evidencias y ground truth dinámico para ejecutar el pipeline completo y el motor de validación sin mezclar resultados con las carpetas globales del prototipo.

## Artefactos usados

- `BrowserHistory`: base SQLite Chromium `History` generada por el propio escenario.
- `EVTX`: exportación del canal `Application` mediante `wevtutil`, precedida por eventos controlados generados con `eventcreate` si la herramienta está disponible.

## Acciones esperadas

El escenario genera tres visitas de navegador distribuidas en los dos minutos previos a la ejecución. La marca base se calcula como `now - 120s`, por lo que los offsets de 0, 60 y 120 segundos producen eventos recientes ya ocurridos.

| URL | Offset |
| --- | -----: |
| `https://example.com/` | 0 segundos |
| `https://www.incibe.es/` | 60 segundos |
| `https://www.osi.es/` | 120 segundos |

Opcionalmente intenta generar dos eventos EVTX controlados:

| Canal | Event ID | Descripción |
| ----- | -------: | ----------- |
| Application | 901 | `WinForensicTimeline S01 controlled event start` |
| Application | 902 | `WinForensicTimeline S01 controlled event end` |

Si `eventcreate` no está disponible o falla por permisos, el escenario continúa solo con BrowserHistory.

## Rutas

Evidencia del escenario:

```text
evidence/scenarios/s01/
```

Output del escenario:

```text
output/scenarios/s01/
```

Ficheros principales:

```text
evidence/scenarios/s01/browser/sample/History
evidence/scenarios/s01/evtx/windows_export/Application.evtx
output/scenarios/s01/ground_truth_s01_browser_evtx.csv
output/scenarios/s01/events.json
output/scenarios/s01/validation_results_s01.csv
output/scenarios/s01/validation_summary_s01.json
output/scenarios/s01/validation_report_s01.md
```

## Ground Truth Dinámico

El ground truth se genera en:

```text
output/scenarios/s01/ground_truth_s01_browser_evtx.csv
```

Este fichero no se versiona porque contiene marcas temporales generadas en tiempo de ejecución. Las filas BrowserHistory usan la marca `scenario_start_utc` y offsets de 0, 60 y 120 segundos. Las filas EVTX solo se añaden si los eventos controlados se generan y se exporta `Application.evtx`.

## Procedimiento de Ejecución

Ejecución completa con intento de EVTX:

```bash
python scripts/run_scenario_s01_browser_evtx.py --overwrite
```

Variante portable sin EVTX:

```bash
python scripts/run_scenario_s01_browser_evtx.py --overwrite --skip-evtx
```

El script ejecuta por defecto:

```bash
python main.py --input evidence/scenarios/s01 --output output/scenarios/s01
```

Y después:

```bash
python -m validation.validator --events output/scenarios/s01/events.json --ground-truth output/scenarios/s01/ground_truth_s01_browser_evtx.csv --output output/scenarios/s01/validation_results_s01.csv --summary output/scenarios/s01/validation_summary_s01.json --report output/scenarios/s01/validation_report_s01.md
```

## Opciones Útiles

- `--skip-evtx`: ejecuta solo la parte BrowserHistory.
- `--no-run-pipeline`: genera evidencias y ground truth, sin ejecutar el pipeline.
- `--no-run-validator`: ejecuta evidencias y pipeline, sin lanzar el validador.
- `--evtx-last-hours`: ajusta la ventana temporal usada al exportar `Application.evtx`.
- `--evtx-no-time-filter`: pasa `--no-time-filter` al exportador EVTX para permitir un fallback sin filtro temporal.
- `--event-source`: define el origen usado por `eventcreate`.
- `--python-executable`: permite indicar un runtime Python concreto.

## Resultado de ejecución inicial

La ejecución inicial del escenario se realizó con intento de generación EVTX controlada.

- `eventcreate` disponible: sí.
- Generación EVTX controlada: no.
- Motivo: `Acceso denegado`.
- Exportación EVTX: no ejecutada, al no generarse eventos controlados.
- Resultado final del escenario: BrowserHistory validado correctamente.

Métricas obtenidas para la parte BrowserHistory:

| Métrica | Valor |
| ------- | ----: |
| ground_truth_total | 3 |
| correct | 3 |
| partial | 0 |
| not_detected | 0 |
| false_positives | 0 |
| coverage_rate | 1.0 |
| correct_rate | 1.0 |
| precision_rate | 1.0 |
| traceability_rate | 1.0 |

El EVTX controlado queda pendiente de ejecución en un entorno con permisos adecuados para escribir eventos en el log `Application`.

## Interpretación

El escenario funciona como orquestador reproducible de evidencias, pipeline y validación sobre rutas aisladas. La parte BrowserHistory queda validada de forma controlada, con tres eventos esperados detectados correctamente y trazabilidad completa.

El intento de generación EVTX identifica una limitación operativa real: la escritura de eventos controlados en `Application` puede requerir permisos elevados o una configuración específica del entorno. El prototipo no fuerza elevación ni aplica cambios de configuración del sistema; registra la limitación y continúa con el subconjunto de evidencias disponible.

Por tanto, la validación combinada BrowserHistory + EVTX queda pendiente. La ejecución actual debe interpretarse como una validación reproducible del flujo S01 con fallback BrowserHistory y como una comprobación de las condiciones necesarias para incorporar EVTX controlado.

## Limitaciones

- La generación EVTX depende de herramientas nativas de Windows y permisos del usuario.
- La marca temporal de EVTX se registra de forma aproximada alrededor de la llamada a `eventcreate`; por eso usa una tolerancia amplia de 120 segundos.
- La variante `--skip-evtx` valida la infraestructura del escenario, pero solo cubre BrowserHistory.
- El escenario no sustituye una validación experimental completa con más acciones, usuarios y artefactos.

## Privacidad

Las evidencias y salidas del escenario se guardan bajo `evidence/` y `output/`, carpetas ignoradas por Git. No deben versionarse `.evtx`, bases SQLite generadas ni outputs con datos de eventos reales. El script no imprime XML completo ni contenido de eventos EVTX reales.
