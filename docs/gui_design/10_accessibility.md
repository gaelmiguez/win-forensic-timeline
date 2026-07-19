# Estrategia de accesibilidad

## Requisitos base

- Contraste mínimo WCAG AA para texto y controles.
- Navegación completa por teclado y orden de tabulación predecible.
- Foco visible en botones, filtros, pestañas, filas y elementos seleccionables.
- Etiquetas explícitas para todos los controles; los iconos no actúan solos sin tooltip o texto accesible.
- Tamaño de cuerpo mínimo 14 px y zoom del navegador soportado al 200 %.

## Color y gráficos

Las fuentes y estados usan color más símbolo y etiqueta. Las gráficas ofrecen resumen textual, leyenda y valores en hover accesible. Correcto, parcial y error nunca se distinguen únicamente por verde, ámbar o rojo.

## Tablas

Cabeceras semánticas, orden anunciado, paginación controlable por teclado, fila seleccionada visible y mensaje de cero resultados. Abreviaturas como GT, UTC y FP se explican la primera vez o mediante ayuda contextual.

## Fechas y números

Formato visual consistente `YYYY-MM-DD HH:mm:ss[.ffffff] UTC`. Se conserva precisión disponible. Las tasas muestran porcentaje y valor decimal en ayuda. Los deltas indican segundos y signo cuando corresponda.

## Errores

Los mensajes describen qué ocurrió, qué parte sigue disponible y qué puede hacer el usuario. No dependen de códigos internos ni revelan evidencia. Los warnings persistentes pueden revisarse desde un resumen global.

## Verificación futura

- Navegación solo con teclado.
- Revisión con lector de pantalla de flujos principales.
- Auditoría de contraste.
- Zoom 200 % y anchuras 1280/1024/768 px.
- Alternativas textuales para todas las visualizaciones.
