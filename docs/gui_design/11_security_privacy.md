# Seguridad y privacidad

## Modelo local

La GUI escucha en loopback y no se publica en red por defecto. No usa servicios externos, telemetría ni almacenamiento remoto. La documentación de ejecución debe advertir si el usuario cambia la dirección de escucha.

## Evidencia de solo lectura

- La GUI no escribe en la ruta de entrada.
- La salida debe ser distinta de evidencia y validarse con rutas resueltas.
- El pipeline conserva su comportamiento de lectura; la GUI no ofrece editar o borrar evidencias.
- Las operaciones de sobrescritura se limitan a outputs y requieren confirmación.

## Rutas y ejecución

- Resolver y validar rutas con `pathlib`.
- Rechazar salida contenida dentro de un fichero y combinaciones ambiguas entrada/salida.
- Invocar APIs Python cuando exista función pública.
- La GUI no usa `subprocess`: la ejecución se integra mediante la función pública `main.run_pipeline()`.
- No construir comandos con texto libre.

## Datos sensibles

Nombres de usuario, equipo, SID, rutas, URLs, `event_data` y descripciones EVTX pueden ser sensibles. Las vistas muestran datos necesarios al analista, pero ofrecen modo de enmascarado para capturas y exports públicos. Los logs no incluyen XML completo ni JSON de evidencia.

## Errores y logs

Los logs conservan etapa, fichero relativo, tipo de error y contador. El detalle técnico completo se guarda solo en output si el usuario lo solicita y tras advertencia. No se renderizan trazas que contengan registros completos.

## Exportación

El usuario revisa columnas y filtros antes de exportar. Los manifests advierten si se incluyen `source_location`, `raw_evidence` o `provenance`. Los exports públicos deben pasar por enmascarado explícito; no se asume anonimización automática completa.

## Amenazas principales

- Path traversal o selección de destinos no deseados.
- Exposición del servidor local a la red.
- Inyección en comandos auxiliares.
- Saturación de memoria con JSON grande.
- Filtración por logs, capturas o exportaciones.
- Confusión entre output derivado y evidencia original.
