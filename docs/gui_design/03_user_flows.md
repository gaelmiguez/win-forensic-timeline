# Flujos de usuario

## Ejecutar análisis

1. Inicio muestra rutas vacías y privacidad local.
2. Usuario selecciona evidencia y salida.
3. Servicio valida existencia, permisos y que entrada y salida no sean la misma ruta.
4. Se muestran fuentes detectadas y advertencias por carpetas vacías.
5. Usuario pulsa `Ejecutar análisis`.
6. GUI bloquea un segundo lanzamiento, muestra etapa y logs resumidos.
7. `PipelineService` invoca directamente `main.run_pipeline(input_root, output_root)` y adapta el diccionario devuelto, sin `shell=True` ni construcción de comandos con texto del usuario.
8. Resultado final distingue correcto, parcial con warnings o fallo.
9. Usuario abre Dashboard.

Flujos alternativos: ruta inexistente impide ejecutar; salida no escribible ofrece corrección; parser aislado con error produce resultado parcial; fallo global conserva el mensaje técnico sin volcar evidencia.

## Cargar outputs existentes

1. Usuario elige una carpeta de salida.
2. Repositorios detectan `events.json`, `timeline.csv` y validaciones.
3. Se validan esquemas y timestamps.
4. Si hay al menos un dataset válido, se habilitan las vistas compatibles.
5. Ficheros inválidos aparecen como warnings individuales.

## Filtrar timeline

1. Usuario abre Timeline.
2. Se carga una vista agregada del intervalo completo.
3. Ajusta rango, fuente, categoría o acción.
4. Filtros vectorizados producen subconjunto y resumen textual.
5. El gráfico cambia granularidad según rango y volumen.
6. Seleccionar un punto o grupo abre eventos asociados.

## Abrir evento y revisar trazabilidad

1. Usuario selecciona una fila o evento del gráfico.
2. Detalle muestra primero campos normalizados.
3. Panel de tiempo explica UTC, timestamp local y `timestamp_type`.
4. Panel de trazabilidad muestra `traceability_ref`, `source_location` y `provenance`.
5. `raw_evidence` se carga al expandir, con claves sensibles señaladas.
6. Usuario vuelve al subconjunto sin perder filtros.

## Revisar validación

1. Usuario selecciona un resumen disponible.
2. Se muestran métricas y advertencia de alcance controlado.
3. Tabla relaciona cada `gt_id` con evento detectado o ausencia.
4. Seleccionar un match abre el evento sin perder la fila ground truth.
5. Parciales y no detectados ofrecen notas del validador.

## Exportar

1. Usuario llega desde Explorador o Timeline con filtros activos.
2. Revisa número de filas, formato, destino y manifiesto de filtros.
3. La GUI comprueba colisión de nombre.
4. Si existe, solicita confirmación o nuevo nombre.
5. `export_service` escribe en salida, nunca en evidencia.
6. Se muestra ruta relativa, tamaño y checksum opcional del resultado.
