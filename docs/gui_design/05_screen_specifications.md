# Especificaciones de pantallas

## Inicio y ejecución

Controles: selector de evidencia, selector de salida, validación de rutas, fuentes detectadas, `Ejecutar análisis`, `Cargar outputs existentes` y acceso a privacidad. El progreso indica descubrimiento, parsing, correlación y reportes. Los logs son resumidos y no incluyen XML ni valores sensibles.

Estados: sin ruta; ruta inexistente; entrada vacía; salida no escribible; listo; ejecución; correcto; parcial con warnings; fallo. El botón se deshabilita durante ejecución y nunca sobrescribe sin confirmación explícita.

## Dashboard

Tarjetas: total de eventos, fuentes, intervalo UTC, proporción con `provenance`, warnings y validaciones disponibles. Gráficas: eventos por fuente y categoría, histograma temporal adaptativo y distribución de `confidence` desglosada por fuente. La GUI no presenta una media global de `confidence` como indicador de calidad general. Puede mostrar mediana, intervalos o recuentos por fuente, siempre etiquetados como indicadores heurísticos asignados por cada parser, no como probabilidades calibradas ni valores directamente comparables entre artefactos. La distinción real/sintético solo se muestra cuando `scenario_id` o el contexto de carga lo permite; no se infiere por fecha.

Estado vacío: explica qué archivos faltan. Estado parcial: muestra métricas de datasets válidos y lista contratos fallidos.

## Timeline

Eje UTC, carril o color por fuente, zoom, selección de rango, hover accesible y enlace al detalle. Para grandes volúmenes usa agregación por minuto, hora o día; al ampliar cambia a eventos individuales. Los grupos muestran conteo y rango, no causalidad.

Estados: sin eventos; rango sin resultados; timestamps inválidos omitidos; volumen alto con agregación activa.

## Explorador de eventos

Filtros: fecha inicial/final, fuente, categoría, acción, parser, confianza mínima, escenario, texto libre y con/sin trazabilidad. La tabla incluye timestamp UTC, fuente, categoría, acción, objeto, descripción, confianza, parser y escenario.

Requisitos: paginación o virtualización, ordenación estable, selección persistente, contador antes/después, chips de filtros, restablecimiento y exportación. El texto libre busca sobre campos normalizados; buscar dentro de `raw_evidence` requiere una opción explícita por coste.

## Detalle y trazabilidad

Bloques separados:

1. Evento normalizado: todos los campos `CommonEvent`.
2. Semántica temporal: UTC, local, `timestamp_type` y advertencias.
3. Procedencia: `traceability_ref`, ubicación, parser y `provenance`.
4. Evidencia original: `raw_evidence` plegado, con copiar campo y enmascarado.
5. Contexto experimental: `scenario_id` y enlace a validación si existe.

La ausencia de procedencia genera una advertencia, no una afirmación de falsedad.

## Validación

Selector de escenario o fichero. Tarjetas: ground truth, correctos, parciales, no detectados, falsos positivos, cobertura, precisión estricta, desviación media/máxima y trazabilidad. Tabla: `gt_id`, esperado, detectado, delta, resultado, fuente y notas.

Advertencia fija: **Las métricas corresponden a escenarios controlados y no representan por sí solas el rendimiento ante evidencias reales complejas.**

La vista explica que los falsos positivos son cero por defecto porque su cálculo exhaustivo solo se activa de forma explícita y se limita a fuentes y ventana global del ground truth. El conteo se toma de `validation_summary_*.json`; las filas `falso_positivo` se muestran en la tabla solo si la ejecución con `--include-false-positives` las generó. EVTX se muestra como fuente procesada con logs reales, pero sin atribuirle una validación controlada que no se realizó.

Estados: sin validación; resumen sin resultados; schema inválido; ground truth vacío; métricas cargadas con tabla ausente.

## Exportación

Formatos: CSV, JSON, JSONL, reporte resumido y salidas de validación. Muestra filtros, columnas, filas y destino. No sobrescribe sin confirmación. El manifiesto asociado incluye fecha UTC, fuente de datos, filtros, orden, recuento y versión del prototipo.

## Ayuda, metodología y limitaciones

Fuentes soportadas y no soportadas, modelo `CommonEvent`, significado de métricas, semántica de timestamps, UTC, privacidad, estrategia de metadata externa, limitaciones, versión y referencias documentales. Incluye glosario de GT, UTC, provenance y trazabilidad.

## Comportamiento responsive

En escritorio se usa navegación lateral y dos paneles. En anchura reducida, filtros pasan a un panel desplegable, tarjetas a una columna y detalle bajo la tabla. No se pretende optimizar la primera versión para móvil, pero no debe producir solapamientos ni contenido fuera de margen.
