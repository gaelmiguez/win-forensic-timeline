# PUBLICATION_MANIFEST

Fecha de preparación: 2026-07-19.

Versión del proyecto: `0.9.0`.

Repositorio: <https://github.com/gaelmiguez/win-forensic-timeline>.

Visibilidad inicial: privada.

## Archivos preparados para publicación

- Código del pipeline, GUI, parsers, modelo `CommonEvent`, correlador, reporters y validador.
- Configuración relativa y segura.
- Dependencias de CLI y GUI.
- Tests y fixtures exclusivamente sintéticas.
- Scripts de generación sintética y exportación controlada.
- Ground truth exclusivamente sintético.
- Documentación técnica, escenarios y decisiones arquitectónicas.
- `README.md`, `.gitignore`, `SECURITY.md`, `PRIVACY.md`, `CONTRIBUTING.md` y `CITATION.cff`.
- Auditoría recursiva en `REPOSITORY_AUDIT.md`.

El detalle por ruta figura en `REPOSITORY_AUDIT.md`. La copia inicial mediante lista positiva incorporó 179 archivos versionados del proyecto de origen; los documentos de publicación se añadieron después en esta carpeta saneada.

## Elementos excluidos

- Evidencias reales o adquiridas y cualquier output derivado.
- EVTX, historiales reales, hives, Prefetch, SRUM, bases de datos, volcados e imágenes forenses.
- Word, PDF, informes académicos, paquetes ZIP y copias de seguridad.
- Entornos virtuales, dependencias descargadas, cachés, bytecode y artefactos generados.
- Historial Git original.
- Documentos internos que no forman parte de la lista positiva.
- Cualquier archivo no versionado o dudoso.

## Pruebas ejecutadas sobre la copia saneada

| Comprobación | Resultado |
| --- | --- |
| Suite completa | 234 passed, 1 skipped |
| Suite `tests/gui` | 152 passed, 1 skipped |
| Streamlit AppTest (`test_app_smoke.py`) | 19 passed |
| `compileall` | Correcto |
| `pip check` | Sin dependencias rotas |

Las suites se solapan y sus recuentos no deben sumarse.

## Seguridad y privacidad

| Control | Resultado |
| --- | --- |
| Gitleaks sobre la carpeta saneada | Sin secretos detectados |
| Búsqueda propia de rutas personales, usuario local, correos, IP privadas, UNC, claves privadas, secretos asignados y URLs con credenciales | 187 archivos de texto revisados; 0 hallazgos |
| Ficheros mayores de 10 MB | 0 |
| Binarios forenses o documentos privados | 0 |
| Enlaces simbólicos | 0 |

Los valores de loopback `127.0.0.1` y las rutas sintéticas `C:\Tools\ExampleApp.exe` o `C:\Windows\System32\notepad.exe` son deliberadamente genéricos y no identifican el entorno personal.

## Licencia

No se añadió una licencia porque no existe una elección expresa y verificable del autor. Debe resolverse antes de cambiar la visibilidad del repositorio a pública.
