# Criterios de aceptación de la GUI

## Verificación de Fase 9.1

- [x] Compatibilidad comprobada en entorno aislado con Python 3.14.6, Streamlit 1.59.2 y Plotly 6.9.0.
- [x] Dependencias GUI separadas en `requirements-gui.txt`.
- [x] Repositorios y filtros testeables sin Streamlit.
- [x] Rutas locales validadas sin crear directorios ni salir de la raíz seleccionada.
- [x] Carga completa, parcial, vacía y corrupta representada mediante resultados e incidencias estructurados.
- [x] Las 16 claves canónicas de `CommonEvent` se comprueban sin eliminar extensiones desconocidas.
- [x] Caché de carga invalidada por ruta resuelta, tamaño y `mtime_ns`.
- [x] Aplicación mínima en loopback, sin telemetría, escritura, parsers directos ni ejecución del pipeline.
- [x] Preview limitado que no expande `raw_evidence`, `provenance` ni rutas completas.
- [x] `confidence` solo se resume por fuente y no se presenta como probabilidad o media global.
- [x] Los falsos positivos se obtienen del resumen agregado y las filas `falso_positivo` son opcionales.
- [x] Dashboard, timeline interactiva, explorador, detalle, exportación y ejecución del pipeline implementados después de Fase 9.1.

## Arquitectura

- [x] Ninguna página importa parsers directamente.
- [x] Servicios y repositorios son testeables sin Streamlit.
- [x] El pipeline existente sigue siendo ejecutable por CLI.
- [x] Evidencia y outputs tienen límites de escritura diferenciados.

## Inicio

- [x] Valida entrada, salida, permisos y conflictos.
- [ ] Detecta fuentes sin leer contenido sensible en pantalla.
- [x] Distingue correcto, parcial y fallo.
- [x] Reserva directorios únicos de forma atómica con microsegundos y sufijo aleatorio.

## Dashboard y timeline

- [x] Conteos coinciden con outputs cargados.
- [x] Intervalos indican UTC.
- [x] Agregación se declara y cambia según volumen.
- [x] Gráficas tienen título, leyenda textual y no dependen solo del color.
- [x] `confidence` se desglosa por fuente y no se presenta como media global, probabilidad calibrada ni medida comparable entre artefactos.

## Explorador y detalle

- [x] Todos los filtros requeridos funcionan combinados.
- [x] Tabla es paginada u ofrece virtualización.
- [x] Todos los campos `CommonEvent` son accesibles.
- [x] `raw_evidence` se carga bajo demanda.
- [x] `traceability_ref` y `provenance` son visibles o su ausencia se advierte.

## Validación

- [x] Muestra todos los campos del resumen sin inventar valores ausentes.
- [x] Relaciona ground truth con evento detectado.
- [x] Explica parciales, no detectados y el conteo agregado de falsos positivos; solo espera filas `falso_positivo` cuando el output las contiene.
- [x] Advertencia metodológica de escenarios controlados permanece visible.

## Exportación

- [x] CSV, JSON y JSONL respetan el subconjunto filtrado.
- [x] El usuario conoce filtros, filas, formato y tamaño estimado antes de exportar.
- [x] La exportación se construye en memoria y no sobrescribe archivos.
- [x] Nunca escribe en evidencia.

## Seguridad y privacidad

- [x] Ejecución local/loopback por defecto.
- [x] Sin telemetría ni servicios externos.
- [x] Sin `shell=True` ni comandos construidos con texto libre.
- [x] Errores y logs no vuelcan XML o evidencia completa.
- [ ] Existe modo de enmascarado para capturas y exports públicos.

## Accesibilidad

- [x] Navegación principal y widgets usan controles nativos operables por teclado.
- [x] Foco visible reforzado y revisión manual favorable de contraste claro/oscuro.
- [x] Iconos de navegación conservan etiquetas textuales; no hay controles propios icon-only.
- [x] UTC, estados y abreviaturas se explican en contexto.
- [x] Reflow comprobado a 1024 px; el zoom 200 % se documenta como revisión manual no certificada.

## Sistema visual Forensic Clarity

- [x] Marca SVG local y original, sin scripts ni recursos externos.
- [x] Tokens, tema Plotly y CSS centralizados.
- [x] Colores de fuente consistentes y redundantes con texto.
- [x] Tema claro y oscuro funcional sin negro puro.
- [x] Estados vacío, error, parcial y cargado siguen el mismo patrón.
- [x] No se usa `unsafe_allow_html`, JavaScript ni selectores CSS posicionales.

## Rendimiento

- [x] 10.000 eventos cumplen la medición contextual documentada.
- [x] 100.000 eventos se filtran y agregan sin renderizado individual; la medición no constituye garantía universal.
- [x] Cache se invalida al cambiar outputs.
- [x] Filtros no recargan disco innecesariamente.

## Calidad forense

- [x] La GUI no afirma causalidad por proximidad temporal.
- [x] Distingue valor original y normalizado.
- [x] No presenta Prefetch/Registry JSON como parsing binario.
- [x] No generaliza métricas sintéticas al rendimiento real.
