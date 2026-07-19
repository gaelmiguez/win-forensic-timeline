# Revisión visual y de accesibilidad

## Alcance

La revisión cubre las ocho pantallas, tema claro y oscuro, viewports de 1440x1000 y 1024x768, estados vacío/error/cargado, navegación por teclado y representación redundante de estados. No constituye una certificación WCAG formal ni una evaluación con tecnologías asistivas.

## WCAG 2.2 AA aplicable

| Criterio | Tratamiento | Estado |
| --- | --- | --- |
| 1.3.1 Información y relaciones | headings, labels, tabs, tablas y navegación nativos | verificado estructuralmente |
| 1.4.1 Uso del color | fuentes y estados incluyen texto/leyenda | verificado |
| 1.4.3 Contraste mínimo | pares principales y secundarios comprobados sobre los tokens implementados | verificado para texto de interfaz |
| 1.4.10 Reflow | columnas con wrap y tablas con scroll a 1024 px | verificado manualmente |
| 1.4.11 Contraste no textual | bordes, foco y controles con separación visible | revisión manual favorable |
| 2.1.1 Teclado | widgets y navegación nativos de Streamlit | recorrido básico verificado |
| 2.4.7 Foco visible | outline reforzado en botones, inputs y selectores | verificado manualmente |
| 2.4.11 Foco no oculto | shell sin overlays propios | verificado |
| 2.5.8 Tamaño del objetivo | controles principales cercanos a 40 px y controles nativos sin reducción artificial | revisión manual favorable |
| 3.3.1 Identificación de errores | errores estructurados y sin traceback | verificado |

## Teclado

El orden principal sigue navegación, título, ruta, acciones, filtros y contenido. No existen controles icon-only propios. Los iconos Material de navegación mantienen etiqueta textual. El selector por `event_id` ofrece una alternativa estable a la selección directa de Plotly.

## Contraste medido

Los ratios se calcularon con la fórmula de luminancia relativa de WCAG sobre los colores efectivos del sistema visual. Cubren los pares de texto utilizados como base por Streamlit, el shell y Plotly; los estados conservan además una etiqueta textual y no dependen solo del color.

| Par | Ratio | Umbral AA de texto normal |
| --- | ---: | ---: |
| Texto principal claro `#243247` sobre canvas `#F5F7FA` | 12,06:1 | cumple |
| Texto secundario claro `#667085` sobre superficie `#FFFFFF` | 4,97:1 | cumple |
| Texto secundario claro `#667085` sobre canvas `#F5F7FA` | 4,64:1 | cumple |
| Texto principal oscuro `#E7ECF3` sobre canvas `#101828` | 14,95:1 | cumple |
| Texto secundario oscuro `#AAB4C3` sobre canvas `#101828` | 8,47:1 | cumple |
| Texto secundario oscuro `#AAB4C3` sobre superficie `#182230` | 7,65:1 | cumple |
| Accent `#0071E3` sobre superficie clara `#FFFFFF` | 4,70:1 | cumple |
| Texto blanco sobre botón primario `#0071E3` | 4,70:1 | cumple |
| Texto blanco sobre hover primario `#005FBF` | 6,20:1 | cumple |
| Texto blanco sobre botón deshabilitado `#667085` | 4,97:1 | cumple |

## Tema oscuro

Se verifican fondo azul grisáceo, texto claro, iconos laterales legibles, grid visible y ausencia de negro puro. Plotly adapta texto, ejes y hover al tema reportado. Streamlit es la única fuente del estado de tema y no existe una media query paralela que pueda producir una interfaz híbrida.

## Limitaciones

- No se realizó prueba con lector de pantalla.
- El grid interactivo de Streamlit conserva su accesibilidad propia, que depende de la versión instalada.
- El contraste de todos los estados internos de Plotly requiere comprobación instrumental adicional.
- El zoom al 200 % no sustituye una revisión completa en dispositivos móviles, fuera del objetivo de escritorio.

## Verificación de cabecera y foco 9.8c

Se midieron las ocho pantallas a 1440x1000 en temas claro y oscuro, junto con Inicio en 1280x800 y 1024x768. En las 22 mediciones el desplazamiento vertical fue 0, la cabecera terminó en 60 px y el título comenzó en 80 px. La separación mínima obtenida fue 20 px frente al criterio de 12 px.

Las capturas se generaron después de retirar el foco de inputs y selectores. No contienen el mensaje `Press Enter to apply`, desplegables, tooltips, loaders ni overlays. Los valores Aceptados, Rechazados, Trazables e Incidencias se muestran completos. `confidence` se representa mediante un bloque informativo y texto explicativo, sin semántica visual de éxito.
