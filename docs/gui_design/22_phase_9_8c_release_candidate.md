# Fase 9.8c - Release candidate de composición y validación

## Objetivo

Esta fase corrige la composición bajo la cabecera nativa de Streamlit y alinea la presentación de validación con el comportamiento efectivo del validador. No modifica parsers, `CommonEvent`, correlación, validación ni reporters.

## Semántica de validación

El validador considera coincidencia de objeto cuando el valor esperado aparece en `object`, `description` o en la representación serializada de `raw_evidence`. El CSV de resultados conserva el evento emparejado, pero no identifica cuál de esos campos concreto produjo la coincidencia. Por esta razón, la tabla compacta de la GUI muestra:

| Columna | Significado |
| --- | --- |
| ID GT | identificador de la fila de ground truth |
| Resultado | `correcto`, `parcial` o `no_detectado` |
| Objeto esperado | valor definido en el ground truth |
| Evento | referencia abreviada del evento emparejado |
| Timestamp esperado | marca temporal del ground truth |
| Delta (s) | desviación temporal calculada |
| Trazabilidad | disponibilidad de referencia y procedencia |

El detalle secundario presenta el identificador completo, la fuente, el objeto normalizado, el timestamp detectado y la referencia de trazabilidad. Este reparto evita presentar el objeto normalizado como si fuera necesariamente el campo que resolvió el matching. En Registry, `ExampleApp` y `UpdaterTask` se mantienen como objetos esperados, mientras las rutas completas normalizadas se consultan en el detalle.

## Métricas

La GUI usa las claves del resumen sin intercambiarlas:

| Etiqueta visible | Clave | Definición actual |
| --- | --- | --- |
| Cobertura | `coverage_rate` | `(correct + partial) / ground_truth_total` |
| Tasa de correctos | `correct_rate` | `correct / ground_truth_total` |
| Precisión estricta | `precision_rate` | `correct / (correct + partial + false_positives)` |
| Trazabilidad | `traceability_rate` | proporción de coincidencias con referencia trazable |

Un test usa deliberadamente `correct_rate=0.50` y `precision_rate=0.75` para impedir regresiones de etiquetado.

## Confidence

`confidence` se presenta como información neutral y se acompaña de la advertencia: "Valor heurístico asignado por el parser; no representa una probabilidad estadística calibrada". No se utiliza color de éxito ni se calcula una media global.

## Conjuntos mixtos

La clasificación sintética solo reconoce los identificadores conocidos `S_BROWSER_SYNTH`, `S_PREFETCH_SYNTH` y `S_REGISTRY_SYNTH`. Los identificadores desconocidos no se clasifican como sintéticos. Se muestra un conteo exacto únicamente cuando los tres escenarios están representados de forma explícita; si existen eventos EVTX y solo parte de los identificadores conocidos está informada, la GUI muestra la nota genérica "Conjunto mixto: eventos sintéticos controlados y procesamiento EVTX real".

En el output empleado para las capturas solo las dos filas Registry conservan `scenario_id`. Por ello se usa la nota genérica y no se afirma que los siete eventos sintéticos puedan derivarse exclusivamente del contrato cargado.

## Composición bajo la cabecera

La separación se resuelve con `padding-top: 5rem` en el bloque principal. No se oculta la cabecera, no se emplea posición absoluta y no existen márgenes negativos.

| Tema | Viewport | scrollY | Cabecera inferior | Título superior | Separación |
| --- | ---: | ---: | ---: | ---: | ---: |
| Claro | 1440x1000 | 0 | 60 px | 80 px | 20 px |
| Claro | 1280x800 | 0 | 60 px | 80 px | 20 px |
| Claro | 1024x768 | 0 | 60 px | 80 px | 20 px |
| Oscuro | 1440x1000 | 0 | 60 px | 80 px | 20 px |
| Oscuro | 1280x800 | 0 | 60 px | 80 px | 20 px |
| Oscuro | 1024x768 | 0 | 60 px | 80 px | 20 px |

Las ocho pantallas se midieron además a 1440x1000 en ambos temas. Todas obtuvieron `scrollY=0`, cabecera a 60 px, título a 80 px y separación de 20 px, por encima del mínimo de 12 px. El detalle completo se conserva en `artifacts/gui_phase_9_2_9_8_release_candidate/geometry_audit.json`, fuera de Git.

## Calidad de Inicio

Los recuentos Aceptados, Rechazados, Trazables e Incidencias se muestran como líneas explícitas. No dependen del truncado interno de `st.metric` y permanecen completos en la composición de 1440x1000.

## Capturas

Las capturas se realizaron sobre el viewport visible de 1440x1000, sin `fullPage`, con `scrollY=0`, foco retirado de los campos y ausencia comprobada de mensajes `Press Enter to apply`, menús, loaders y overlays.

1. `01_inicio.png`.
2. `02_dashboard.png`.
3. `03_timeline.png`.
4. `04_explorador.png`.
5. `05_detalle_trazabilidad.png`.
6. `06_validacion_browserhistory.png`.
7. `07_validacion_prefetch.png`.
8. `08_validacion_registry.png`.
9. `09_exportacion.png`.
10. `10_ayuda_limitaciones.png`.
11. `11_dashboard_oscuro.png`.

Los PNG se guardan en `artifacts/gui_phase_9_2_9_8_release_candidate/screenshots/` y la selección de ocho imágenes en `artifacts/gui_phase_9_2_9_8_release_candidate/memory_shortlist/`. Ambas rutas están ignoradas.

## Verificación

- Python principal: `204 passed, 3 skipped`.
- Entorno GUI: `234 passed, 1 skipped`.
- Tests GUI: `152 passed, 1 skipped`.
- AppTest: `19 passed`.
- `compileall`: correcto.
- `pip check`: sin dependencias rotas.

La evidencia visual verifica composición y presentación, pero no constituye una nueva validación forense. No se realizó staging ni commit durante esta fase.
