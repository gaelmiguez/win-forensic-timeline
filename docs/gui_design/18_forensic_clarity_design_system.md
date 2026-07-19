# Forensic Clarity - sistema visual implementado

## Objetivo

`Forensic Clarity` traduce los principios de precisión, trazabilidad, neutralidad y legibilidad del prototipo a una interfaz de escritorio web local. La referencia combina claridad tipográfica inspirada en aplicaciones profesionales de Apple con patrones de densidad y estado propios de Fluent y Carbon, sin replicar una marca concreta. La identidad se apoya en una marca SVG original de tres nodos temporales.

El sistema evita estética de terminal, exceso de tarjetas y color decorativo. Las superficies enmarcadas se reservan para bloques conceptuales; tablas y gráficas ocupan el protagonismo operativo.

## Implementación centralizada

| Capa | Archivo | Responsabilidad |
| --- | --- | --- |
| Tokens | `gui/theme/tokens.py` | Paleta de fuentes, estados y modos Plotly |
| Plotly | `gui/theme/plotly_theme.py` | Tipografía, márgenes, ejes, grid, hover y leyenda |
| Carga | `gui/theme/theme_loader.py` | CSS local y detección del tema nativo |
| CSS | `gui/assets/forensic_clarity.css` y `forensic_clarity_dark.css` | Shell, densidad, foco, modo oscuro y respuesta a viewport |
| Marca | `gui/assets/app_mark.svg`, `app_brand.svg` y `app_brand_dark.svg` | Identidad vectorial local y legible en ambos temas |
| Streamlit | `.streamlit/config.toml` | Tema oficial, loopback y telemetría desactivada |

No se usa JavaScript, `unsafe_allow_html`, CDN, fuente remota ni recurso descargado. `st.html(Path)` carga únicamente el fichero CSS local.

## Paleta

### Semántica de fuente

| Fuente | Color | Hex | Codificación redundante |
| --- | --- | --- | --- |
| BrowserHistory | azul | `#0071E3` | nombre y leyenda |
| EVTX | índigo | `#5856D6` | nombre y leyenda |
| Prefetch | naranja oscuro | `#C75C00` | nombre y leyenda |
| Registry | verde azulado | `#16856C` | nombre y leyenda |
| Desconocida | gris | `#667085` | etiqueta explícita |

### Semántica de estado

- Correcto: `#16856C` y texto descriptivo.
- Advertencia: `#A15C00` y consecuencia visible.
- Error: `#B42318` y acción de recuperación.
- Información: `#0071E3` y contexto no alarmista.

El color nunca es el único canal. Fuentes y estados conservan nombres, leyendas o badges textuales.

## Tipografía, densidad y geometría

Se usa la familia sans-serif del sistema, con `Segoe UI` cuando está disponible. Los títulos de pantalla se mantienen por debajo de 31 px; las métricas usan números tabulares y no escalan con el viewport. Los radios máximos son 8 px, los botones 6 px y las sombras se limitan a una elevación muy sutil.

La escala principal es 4, 8, 12, 16, 24 y 32 px. La anchura de contenido se limita a 1480 px. En 1024 px se reduce el padding y las columnas pueden replegarse sin ocultar controles.

## Jerarquía de pantalla

1. Título y descripción breve.
2. Estado operacional o referencia UTC.
3. Tira compacta de métricas.
4. Filtros de investigación.
5. Visualización o tabla principal.
6. Detalle, metodología e incidencias secundarias.

## Gráficas

Todas las figuras pasan por `apply_forensic_clarity_theme()`. La función fija fondo transparente, márgenes compactos, grid suave, hover legible, leyenda horizontal y tipografía común. La semántica de colores por fuente permanece centralizada.

La Timeline declara si representa puntos individuales o agregación. `confidence` se muestra solo desglosada por fuente y como indicador heurístico, nunca como probabilidad ni media global de calidad.

## Tema oscuro

Streamlit actúa como única fuente del tema mediante `st.context.theme`. `theme_loader.py` carga el override oscuro únicamente cuando ese contexto informa `dark`, y Plotly usa la misma señal. No se emplea `prefers-color-scheme`, lo que evita mezclar un sistema operativo oscuro con una sesión Streamlit clara. El fondo oscuro usa azul grisáceo, no negro puro; texto, bordes, grid y hover cambian de forma coordinada.

## Selectores CSS auditados

| Selector | Uso | Riesgo | Fallback |
| --- | --- | --- | --- |
| `stAppViewContainer` | canvas | bajo, test id estable | tema oficial |
| `stMain` | ancho y padding | bajo | layout wide de Streamlit |
| `stHeader` | separación superior | medio | header nativo |
| `stAppDeployButton` | ocultar Deploy local | medio | el botón reaparece sin afectar función |
| `stSidebar` | superficie lateral | bajo | `[theme.sidebar]` |
| `stSidebarNav` | densidad de navegación | medio | navegación nativa sigue operativa |
| `stIconMaterial` | contraste estable de iconos Material | medio | etiqueta textual permanece visible |
| `stBaseButton-primary` | fondo, hover, deshabilitado y texto del botón primario | medio | botón nativo conserva función y etiqueta |
| `stVerticalBlockBorderWrapper` | paneles conceptuales | medio | borde nativo de `st.container` |
| `stMetric` | tira de métricas | bajo | `st.metric` nativo |
| `stDataFrame` | tabla | bajo | tema de dataframe oficial |
| `stPlotlyChart` | marco de gráfica | bajo | figura Plotly mantiene su tema |
| `stExpander` | detalle secundario | bajo | expander nativo |

No se usan selectores posicionales como `nth-child`, nombres de clases generadas ni reglas que alteren la semántica de widgets.

## Estados

- Vacío: explica qué falta y dónde iniciar la carga.
- Error: mensaje acotado, sin traceback ni rutas completas.
- Parcial: conserva datos válidos y muestra recuento rechazado.
- Cargado: badges por archivo, calidad de carga y navegación al Dashboard.
- Agregado: total real, granularidad y umbral visibles junto a la Timeline.

## Responsividad

La composición objetivo es 1440x1000. Se revisa además a 1024 px. La navegación lateral conserva texto, las métricas se compactan, las columnas admiten wrap y las tablas usan su scroll nativo. Las capturas se realizan sobre viewport visible, sin `fullPage`, para evitar relleno negro artificial.

## Ajuste de composición 9.8c

El bloque principal reserva `5rem` sobre el contenido para convivir con la cabecera nativa de Streamlit. La medición en 1440x1000, 1280x800 y 1024x768, tanto en tema claro como oscuro, situó el borde inferior de la cabecera en 60 px y el inicio del título en 80 px: una separación constante de 20 px. No se oculta la cabecera ni se emplean posiciones absolutas o márgenes negativos.

Los indicadores de calidad de carga se presentan como texto completo para evitar elipsis. En validación, la tabla principal se limita a ground truth, resultado, objeto esperado, evento emparejado, timestamp, delta y trazabilidad; el objeto normalizado y los campos extensos se trasladan al detalle secundario. `confidence` usa tratamiento informativo neutral y conserva su explicación heurística.
