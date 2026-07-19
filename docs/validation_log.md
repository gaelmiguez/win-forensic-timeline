# Validation Log

## 2026-06-20 - Estado inicial

Todavía no existe validación experimental real porque los parsers forenses complejos no se han implementado. Se crea el esquema inicial `validation/ground_truth.csv` y se reserva el módulo `validation/validator.py` para comparar resultados contra escenarios controlados en fases posteriores.

## 2026-06-20 - Validación sintética BrowserHistory

Se crea una base SQLite sintética compatible con Chromium mediante `scripts/generate_sample_browser_history.py`.

- Evidencia: `evidence/browser/sample/History`.
- Tablas utilizadas: `urls` y `visits`.
- Eventos esperados: 3 visitas web.
- Eventos generados: 3 eventos `BrowserHistory`.
- Resultado: validación sintética correcta para el flujo de parsing, normalización temporal, correlación y reporting.

Esta validación no sustituye a una evaluación experimental con una VM o imagen forense real, pero permite comprobar de forma reproducible el comportamiento mínimo del parser de navegador.

## 2026-06-20 - Fase 3.2 - Prueba inicial con EVTX reales

Se realiza una exportación controlada de registros Windows Event Log mediante `wevtutil` para probar el parser EVTX inicial con evidencias reales.

- Logs solicitados: `Application`, `System`.
- Ventana temporal: últimas 24 horas.
- Ficheros exportados:
  - `evidence/evtx/windows_export/Application.evtx` (`1118208` bytes).
  - `evidence/evtx/windows_export/System.evtx` (`1118208` bytes).
- Total de eventos generados por el pipeline: `1495`.
- Eventos `EVTX`: `1492`.
- Eventos `BrowserHistory`: `3`.
- Eventos EVTX por canal:
  - `Application`: `633`.
  - `System`: `859`.
- Tests automatizados: `29 passed`.
- Resultado: el pipeline procesa EVTX reales y conserva la evidencia sintética de navegador.

Problemas observados:

- La primera ejecución del pipeline falló al mezclar timestamps ISO 8601 con distinta precisión de microsegundos entre fuentes. Se ajustó la conversión del correlator para aceptar formatos ISO mixtos.
- La validación con EVTX reales sigue siendo inicial: no se ha contrastado todavía contra ground truth experimental.

Nota de privacidad:

- Las evidencias reales permanecen en `evidence/`, que está ignorado por Git.
- No se almacena XML completo en la salida normalizada.
- Los resultados publicados deben anonimizar nombres de equipo, usuarios, SID y rutas personales si aparecen.

Nota de saneamiento posterior:

- La exportación con filtro temporal mediante `wevtutil` funcionó correctamente para `Application` y `System`.
- Se procesaron `1492` eventos `EVTX`.
- Se detectó un problema inicial al mezclar timestamps ISO 8601 con y sin microsegundos.
- El problema se resolvió en el correlator usando `format="mixed"` y se añadió un test de regresión.
- El intervalo temporal del reporte combina evidencia `BrowserHistory` sintética de 2024 con EVTX reales de 2026; no debe interpretarse como un escenario experimental único.
- Las evidencias reales permanecen en `evidence/`, que está ignorado por Git.
- No se almacena XML completo en `raw_evidence`.

## 2026-06-20 - Fase 4.2 - Validación controlada con BrowserHistory sintético

Se ejecuta una validación controlada del motor ground truth usando la evidencia sintética generada por `scripts/generate_sample_browser_history.py`.

- Ground truth usado: `validation/ground_truth_browser_synthetic.csv`.
- Eventos esperados: `3`.
- Fuente esperada: `BrowserHistory`.
- `correct`: `3`.
- `partial`: `0`.
- `not_detected`: `0`.
- `false_positives`: `0`.
- `coverage_rate`: `1.0`.
- `correct_rate`: `1.0`.
- `precision_rate`: `1.0`.
- `average_time_delta_seconds`: `0.0`.
- `max_time_delta_seconds`: `0.0`.
- `traceability_rate`: `1.0`.

Los EVTX reales pueden coexistir en `output/events.json`, pero no forman parte de este ground truth porque `expected_sources` se limita a `BrowserHistory`. El cálculo de falsos positivos no se activa por defecto, por lo que los eventos EVTX reales no penalizan esta validación controlada.

Esta validación sirve como primera prueba cuantificada y reproducible del motor de validación.

Esta prueba valida el funcionamiento del motor de comparación en un escenario controlado, pero no sustituye a una validación experimental completa con múltiples artefactos.

## 2026-06-20 - Fase 5.2 - Ejecución del escenario S01

Se ejecuta el escenario `S01_BROWSER_EVTX` mediante `scripts/run_scenario_s01_browser_evtx.py`, usando rutas aisladas bajo `evidence/scenarios/s01/` y `output/scenarios/s01/`.

- `eventcreate` disponible: sí.
- Eventos EVTX controlados generados: no.
- Motivo: `eventcreate` devolvió `Acceso denegado` para los Event ID `901` y `902`.
- Exportación de `Application.evtx`: no se ejecutó, al no generarse eventos EVTX controlados.
- Filas de ground truth generadas: `3`.
- Fuentes en ground truth: `BrowserHistory`.
- Eventos normalizados del escenario: `3`.
- Eventos por fuente: `BrowserHistory=3`, `EVTX=0`.
- EVTX `901` detectado: no.
- EVTX `902` detectado: no.

Métricas del validador:

- `ground_truth_total`: `3`.
- `correct`: `3`.
- `partial`: `0`.
- `not_detected`: `0`.
- `false_positives`: `0`.
- `coverage_rate`: `1.0`.
- `correct_rate`: `1.0`.
- `precision_rate`: `1.0`.
- `average_time_delta_seconds`: `0.0`.
- `max_time_delta_seconds`: `0.0`.
- `traceability_rate`: `1.0`.

Limitaciones observadas:

- La generación EVTX controlada requiere permisos suficientes para escribir eventos en el log `Application`.
- El escenario combinado queda pendiente de una ejecución con permisos adecuados o con una alternativa controlada equivalente.
- La validación BrowserHistory permanece correcta y reproducible dentro del escenario S01.
- Las evidencias y outputs del escenario permanecen en `evidence/` y `output/`, ambos excluidos de Git.

## 2026-06-20 - Fase 6.2 - Validación Prefetch mediante metadata externa

Se ejecuta una validación controlada de eventos Prefetch generados desde metadata externa JSON sidecar.

- Ground truth usado: `validation/ground_truth_prefetch_synthetic.csv`.
- Eventos esperados: `2`.
- Fuente esperada: `Prefetch`.
- Eventos esperados:
  - `NOTEPAD.EXE` a `2024-01-10T09:15:00Z`.
  - `POWERSHELL.EXE` a `2024-01-10T09:20:00Z`.
- `correct`: `2`.
- `partial`: `0`.
- `not_detected`: `0`.
- `false_positives`: `0`.
- `coverage_rate`: `1.0`.
- `correct_rate`: `1.0`.
- `precision_rate`: `1.0`.
- `average_time_delta_seconds`: `0.0`.
- `max_time_delta_seconds`: `0.0`.
- `traceability_rate`: `1.0`.

La validación utiliza metadata JSON controlada asociada a ficheros `.pf` placeholder. El parsing binario nativo de Prefetch queda pendiente de validación con un backend real o una herramienta externa documentada.

## 2026-06-20 - Fase 7.1 - Validación Registry mediante metadata externa

Se ejecuta una validación controlada de eventos Registry generados desde metadata externa JSON.

- Ground truth usado: `validation/ground_truth_registry_synthetic.csv`.
- Eventos esperados: `2`.
- Fuente esperada: `Registry`.
- Eventos esperados:
  - `ExampleApp` a `2024-01-10T09:25:00Z`.
  - `UpdaterTask` a `2024-01-10T09:30:00Z`.
- `correct`: `2`.
- `partial`: `0`.
- `not_detected`: `0`.
- `false_positives`: `0`.
- `coverage_rate`: `1.0`.
- `correct_rate`: `1.0`.
- `precision_rate`: `1.0`.
- `average_time_delta_seconds`: `0.0`.
- `max_time_delta_seconds`: `0.0`.
- `traceability_rate`: `1.0`.

La validación utiliza metadata JSON controlada para representar entradas de autorun `Run` y `RunOnce`. El parser no accede al Registro real, no modifica claves reales y no realiza parsing binario de hives; esa capacidad queda pendiente para una fase posterior con backend o herramienta externa documentada.
