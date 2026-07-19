# ADR-0011 - Estrategia Registry mediante metadata externa JSON

## Contexto

El Registro de Windows es una fuente relevante en análisis forense, especialmente para identificar persistencia, configuración del sistema y mecanismos de ejecución automática. En esta fase del prototipo se priorizan entradas de autorun asociadas a claves `Run` y `RunOnce`, por su valor para escenarios de persistencia y por su integración clara en una timeline forense.

## Decisión

Se adopta una estrategia basada en metadata externa JSON controlada bajo `evidence/registry/`, sin acceder al Registro real del sistema y sin parsear hives binarios en esta fase.

El parser Registry:

- descubre ficheros JSON de forma recursiva;
- carga entradas normalizadas;
- exige un timestamp forense explícito mediante `last_write_time_utc` o `timestamp_utc`;
- transforma cada entrada válida en un evento `CommonEvent`.

## Alternativas consideradas

- Acceder al Registro real mediante APIs del sistema.
- Parsear hives binarios directamente.
- Consumir exports `.reg`.
- Aplazar la incorporación de Registry.
- Usar JSON externo como formato interoperable de metadata.

## Justificación

La estrategia JSON evita riesgos derivados de depender del sistema anfitrión o de modificarlo accidentalmente. También mantiene la reproducibilidad del prototipo, permite validar el flujo `Registry -> CommonEvent -> timeline -> validation`, preserva trazabilidad explícita y deja abierta la futura integración con parsers de hives o herramientas externas especializadas.

El uso de metadata externa es coherente con la estrategia aplicada en Prefetch: se normaliza una representación controlada del artefacto sin afirmar soporte binario completo antes de validarlo de forma rigurosa.

## Limitaciones

- No parsea hives binarios del Registro.
- No lee el Registro real del sistema.
- Depende de que la metadata externa sea correcta y esté documentada.
- Se centra inicialmente en autoruns `Run` y `RunOnce`.
- Requiere documentar el origen del JSON usado como evidencia intermedia.

## Impacto en el TFM

La decisión añade la dimensión de persistencia y configuración al modelo común de eventos. Registry pasa a ser una cuarta fuente normalizada del pipeline junto a BrowserHistory, EVTX y Prefetch. Además, permite una validación sintética controlada con métricas cuantificables, manteniendo claramente documentada la limitación de no realizar parsing binario de hives en esta versión.
