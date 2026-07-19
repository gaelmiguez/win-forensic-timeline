# Arquitectura de información

## Navegación principal

| Sección | Propósito | Requiere datos |
| --- | --- | --- |
| Inicio | Configurar y ejecutar análisis o cargar outputs | No |
| Dashboard | Resumen global y calidad de carga | Sí |
| Timeline | Explorar distribución temporal | Sí |
| Eventos | Filtrar, ordenar y seleccionar | Sí |
| Detalle | Auditar un `CommonEvent` | Evento seleccionado |
| Validación | Revisar métricas y matches | Outputs de validación |
| Exportación | Guardar subconjuntos y manifiestos | Sí |
| Ayuda | Metodología, fuentes, privacidad y límites | No |

## Jerarquía

```text
Aplicación
├── Inicio
│   ├── Nueva ejecución
│   └── Cargar outputs
├── Análisis actual
│   ├── Dashboard
│   ├── Timeline
│   ├── Explorador de eventos
│   │   └── Detalle y trazabilidad
│   ├── Validación
│   └── Exportación
└── Ayuda y limitaciones
```

## Estado global mínimo

- `input_root`, `output_root` y huella de outputs.
- Estado del pipeline y warnings.
- Dataset cargado y errores de esquema.
- `FilterState` serializable.
- `selected_event_id`.
- Validación seleccionada.
- Política de enmascarado de rutas sensibles.

## Reglas de navegación

- Sin dataset, Dashboard, Timeline, Eventos y Exportación muestran estado vacío con enlace a Inicio.
- El detalle se abre desde tabla, timeline o validación y conserva el contexto anterior.
- Los filtros son compartidos entre Timeline, Eventos y Exportación.
- Cambiar carpeta de outputs invalida caches, selección y filtros incompatibles.
- La sección Ayuda siempre está disponible.

## Arquitectura técnica propuesta

```text
GUI Streamlit
  -> application services
      -> main.run_pipeline(input_root, output_root) / validator CLI-compatible API
      -> output repositories
          -> events.json / timeline.csv
          -> validation_summary_*.json
          -> validation_results_*.csv
```

La presentación no importa parsers ni reporters directamente. Los repositorios validan contratos y devuelven modelos de vista; los servicios encapsulan ejecución y exportación.

## Estructura prevista

```text
gui/
├── app.py
├── config.py
├── services/
│   ├── pipeline_service.py
│   ├── event_repository.py
│   ├── validation_repository.py
│   └── export_service.py
├── models/
│   ├── filter_state.py
│   └── ui_state.py
├── components/
│   ├── metrics.py
│   ├── filters.py
│   ├── event_table.py
│   ├── event_detail.py
│   ├── timeline_chart.py
│   ├── warnings.py
│   └── provenance_view.py
├── pages/
│   ├── home.py
│   ├── dashboard.py
│   ├── timeline.py
│   ├── event_explorer.py
│   ├── validation.py
│   ├── export.py
│   └── about.py
└── assets/
```
