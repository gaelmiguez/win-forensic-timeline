# Implementation Log

## 2026-06-20 - Creación del esqueleto baseline

- Se crea la estructura modular inicial del proyecto `win-forensic-timeline`.
- Se implementa `CommonEvent` con validación mínima, generación de `event_id` y serialización ISO 8601.
- Se añaden utilidades de conversión temporal a UTC.
- Se implementa correlación básica con `pandas`.
- Se añaden reporters CSV, JSON, JSONL y Markdown.
- Se crean parsers stub para EVTX, Prefetch, Registry y Browser History.
- Se añade CLI básica ejecutable mediante `python main.py --input evidence --output output`.
- Se incorporan tests unitarios mínimos con `pytest`.

## 2026-06-20 - Fase 2 - Parser de historial de navegador

- Se implementa `parsers/browser_history_parser.py` para procesar ficheros SQLite `History` de navegadores basados en Chromium.
- El parser descubre ficheros de historial de forma recursiva bajo `evidence/browser`.
- Se validan ficheros SQLite y presencia de tablas `urls` y `visits`.
- Cada fichero se copia a una ubicación temporal antes de abrirlo, reduciendo problemas con bases bloqueadas.
- Se convierten timestamps Chrome/WebKit mediante `chrome_time_to_utc`.
- Las visitas web se transforman en eventos `CommonEvent` con `source_artifact` igual a `BrowserHistory`.
- Se añade un generador de evidencia sintética en `scripts/generate_sample_browser_history.py`.
- Se añaden tests unitarios del parser y una prueba de integración ligera con `run_pipeline`.

## 2026-06-20 - Fase 2.5 - Saneamiento previo a Fase 3

- Se inicializa el repositorio Git local y se añade `.gitignore` para excluir cachés, entornos virtuales, outputs, evidencias y ficheros temporales.
- Se completa el esquema documental de validación para `ground_truth.csv` y `validation_results.csv`.
- Se ajusta el mensaje del reporte Markdown para reflejar que el parser de historial de navegador ya está operativo.
- Se serializan campos complejos como `raw_evidence` y `provenance` en CSV mediante JSON estable.
- Se añade validación de `timestamp_local` timezone-aware cuando el campo está presente en `CommonEvent`.

## 2026-06-20 - Fase 3.1 - Implementación inicial del parser EVTX

- Se añade la dependencia `python-evtx` para lectura defensiva de ficheros Windows Event Log `.evtx`.
- Se implementa parsing XML de registros EVTX y extracción de campos `System`, `EventData` y `UserData` simples.
- Se mapean eventos EVTX al modelo común `CommonEvent`, preservando trazabilidad en `raw_evidence` y `provenance` sin almacenar XML completo.
- Se normaliza `System/TimeCreated/@SystemTime` a UTC mediante `parse_iso_to_utc`.
- Se añaden tests con XML EVTX sintético para validar el mapeo sin requerir evidencias reales.
- La lectura con ficheros `.evtx` reales queda pendiente de validación experimental en Fase 3.2.

## 2026-06-20 - Fase 3.2b - Saneamiento post-validación EVTX

- Se actualiza el reporte Markdown para reflejar que los parsers de historial de navegador y EVTX ya están operativos.
- Se documenta el problema detectado al combinar timestamps ISO 8601 con y sin microsegundos.
- Se mantiene el uso de `format="mixed"` en Pandas para soportar esa variabilidad y conservar normalización UTC.
- Se ajusta el requisito mínimo a `pandas>=2.0`, necesario para `format="mixed"`.
- Se verifica que la batería de tests continúa pasando tras el saneamiento.

## 2026-06-20 - Fase 3.3 - Consolidación del parser EVTX

- Se crea `ADR-0008-parser-evtx.md` para documentar la decisión técnica de incorporar EVTX mediante `python-evtx`.
- Se actualizan fragmentos reutilizables para la memoria del TFM sobre desarrollo del prototipo, modelo de eventos y validación de resultados.
- Se actualiza el README para reflejar dependencias, uso del parser EVTX, exportación controlada con `wevtutil` y advertencias de privacidad.
- Se prepara un commit limpio con código, tests, documentación y script auxiliar, manteniendo evidencias reales fuera de Git.

## 2026-06-20 - Fase 4.1 - Motor de validación ground truth

- Se implementa `validation/validator.py` como motor de validación ejecutable con `python -m validation.validator`.
- Se añade lectura de eventos normalizados desde `output/events.json`.
- Se añade lectura de `validation/ground_truth.csv` con comparación por fuente, objeto esperado y tolerancia temporal.
- Se generan `validation_results.csv`, `validation_summary.json` y `validation_report.md` en la carpeta de salida.
- Se calculan métricas básicas: cobertura, tasa de correctos, precisión conservadora, desviación temporal y trazabilidad.
- Se incorporan tests sintéticos para correctos, parciales, no detectados, métricas, serialización y casos de timestamps inválidos.

## 2026-06-20 - Fase 4.3 - Consolidación del validador ground truth

- Se crea `ADR-0009-validador-ground-truth.md` para documentar la decisión técnica del motor de validación.
- Se consolida el ground truth sintético de BrowserHistory como primer escenario controlado.
- Se documentan resultados cuantificados de validación con cobertura y trazabilidad completas en el escenario sintético.
- Se actualiza el esquema de validación para describir `validation_summary.json`.
- Se prepara un commit limpio con validador, tests, ground truth sintético y documentación.

## 2026-06-20 - Fase 5.1 - Diseño e instrumentación del escenario S01

- Se crea `scripts/run_scenario_s01_browser_evtx.py` como orquestador del escenario `S01_BROWSER_EVTX`.
- Se añade generación de BrowserHistory sintético con timestamps actuales y offsets controlados.
- Se incorpora soporte opcional para generar EVTX controlado mediante `eventcreate` y exportar `Application.evtx` si el entorno lo permite.
- Se genera ground truth dinámico en `output/scenarios/s01/`, evitando versionar marcas temporales de ejecución.
- Se permite ejecutar opcionalmente el pipeline y el validador sobre rutas separadas del escenario.
- Se documenta el escenario en `docs/scenarios/S01_BROWSER_EVTX.md`.
- Se añaden tests del script en modo `--skip-evtx`, sin depender de Windows Event Log real.

## 2026-06-20 - Fase 5.2b - Consolidación documental de S01

- Se documenta la limitación operativa detectada al intentar generar EVTX controlado con `eventcreate`.
- Se refleja que el escenario mantiene una ejecución reproducible con fallback a BrowserHistory cuando EVTX no puede generarse.
- Se incorporan los resultados BrowserHistory del escenario S01 con métricas completas.
- Se aclara que la validación combinada BrowserHistory + EVTX queda pendiente de un entorno con permisos adecuados.

## 2026-06-20 - Fase 6.1 - Parser Prefetch inicial

- Se sustituye el stub de `parsers/prefetch_parser.py` por una capa inicial defensiva.
- Se añade descubrimiento recursivo de ficheros `.pf`, aceptando carpetas o ficheros individuales.
- Se implementa el mapeo de metadata Prefetch normalizada a `CommonEvent` con `source_artifact` igual a `Prefetch`.
- El timestamp principal se basa en `last_run_time_utc` o, en su ausencia, en la marca más reciente de `last_run_times_utc`.
- Se evita generar eventos cuando no existe timestamp real de ejecución, descartando el uso de `mtime` del fichero `.pf`.
- Se evalúa `prefetch-parser`, pero no se integra como dependencia porque requiere compilar `libscca-python` en este entorno.
- Se deja preparado un adaptador opcional para `prefetch_parser.prefetch2json` si estuviera disponible en un entorno futuro.
- Se añaden tests con metadata sintética y fallback sin backend real; la validación con `.pf` reales queda pendiente para Fase 6.2.

## 2026-06-20 - Fase 6.2 - Metadata externa para Prefetch

- Se añade soporte para ficheros JSON sidecar junto a `.pf` como metadata externa controlada.
- El fallback permite validar eventos Prefetch sin depender de compilar `libscca-python` ni integrar herramientas nativas.
- Se crea `scripts/generate_sample_prefetch_metadata.py` para generar `.pf` placeholder y sidecars JSON sintéticos.
- Se añade `validation/ground_truth_prefetch_synthetic.csv` para validar ejecuciones `NOTEPAD.EXE` y `POWERSHELL.EXE`.
- El parser sigue sin usar `mtime` del `.pf` y no genera eventos si el sidecar carece de timestamp de ejecución.
- Se incorporan tests para sidecars válidos, JSON inválido, ausencia de timestamp, generación sintética e integración con el pipeline.

## 2026-06-20 - Fase 6.2b - Consolidación documental Prefetch

- Se crea `ADR-0010-prefetch-metadata-json.md` para documentar la estrategia de metadata externa JSON.
- Se actualizan fragmentos del TFM sobre desarrollo del prototipo, modelo de eventos y validación de resultados.
- Se documenta explícitamente la limitación: la versión actual no realiza parsing binario nativo de `.pf`.
- Se presenta Prefetch como tercera fuente normalizada del pipeline mediante sidecars JSON controlados.
- Se conserva la futura integración de un backend binario real como trabajo posterior.

## 2026-06-20 - Fase 7.1 - Registry parser inicial mediante metadata JSON

- Se sustituye el stub de `parsers/registry_parser.py` por un parser inicial basado en metadata JSON externa.
- Se soportan entradas de autorun/persistencia de tipo `Run` y `RunOnce` representadas como evidencias controladas.
- El parser no accede al Registro real del sistema, no modifica claves reales y no realiza parsing binario de hives.
- Se evita el uso de `mtime` del fichero JSON como evidencia temporal; solo se generan eventos con timestamp forense explícito.
- Se crea `scripts/generate_sample_registry_metadata.py` para generar metadata sintética reproducible.
- Se añade `validation/ground_truth_registry_synthetic.csv` para validar `ExampleApp` y `UpdaterTask`.
- Se incorporan tests de descubrimiento, carga JSON, mapeo a `CommonEvent`, propagación de `scenario_id`, `max_files` e integración con el pipeline.

## 2026-06-20 - Fase 7.2 - Consolidación documental Registry

- Se crea `ADR-0011-registry-metadata-json.md` para documentar la estrategia Registry mediante metadata externa JSON.
- Se actualizan fragmentos del TFM sobre desarrollo del prototipo, modelo de eventos y validación de resultados.
- Se documenta la limitación de la fase: no hay lectura directa del Registro real ni parsing binario de hives.
- Se presenta Registry como cuarta fuente normalizada del pipeline junto a BrowserHistory, EVTX y Prefetch.

## 2026-06-20 - Fase 8.1 - Cierre técnico del prototipo

- Se ejecutan validaciones finales de tests, pipeline y ground truth sintéticos para BrowserHistory, Prefetch y Registry.
- Se crea `docs/final_metrics.md` con métricas finales de eventos, fuentes y validaciones controladas.
- Se actualiza el README para reflejar el estado final, fuentes soportadas, scripts sintéticos, validación y limitaciones.
- Se consolidan fragmentos del TFM con el estado final del prototipo y el resumen global de validación.
- No se incorporan nuevas funcionalidades ni dependencias en esta fase.

## 2026-07-13 - Fase 9.0 - Cierre académico y preparación de la GUI

- Se incorpora el feedback académico pendiente mediante un fragmento explícito del gap investigador.
- Se documentan en profundidad limitaciones, ambigüedad temporal, zonas horarias, artefactos ausentes y amenazas a la validez interna, externa y de constructo.
- Se contextualizan las métricas perfectas como resultados exclusivos de escenarios sintéticos controlados.
- Se diseña el escenario S02 de robustez sin implementarlo ni presentarlo como ejecutado.
- Product Design no estaba disponible en la sesión y se crea la skill local `forensic-gui-design` como fallback documentado.
- Se comparan Streamlit + Plotly, PySide6 y FastAPI con frontend independiente; se selecciona Streamlit + Plotly en ADR-0012.
- Se definen arquitectura, flujos, pantallas, wireframes, componentes, contratos, accesibilidad, privacidad, rendimiento, testing y criterios de aceptación.
- Se establece un plan de implementación incremental entre las fases 9.1 y 9.10.
- No se modifica lógica funcional, no se añaden dependencias GUI y no se implementa todavía la interfaz.

## 2026-07-13 - Fase 9.1 - Infraestructura GUI y carga segura de resultados

- Se comprueba en un entorno virtual aislado la compatibilidad real de Python 3.14.6 con Streamlit 1.59.2, Plotly 6.9.0 y Pandas 3.0.3.
- Las dependencias directas de interfaz se fijan en `requirements-gui.txt`, separadas de `requirements.txt` y del entorno principal de la CLI.
- Se crea el paquete `gui/` con modelos tipados, validación de rutas, catálogo de outputs y repositorios de eventos, timeline y validaciones independientes de Streamlit.
- El loader de `events.json` valida las 16 claves de `CommonEvent`, conserva extensiones desconocidas, detecta identificadores duplicados y registra todas las filas rechazadas.
- El loader de `timeline.csv` conserva las cadenas originales y añade representaciones internas para timestamps y JSON serializado sin sobrescribir el fichero.
- Se implementan filtros puros y combinables por tiempo, fuente, categoría, acción, parser, escenario, texto, trazabilidad y rango de `confidence`; los indicadores de confianza se desglosan por fuente.
- La aplicación Streamlit mínima carga únicamente outputs existentes, muestra estado, preview limitado e incidencias, usa caché invalidada por ruta, tamaño y `mtime_ns`, y no ejecuta `main.run_pipeline()`.
- Se añaden fixtures sintéticas y tests de rutas, catálogo, cargas completas/parciales, formatos corruptos, validaciones, filtros y smoke test con `streamlit.testing.v1.AppTest`.
- No se modifican parsers, modelo común, correlador, validador ni outputs forenses. El dashboard completo, las gráficas y la ejecución del pipeline quedan fuera del alcance de esta fase.

## 2026-07-13 - Fases 9.2-9.8 - Interfaz gráfica funcional

- Se implementa navegación nativa de Streamlit con ocho pantallas: Inicio, Dashboard, Timeline, Explorador, Detalle, Validación, Exportación y Ayuda.
- El Dashboard presenta conteos, actividad temporal, categorías, trazabilidad y distribución de `confidence` por fuente sin calcular una media global.
- La Timeline alterna de forma explícita entre detalle y agregación temporal a partir de 5.000 eventos válidos; los filtros permanecen en servicios puros.
- El Explorador incorpora ordenación, paginación y selección persistente. El detalle separa `CommonEvent`, localización, `raw_evidence` y `provenance`, con rutas enmascaradas por defecto.
- La página de validación mantiene escenarios separados, trata `default` como no clasificado y conserva el resumen como fuente principal para falsos positivos.
- Las exportaciones CSV, JSON y JSONL se construyen en memoria con las 16 claves canónicas y sin campos internos `_ui_*`.
- `PipelineService` llama directamente a `main.run_pipeline()`, valida relaciones peligrosas entre rutas, crea outputs únicos y distingue ejecución correcta, parcial y fallida sin usar `subprocess`.
- La carga real inspeccionó 1.465 eventos sin rechazos; una ejecución controlada generó y recargó 1.465 eventos sin modificar las evidencias originales.
- Se midieron filtros y agregación con 1.000, 10.000 y 100.000 eventos sintéticos. En la medición final del equipo de desarrollo, 100.000 filas requirieron 1,61 s para filtrado combinado y 0,009 s para agregación por hora; son medidas contextuales, no garantías universales.
- Se amplía la suite con servicios de dashboard, timeline, paginación, detalle, validación, exportación, ejecución y navegación AppTest. No se modifica lógica forense ni la memoria DOCX/PDF.

## 2026-07-13 - Fases 9.2-9.8R - Rediseño visual Forensic Clarity

- Se audita la interfaz funcional antes de editar y se documentan jerarquía, densidad, estados y riesgos de selectores.
- Se crea un sistema visual centralizado con tokens, tema Plotly, CSS local, configuración oficial de Streamlit y una marca SVG original.
- Se reorganizan las ocho pantallas sin retirar funciones: Dashboard jerárquico, Timeline explícita, Explorador operativo, detalle trazable, validación contextual, exportación guiada y ayuda por temas.
- Se refuerzan tema oscuro, foco, reflow a 1024 px, representación redundante de fuentes y estados, y ausencia de recursos remotos o HTML inseguro.
- `PipelineService` reserva directorios con microsegundos, sufijo aleatorio y creación atómica; la Timeline agregada muestra el total real representado.
- Se añaden tests del sistema visual, CSS, SVG, tema claro/oscuro y uso central de Plotly. No se modifican parsers, `CommonEvent`, correlador, validador, reporters ni la memoria DOCX/PDF.
