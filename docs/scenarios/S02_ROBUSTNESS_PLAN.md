# S02 - Plan de robustez y validación menos idealizada

## Estado

Diseñado, no ejecutado. Este documento no altera los resultados de validación existentes.

## Objetivo

Evaluar cómo se degradan el matching, la cobertura, la precisión y la trazabilidad cuando las entradas dejan de ser ideales. El escenario separará errores de carga, eventos parcialmente compatibles, ruido temporal y ausencia de evidencia.

La evaluación distinguirá cuatro dimensiones: robustez del parser o loader ante entradas defectuosas, robustez del pipeline para continuar con datos parciales, robustez del validador al clasificar discrepancias y calidad investigadora de los eventos resultantes. Superar las tres primeras no implica que la evidencia sea completa ni suficiente para sostener una conclusión forense.

## Dataset propuesto

El escenario utilizará copias sintéticas aisladas bajo `evidence/scenarios/s02/` y salidas bajo `output/scenarios/s02/`. No reutilizará evidencias reales con datos personales.

| Caso | Entrada diseñada | Resultado esperado |
| --- | --- | --- |
| S02-01 | Objeto esperado parcialmente diferente | `correcto` si la coincidencia parcial es inequívoca; documentar la regla |
| S02-02 | Evento sin timestamp válido | Registro omitido con warning; no emparejado |
| S02-03 | JSON inválido | Error controlado del loader/parser; resto del escenario continúa |
| S02-04 | Ruido dentro de la ventana | Selección del candidato con mejor objeto y menor delta |
| S02-05 | Fuente correcta y objeto incorrecto | `parcial` |
| S02-06 | Evento esperado ausente | `no_detectado` |
| S02-07 | Evento fuera de tolerancia | `no_detectado` |
| S02-08A | Falta una clave obligatoria de trazabilidad, como `traceability_ref` | Entrada inválida o rechazada por el loader; no representa un `CommonEvent` válido producido por parsers |
| S02-08B | `traceability_ref` existe, pero `provenance` está vacío o incompleto | Evento cargado con warning cuando el contrato lo permita y posible reducción de la tasa de trazabilidad |
| S02-09 | Evidencia duplicada | Un evento no se reutiliza para dos filas si existe alternativa |
| S02-10 | Mezcla real y sintética | El ruido fuera de fuentes/ventanas no penaliza por defecto |

S02-08A y S02-08B prueban capas distintas. La variante A evalúa la validación contractual del loader. La variante B evalúa el tratamiento del validador y de la GUI ante una procedencia incompleta. Ninguna variante implica que los parsers deban producir eventos inválidos.

## Ground truth propuesto

El ground truth incluirá al menos ocho filas válidas y una fila deliberadamente inválida. Cada fila documentará la razón de su tolerancia. No se modificarán tolerancias tras observar los resultados, salvo que se publique una segunda ejecución diferenciada.

## Métricas esperadas

Las degradaciones siguientes son hipótesis previas a la ejecución, no resultados observados. Se conservarán aunque la ejecución posterior produzca valores distintos.

- `coverage_rate` inferior a 1.0 por el evento ausente y fuera de tolerancia.
- `correct_rate` inferior a `coverage_rate` por al menos un resultado parcial.
- `precision_rate` inferior a 1.0 cuando se active el cálculo conservador de falsos positivos dentro de la ventana global.
- `traceability_rate` inferior a 1.0 por el evento sin procedencia.
- Desviación temporal media y máxima mayores que cero.
- Conteo explícito de entradas inválidas omitidas, separado de `not_detected` si se amplía el esquema.

## Riesgos

- Diseñar los casos con conocimiento del algoritmo puede favorecer resultados previsibles.
- Una comparación parcial demasiado permisiva puede producir falsos emparejamientos.
- Mezclar EVTX real puede introducir datos sensibles y ruido no reproducible.
- El tratamiento actual de filas ground truth inválidas no incrementa el total válido, lo que debe explicarse.

## Criterios contra resultados artificialmente favorables

1. Congelar ground truth, tolerancias y dataset antes de ejecutar.
2. Publicar reglas de matching y cálculo de falsos positivos antes de conocer las métricas.
3. No eliminar casos fallidos del resumen.
4. Conservar logs de warnings sin contenido sensible.
5. Ejecutar con `--include-false-positives` y también con el modo conservador por defecto.
6. Diferenciar errores de ingestión, no detección y discrepancias semánticas.
7. No presentar el escenario como ejecutado hasta versionar evidencia sintética segura, tests y resultados.

## Criterios de aceptación para una ejecución posterior

- El pipeline y el validador terminan sin abortar ante entradas inválidas aisladas.
- Las diferencias respecto a las hipótesis publicadas se documentan sin ajustar a posteriori dataset, reglas o tolerancias para forzar coincidencias.
- No se modifica evidencia de entrada.
- Los tests existentes permanecen verdes.
- La documentación distingue claramente el diseño del resultado ejecutado.
