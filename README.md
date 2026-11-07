# Quantile and event-probability compatibility

This release accompanies the manuscript on compatibility between quantile and event-probability outputs in remaining useful life prediction. It includes the diagnostic and analysis code, original protocols, result tables, calibration/test predictions, manuscript sources and the S0-S14 supplement. The repository is https://github.com/amirhossein2004-mozafari/rul-quantile-event-compatibility.

## Folder map

- code/ contains verbatim original implementations and new public entry points.
- protocols/ contains protocols, lock documents and small hash-referenced inputs.
- results/ contains the approved result CSVs, reports, prediction files and calibration metadata.
- paper/ contains the readable manuscript, bibliography, original figure, regenerated tables/figure and manuscript_v4_readable.pdf.
- supplement/ contains the unchanged supplement source, regenerated validation_supplement.pdf and table-source companions.
- predictions_index/predictions.csv lists the included prediction CSVs and their hashes.
- docs/file_index.csv maps original relative input names to their release locations, recording source and release hashes.
- docs/ contains requirements, preserved command/provenance records, exclusion lists and verification results.

The private inventory remains at docs/phase1_inventory/ on the author's machine. It is ignored by Git and excluded from the distributable checksum manifest. The .build/ directory contains ignored local build intermediates and fresh check outputs.

## Preserved execution records and omitted inputs

The original local paths in commands.log, compute_amendment.json, compute_amendment_lock.json, investigation_protocol_lock.json and synthetic_source_lock.json are preserved on purpose because these records are hash-locked or part of the execution log.

Exactly 185 hash-referenced files were left out of the public release. docs/excluded_hash_referenced.csv lists each original relative path, expected SHA-256, size, exclusion reason and referencing lock. Verification of those omitted files requires the full local archive. Checkpoints, optimizer states, tensors and raw NASA data remain excluded even when a protocol refers to them. No full model replay is claimed from this public folder. docs/protocol_lineage.md explains the preserved base/follow-up protocol versions and the scope of the immutable-copy check.

The five intentionally preserved path-bearing records and all immutable source copies are listed in docs/locked_files.csv. Other local path substitutions are recorded in release_cleanup_log.md and docs/path_replacements.csv. The excluded-file hashes are the recorded values used by the lock inventory, rather than fresh checks of the omitted files during this build.

## Software

The reference requirements are docs/requirements-lock-win-py311.txt. Rendering and public checks used Windows x64, Python 3.11.9, NumPy 2.3.4, pandas 3.0.0, SciPy 1.17.0, scikit-learn 1.9.0 and Matplotlib 3.10.7. PDF compilation used Pandoc 3.12.1 and MiKTeX-XeTeX 4.15 (MiKTeX 25.4), with Times New Roman, Arial and Consolas fonts.

Historical analysis environments are recorded in the verbatim provenance files and can differ from this rendering environment. No package installation, model fitting, inference or bootstrap re-estimation was performed to prepare this release.

The CSV and cross-head checks use only the Python standard library. For figure rendering, use an environment with Matplotlib. To install the recorded reference packages in a separate environment:

    python -m pip install -r docs/requirements-lock-win-py311.txt

## Regenerate every main-text table

Run from the release root:

    python -B code/render_manuscript.py tables

This regenerates paper/generated_tables/table_1.md through table_4.md and checks all 40 displayed data rows against the unchanged manuscript values.

- Table 1 reads the stored coefficients, CIs, own means and approximate MDEs from controls_projection_power/C_effect_sizes_power.csv.
- Table 2 reads incompatibility and distance summaries from contribution_step12/summary.csv.
- Table 3 reads point errors from fair_comparison_step2/per_run.csv and Brier summaries from contribution_step12/summary.csv.
- Table 4 reads the EqualSearch method results in risk_context_step8/per_run.csv.

The entry point resolves these original input names through docs/file_index.csv. It formats stored values or calculates the displayed means and sample SDs from the existing per-run CSVs. It does not fit models, calculate new CIs or alter table values.

## Regenerate the main-text figure

    python -B code/render_manuscript.py figure

This renders paper/figures/projection_brier_44_groups_regenerated.png and .pdf from all 44 projection/Brier rows in A_all_scores.csv. It uses the stored paired differences and engine-bootstrap CIs. The original included figure remains the manuscript input. These groups share 707 test engines, with 100/259/100/248 engines in FD001-FD004.

The proposed pooled true-RUL-bin figure is unavailable because no included CSV contains its pooled bin rates and engine-bootstrap CIs. The release does not invent these intervals.

## Build and verify the PDFs

    python -B code/build_pdfs.py
    python -B code/verify_documents.py

The first command writes paper/manuscript_v4_readable.pdf and supplement/validation_supplement.pdf. The second checks the rendered manuscript prose, all 40 table rows and the correspondence of main-text S0-S14 references with the supplement. docs/document_verification.json records the results. The source supplement is unchanged. paper/readability_changes.md lists each manuscript sentence edit, and docs/readability_verification.json records number, equation, citation and AI-declaration preservation.

## Portable public checks

    python -B code/reproduce_public.py csv
    python -B code/reproduce_public.py cross-head
    python -B code/verify_release.py locks
    python -B code/verify_release.py checksums

Fresh arithmetic-check outputs are written under .build/checks/. The included build records are docs/checks/csv/summary.json and docs/checks/cross_head/summary.json.

The CSV check verifies the existing validation-history and selection arithmetic, 40 point-error runs, 240 probability-method results and 160 monitoring counts. The cross-head check verifies 40 models, 160 method runs, 28,280 engine-method rows, 32 summaries and 10 boundary cases. Both pass from this public folder alone.

The original arithmetic implementations remain byte-identical. The public runner changes input-path resolution in memory and verifies the 1,281 indexed release inputs instead of the older review-packet manifest. Because raw NASA files are excluded, it checks consistency of labels stored in predictions instead of independently checking official NASA labels. The cross-head runner also omits the optional extremal-example comparison because that CSV was outside the approved copy list. These adaptations are recorded in each check summary.

Forward inference requires the omitted checkpoints/preprocessors and sensor data. Full training, synthetic replay, bootstrap re-estimation and verification of all historical lock dependencies require additional material from the full local archive, plus appropriate runtimes and the original input layout. Passing the public arithmetic checks does not establish full reproduction or independent scientific validation.

## Licensing, citation and NASA data

Copyright (c) 2026 Amir Hossein Mozafari.

Code is released under MIT; see LICENSE. Derived result CSVs and saved predictions are released under CC BY 4.0; see docs/DATA_LICENSE.md. Existing third-party notices continue to apply. CITATION.cff provides citation metadata and the repository URL; no DOI is assigned.

NASA raw data are not redistributed and remain under NASA's terms. docs/NASA_DOWNLOAD.md gives download instructions, and docs/NASA_EXPECTED_SHA256.csv lists known project-recorded raw-file hashes.

## Limitations and AI assistance

This is a single benchmark. The analyses are exploratory and use examined data, including later questions chosen after earlier results. Model groups share engines. No independent human review has been completed. OpenAI Codex assisted with code, analysis scripts, figures, language editing and checks; the same AI tool performed these checks. The manuscript's AI declaration and original provenance records are preserved verbatim. The exact served checkpoint identifier is unavailable.

## Integrity and Git

CHECKSUMS.sha256 covers every distributable payload file except itself. It excludes .git/, ignored private inventory, build intermediates and Python caches. .gitattributes preserves input bytes across Git checkout because lock hashes depend on line endings.

GitHub currently warns above 50 MiB and blocks regular Git files above 100 MiB: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github . The build checks for files above the requested 50 MB and 100 MB thresholds before committing. The repository has local commits only and has not been pushed.
