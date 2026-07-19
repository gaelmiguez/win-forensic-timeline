# Wireframes textuales

## Inicio

```text
┌ Navegación ─────┬─────────────────────────────────────────────┐
│ Inicio          │ Nuevo análisis                             │
│ Dashboard       │ Evidencia [ ruta... ] [Seleccionar]        │
│ Timeline        │ Salida    [ ruta... ] [Seleccionar]        │
│ Eventos         │ Fuentes detectadas: EVTX · Browser · ...   │
│ Validación      │ [Advertencias de ruta]                     │
│ Exportación     │ [Ejecutar análisis] [Cargar outputs]       │
│ Ayuda           │ Progreso: parsing EVTX 42 %                │
└─────────────────┴─────────────────────────────────────────────┘
```

Errores aparecen bajo el control correspondiente. En ejecución, controles de rutas quedan bloqueados y se permite cancelar solo si el servicio puede hacerlo sin dejar outputs inconsistentes.

## Dashboard

```text
┌ Total ┐ ┌ Fuentes ┐ ┌ UTC ┐ ┌ Trazabilidad ┐ ┌ Validación ┐
┌ Eventos por fuente ─────────┐ ┌ Categorías ───────────────┐
│ barras + resumen textual    │ │ barras + tabla accesible  │
└─────────────────────────────┘ └────────────────────────────┘
┌ Distribución temporal agregada ───────────────────────────┐
└────────────────────────────────────────────────────────────┘
[Warnings y alcance de los datos]
```

El Dashboard no incluye una tarjeta de confianza media global. Si se visualiza `confidence`, se hace mediante distribución, mediana o intervalos separados por fuente y con una nota sobre su carácter heurístico.

## Timeline

```text
[Rango UTC] [Fuente] [Categoría] [Acción] [Agrupación: auto]
┌ EVTX      ···■■······■■■■······························ ┐
├ Browser   ··●────────●────────●························· ┤
├ Prefetch  ··············●────●························· ┤
├ Registry  ····················●────●··················· ┤
└──────────────── UTC · zoom · selección ───────────────────┘
[Resumen del rango] [Abrir eventos asociados]
```

Símbolo y etiqueta acompañan al color. A gran volumen se muestran barras agregadas; un aviso indica la granularidad.

## Explorador y detalle

```text
┌ Filtros ──────────┬ Tabla paginada ──────────────────────────┐
│ Fecha UTC         │ UTC | Fuente | Acción | Objeto | Conf.   │
│ Fuente            │ ...                                      │
│ Categoría         │ [<] Página 1/20 [>]                      │
│ Acción            ├ Detalle seleccionado ────────────────────┤
│ Confianza         │ Normalizado | Tiempo | Procedencia       │
│ Texto             │ [raw_evidence plegado] [provenance]      │
│ Trazabilidad      │                                          │
└───────────────────┴──────────────────────────────────────────┘
```

Sin selección, el panel derecho muestra instrucciones breves. En pantallas estrechas, detalle se abre debajo o en página propia.

## Validación

```text
[Escenario: BrowserHistory sintético v]
[GT 3] [Correctos 3] [Parciales 0] [ND 0] [Cobertura 1.0]
⚠ Métricas de escenario controlado; no equivalen a rendimiento real.
┌ GT ID | Esperado | Detectado | Delta | Resultado | Notas ┐
└────────────────────────────────────────────────────────────┘
[Abrir evento emparejado]
```

## Exportación

```text
Dataset: 143 eventos filtrados
Filtros: EVTX · 2026-06-19 · confidence >= 0.8
Formato [CSV v]  Columnas [Todas v]
Destino [ output/exports/... ]
[ ] Incluir manifiesto de filtros
[Exportar]
```

## Estados vacíos y de error

Cada vista reserva el área principal para un mensaje, causa y acción: `No hay outputs cargados -> Ir a Inicio`; `0 resultados -> Restablecer filtros`; `JSON inválido -> Revisar fichero / continuar con otros outputs`.
