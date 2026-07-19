# Plan de integración de la GUI en la memoria

## Momento de actualización

La memoria Word/PDF se actualizará después de implementar, probar y capturar la GUI. La Fase 9.0 solo prepara textos y estructura; no modifica el documento final.

## Secciones a revisar

| Sección | Integración prevista |
| --- | --- |
| Resumen y abstract | Añadir interfaz local, exploración y trazabilidad visual |
| Objetivos | Incorporar objetivos medibles de interacción y usabilidad |
| Metodología | Explicar diseño por servicios, iteraciones y pruebas GUI |
| Arquitectura | Añadir capa GUI -> servicios -> pipeline -> repositorios |
| Desarrollo | Describir tecnología, páginas, filtros y detalle |
| Validación | Añadir pruebas funcionales, rendimiento y usabilidad |
| Resultados | Capturas, tiempos de carga y tareas completadas |
| Discusión | Límites de Streamlit, escala y privacidad |
| Limitaciones | Accesibilidad evaluada, ausencia de análisis causal y alcance local |
| Conclusiones | Valorar mejora de operabilidad sin alterar lógica forense |
| Trabajo futuro | Empaquetado, backend binario y estudios con usuarios |
| Anexos | Manual, configuración, tests y estructura GUI |

## Figuras futuras

1. Pantalla de inicio con rutas anonimizadas.
2. Dashboard con datos sintéticos o enmascarados.
3. Timeline agregada e intervalo UTC.
4. Panel de filtros activos.
5. Detalle de `CommonEvent`.
6. Vista de `provenance` y `traceability_ref`.
7. Resultados de validación con advertencia sintética.
8. Exportación y manifiesto de filtros.
9. Estado vacío o error controlado.

## Tablas futuras

- Comparativa tecnológica y justificación de Streamlit + Plotly.
- Correspondencia entre requisitos GUI, componentes y tests.
- Resultados de tareas de usabilidad.
- Rendimiento con 1.000, 10.000 y 100.000 eventos sintéticos.
- Limitaciones y mitigaciones de la interfaz.

## Evidencia necesaria antes de redactar

- Commits y suite final.
- Capturas anonimizadas reales de la aplicación.
- Resultados de smoke tests y accesibilidad.
- Medidas de carga, filtrado y agregación.
- Registro de warnings y errores probados.
- Confirmación de que la CLI sigue siendo compatible.

## Reglas de redacción

- No describir pantallas que no estén implementadas.
- Distinguir métricas del pipeline, rendimiento GUI y usabilidad.
- Mantener la contextualización de resultados sintéticos.
- No incluir rutas personales, SIDs, nombres de equipo o eventos privados.
- Actualizar índices y figuras únicamente en la fase documental final.
