# Estrategia de testing de la GUI

## Pirámide

1. Tests unitarios de modelos, loaders, filtros y servicios.
2. Tests de integración con outputs sintéticos temporales.
3. Smoke tests de páginas Streamlit.
4. Pruebas manuales de accesibilidad, rendimiento y privacidad.

## Loaders y contratos

- `events.json` válido, vacío, raíz incorrecta y JSON inválido.
- Campos obligatorios ausentes y tipos incorrectos.
- Timestamps válidos mixtos, naive e inválidos.
- `timeline.csv` con JSON complejo válido e inválido.
- Discrepancia de recuentos entre JSON y CSV.
- Resumen o resultados de validación ausentes/parciales.

## Filtros

- Rango inclusivo, rango invertido y sin resultados.
- Fuente, categoría, acción, parser, confianza y escenario múltiples.
- Texto case-insensitive y valores null.
- Con/sin trazabilidad.
- Composición, restablecimiento y serialización de filtros.

## Servicios

- Rutas inexistentes, vacías y no escribibles.
- Entrada y salida conflictivas.
- Pipeline correcto, parcial y con excepción.
- No uso de `shell=True`.
- Exportación CSV/JSON/JSONL y colisión de destino.
- Manifiesto contiene filtros y recuentos.

## Volumen

Fixtures generadas en memoria de 1.000, 10.000 y 100.000 eventos. Medir carga, filtros y agregación sin incluir evidencia real. Confirmar que el detalle no serializa todas las evidencias brutas.

## UI y smoke tests

- Inicio renderiza sin outputs.
- Dashboard renderiza con dataset mínimo.
- Timeline cambia a agregación con volumen alto.
- Explorador mantiene filtros al abrir/cerrar detalle.
- Validación muestra advertencia sintética.
- Error de loader no derriba navegación.

## Accesibilidad y privacidad

- Recorrido por teclado.
- Contraste y zoom.
- Etiquetas de controles y resúmenes textuales de gráficos.
- Modo de enmascarado no altera datos fuente.
- Capturas de test no contienen rutas personales.

## Criterio de regresión

La suite existente debe seguir pasando en todas las fases. Los tests GUI no dependerán de `.evtx`, `.pf`, SQLite o JSON reales fuera de fixtures temporales.
