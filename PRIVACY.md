# Privacidad y tratamiento de datos

## Datos procesados

La herramienta puede procesar historiales de navegador, registros EVTX, referencias Prefetch y metadatos Registry. Estas fuentes y sus salidas pueden contener usuarios, hosts, SID, rutas, URLs, marcas temporales, programas ejecutados y otra información personal o confidencial.

## Modelo de ejecución

La CLI y la GUI se ejecutan localmente. La GUI escucha en `127.0.0.1`, desactiva la telemetría de Streamlit y no requiere servicios externos. Las evidencias se tratan en modo de solo lectura y las salidas se escriben en directorios separados.

## Responsabilidad del usuario

- Use únicamente datos para los que disponga de autorización.
- Mantenga evidencias y outputs fuera del control de versiones.
- Proteja las salidas con controles de acceso adecuados.
- Revise y minimice los datos antes de compartir un informe o una exportación.
- No adjunte evidencias reales a issues, discusiones ni reportes públicos.

La ocultación de rutas en la interfaz es una ayuda visual, no una técnica de anonimización irreversible.
