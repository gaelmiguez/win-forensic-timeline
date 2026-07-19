# ADR-0002 - Modelo común de eventos

## Contexto

Los artefactos Windows tienen formatos y semánticas distintas. La correlación temporal requiere una representación homogénea.

## Decisión

Definir `CommonEvent` como dataclass estándar, con campos de tiempo, origen, acción, trazabilidad, confianza y evidencia bruta.

## Alternativas consideradas

- Diccionarios libres sin contrato explícito.
- Modelos Pydantic desde la primera fase.

## Justificación

Una dataclass reduce dependencias, mantiene tipado legible y fija un contrato suficiente para MVP, tests y documentación.

## Impacto en el TFM

El modelo común se convierte en el eje metodológico para explicar normalización, correlación y validación.
