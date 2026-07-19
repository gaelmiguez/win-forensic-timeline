# win-forensic-timeline

Prototipo académico modular en Python para la extracción o ingesta, normalización, correlación temporal, validación y exploración de artefactos forenses de Windows.

Repositorio público: <https://github.com/gaelmiguez/win-forensic-timeline>.

## Objetivo y alcance

El proyecto diseña, implementa y valida la viabilidad técnica de un sistema que transforma fuentes heterogéneas en eventos `CommonEvent`, construye una línea temporal común en UTC y conserva la trazabilidad con la evidencia de origen. Su finalidad es apoyar un análisis preliminar más consistente y accesible; no se ha medido una mejora cuantitativa de eficiencia frente a un proceso manual.

Es un prototipo experimental asociado a un Trabajo Fin de Máster. No es una suite forense certificada, no sustituye el juicio del analista y no pretende reemplazar herramientas DFIR consolidadas.

## Arquitectura

```text
evidencia de entrada (solo lectura)
        |
        v
parsers por fuente -> CommonEvent -> correlador UTC -> reporters
                           |                |
                           v                v
                       validador           GUI local
```

- `core/`: contrato `CommonEvent`, constantes, excepciones y utilidades temporales.
- `extractors/`: descubrimiento auxiliar de ficheros.
- `parsers/`: transformación específica de cada fuente.
- `normalizers/`: punto de extensión para normalización.
- `correlator/`: construcción de la línea temporal ordenada.
- `reporters/`: salidas CSV, JSON, JSONL y Markdown.
- `validation/`: ground truth sintético, matching y métricas.
- `gui/`: interfaz local Streamlit y servicios de exploración.
- `tests/`: pruebas del pipeline, los parsers, los servicios y la interfaz.
- `docs/`: arquitectura, decisiones, escenarios y diseño de la GUI.

La separación entre evidencia, parser, evento normalizado y resultado permite localizar fallos sin mezclar responsabilidades. Cada ejecución de la GUI usa un directorio de salida aislado y no modifica las evidencias.

## Fuentes soportadas

| Fuente | Entrada | Estado real |
| --- | --- | --- |
| BrowserHistory | Base SQLite `History` de Chromium, Chrome o Edge | Procesamiento directo |
| EVTX | Ficheros `.evtx` exportados | Procesamiento directo de registros reales; sin ground truth controlado |
| Prefetch | Referencia `.pf` y JSON sidecar | Ingesta de metadatos externos; sin parsing binario nativo |
| Registry | JSON externo de autoruns | Ingesta de metadatos externos; sin lectura directa de hives |

## Limitaciones

- Los resultados perfectos documentados corresponden solo a escenarios sintéticos controlados de BrowserHistory, Prefetch y Registry.
- EVTX demuestra procesamiento técnico de registros reales, pero no exactitud frente a acciones esperadas.
- La trazabilidad indica que existen referencias de procedencia; no acredita autenticidad ni integridad criptográfica.
- La normalización UTC no corrige relojes desincronizados, zonas horarias ausentes ni semánticas temporales ambiguas.
- La ausencia de un evento no demuestra que la actividad no ocurriera: puede existir borrado, rotación, corrupción o adquisición parcial.
- No se incluyen UserAssist, Amcache, SRUM, Jump Lists, LNK, MFT, USN Journal ni ShellBags.
- No se realizó evaluación con usuarios, benchmark científico ni comparación experimental con Plaso, Velociraptor o DFIR ORC.

## Estructura del repositorio

```text
config/        configuración segura y relativa
core/          modelo común y utilidades
correlator/    ordenación temporal
docs/          documentación técnica y ADR
extractors/    descubrimiento de entradas
gui/           interfaz gráfica local
normalizers/   extensiones de normalización
parsers/       BrowserHistory, EVTX, Prefetch y Registry
reporters/     CSV, JSON, JSONL y Markdown
scripts/       generación sintética y exportación controlada
tests/         pruebas automatizadas y fixtures sintéticas
validation/    validador y ground truth sintético
```

No se publican evidencias, salidas, documentos académicos, entornos virtuales ni copias del proyecto original. La selección se documenta en `REPOSITORY_AUDIT.md` y `PUBLICATION_MANIFEST.md`.

## Requisitos

- Python 3.11 o posterior.
- Dependencias de `requirements.txt` para CLI y validación.
- Dependencias de `requirements-gui.txt` para la interfaz.
- Windows para la exportación auxiliar de EVTX; el procesamiento de ficheros ya exportados no requiere adquirirlos desde el sistema activo.

## Instalación

```bash
python -m venv .venv
```

En Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-gui.txt
```

En Linux o macOS:

```bash
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip install -r requirements-gui.txt
```

## Ejecución de la CLI

```bash
python main.py --input evidence --output output
```

La ruta de entrada se trata en modo de solo lectura. `evidence/` y `output/` están excluidos de Git.

## Ejecución de la GUI

```bash
python -m streamlit run gui/app.py --server.address 127.0.0.1 --server.headless true
```

La aplicación se ejecuta localmente, desactiva la telemetría de Streamlit y no envía evidencias a servicios externos. Permite cargar salidas existentes o ejecutar el pipeline, filtrar y paginar eventos, explorar la línea temporal, consultar trazabilidad, revisar validaciones y descargar subconjuntos.

La GUI facilita el acceso a los resultados, pero no añade inferencias forenses ni sustituye el análisis humano.

## Pruebas

```bash
python -m pytest -q
python -m compileall -q core correlator extractors gui normalizers parsers reporters validation main.py
python -m pip check
```

Las suites se solapan y sus recuentos no deben sumarse. El resultado exacto de la preparación de la publicación figura en `PUBLICATION_MANIFEST.md`.

## Generación de muestras sintéticas

```bash
python scripts/generate_sample_browser_history.py
python scripts/generate_sample_prefetch_metadata.py --overwrite
python scripts/generate_sample_registry_metadata.py --overwrite
```

Los scripts usan valores ficticios como `example.com`, `ExampleApp` y `UpdaterTask`. Las muestras generadas se escriben en `evidence/`, que no se versiona.

## Validación reproducible

Ejemplo para BrowserHistory:

```bash
python main.py --input evidence --output output
python -m validation.validator \
  --events output/events.json \
  --ground-truth validation/ground_truth_browser_synthetic.csv \
  --output output/validation_results_browser_synthetic.csv \
  --summary output/validation_summary_browser_synthetic.json \
  --report output/validation_report_browser_synthetic.md
```

También se incluyen:

- `validation/ground_truth_prefetch_synthetic.csv`
- `validation/ground_truth_registry_synthetic.csv`

## Formatos de salida

- `events.json`: colección de eventos normalizados.
- `events.jsonl`: un evento JSON por línea.
- `timeline.csv`: línea temporal reutilizable.
- `report.md`: informe preliminar legible.
- `validation_results_*.csv`: detalle del matching.
- `validation_summary_*.json`: resumen de métricas.
- `validation_report_*.md`: informe de validación.

Las salidas pueden contener rutas, nombres de usuario, SID, hosts, URLs u otros datos sensibles. Deben revisarse antes de compartirse.

## Privacidad y tratamiento de evidencias

- No añada evidencias reales a Git, issues, pull requests ni paquetes de soporte.
- No publique EVTX, historiales de navegador, hives, Prefetch, SRUM, bases de datos, imágenes forenses ni outputs derivados de ellos.
- Ejecute la herramienta sobre copias adquiridas conforme al procedimiento aplicable.
- Documente origen, hash, herramienta y contexto de adquisición cuando use metadatos externos.
- Revise `PRIVACY.md` y `SECURITY.md` antes de colaborar.

## Reproducibilidad

La versión del prototipo documentada en esta publicación es `0.9.0`. La reproducción se apoya en:

- dependencias declaradas;
- fixtures y ground truth exclusivamente sintéticos;
- pruebas automatizadas;
- ADR de las decisiones principales;
- ejecución local y rutas relativas;
- una etiqueta de release y un commit verificables.

La versión reproducible asociada al TFM está identificada mediante la etiqueta `v0.9.0-tfm` y el commit `7e092141720f518ab26ef2ce53ce16d7a518aac6`.

Repositorio público: <https://github.com/gaelmiguez/win-forensic-timeline>.

## Licencia

No se incluye una licencia de software. En ausencia de una licencia expresa, no se conceden permisos generales de reutilización, modificación o redistribución más allá de los previstos legalmente.

## Referencia académica

Míguez Méndez, G. (2026). *Sistema de extracción y análisis de artefactos forenses en Windows* [Prototipo de software asociado a un Trabajo Fin de Máster, Máster Universitario en Ciberseguridad].

Los documentos académicos no forman parte de este repositorio. Los metadatos de citación del software se encuentran en `CITATION.cff`.
