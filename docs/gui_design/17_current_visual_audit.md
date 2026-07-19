# Auditoría visual y funcional previa al rediseño

## Alcance y estado de partida

La auditoría se realizó sobre `fdc740e` con la implementación funcional de las fases 9.2-9.8 aún sin staging. Se inspeccionaron todos los módulos bajo `gui/`, la suite `tests/gui/`, `.streamlit/config.toml`, las capturas de `artifacts/gui_phase_9_2_9_8/screenshots/` y las ocho pantallas ejecutadas en Streamlit 1.59.2.

El intérprete principal se invocó explícitamente desde la instalación local de Python 3.14.6 porque el alias `python` no estaba disponible en la sesión. La línea base fue:

| Comprobación | Resultado |
| --- | --- |
| Suite principal | 186 passed, 2 skipped |
| Suite del entorno GUI | 203 passed, 1 skipped |
| Navegación real | Ocho pantallas accesibles |
| `git diff --check` | Sin errores |
| Configuración de red | `127.0.0.1`, headless, telemetría desactivada |

## Problemas visuales encontrados

### Shell y navegación

- La identidad se limita al nombre generado por Streamlit; no existe marca visual propia ni descriptor de producto.
- La sidebar usa la apariencia predeterminada, con jerarquía débil entre grupos y un pie reducido a una frase.
- El control `Deploy` del shell de desarrollo sigue visible y refuerza la sensación de aplicación sin terminar.
- El estado activo depende casi por completo del resaltado nativo y no existe información compacta sobre versión, UTC y dataset cargado.
- Las ocho páginas comparten navegación, pero no una composición visual suficientemente reconocible.

### Tipografía y jerarquía

- Los títulos `st.title` son demasiado grandes para una herramienta operativa y consumen altura útil.
- Las métricas nativas presentan cifras sobredimensionadas y, en el Dashboard, los timestamps llegan a truncarse.
- Los títulos de gráficas se encuentran dentro de Plotly mientras las secciones carecen de encabezado contextual externo.
- Los captions, avisos y textos de ayuda no siguen una jerarquía consistente.

### Superficies, densidad y espaciado

- Los filtros se agrupan en un expander grande que ocupa la mayor parte del primer viewport de Timeline y Explorador.
- Inicio combina carga y ejecución en una única columna larga; no existe un resumen operacional lateral.
- El Dashboard concede el mismo peso a cinco gráficas, aunque la actividad temporal debería dominar.
- El detalle usa un DataFrame genérico para campos normalizados y expanders para procedencia, sin diferenciar visualmente normalización, origen y evidencia.
- Validación usa avisos y métricas de gran tamaño; la advertencia metodológica domina más de lo necesario.
- Exportación presenta tres botones equivalentes sin una selección compacta de formato, tamaño o preview.
- Ayuda es una secuencia vertical extensa sin índice o pestañas.

### Tablas y gráficas

- Las tablas conservan la presentación nativa: columnas técnicas, densidad y selección no se integran con una jerarquía de producto.
- Los timestamps e identificadores no usan una diferenciación monoespaciada consistente.
- Las gráficas repiten configuración y colores en cada página; no existe un tema Plotly central.
- Los colores actuales no siguen la correspondencia requerida BrowserHistory azul, EVTX índigo, Prefetch naranja y Registry verde azulado.
- La Timeline detallada queda por debajo de un bloque de filtros demasiado alto y pierde protagonismo.
- La captura full-page actual presenta padding negro en varias pantallas, por lo que no es adecuada para memoria o revisión visual.

### Estados y mensajes

- Los estados vacíos se representan como `st.info`, sin una composición específica o acción contextual.
- Los errores dependen de alertas nativas y no siempre están visualmente asociados al campo que los originó.
- Los avisos correctos, parciales y metodológicos usan componentes diferentes sin un sistema semántico común.
- Los valores 1.0 de validación se muestran como métricas prominentes aunque deben permanecer neutrales.

### Responsive y tema

- No existe un sistema de tokens claro/oscuro controlado por la aplicación.
- `.streamlit/config.toml` solo configura servidor y telemetría; no define tipografía, colores, bordes o radios.
- Las cuadrículas rígidas de cuatro o cinco columnas pierden legibilidad en 1024 px.
- El detalle no explicita un apilado responsive de sus bloques y la tabla puede consumir anchura sin priorización.

## Problemas funcionales encontrados

La funcionalidad principal está operativa y la auditoría no detectó pérdidas de datos ni modificaciones de evidencias. Se identificaron estos bordes que requieren saneamiento durante el rediseño:

1. Los nombres de `gui_runs` usan precisión de segundos y un sufijo secuencial. Evitan colisiones ordinarias, pero la creación puede reforzarse con microsegundos y `mkdir(exist_ok=False)` para reducir carreras concurrentes.
2. La Timeline declara el modo agregado y el umbral de 5.000, pero el aviso no muestra de forma suficientemente explícita el total real representado.
3. El bloqueo de ejecución se mantiene en el estado de sesión y evita el doble clic dentro de una sesión. No existe ejecución asíncrona, por lo que una ejecución larga bloquea el rerun actual.
4. `raw_evidence` y `provenance` se despliegan bajo demanda, aunque permanecen en memoria porque `events.json` se carga completo.
5. La selección de evento se conserva correctamente, pero en Timeline depende de un selector estable de `event_id` y no de la selección directa de puntos de Plotly.

## Elementos que deben conservarse

- Navegación nativa de ocho pantallas.
- Repositorios de solo lectura y carga parcial con issues estructurados.
- Caché invalidada por ruta, tamaño y `mtime_ns`.
- Filtros puros, combinables y vectorizados.
- Umbral de 5.000 eventos y agregación explícita.
- Paginación, ordenación y selección persistente.
- Separación de `raw_evidence` y `provenance`.
- Enmascarado de rutas por defecto.
- Escenarios de validación independientes y `default` no clasificado.
- Exportaciones en memoria con las 16 claves canónicas.
- Ejecución directa mediante `main.run_pipeline()` sin shell ni subprocess.
- Configuración local en loopback y telemetría desactivada.

## Elementos que deben rediseñarse

- App shell, identidad, sidebar y encabezados.
- Tokens de color, tipografía, espacio, radio, borde y estados.
- Banda compacta de métricas en lugar de una cuadrícula de cifras grandes.
- Paneles conceptuales y toolbars, evitando una tarjeta por dato.
- Tema Plotly único con semántica de fuente estable.
- Composición asimétrica del Dashboard y mayor protagonismo de Timeline.
- Tabla de eventos a ancho completo y controles de paginación compactos.
- Detalle en columnas normalizado/procedencia con tabs inferiores.
- Validación con advertencia compacta y métricas neutrales.
- Exportación mediante selector de formato, preview y estimación de tamaño.
- Ayuda organizada como documentación técnica navegable.
- Estados vacíos y errores con composición y acción contextual.

## Referencias a capturas previas

Las capturas `03_dashboard.png`, `04_timeline.png`, `05_explorador.png`, `06_detalle_trazabilidad.png`, `07_validacion.png`, `08_exportacion.png` y `10_error_ruta.png` ilustran los problemas anteriores. Varias contienen padding negro generado por la captura full-page, por lo que se sustituirán y no se reutilizarán en la shortlist de memoria.

## Riesgos de personalización de Streamlit

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Selectores `data-testid` cambian entre versiones | Pérdida parcial de estilo | CSS limitado, documentado y con fallback nativo |
| CSS global afecta widgets no previstos | Inconsistencia o contraste | Una única hoja, selectores acotados y pruebas de páginas |
| Tema oscuro depende del tema activo de Streamlit | Contraste desigual | Tokens claro/oscuro con `prefers-color-scheme` y configuración oficial |
| Reruns reconstruyen el DOM | Saltos visuales | Estado serializable, componentes nativos y ausencia de posición absoluta |
| Plotly no hereda todo el CSS | Gráficas incoherentes | Función central `apply_forensic_clarity_theme` |
| Sidebar y cabecera son superficies internas | Fragilidad de versión | Usar solo `data-testid` estables y conservar comportamiento usable sin CSS |

## Separación entre función y presentación

Los problemas principales son visuales: jerarquía, densidad, consistencia, identidad y responsive. Los contratos de datos, la carga, los filtros, las exportaciones y el pipeline funcionan. Los ajustes funcionales se limitan a robustecer nombres de ejecución, hacer más explícito el total agregado y mejorar la presentación de estados; no requieren cambios en parsers, `CommonEvent`, correlador o validador.
