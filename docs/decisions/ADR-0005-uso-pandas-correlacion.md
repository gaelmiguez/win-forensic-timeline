# ADR-0005 - Uso de pandas para correlación

## Contexto

La baseline necesita ordenar, filtrar y exportar eventos de forma simple y testeable.

## Decisión

Usar `pandas.DataFrame` como estructura de correlación temporal del MVP.

## Alternativas consideradas

- Listas de dataclasses ordenadas manualmente.
- Base de datos local desde la primera fase.

## Justificación

`pandas` ofrece ordenación, filtrado y exportación CSV con poco código y una curva de aprendizaje adecuada para el TFM.

## Impacto en el TFM

Permite construir resultados rápidos y explicar una limitación clara: la carga en memoria debe revisarse para datasets grandes.
