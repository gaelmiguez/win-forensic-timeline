# ADR-0010 - Estrategia Prefetch mediante metadata externa JSON

## Contexto

Prefetch es un artefacto relevante en análisis forense Windows porque aporta evidencias sobre ejecución de programas. Sus ficheros `.pf` contienen información como nombre del ejecutable, contador de ejecuciones, tiempos de última ejecución, referencias a ficheros y datos de volumen.

El parsing binario directo de Prefetch puede depender de librerías nativas o herramientas externas. En esta fase se evaluó `prefetch-parser`, pero su instalación requiere compilar `libscca-python` en el entorno utilizado, lo que introduce una dependencia nativa no adecuada para el prototipo en esta etapa.

## Decisión

Se adopta una estrategia de dos niveles:

1. Mantener un parser Prefetch defensivo capaz de integrar backends reales si están disponibles.
2. Soportar metadata externa JSON sidecar junto a `.pf` como formato interoperable para normalizar eventos Prefetch.

El parser busca ficheros `.pf`, intenta usar un backend real si estuviera disponible y, como fallback documentado, carga un JSON con el mismo nombre base que el `.pf`. La metadata externa se normaliza y se transforma en eventos `CommonEvent` cuando contiene una marca temporal real de ejecución.

## Alternativas consideradas

- Integrar `prefetch-parser` como dependencia directa.
- Integrar `libscca`/libyal.
- Consumir directamente salidas de herramientas externas.
- Aplazar Prefetch a una fase posterior.

## Justificación

La estrategia elegida evita bloquear el prototipo por dependencias nativas y mantiene la arquitectura modular. El soporte JSON sidecar permite validar el flujo completo `Prefetch -> CommonEvent -> timeline -> validation` con eventos controlados, preservando trazabilidad y sin fabricar eventos a partir de metadatos del sistema de ficheros.

La decisión deja abierta la sustitución futura por un backend binario real. El parser ya dispone de un punto de integración defensivo para backends compatibles, por lo que la estrategia actual no impide incorporar parsing directo de `.pf` en fases posteriores.

## Limitaciones

Esta versión no parsea directamente binarios `.pf`. La calidad de los eventos depende de que la metadata externa sea correcta, completa y proceda de una herramienta o proceso documentado. El enfoque no sustituye una validación con Prefetch real extraído por herramientas forenses, y requiere documentar el origen de cada sidecar JSON.

El parser tampoco genera eventos si no existe una marca temporal de ejecución. En particular, no usa `mtime` del fichero `.pf` como evidencia de ejecución.

## Impacto en el TFM

La decisión añade la dimensión de ejecución de programas al modelo común de eventos y permite experimentar con eventos Prefetch controlados. Prefetch pasa a ser una tercera fuente normalizada dentro del pipeline, junto con BrowserHistory y EVTX.

La memoria del TFM debe presentar esta estrategia con precisión: el prototipo soporta eventos Prefetch mediante metadata externa JSON sidecar, mientras que el parsing binario nativo de `.pf` queda identificado como trabajo futuro o como una línea de validación posterior con backend real.
