# Product brief de la GUI forense

## Problema

El pipeline funciona desde CLI y genera salidas reutilizables, pero revisar miles de eventos exige abrir ficheros, construir filtros manuales y relacionar por separado timeline, evento, procedencia y validación. Esto dificulta una inspección rápida y verificable para usuarios que no desean operar directamente sobre CSV o JSON.

## Usuario principal

Analista forense, estudiante o investigador de ciberseguridad con conocimientos técnicos que necesita reconstruir actividad Windows y comprobar la procedencia de cada evento.

## Propuesta

Una aplicación local que orquesta el pipeline existente, carga sus outputs y permite explorar eventos, timeline, trazabilidad y validación sin modificar evidencias. La interfaz hará visibles la semántica temporal, el origen de los datos y las limitaciones experimentales.

## Objetivos

1. Ejecutar el análisis con rutas validadas y feedback de progreso.
2. Resumir entre 1.000 y 100.000 eventos sin ocultar advertencias.
3. Filtrar y buscar la timeline de forma reproducible.
4. Inspeccionar todos los campos de `CommonEvent`, `raw_evidence` y `provenance`.
5. Comparar ground truth con eventos detectados.
6. Exportar subconjuntos junto con los filtros aplicados.
7. Explicar fuentes soportadas, timestamps y alcance de las métricas.

## No objetivos

- Modificar o adquirir evidencia.
- Editar eventos normalizados.
- Sustituir suites forenses o implementar análisis causal automático.
- Parsear Prefetch o Registry binarios desde la GUI.
- Ejecutar en un servicio público o enviar datos a la nube.
- Presentar proximidad temporal como causalidad.

## Alcance inicial

- Entrada: ruta de evidencias y ruta de salida.
- Ejecución: el futuro `PipelineService.run(input_root, output_root)` encapsulará la función existente `main.run_pipeline(input_root: str | Path, output_root: str | Path) -> dict` y traducirá su resultado a un contrato estable para la GUI.
- Lectura: `events.json`, `timeline.csv` y salidas de validación.
- Vistas: Inicio, Dashboard, Timeline, Explorador, Detalle, Validación, Exportación y Ayuda.
- Salida: CSV, JSON, JSONL y resumen de filtros.

## Riesgos

- Carga de EVTX dominante y datasets grandes.
- Exposición accidental de rutas, usuarios, equipos o SIDs.
- Confusión entre evidencia sintética y real.
- Métricas 1.0 interpretadas fuera de su contexto.
- Bloqueo de la interfaz durante el pipeline.
- Dependencia excesiva de Streamlit en la lógica de negocio.
- Interpretación de una media global de `confidence` como calidad general, aunque cada parser asigna este indicador con criterios propios.

## Métricas de éxito

- Carga inicial de 10.000 eventos en menos de 3 segundos en el equipo de referencia.
- Interacción de filtros habituales en menos de 1 segundo con datos cacheados.
- 100 % de eventos seleccionables con acceso a trazabilidad o aviso de ausencia.
- Ninguna escritura en la ruta de evidencia durante pruebas.
- Todos los errores de rutas y formatos cubiertos por tests.
- Usuario capaz de ejecutar, filtrar, revisar procedencia y exportar en un recorrido sin CLI.
