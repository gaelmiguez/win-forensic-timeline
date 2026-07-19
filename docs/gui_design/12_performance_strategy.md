# Estrategia de rendimiento

## Objetivo de escala

Diseño para 1.000 a 100.000 eventos, con EVTX como fuente dominante. El límite práctico se medirá en el equipo de referencia antes de fijar garantías.

## Carga

- Cache por ruta, tamaño, `mtime` y versión de loader.
- Carga única de `events.json` a DataFrame normalizado.
- Conversión vectorizada de timestamps con Pandas.
- Columnas ligeras para tabla; `raw_evidence` y `provenance` permanecen como objetos y se serializan solo en detalle/exportación.
- Informe de filas inválidas separado del dataset válido.

## Filtros

- Máscaras vectorizadas para tiempo, fuente, categoría, acción, parser, confianza y escenario.
- Texto libre sobre columnas normalizadas preseleccionadas.
- Búsqueda en evidencia bruta opcional, con advertencia de coste.
- `FilterState` hashable para cachear subconjuntos frecuentes.

## Tabla

Paginación de servidor o virtualización; no enviar 100.000 filas al navegador. Ordenación sobre columnas tipadas. Detalle de una sola fila bajo demanda.

## Timeline

Granularidad automática:

- Hasta 2.000 eventos visibles: puntos individuales.
- 2.001-20.000: agregación por intervalo adaptativo y drill-down.
- Más de 20.000: histograma por fuente y rango, sin puntos individuales iniciales.

La selección de rango vuelve a calcular sobre el subconjunto, no sobre toda la figura.

## Pipeline

La ejecución debe salir del hilo de renderizado o usar un mecanismo de progreso compatible con Streamlit. No se lanzan dos pipelines sobre el mismo output. Los outputs parciales no sustituyen el dataset activo hasta finalizar la validación de contratos.

## Presupuestos iniciales

| Operación | Objetivo de referencia |
| --- | ---: |
| Cargar 10.000 eventos | < 3 s |
| Filtrar 10.000 eventos | < 1 s |
| Paginar tabla | < 500 ms |
| Abrir detalle | < 300 ms |
| Construir agregado de 100.000 | < 5 s |

Se medirán con pruebas reproducibles; no son resultados actuales.

## Invalidación

Cambiar output root, tamaño o fecha de un output invalida repositorios, agregados, selección y validación. Cambiar solo filtros no recarga disco.
