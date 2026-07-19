# Plan de implementación de la GUI

## Estado de implementación de 9.2 a 9.8

Las fases funcionales se implementaron de forma conjunta sobre la infraestructura de 9.1. El código real utiliza páginas bajo `gui/pages/`, componentes reutilizables y servicios puros para dashboard, timeline, paginación, detalle, validación, exportación y ejecución. `PipelineService` encapsula la función pública existente `main.run_pipeline()` sin `subprocess`; las descargas se generan en memoria y la timeline declara cuándo cambia a modo agregado.

La medición local cubrió 1.000, 10.000 y 100.000 filas sintéticas. El caso de 100.000 filas tardó 1,53 s en aplicar un filtro combinado y 0,007 s en agregar por hora en el equipo de desarrollo. Esta medida no representa un SLA. Persisten como trabajo posterior el empaquetado, la evaluación formal con usuarios y la verificación completa de accesibilidad con tecnologías asistivas.

## 9.1 - Infraestructura GUI y carga de datos

- Objetivo implementado: aplicación Streamlit mínima, modelos tipados, loaders seguros, catálogo y filtros desacoplados.
- Archivos reales: `requirements-gui.txt`, `.streamlit/config.toml`, `gui/models.py`, `gui/app.py`, `gui/components/load_status.py`, servicios bajo `gui/services/` y tests bajo `tests/gui/` con fixtures en `tests/fixtures/gui/`.
- Reconciliación: se utiliza un único `gui/models.py` porque los modelos de infraestructura aún son reducidos; no se crean módulos o páginas vacías para fases futuras. Los tests se agrupan por servicio para mantener correspondencia directa con la implementación.
- Tests: rutas, archivos válidos, vacíos y corruptos, columnas ausentes o extra, carga parcial, duplicados, timestamps, validaciones múltiples, filtros combinados, caché y smoke test AppTest.
- Dependencias verificadas: Python 3.14.6, Streamlit 1.59.2, Plotly 6.9.0 y Pandas 3.0.3 en `.venv-gui`; la CLI principal conserva sus dependencias separadas.
- Riesgos vigentes: memoria al cargar JSON completo, reruns, estado de sesión, exposición de rutas y rendimiento por encima del volumen probado.
- Aceptación alcanzada: abre outputs existentes en solo lectura, muestra calidad de carga y no importa parsers ni ejecuta el pipeline.
- Entregables: shell funcional, repositorios de eventos/timeline/validación, catálogo, filtros y suite GUI.
- Commit esperado: `Añade infraestructura inicial de la GUI`.

## 9.2 - Dashboard

- Objetivo: métricas globales y gráficas agregadas.
- Archivos: `gui/pages/dashboard.py`, `gui/components/metrics.py`.
- Tests: conteos, intervalos, trazabilidad, dataset vacío y distribuciones o estadísticos de `confidence` por fuente sin media global.
- Dependencias: Plotly ya fijado en 9.1.
- Riesgos: inferir real/sintético sin dato explícito.
- Aceptación: todas las métricas incluyen definición y warnings de calidad.
- Entregables: dashboard responsive y accesible.
- Commit esperado: `Añade dashboard forense`.

## 9.3 - Timeline interactiva

- Objetivo: zoom, rango, fuentes y agregación adaptativa.
- Archivos: `gui/pages/timeline.py`, `gui/components/timeline_chart.py`.
- Tests: granularidad, rangos, selección y 100.000 eventos sintéticos.
- Dependencias: repositorio tipado y Plotly.
- Riesgos: saturación del navegador y selección ambigua de agregados.
- Aceptación: no renderizar miles de puntos cuando excede umbral; UTC visible.
- Entregables: timeline con drill-down y resumen textual.
- Commit esperado: `Añade timeline interactiva`.

## 9.4 - Explorador de eventos

- Objetivo: filtros combinables, búsqueda, tabla paginada y selección.
- Archivos: `gui/pages/event_explorer.py`, `filters.py`, `event_table.py`, `filter_state.py`.
- Tests: cada filtro, composición, nulls, restablecimiento y paginación.
- Dependencias: Pandas existente.
- Riesgos: búsquedas costosas en JSON bruto.
- Aceptación: filtros vectorizados, chips visibles y cero resultados explicativo.
- Entregables: explorador completo.
- Commit esperado: `Añade explorador y filtros de eventos`.

## 9.5 - Detalle y trazabilidad

- Objetivo: mostrar `CommonEvent`, tiempo, evidencia y procedencia.
- Archivos: `event_detail.py`, `provenance_view.py`, `warnings.py`.
- Tests: evento completo, provenance vacío, JSON grande y campos sensibles.
- Dependencias: ninguna nueva.
- Riesgos: exponer rutas o cargar evidencia pesada.
- Aceptación: separación visual normalizado/original/decisiones; carga diferida.
- Entregables: panel de auditoría por evento.
- Commit esperado: `Añade detalle y trazabilidad de eventos`.

## 9.6 - Validación

- Objetivo: descubrir validaciones, mostrar métricas y enlazar matches.
- Archivos: `validation_repository.py`, `gui/pages/validation.py`.
- Tests: summary/results completos, ausentes, inválidos y match huérfano.
- Dependencias: ninguna nueva.
- Riesgos: presentar 1.0 como rendimiento general.
- Aceptación: advertencia visible, definiciones y comparación GT-evento.
- Entregables: vista de validación.
- Commit esperado: `Integra resultados de validación en la GUI`.

## 9.7 - Ejecución del pipeline desde GUI

- Objetivo: validar rutas, encapsular `main.run_pipeline(input_root, output_root) -> dict` en `PipelineService.run(...)` y mostrar progreso/warnings.
- Archivos: `pipeline_service.py`, `gui/pages/home.py`.
- Tests: éxito, parcial, fallo, rutas y doble ejecución.
- Dependencias: API existente de `main.py`; posible refactor mínimo futuro para callbacks de progreso.
- Riesgos: bloqueo de UI y outputs parciales.
- Aceptación: no invocar parsers desde pantalla, no usar `shell=True`, no escribir en evidencia.
- Entregables: flujo end-to-end local.
- Commit esperado: `Permite ejecutar el pipeline desde la GUI`.

## 9.8 - Exportación

- Objetivo: exportar subconjuntos filtrados y validaciones con manifiesto.
- Archivos: `export_service.py`, `gui/pages/export.py`.
- Tests: formatos, columnas, filtros, colisiones y destinos inválidos.
- Dependencias: reporters existentes cuando sean reutilizables.
- Riesgos: sobrescritura o exposición de datos sensibles.
- Aceptación: confirmación, manifiesto y advertencia de privacidad.
- Entregables: exportación reproducible.
- Commit esperado: `Añade exportación filtrada desde la GUI`.

## 9.9 - Robustez, rendimiento y accesibilidad

- Objetivo: endurecer errores, cache, volumen y navegación accesible.
- Archivos: suite GUI, benchmarks, estilos y ayuda contextual.
- Tests: 100.000 eventos, fallos de schema, teclado, contraste y zoom.
- Dependencias: herramientas de test elegidas tras comprobar soporte Streamlit.
- Riesgos: optimizaciones prematuras o cache obsoleta.
- Aceptación: presupuestos medidos, errores recuperables y checklist de accesibilidad.
- Entregables: informe de QA y correcciones.
- Commit esperado: `Sanea rendimiento y accesibilidad de la GUI`.

## 9.10 - Consolidación documental y memoria

- Objetivo: cerrar documentación, capturas, validación de usabilidad y memoria.
- Archivos: README, ADR, fragmentos TFM, manual de uso y DOCX en fase específica.
- Tests: suite completa, smoke final y ejecución reproducible.
- Dependencias: ninguna funcional nueva.
- Riesgos: documentar capacidades no implementadas o capturas sensibles.
- Aceptación: documentación coincide con código, capturas anonimizadas y métricas contextualizadas.
- Entregables: release técnica y material para memoria.
- Commit esperado: `Consolida interfaz gráfica y documentación final`.

## Orden y disciplina

Cada fase comienza con working tree limpio, añade tests proporcionales, ejecuta la suite completa y no versiona `evidence/` ni `output/`. Los commits propuestos son orientativos y no se crean en la Fase 9.0.
