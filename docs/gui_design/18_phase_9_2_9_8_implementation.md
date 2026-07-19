# Fases 9.2-9.8 - Implementación funcional de la GUI

## Objetivo

Las fases 9.2 a 9.8 convierten la infraestructura de carga de la Fase 9.1 en una aplicación local completa para revisar outputs, explorar eventos, inspeccionar trazabilidad, contextualizar validaciones, descargar subconjuntos y ejecutar el pipeline existente. La interfaz no sustituye la lógica forense: consume `events.json`, `timeline.csv`, resultados de validación y la función pública `main.run_pipeline()`.

## Arquitectura implementada

```text
Streamlit pages
  -> componentes reutilizables
  -> servicios puros de dashboard, filtros, timeline, paginación,
     detalle, validación, exportación y ejecución
  -> repositorios de solo lectura de Fase 9.1
  -> outputs existentes / main.run_pipeline()
```

Las páginas se encuentran en `gui/pages/`. El estado compartido mantiene la raíz activa, resultados cargados, filtros, selección de evento, escenario seleccionado y última ejecución. Los servicios no dependen de Streamlit salvo los wrappers de caché de `gui/runtime.py`.

## Navegación y pantallas

La navegación usa `st.navigation` y `st.Page`, disponibles en Streamlit 1.59.2. Se implementaron ocho pantallas:

1. **Inicio y ejecución:** carga outputs o ejecuta un análisis aislado.
2. **Dashboard:** presenta métricas descriptivas y cinco visualizaciones Plotly.
3. **Timeline:** cambia entre puntos individuales y agregación declarada.
4. **Explorador:** filtra, ordena y pagina eventos.
5. **Detalle y trazabilidad:** separa evento normalizado, ubicación, evidencia y procedencia.
6. **Validación:** mantiene escenarios y métricas independientes.
7. **Exportación:** genera CSV, JSON y JSONL en memoria.
8. **Ayuda y limitaciones:** documenta alcance, privacidad e interpretación.

## Dashboard y timeline

El Dashboard muestra total de eventos, fuentes, rango UTC, trazabilidad, escenarios e incidencias. Las gráficas representan eventos por fuente y categoría, actividad temporal, `confidence` por fuente y trazabilidad por fuente. No se calcula una confianza media global: `confidence` se trata como indicador heurístico propio de cada parser.

La Timeline usa un punto por evento hasta 5.000 timestamps válidos. Por encima del umbral agrega por minuto, hora, día o semana y avisa del cambio de representación. Los timestamps inválidos quedan fuera de la visualización temporal, pero no se eliminan del dataset cargado.

## Exploración y trazabilidad

Los filtros abarcan rango UTC, fuente, categoría, acción, parser, escenario, texto, trazabilidad y `confidence`. Se implementan como operaciones vectorizadas sobre copias de DataFrame. El Explorador renderiza 25, 50 o 100 filas por página y conserva el `event_id` seleccionado durante la navegación.

El detalle mantiene visibles los campos normalizados y despliega `raw_evidence` y `provenance` en bloques independientes. Las rutas se reducen al nombre final salvo activación explícita. Se advierte de timestamps inválidos, procedencia incompleta o escenario sintético únicamente cuando existe un identificador explícito.

## Validación

La página detecta todos los pares o elementos huérfanos `validation_summary_*.json` y `validation_results_*.csv`. `default` se presenta como escenario no clasificado. Las métricas ausentes se muestran como no disponibles y el resumen JSON sigue siendo la fuente principal del conteo de falsos positivos; las filas `falso_positivo` son opcionales.

Los resultados se enlazan con `matched_event_id` para mostrar objeto detectado y disponibilidad de trazabilidad. Cada escenario conserva sus métricas y gráficas; no se calcula una precisión global entre escenarios heterogéneos. La pantalla mantiene una advertencia sobre el alcance de la validación sintética y no atribuye ground truth controlado a EVTX real.

## Ejecución segura

`PipelineService` llama directamente a `main.run_pipeline(input_root, output_root)`. No utiliza `subprocess`, `shell=True` ni comandos construidos con texto. Valida existencia y lectura de evidencias, escritura de salida y relaciones peligrosas entre raíces. Cada ejecución crea de forma atómica `<output_root>/gui_runs/YYYYMMDD_HHMMSS_microseconds_<suffix>`, evitando colisiones concurrentes.

El resultado distingue éxito, parcial y error. Los errores de parser convierten la ejecución en parcial, mientras que las excepciones de frontera se sanitizan. Al terminar, la GUI carga automáticamente el nuevo directorio. Una prueba real generó 1.465 eventos y confirmó que tamaño y `mtime_ns` de las evidencias permanecieron sin cambios.

## Exportación y privacidad

Las exportaciones se construyen en memoria y requieren una descarga explícita. CSV, JSON y JSONL contienen las 16 claves canónicas de `CommonEvent`; los campos internos `_ui_*` no salen de la GUI. El manifest opcional conserva filtros y conteos, pero solo incluye el nombre de la carpeta de origen. Una advertencia recuerda que los datos exportados pueden contener información sensible.

La configuración fija loopback, modo headless y telemetría desactivada. No existe HTML inseguro, red externa ni escritura automática de exports. Los errores visibles no incluyen traceback ni vuelcan evidencia completa.

## Rendimiento medido

Las mediciones realizadas en el equipo de desarrollo fueron:

| Filas | Filtro combinado | Agregación por hora |
| ---: | ---: | ---: |
| 1.000 | 0,017 s | 0,004 s |
| 10.000 | 0,185 s | 0,004 s |
| 100.000 | 1,612 s | 0,009 s |

La carga de los 1.465 eventos reales disponibles requirió 0,116 s, sin rechazos ni incidencias. Estas cifras describen una ejecución concreta y no constituyen garantía de rendimiento en otros equipos. El navegador no recibe 100.000 puntos: la tabla pagina y la timeline agrega el volumen superior al umbral.

## Pruebas

La suite añadida cubre métricas, datasets vacíos, timestamps inválidos, timeline detallada y agregada, paginación, ordenación, selección, enmascarado de rutas, trazabilidad, métricas ausentes, `default` no clasificado, exportaciones canónicas, Unicode, manifest, rutas peligrosas, colisiones de salida y excepciones controladas. AppTest verifica arranque, navegación y páginas con datos sintéticos cargados.

La ejecución del pipeline se prueba con mocks en tests unitarios y una vez con evidencias locales en una ruta ignorada. No se modificaron parsers, `CommonEvent`, correlador, validador ni reporters.

## Diferencias respecto al diseño previo

- La selección de la Timeline se completa con un selector de `event_id`, porque ofrece un comportamiento estable y testeable incluso si la selección directa de Plotly cambia entre versiones.
- Las exportaciones no escriben en un directorio: se entregan mediante `st.download_button`, reduciendo colisiones y efectos laterales.
- Los servicios se organizan por responsabilidad y los componentes solo contienen presentación compartida; no se crearon módulos vacíos previstos para trabajo futuro.
- La ejecución es síncrona porque `main.run_pipeline()` no expone progreso. La GUI muestra actividad indeterminada y bloquea el botón durante el rerun, sin inventar porcentajes.
- El rediseño `Forensic Clarity` centraliza Streamlit y Plotly, sustituye la apariencia genérica por una identidad local y mantiene intactos servicios y contratos.
- La vista agregada de Timeline declara el total real de eventos representados, además del umbral y la granularidad.

## Limitaciones pendientes

- Streamlit mantiene el dataset aceptado en memoria durante la sesión.
- La ejecución del pipeline bloquea la sesión hasta terminar.
- No se realizó una evaluación formal de usabilidad con participantes.
- La accesibilidad se apoya en controles nativos, etiquetas y contraste, pero requiere auditoría con teclado, zoom y tecnologías asistivas.
- No existe empaquetado como aplicación de escritorio.
- El estado de sesión no se conserva después de cerrar el servidor.
- La carga de `raw_evidence` y `provenance` es diferida en pantalla, aunque los objetos ya están en memoria.

## Trabajo posterior

La revisión externa debe comprobar las capturas, el comportamiento en navegador y los riesgos pendientes. La integración en la memoria académica se realizará en una fase separada; no se modificaron los documentos DOCX o PDF durante esta implementación.
