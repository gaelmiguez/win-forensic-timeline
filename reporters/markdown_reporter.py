"""Markdown summary report generation."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd

from core.event_model import CommonEvent


def generate_markdown_report(
    events: Iterable[CommonEvent],
    df: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Generate a preliminary Markdown report for the prototype timeline."""

    event_list = list(events)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()
    total_events = len(event_list)
    source_counts = Counter(event.source_artifact for event in event_list)
    sources = sorted(source_counts)

    lines = [
        "# win-forensic-timeline - Reporte preliminar",
        "",
        f"Fecha de generación (UTC): {generated_at}",
        "",
        "> Advertencia: reporte preliminar generado por el prototipo. En esta versión, BrowserHistory y EVTX se procesan directamente; Prefetch y Registry se integran mediante metadata JSON externa. El parsing binario nativo de Prefetch y Registry queda documentado como trabajo futuro.",
        "",
        "## Resumen",
        "",
        f"- Total de eventos: {total_events}",
        f"- Fuentes procesadas: {', '.join(sources) if sources else 'sin eventos normalizados'}",
    ]

    if total_events:
        timestamps = sorted(event.timestamp_utc for event in event_list)
        lines.extend(
            [
                f"- Intervalo temporal UTC: {timestamps[0].isoformat()} - {timestamps[-1].isoformat()}",
            ]
        )
    else:
        lines.append("- Intervalo temporal UTC: no disponible")

    lines.extend(["", "## Eventos por artefacto", ""])
    if source_counts:
        for source, count in sorted(source_counts.items()):
            lines.append(f"- {source}: {count}")
    else:
        lines.append("- No hay eventos normalizados para contabilizar.")

    lines.extend(["", "## Timeline", ""])
    if df.empty:
        lines.append("La timeline está vacía en esta ejecución.")
    else:
        preview_columns = [
            column
            for column in ("timestamp_utc", "source_artifact", "event_action", "description")
            if column in df.columns
        ]
        lines.append("| " + " | ".join(preview_columns) + " |")
        lines.append("| " + " | ".join("---" for _ in preview_columns) + " |")
        for _, row in df[preview_columns].head(25).iterrows():
            values = [str(row[column]).replace("|", "\\|") for column in preview_columns]
            lines.append("| " + " | ".join(values) + " |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
