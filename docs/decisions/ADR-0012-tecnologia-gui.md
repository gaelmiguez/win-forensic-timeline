# ADR-0012 - Tecnología para la interfaz gráfica

## Contexto

El prototipo está implementado en Python, usa Pandas para la timeline y genera JSON, JSONL, CSV y Markdown. La GUI debe ejecutarse localmente, visualizar entre 1.000 y 100.000 eventos, preservar privacidad y reutilizar el pipeline y el validador sin duplicar lógica forense.

## Alternativas consideradas y criterios

Se compararon Streamlit con Plotly, PySide6 y una arquitectura FastAPI con frontend independiente. Los criterios fueron integración con Python y Pandas, coste de desarrollo, visualización temporal, testabilidad, privacidad local, accesibilidad, rendimiento con volumen alto, distribución y capacidad de sustituir la capa visual sin reescribir la lógica forense.

| Criterio | Streamlit + Plotly | PySide6 | FastAPI + frontend independiente |
| --- | --- | --- | --- |
| Integración Python | Directa | Directa | Requiere API y cliente |
| Pandas | Nativa y rápida de prototipar | Requiere modelos/adaptadores | Conversión y transporte JSON |
| Visualización | Plotly y tablas interactivas | Widgets o librerías adicionales | Máxima libertad web |
| Complejidad | Baja-media | Media-alta | Alta |
| Pruebas | Servicios puros + smoke tests | Buena, con mayor coste de UI | Buena por capas, más infraestructura |
| Distribución | Proceso local sencillo | Aplicación de escritorio empaquetable | Dos aplicaciones o bundle complejo |
| Seguridad | Local; debe fijarse host y desactivar telemetría | Superficie de red mínima | Mayor superficie HTTP |
| Accesibilidad | Depende de componentes web; razonable | Control detallado, más trabajo | Máximo control, mayor coste |
| Rendimiento | Adecuado con cache, paginación y agregación | Buen control de datasets grandes | Escalable, pero sobredimensionado para el MVP |
| Calidad visual | Profesional con personalización contenida | Escritorio sólido | Máxima flexibilidad |

## Decisión

Se selecciona **Streamlit + Plotly** para la primera GUI local. Encaja con Python y Pandas, reduce el coste de integración y permite construir dashboard, filtros, timeline y tablas interactivas sin introducir una API de red separada. Plotly se reservará para visualizaciones agregadas e interactivas; las tablas y filtros se apoyarán en Pandas.

## Justificación

La alternativa seleccionada permite reutilizar los outputs y servicios Python existentes con una superficie de integración pequeña. Es suficiente para evaluar navegación, filtrado, trazabilidad y visualización temporal en el alcance del TFM. La decisión no presupone que Streamlit sea la solución óptima para cualquier volumen, distribución o grado de personalización.

## Condiciones de diseño

- La GUI llamará a servicios de aplicación, no a parsers desde las páginas.
- El servidor escuchará únicamente en loopback por defecto.
- No se enviarán evidencias ni telemetría a servicios externos.
- La carga y filtrado se cachearán con invalidación por ruta, tamaño y fecha de modificación.
- Los detalles pesados se cargarán bajo demanda.
- La lógica de servicios y repositorios será independiente de Streamlit para facilitar tests y una migración futura.

## Consecuencias positivas

- Integración directa con Python, Pandas y los contratos existentes.
- Menor coste de prototipado para dashboard, filtros y timeline interactiva.
- Ejecución local sin desplegar una API independiente.
- Posibilidad de probar repositorios, filtros y servicios fuera de la UI.

## Consecuencias negativas

- El modelo de rerun de Streamlit obliga a gestionar de forma explícita estado, selección, cache e invalidación.
- La personalización visual, navegación avanzada y control fino de accesibilidad son menores que en un frontend dedicado.
- El empaquetado como aplicación de escritorio nativa es menos directo que con PySide6.
- Los datasets grandes pueden degradar navegador y servidor si se renderizan sin paginación, agregación o carga diferida.

## Riesgos y mitigaciones

- **Acoplamiento a Streamlit:** aislar repositorios, filtros, ejecución y exportación en servicios puros.
- **Estado incoherente tras reruns:** definir modelos serializables de estado y reglas de invalidación.
- **Consumo de memoria:** cargar detalle y `raw_evidence` bajo demanda, paginar tablas y agregar la timeline.
- **Exposición accidental:** fijar loopback, evitar telemetría y aplicar enmascarado de rutas en vistas y logs.
- **Bloqueo durante el pipeline:** impedir ejecuciones simultáneas y mostrar estados completo, parcial y fallido.

## Limitaciones

La compatibilidad básica se validó en Fase 9.1 mediante una aplicación mínima y tests de Streamlit sobre Python 3.14.6. La implementación funcional posterior midió filtros y agregación con hasta 100.000 eventos sintéticos; la medida local no constituye una garantía de rendimiento en otros equipos. La distribución nativa, la evaluación de usabilidad y la comprobación formal con tecnologías asistivas requieren trabajo específico posterior.

## Impacto en el TFM

La infraestructura y las pantallas funcionales permiten cargar outputs, ejecutar de forma segura el pipeline, explorar timeline y eventos, inspeccionar trazabilidad, revisar validaciones y descargar subconjuntos sin alterar la lógica forense. Se mantiene una separación explícita entre servicios y presentación. Las pruebas automatizadas y las mediciones técnicas no equivalen a una evaluación de usabilidad con usuarios.

## Condiciones para reconsiderar la tecnología

Se reevaluará Streamlit si las pruebas reproducibles muestran que la paginación y agregación no mantienen tiempos aceptables, si se exige una aplicación de escritorio instalable sin servidor local, si los requisitos de accesibilidad o personalización no pueden satisfacerse, o si la ejecución asíncrona del pipeline resulta incompatible con el modelo de rerun. PySide6 sería la alternativa para escritorio nativo; FastAPI con frontend separado, para una interfaz web con control y despliegue más amplios.

## Consecuencias generales

La implementación inicial será rápida y coherente con el stack. A cambio, el control fino de escritorio, empaquetado y navegación accesible será menor que en PySide6 o un frontend dedicado. Si las pruebas con 100.000 eventos o los requisitos de distribución muestran límites, la capa de servicios permitirá migrar la presentación sin rehacer el pipeline.

## Estado

Aceptada y verificada para la infraestructura y la implementación funcional. Compatibilidad comprobada en un entorno aislado con Python 3.14.6, Streamlit 1.59.2, Plotly 6.9.0 y Pandas 3.0.3; las dependencias GUI permanecen separadas de la CLI en `requirements-gui.txt`.
