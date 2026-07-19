# Fase 9.8b - Pulido final y coherencia metodológica

## Objetivo

La fase 9.8b cierra la revisión visual y metodológica de la GUI sin modificar la lógica forense. El trabajo se concentra en cuatro frentes: separar correctamente los escenarios de validación, completar la localización visible al español, estabilizar los temas claro y oscuro y obtener capturas definitivas aptas para revisión académica.

## Coherencia de validación

La demostración oficial carga tres escenarios sintéticos independientes:

| Escenario | Fuente esperada | Ground truth | Correctos | Cobertura | Precisión estricta | Trazabilidad |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| BrowserHistory sintético | BrowserHistory | 3 | 3 | 1.0 | 1.0 | 1.0 |
| Prefetch sintético | Prefetch | 2 | 2 | 1.0 | 1.0 | 1.0 |
| Registry sintético | Registry | 2 | 2 | 1.0 | 1.0 | 1.0 |

Los ficheros de captura se generan a partir de `events.json` con 1465 eventos normalizados: 1458 EVTX, 3 BrowserHistory, 2 Prefetch y 2 Registry. EVTX se presenta como procesamiento de volumen real, pero no como escenario con ground truth controlado. Ningún resultado EVTX se mezcla con los tres escenarios sintéticos.

## Localización y contrato de datos

Los controles, estados, incidencias y descriptores visibles se muestran en español. Las claves técnicas se acompañan de una etiqueta humana mediante el diccionario central `EVENT_FIELD_LABELS`. Este cambio afecta exclusivamente a la presentación: las 16 claves canónicas de `CommonEvent` permanecen intactas en memoria, en el JSON de detalle y en las exportaciones.

La versión visible del producto es `0.9.0`. Se retiraron textos internos de desarrollo, eyebrows redundantes y nombres de escenario poco legibles. Los escenarios desconocidos se muestran como no clasificados y no se etiquetan como sintéticos sin evidencia.

## Tema y accesibilidad visual

`st.context.theme` es la única fuente del estado claro u oscuro. El CSS base no contiene `prefers-color-scheme`; el override oscuro se carga solo cuando Streamlit informa ese tema. De este modo se evita una combinación accidental entre tema del sistema y tema de la aplicación.

Los botones primarios utilizan texto blanco sobre `#0071E3`, con estados hover, deshabilitado y foco definidos. Los ratios de contraste de los tres fondos de botón se verifican mediante test automatizado. Los iconos Material de la navegación heredan el color efectivo y mantienen etiqueta textual, incluida la variante oscura.

## Capturas definitivas

Las capturas se guardan fuera de Git en `artifacts/gui_phase_9_2_9_8_final/screenshots/`:

1. `01_inicio_resultados.png`.
2. `02_dashboard_real.png`.
3. `03_timeline_real.png`.
4. `04_explorador.png`.
5. `05_detalle_trazabilidad.png`.
6. `06_validacion_browser.png`.
7. `07_validacion_prefetch.png`.
8. `08_validacion_registry.png`.
9. `09_exportacion.png`.
10. `10_ayuda.png`.
11. `11_tema_oscuro.png`.

La selección de ocho imágenes para la memoria reside en `artifacts/gui_phase_9_2_9_8_final/memory_shortlist/`. Las vistas generales usan los 1465 eventos actuales. El detalle usa el evento Prefetch controlado `NOTEPAD.EXE`, oculta la ruta completa y no expone datos personales. Las tres capturas de validación corresponden a escenarios separados.

## Pruebas añadidas

Las pruebas nuevas cubren:

- separación estricta de los tres escenarios oficiales y ausencia de EVTX en su ground truth;
- nombres de escenario amigables y tratamiento neutral de escenarios desconocidos;
- localización de controles y ausencia de términos internos visibles;
- etiquetas humanas sin alterar columnas canónicas;
- selección de un evento en Detalle sin excepción;
- invalidación visual de timestamps sobre una copia de presentación;
- fuente única de tema, recursos SVG locales y contraste de botones;
- presencia de estados compactos y versión pública.

La validación final obtuvo `195 passed, 3 skipped` con el intérprete principal, `224 passed, 1 skipped` en el entorno GUI, `142 passed, 1 skipped` para `tests/gui` y `19 passed` en la batería AppTest. `compileall`, `pip check` y `git diff --check` finalizaron correctamente. El alias `python` no estaba disponible en `PATH`, por lo que la batería principal se ejecutó con el intérprete Python 3.14.6 instalado.

## Limitaciones

La revisión visual no constituye una certificación WCAG ni una prueba formal con lector de pantalla. Algunos textos de accesibilidad pertenecen a widgets internos de Streamlit, Plotly o al grid de datos y dependen de las traducciones ofrecidas por esas bibliotecas. Las capturas son evidencia de funcionamiento y maquetación, no una nueva validación forense.

## Alcance del cambio

No se modificaron parsers, `CommonEvent`, correlador, validador, reporters, evidencias ni outputs históricos. No se añadió ninguna dependencia, no se realizó staging y no se creó commit.
