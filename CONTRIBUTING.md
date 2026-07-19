# Contribución

## Preparación

1. Cree un entorno virtual.
2. Instale `requirements.txt` y, para cambios de interfaz, `requirements-gui.txt`.
3. Ejecute las pruebas antes y después del cambio.

```bash
python -m pytest -q
python -m compileall -q core correlator extractors gui normalizers parsers reporters validation main.py
python -m pip check
```

## Normas de contribución

- Mantenga la separación entre parser, `CommonEvent`, correlación, reporter, validador y GUI.
- Añada pruebas proporcionales al cambio.
- Documente nuevas semánticas temporales y reglas de mapeo.
- No presente capacidades futuras como implementadas.
- No incluya una evaluación, benchmark o métrica que no pueda reproducirse.

## Prohibición de evidencias reales

Solo se aceptan fixtures completamente sintéticas. No añada EVTX, historiales, hives, Prefetch, SRUM, bases de datos, volcados, rutas personales, nombres reales, SID, hosts, correos, IP de entornos privados, credenciales ni outputs derivados de evidencias reales.

Use valores inequívocamente ficticios como `example.com`, `ExampleApp`, `UpdaterTask` y timestamps controlados.
