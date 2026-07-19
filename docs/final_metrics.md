# Métricas finales del prototipo

## Estado de ejecución

| Elemento | Valor |
| --- | --- |
| Fecha | 2026-06-20 |
| Commit de cierre técnico | `7c5a495` |
| Tests | 82 passed |
| Eventos normalizados | 1499 |
| Fuentes procesadas | BrowserHistory, EVTX, Prefetch, Registry |
| Pipeline | `python main.py --input evidence --output output` |

## Eventos por fuente

| Fuente | Eventos |
| --- | ---: |
| EVTX | 1492 |
| BrowserHistory | 3 |
| Prefetch | 2 |
| Registry | 2 |

## Contexto de las mediciones EVTX

Los recuentos EVTX varían con la actividad registrada y el momento de exportación. Las cifras siguientes corresponden a ejecuciones distintas y no son intercambiables:

| Contexto de ejecución | Total | EVTX | BrowserHistory | Prefetch | Registry |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cierre técnico documentado | 1499 | 1492 | 3 | 2 | 2 |
| Auditoría documental de Fase 9.0 | 1465 | 1458 | 3 | 2 | 2 |
| Demostración anterior tras reexportar EVTX | 1766 | 1759 | 3 | 2 | 2 |

La tabla principal conserva los 1499 eventos del cierre técnico. La ejecución de auditoría y la demostración anterior se registran como mediciones independientes; no sustituyen silenciosamente el baseline documental.

## Validaciones controladas

| Escenario | Fuente | Ground truth | Correctos | Cobertura | Precisión estricta | Trazabilidad |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| BrowserHistory sintético | BrowserHistory | 3 | 3 | 1.0 | 1.0 | 1.0 |
| Prefetch sintético | Prefetch | 2 | 2 | 1.0 | 1.0 | 1.0 |
| Registry sintético | Registry | 2 | 2 | 1.0 | 1.0 | 1.0 |

### Interpretación de las métricas obtenidas

Los valores de cobertura, precisión estricta y trazabilidad del 100 % corresponden exclusivamente a escenarios sintéticos controlados. Se conocían los eventos, timestamps, objetos y fuentes esperadas, y las evidencias fueron preparadas para comprobar el pipeline. Los resultados validan integración, normalización a `CommonEvent`, matching temporal y procedencia; no estiman el rendimiento ante investigaciones reales con ruido, pérdida, corrupción, manipulación o timestamps ambiguos.

| Resultado | Qué demuestra | Qué no demuestra |
| --- | --- | --- |
| Cobertura 1.0 | Todos los eventos esperados fueron detectados en el escenario controlado | Cobertura completa de Windows real |
| Precisión estricta 1.0 | Fuente, tiempo y objeto coinciden con el ground truth | Ausencia de falsos positivos en casos reales |
| Trazabilidad 1.0 | Los matches conservan referencias de procedencia | Autenticidad absoluta del artefacto |
| Desviación 0 s | Timestamps preparados y detectados coinciden | Igual exactitud en fuentes reales heterogéneas |

## Estado EVTX

El parser EVTX está operativo para ficheros `.evtx` exportados. En la validación técnica inicial se procesaron 1492 eventos reales de `Application` y `System`. No se dispone todavía de un ground truth EVTX controlado porque la generación de eventos con `eventcreate` falló por permisos en el entorno probado.

## Limitaciones principales

- Prefetch se integra mediante metadata JSON sidecar; el parsing binario nativo de `.pf` queda pendiente de backend real o herramienta externa documentada.
- Registry se integra mediante metadata JSON externa; no se lee el Registro real ni se parsean hives binarios en esta versión.
- La validación cuantificada cubre escenarios sintéticos controlados para BrowserHistory, Prefetch y Registry.
- EVTX fue probado con eventos reales, pero queda pendiente una validación controlada con ground truth.
- Los outputs pueden mezclar evidencias reales y sintéticas si comparten la misma carpeta `evidence/`; esta mezcla debe interpretarse con cuidado en resultados experimentales.
- Las evidencias y salidas se mantienen fuera de Git para evitar versionar datos sensibles.
- Los timestamps pueden representar semánticas distintas y la correlación temporal no demuestra causalidad.
- Zonas horarias desconocidas, relojes desajustados, rotación, borrado o adquisición parcial pueden alterar la timeline.
- No se ha validado un corpus amplio con múltiples versiones, idiomas y configuraciones Windows.

El tratamiento académico completo se encuentra en `docs/tfm_fragments/limitaciones_y_amenazas_validez.md`. El escenario `docs/scenarios/S02_ROBUSTNESS_PLAN.md` está diseñado, pero no se ha ejecutado ni modifica estas métricas.
