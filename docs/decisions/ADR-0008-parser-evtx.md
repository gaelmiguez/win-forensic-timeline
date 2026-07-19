# ADR-0008 - Parser EVTX

## Contexto

Los registros EVTX son una fuente central de evidencia en sistemas Windows. Recogen eventos de sistema, aplicaciones, servicios y actividad registrada por componentes del sistema operativo, por lo que aportan información relevante para construir una línea temporal forense.

## Decisión

Se implementa un parser EVTX usando `python-evtx`, con lectura defensiva de ficheros `.evtx`, extracción del XML de cada registro, parsing de campos relevantes y transformación a `CommonEvent`.

El parser descubre ficheros `.evtx`, procesa cada registro de forma tolerante, normaliza `System/TimeCreated/@SystemTime` a UTC y conserva trazabilidad mediante `raw_evidence` y `provenance`. La salida normalizada no almacena XML completo.

## Alternativas consideradas

- Usar la CLI Rust `evtx` y consumir su salida JSON o XML.
- Usar herramientas externas como Hayabusa o Chainsaw y consumir sus resultados.
- Aplazar EVTX para una fase posterior.

## Justificación

La integración directa en Python mantiene coherencia con la arquitectura modular del prototipo y evita depender de herramientas externas durante la ejecución principal. Esta decisión ofrece control sobre la normalización temporal, el modelo común de eventos, la trazabilidad y el tratamiento de errores.

La solución es suficiente para el MVP porque permite extraer eventos reales de Windows, mapearlos a `CommonEvent` y correlacionarlos con otros artefactos ya soportados.

## Impacto en el TFM

La incorporación de EVTX añade una fuente forense real al prototipo y refuerza la generación de timelines con eventos del sistema operativo. Además, permite validar el pipeline con registros reales de Windows y no solo con evidencias sintéticas.

La decisión introduce limitaciones documentadas: posible volumen elevado de eventos, sensibilidad de datos personales, heterogeneidad de campos entre proveedores y dependencia del parsing XML generado a partir de los registros EVTX.
