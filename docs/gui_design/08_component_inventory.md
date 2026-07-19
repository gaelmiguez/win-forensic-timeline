# Inventario de componentes

| Componente | Responsabilidad | Entradas | Estados críticos |
| --- | --- | --- | --- |
| `PathSelector` | Seleccionar y validar rutas | tipo, valor, permisos | vacío, inválido, no escribible |
| `SourceDetection` | Resumir carpetas detectadas | inventario | ninguna, parcial |
| `PipelineProgress` | Etapa, progreso y warnings | estado de servicio | running, partial, failed |
| `MetricStrip` | Mostrar métricas compactas y contexto | valor, unidad, ayuda | n/a, warning |
| `FilterToolbar` | Editar `FilterState` | columnas y rangos | sin opciones, inválido |
| `ActiveFilters` | Mostrar y quitar filtros | estado serializado | ninguno |
| `TimelineChart` | Agregado temporal seleccionable | dataframe reducido | vacío, agregado, error |
| `EventTable` | Tabla paginada/ordenada | vista de eventos | vacío, loading |
| `EventDetail` | Campos normalizados | evento | sin selección |
| `TimestampPanel` | Semántica temporal | timestamps y provenance | naive, ausente |
| `ProvenanceView` | Trazabilidad y decisiones | provenance | vacío, incompleto |
| `RawEvidenceView` | JSON bajo demanda | raw_evidence | grande, inválido |
| `ValidationMetrics` | Resumen contextualizado | summary | vacío, schema inválido |
| `ValidationTable` | GT frente a evento | results | sin match, parcial |
| `WarningBanner` | Riesgo o limitación | nivel, texto, acción | persistente |
| `ExportForm` | Formato, destino y manifiesto | filtros, dataset | colisión, fallo |
| `EmptyState` | Explicar ausencia y siguiente acción | causa | inicial, sin resultados |
| `AppShell` | Identidad, navegación agrupada y contexto local | estado de sesión | sin datos, cargado |
| `PageHeader` | Título, descripción y estado | texto, badge | normal, warning |
| `StatusBadge` | Estado textual redundante | etiqueta, severidad | cinco severidades |
| `SourceLegend` | Semántica de fuente | lista de fuentes | desconocida |
| `UtcRange` | Rango temporal principal | inicio, fin | no disponible |
| `DataQualitySummary` | Aceptados, rechazados, trazabilidad e incidencias | conteos | parcial |
| `EventSummary` | Identidad y acción del evento | CommonEvent | trazabilidad incompleta |

## Límites de componentes

Los componentes reciben datos preparados y emiten intenciones. No leen ficheros, ejecutan parsers, calculan matching ni escriben exports directamente. Esa lógica pertenece a servicios y repositorios.

`MetricStrip` no presenta una media global de `confidence`. Los componentes analíticos solo muestran distribuciones o estadísticos por fuente con su contexto heurístico.

Los componentes implementados residen en `gui/components/`. El CSS y el tema Plotly se mantienen en `gui/theme/` y `gui/assets/`; las páginas no definen estilos aislados.

## Modelos de estado

`FilterState` contiene rango UTC, fuentes, categorías, acciones, parsers, confianza, escenario, texto y requisito de trazabilidad. `UIState` contiene dataset activo, evento seleccionado, validación activa, navegación de retorno y política de enmascarado.
