# Sistema de diseño

## Principios

Precisión, neutralidad, trazabilidad y legibilidad. Interfaz clara, densa y sin estética de terminal o “hacker”.

## Paleta

| Uso | Color | Hex |
| --- | --- | --- |
| Fondo | gris azulado muy claro | `#F5F7FA` |
| Superficie | blanco | `#FFFFFF` |
| Texto principal | azul grafito | `#243247` |
| Texto secundario | gris | `#667085` |
| Acción primaria | azul | `#0071E3` |
| Borde | gris | `#D8DEE8` |
| Correcto | verde azulado | `#16856C` |
| Advertencia | ámbar | `#A15C00` |
| Error | rojo | `#B42318` |
| Información | azul oscuro | `#175CD3` |

## Colores por fuente

- BrowserHistory: azul `#0071E3`, etiqueta `BrowserHistory`.
- EVTX: índigo `#5856D6`, etiqueta `EVTX`.
- Prefetch: naranja oscuro `#C75C00`, etiqueta `Prefetch`.
- Registry: verde azulado `#16856C`, etiqueta `Registry`.

Siempre se muestran nombre o símbolo además del color. Los patrones de gráfica deben permitir distinguir series en escala de grises.

## Tipografía

Interfaz: `Inter`, `Segoe UI` o sans-serif del sistema. Código y valores estructurados: `Consolas` o `JetBrains Mono`. Cuerpo mínimo 14 px; títulos de pantalla 24 px; métricas 24-30 px sin escalado por viewport.

## Espaciado y geometría

Escala: 4, 8, 12, 16, 24 y 32 px. Radios máximos de 8 px. Controles de al menos 36 px de alto. Bordes suaves, sin sombras intensas ni paneles anidados.

## Jerarquía

1. Título y contexto del dataset.
2. Acciones principales y warnings.
3. Filtros y métricas.
4. Datos operativos.
5. Metadatos y ayuda contextual.

## Tablas

Cabecera fija, alineación numérica a la derecha, UTC no truncado, zebra muy sutil, selección visible y paginación. Descripciones largas se recortan con acceso al detalle. Estados de orden y filtros se anuncian en texto.

## Gráficas

Incluyen título descriptivo, unidades, zona temporal, resumen textual y leyenda accesible. No usan 3D. Agregación y muestreo se declaran junto al gráfico.

Las visualizaciones de `confidence` se separan por fuente. No se usa una media global ni se representa el valor como probabilidad calibrada o como comparación directa de calidad entre artefactos.

## Paneles de evidencia

`raw_evidence` y `provenance` usan árbol JSON plegable con copia por campo. El panel de procedencia aparece antes que el contenido bruto. Claves sensibles pueden enmascararse sin alterar el archivo.

## Advertencias

- Informativa: alcance o agregación.
- Advertencia: datos parciales, trazabilidad ausente o timestamp asumido.
- Error: contrato inválido o ejecución fallida.

Cada aviso incluye título, consecuencia y acción posible.

## Implementación Forensic Clarity

La implementación efectiva se documenta en `18_forensic_clarity_design_system.md`. Los tokens, Plotly, CSS y tema oficial de Streamlit están centralizados; no se usan JavaScript, recursos remotos ni HTML inseguro.
