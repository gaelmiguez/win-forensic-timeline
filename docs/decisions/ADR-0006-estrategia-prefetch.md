# ADR-0006 - Estrategia Prefetch

## Contexto

Prefetch aporta evidencias relevantes de ejecución, pero su parsing depende de versiones de Windows y detalles del formato.

## Decisión

Mantener un parser stub en la baseline y documentar una estrategia futura con extracción de ejecutable, contador de ejecuciones y timestamps.

## Alternativas consideradas

- Implementar un parser parcial sin validar en esta fase.
- Excluir Prefetch del MVP inicial.

## Justificación

Prefetch es valioso para el TFM, pero incorporarlo sin validación aumentaría el riesgo técnico de la baseline.

## Impacto en el TFM

Se preserva Prefetch como artefacto MVP previsto y se deja explícito que puede requerir fallback técnico en fases posteriores.
