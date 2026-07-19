# ADR-0003 - Validación mediante ground truth

## Contexto

El proyecto necesita demostrar que los eventos generados por la herramienta se corresponden con actividad esperada.

## Decisión

Usar un fichero `ground_truth.csv` con eventos esperados por escenario controlado.

## Alternativas consideradas

- Validación manual sin dataset estructurado.
- Comparación directa contra herramientas externas sin escenario propio.

## Justificación

El ground truth permite reproducibilidad, trazabilidad y cálculo de métricas básicas de cobertura y desviación temporal.

## Impacto en el TFM

Esta decisión aporta una base experimental defendible para la fase de evaluación.
