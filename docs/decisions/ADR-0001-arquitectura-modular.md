# ADR-0001 - Arquitectura modular

## Contexto

El TFM requiere una herramienta extensible para trabajar con artefactos forenses heterogéneos de Windows.

## Decisión

Separar el proyecto en módulos de `core`, `extractors`, `parsers`, `normalizers`, `correlator`, `reporters` y `validation`.

## Alternativas consideradas

- Script monolítico con todo el flujo en un único fichero.
- Organización por caso de uso en lugar de por responsabilidad técnica.

## Justificación

La separación por responsabilidades facilita pruebas unitarias, sustitución de parsers y evolución incremental sin reescribir el pipeline completo.

## Impacto en el TFM

La arquitectura permite explicar con claridad el diseño del prototipo y justificar futuras ampliaciones de artefactos.
