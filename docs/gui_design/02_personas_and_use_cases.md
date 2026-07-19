# Personas y casos de uso

## Persona primaria: analista forense técnico

Necesita revisar rápidamente una secuencia, aislar fuentes y verificar el origen de un evento. Valora densidad informativa, filtros precisos, UTC visible y acceso inmediato a procedencia. Rechaza interfaces decorativas que oculten datos o simplifiquen en exceso.

## Persona secundaria: estudiante de ciberseguridad

Necesita comprender cómo artefactos heterogéneos se convierten en eventos comunes. Valora explicaciones breves de `timestamp_type`, métricas y limitaciones, además de ejemplos controlados reproducibles.

## Persona secundaria: investigador o revisor académico

Necesita comprobar resultados, metodología y trazabilidad sin ejecutar cada script manualmente. Valora comparaciones ground truth, advertencias experimentales y exportaciones reproducibles.

## Casos de uso principales

| ID | Caso de uso | Resultado útil |
| --- | --- | --- |
| UC-01 | Seleccionar evidencia y salida | Rutas válidas, fuentes detectadas y análisis listo |
| UC-02 | Ejecutar pipeline | Outputs generados con progreso, warnings y resumen |
| UC-03 | Abrir outputs existentes | Dashboard disponible sin repetir parsing |
| UC-04 | Acotar una ventana temporal | Timeline y tabla sincronizadas con el rango |
| UC-05 | Buscar actividad concreta | Eventos filtrados por texto, fuente y acción |
| UC-06 | Auditar un evento | Campos normalizados, evidencia y procedencia visibles |
| UC-07 | Revisar validación | Métricas y comparación GT-evento contextualizadas |
| UC-08 | Exportar selección | Fichero filtrado más manifiesto de filtros |
| UC-09 | Entender una limitación | Ayuda contextual sobre timestamp, fuente o métrica |

## Necesidades transversales

- No modificar la evidencia.
- Saber qué filtros están activos.
- Diferenciar dato original, valor normalizado e inferencia.
- Reconocer estados parciales y errores recuperables.
- Navegar con teclado y sin depender únicamente del color.
