# Revisión antes y después del rediseño

## Comparación

| Área | Antes | Después |
| --- | --- | --- |
| Identidad | Streamlit genérico y botón Deploy visible | marca propia, descriptor, navegación agrupada y contexto local |
| Jerarquía | títulos y métricas sobredimensionados | cabecera compacta, tira de métricas y contenido prioritario |
| Dashboard | cinco gráficas con peso similar | actividad temporal dominante, fuente secundaria y análisis en tabs |
| Timeline | filtros dominantes y modo poco visible | toolbar compacta, modo explícito, total real y leyenda |
| Explorador | controles y tabla sin ritmo visual | filtros, control de página, resumen y tabla jerarquizados |
| Detalle | tabla genérica y expanders aislados | resumen del evento, dos columnas y tabs de evidencia/provenance |
| Validación | warning y métricas como bloque largo | selector contextual, métricas compactas, tabs y alcance separado |
| Exportación | tres botones equivalentes | formato único, estimación, preview y acción primaria |
| Ayuda | documento vertical extenso | referencia por tabs con alcance y privacidad localizables |
| Tema | estilos dispersos de Streamlit/Plotly | tokens, CSS, configuración y Plotly centralizados |
| Localización | términos internos y placeholders heterogéneos | vocabulario visible en español y claves canónicas preservadas en datos/exportación |
| Validación | fixture de demostración con escenarios mezclados | tres escenarios sintéticos separados; EVTX queda como procesamiento real sin ground truth controlado |

## Elementos conservados

Se mantienen los ocho flujos, carga segura, filtros puros, paginación, selección de evento, trazabilidad, validaciones por escenario, exportación canónica y ejecución directa mediante `main.run_pipeline()`. No se modifican parsers, `CommonEvent`, correlador, validador ni reporters.

## Evidencia visual

Las capturas definitivas se almacenan en `artifacts/gui_phase_9_2_9_8_final/screenshots/`. La selección para memoria se copia a `artifacts/gui_phase_9_2_9_8_final/memory_shortlist/`. Ambas rutas están ignoradas; las vistas operativas usan el resultado real de 1465 eventos y el detalle emplea un evento controlado con ruta enmascarada.

## Release candidate 9.8c

La revisión final sustituye esas capturas por el conjunto de release candidate ubicado en `artifacts/gui_phase_9_2_9_8_release_candidate/`. El ajuste reserva espacio estable bajo la cabecera, elimina truncados en Inicio y compacta la tabla de validación.

La presentación deja de equiparar objeto normalizado con campo de matching: el evento emparejado aparece en la tabla y el objeto completo se consulta en el detalle. `correct_rate` se etiqueta como tasa de correctos y `precision_rate` como precisión estricta. La confianza se describe como indicador heurístico neutral, y la nota de conjunto mixto solo usa identificadores de escenario sintético conocidos.
