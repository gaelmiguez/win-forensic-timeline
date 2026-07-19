# REPOSITORY_AUDIT

Fecha de auditoría: 2026-07-19.

Método: inventario recursivo del proyecto original y copia a una carpeta independiente mediante una lista positiva. Los directorios voluminosos excluidos se agrupan por prefijo; todos sus archivos fueron contabilizados y ninguno se copió.

## Directorios excluidos agrupados

| Ruta relativa | Archivos | Tamaño aproximado | Categoría | Acción | Motivo | Riesgo |
| --- | ---: | ---: | --- | --- | --- | --- |
| `.git/**` | 43 | 122.64 MB | Generado o innecesario: no publicar | Excluido | Se crea un historial Git nuevo para evitar arrastrar objetos borrados o datos históricos. | Medio |
| `.pytest_cache/**` | 5 | 0.02 MB | Generado o innecesario: no publicar | Excluido | Entorno, caché o bytecode regenerable. | Bajo |
| `.venv-gui/**` | 14588 | 414.89 MB | Generado o innecesario: no publicar | Excluido | Entorno, caché o bytecode regenerable. | Bajo |
| `__pycache__/**` | 2 | 0.01 MB | Generado o innecesario: no publicar | Excluido | Entorno, caché o bytecode regenerable. | Bajo |
| `artifacts/**` | 930 | 191.31 MB | Privado o sensible: no publicar | Excluido | Material de trabajo, copias y artefactos académicos no necesarios para ejecutar el prototipo. | Alto |
| `backup/**` | 5 | 11.94 MB | Privado o sensible: no publicar | Excluido | Material de trabajo, copias y artefactos académicos no necesarios para ejecutar el prototipo. | Alto |
| `evidence/**` | 9 | 2.16 MB | Privado o sensible: no publicar | Excluido | Puede contener evidencias reales o salidas derivadas de ellas. | Alto |
| `output/**` | 24 | 6.48 MB | Privado o sensible: no publicar | Excluido | Puede contener evidencias reales o salidas derivadas de ellas. | Alto |

## Inventario individual

| Ruta relativa | Tipo | Categoría | Acción | Motivo | Riesgo |
| --- | --- | --- | --- | --- | --- |
| `.agents/skills/forensic-gui-design/references/design-principles.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `.agents/skills/forensic-gui-design/references/domain-model.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `.agents/skills/forensic-gui-design/SKILL.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `.gitignore` | sin extensión | Publicable después de sanear | Copiado a la carpeta saneada y revisado | Documento necesario para publicación; se elimina cualquier supuesto no verificable. | Bajo |
| `.streamlit/config.toml` | toml | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `CODEX_REVIEW_BUNDLE_PHASE_9_0_ACADEMIC.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_0_GUI_DESIGN.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_1.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_2_9_8.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_2_9_8_REDESIGN.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_8B_FINAL_POLISH.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `CODEX_REVIEW_BUNDLE_PHASE_9_8C_RELEASE_CANDIDATE.md` | md | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `config/artifacts.yaml` | yaml | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `config/settings.yaml` | yaml | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `core/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `core/__pycache__/__init__.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/event_model.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/event_model.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/exceptions.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/exceptions.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/time_utils.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/__pycache__/time_utils.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `core/constants.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `core/event_model.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `core/exceptions.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `core/time_utils.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `correlator/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `correlator/__pycache__/__init__.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `correlator/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `correlator/__pycache__/timeline_correlator.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `correlator/__pycache__/timeline_correlator.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `correlator/timeline_correlator.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/00_baseline_arquitectura_v3.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0001-arquitectura-modular.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0002-modelo-comun-eventos.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0003-validacion-ground-truth.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0004-normalizacion-temporal-utc.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0005-uso-pandas-correlacion.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0006-estrategia-prefetch.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0007-parser-historial-navegador.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0008-parser-evtx.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0009-validador-ground-truth.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0010-prefetch-metadata-json.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0011-registry-metadata-json.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/decisions/ADR-0012-tecnologia-gui.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/final_metrics.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/01_product_brief.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/02_personas_and_use_cases.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/03_user_flows.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/04_information_architecture.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/05_screen_specifications.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/06_wireframes.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/07_design_system.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/08_component_inventory.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/09_data_contracts.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/10_accessibility.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/11_security_privacy.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/12_performance_strategy.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/13_testing_strategy.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/14_implementation_plan.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/15_acceptance_criteria.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/16_memory_integration_plan.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/17_current_visual_audit.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/17_phase_9_1_implementation.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/18_forensic_clarity_design_system.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/18_phase_9_2_9_8_implementation.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/19_visual_accessibility_review.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/20_before_after_review.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/21_phase_9_8b_final_polish.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/gui_design/22_phase_9_8c_release_candidate.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/implementation_log.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/scenarios/S01_BROWSER_EVTX.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/scenarios/S02_ROBUSTNESS_PLAN.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `docs/tfm_fragments/desarrollo_prototipo.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/tfm_fragments/gap_estado_del_arte.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/tfm_fragments/gui_implementation.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/tfm_fragments/limitaciones_y_amenazas_validez.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/tfm_fragments/modelo_eventos.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/tfm_fragments/validacion_resultados.md` | md | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `docs/validation_log.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `extractors/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `extractors/file_collector.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/__pycache__/app.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/__pycache__/config.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/__pycache__/models.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/__pycache__/runtime.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/app.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/assets/app_brand.svg` | svg | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/assets/app_brand_dark.svg` | svg | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/assets/app_mark.svg` | svg | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/assets/forensic_clarity.css` | css | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/assets/forensic_clarity_dark.css` | css | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/app_shell.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/data_quality.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/dataset_context.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/empty_state.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/event_summary.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/event_table.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/filters.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/issues.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/load_status.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/methodology_warning.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/metrics.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/page_header.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/section_panel.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/source_legend.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/status_badge.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/__pycache__/utc_range.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/components/app_shell.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/data_quality.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/dataset_context.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/empty_state.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/event_summary.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/event_table.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/filters.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/issues.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/load_status.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/methodology_warning.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/metrics.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/page_header.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/section_panel.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/source_legend.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/status_badge.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/components/utc_range.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/config.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/models.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/about.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/dashboard.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/event_detail.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/event_explorer.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/export.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/home.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/timeline.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/__pycache__/validation.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/pages/about.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/dashboard.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/event_detail.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/event_explorer.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/export.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/home.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/timeline.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/pages/validation.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/runtime.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/dashboard_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/event_detail_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/event_repository.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/export_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/filter_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/output_catalog.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/pagination_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/path_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/pipeline_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/state_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/timeline_repository.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/timeline_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/validation_repository.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/validation_view_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/__pycache__/version_service.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/services/dashboard_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/event_detail_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/event_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/export_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/filter_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/output_catalog.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/pagination_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/path_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/pipeline_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/state_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/timeline_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/timeline_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/validation_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/validation_view_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/services/version_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/theme/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/theme/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/theme/__pycache__/plotly_theme.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/theme/__pycache__/theme_loader.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/theme/__pycache__/tokens.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `gui/theme/plotly_theme.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/theme/theme_loader.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `gui/theme/tokens.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `main.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `normalizers/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `normalizers/event_normalizer.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `parsers/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `parsers/__pycache__/__init__.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/browser_history_parser.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/browser_history_parser.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/evtx_parser.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/evtx_parser.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/prefetch_parser.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/prefetch_parser.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/registry_parser.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/__pycache__/registry_parser.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `parsers/browser_history_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `parsers/evtx_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `parsers/prefetch_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `parsers/registry_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `README.md` | md | Publicable después de sanear | Copiado a la carpeta saneada y revisado | Documento necesario para publicación; se elimina cualquier supuesto no verificable. | Bajo |
| `reporters/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `reporters/__pycache__/__init__.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/csv_reporter.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/csv_reporter.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/json_reporter.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/json_reporter.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/markdown_reporter.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/__pycache__/markdown_reporter.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `reporters/csv_reporter.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `reporters/json_reporter.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `reporters/markdown_reporter.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `requirements-gui.txt` | txt | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `requirements.txt` | txt | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `scripts/__pycache__/generate_sample_prefetch_metadata.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/__pycache__/generate_sample_prefetch_metadata.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/__pycache__/generate_sample_registry_metadata.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/__pycache__/generate_sample_registry_metadata.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/__pycache__/run_scenario_s01_browser_evtx.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/__pycache__/run_scenario_s01_browser_evtx.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `scripts/export_windows_evtx.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `scripts/generate_sample_browser_history.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `scripts/generate_sample_prefetch_metadata.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `scripts/generate_sample_registry_metadata.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `scripts/run_scenario_s01_browser_evtx.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_browser_history_parser.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_browser_history_parser.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_event_model.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_event_model.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_evtx_parser.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_evtx_parser.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_main_with_browser_fixture.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_main_with_browser_fixture.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_prefetch_parser.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_prefetch_parser.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_registry_parser.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_registry_parser.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_reporters.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_reporters.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_scenario_s01_script.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_scenario_s01_script.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_time_utils.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_time_utils.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_timeline_correlator.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_timeline_correlator.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_validator.cpython-312-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/__pycache__/test_validator.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/fixtures/gui/capture_validation/validation_results_browser_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/capture_validation/validation_results_prefetch_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/capture_validation/validation_results_registry_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/capture_validation/validation_summary_browser_synthetic.json` | json | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/capture_validation/validation_summary_prefetch_synthetic.json` | json | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/capture_validation/validation_summary_registry_synthetic.json` | json | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/events_valid.json` | json | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/timeline_valid.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/validation_results_fixture.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/fixtures/gui/validation_summary_fixture.json` | json | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/__init__.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/__pycache__/__init__.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/conftest.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_app_smoke.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_capture_validation_fixtures.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_dashboard_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_event_detail_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_event_repository.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_export_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_filter_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_gui_localization.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_output_catalog.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_pagination_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_path_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_performance_paths.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_pipeline_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_state_and_version_services.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_theme_system.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_timeline_repository.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_timeline_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_validation_repository.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/__pycache__/test_validation_view_service.cpython-314-pytest-9.1.1.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `tests/gui/conftest.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_app_smoke.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_capture_validation_fixtures.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_dashboard_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_event_detail_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_event_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_export_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_filter_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_gui_localization.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_output_catalog.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_pagination_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_path_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_performance_paths.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_pipeline_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_state_and_version_services.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_theme_system.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_timeline_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_timeline_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_validation_repository.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/gui/test_validation_view_service.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_browser_history_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_event_model.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_evtx_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_main_with_browser_fixture.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_prefetch_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_registry_parser.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_reporters.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_scenario_s01_script.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_time_utils.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_timeline_correlator.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `tests/test_validator.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `TFM_FINAL_LIMITED_DIFF_REPORT.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL.docx` | docx | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL.pdf` | pdf | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CHANGELOG.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CORREGIDO.docx` | docx | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CORREGIDO.pdf` | pdf | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CORREGIDO_ENTREGA.zip` | zip | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CORREGIDO_MANIFEST.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_CORREGIDO_QA.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_ENTREGA.zip` | zip | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_ENTREGA_V2.zip` | zip | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_PAGE_COUNT.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_QA_REPORT.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_RELEASE_MANIFEST.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_REVIEW.pdf` | pdf | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_GaelMiguezMendez_FINAL_WORKING.docx` | docx | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `TFM_SOURCE_SELECTION_REPORT.md` | md | Privado o sensible: no publicar | Excluido | Documento académico, informe o paquete de entrega no autorizado para publicación. | Alto |
| `validation/__pycache__/validator.cpython-312.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `validation/__pycache__/validator.cpython-314.pyc` | pyc | Dudoso: no publicar hasta verificarlo | Excluido | Archivo no versionado y no incluido expresamente en la lista positiva. | Medio |
| `validation/ground_truth.csv` | csv | Generado o innecesario: no publicar | Excluido | Archivo versionado que no forma parte de la lista positiva de publicación. | Bajo |
| `validation/ground_truth_browser_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `validation/ground_truth_prefetch_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `validation/ground_truth_registry_synthetic.csv` | csv | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `validation/validation_schema.md` | md | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |
| `validation/validator.py` | py | Publicable sin cambios | Copiado mediante lista positiva | Archivo versionado necesario para comprender, ejecutar o probar el prototipo. | Bajo |

## Resultado de la lista positiva

Se copiaron 179 archivos versionados. No se copiaron evidencias, salidas, entornos virtuales, cachés, documentos académicos, paquetes de entrega ni el historial Git original.

La revisión de secretos y datos personales se documenta en `PUBLICATION_MANIFEST.md` tras ejecutar los escaneos sobre esta copia.
