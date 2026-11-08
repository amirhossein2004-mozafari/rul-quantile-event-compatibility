# Quantile and event-probability compatibility

Author: **Amirhossein Mozafari**.

Repository: https://github.com/amirhossein2004-mozafari/rul-quantile-event-compatibility

The final IJPHM submission is paper/manuscript.pdf, with editable source paper/manuscript.tex, paper/references.bib, the supplied paper/phmsociety.cls, and paper/ijphm_submission_source.zip. These replace the earlier editorial drafts. The PDF and TeX are unchanged from the approved final submission.

## IJPHM upload files

Upload paper/manuscript.pdf as the article PDF. Upload paper/ijphm_submission_source.zip as the LaTeX source archive where requested by the portal. Upload supplement/validation_supplement.pdf and supplement/ijphm_supplementary_csvs.zip as supplementary files. The supplement covers S0a-S0d and Tables S1-S14; CSV companions include A_all_scores, C_dose_response, D_mechanism, E_associations, real_RUL_bins and near_threshold_table. The supplement PDF and scientific CSV values are unchanged.

## Folder map

- paper/: final two-column manuscript, bibliography, official class, figure, exact table values and build instructions; supporting claim/source records are retained.
- supplement/: validation supplement sources/PDF, table-source companions and upload-ready CSV archive.
- code/: diagnostic, controls, projection, calibration and association implementations, plus portable public checks.
- protocols/: original protocols, hashes and small hash-referenced inputs.
- results/: result CSVs, reports, calibration/test predictions and metadata.
- predictions_index/predictions.csv: included predictions and recorded hashes.
- docs/: requirements, provenance, immutable-file index and excluded-input inventory.

## Build and portable checks

From the release root:

    python -B paper/build.py
    python -B code/render_manuscript.py tables
    python -B code/reproduce_public.py csv
    python -B code/reproduce_public.py cross-head
    python -B code/verify_release.py locks
    python -B code/verify_release.py checksums

The manuscript build requires XeLaTeX, BibTeX, Times New Roman and the TeX dependencies listed in paper/README.md. It performs compilation only. Scientific tables use existing CSV values; no new CIs are estimated. See docs/requirements-lock-win-py311.txt for the recorded analysis environment; the public CSV/cross-head checks use Python's standard library. Original environment/build identifiers remain in the provenance records.

The public checks verify arithmetic and saved-label consistency; they do not independently validate NASA labels. The cross-head optional extremal-example comparison is omitted because its CSV was outside the approved copy list. Passing these checks is not full model reproduction or independent scientific validation. docs/file_index.csv maps retained historical input names to current release bytes; retired editorial drafts are no longer indexed as public inputs.

## Preserved records and omitted inputs

Exactly 185 hash-referenced inputs, including checkpoints, tensors, raw NASA data and other reproduction material, are omitted. docs/excluded_hash_referenced.csv lists their SHA-256 values and referencing locks. Full retraining and full lock verification require the full local archive. NASA download instructions and known hashes are in docs/NASA_DOWNLOAD.md and docs/NASA_EXPECTED_SHA256.csv.

Original local paths in commands.log, compute_amendment.json, compute_amendment_lock.json, investigation_protocol_lock.json and synthetic_source_lock.json are intentionally preserved because they are hash-locked or execution records. All immutable scientific inputs and historical protocols/reports retain their original bytes. They can contain historical review wording; they are not earlier manuscript drafts. Prior Git commits also retain their history and were not rewritten.

Superseded manuscript/editorial files are archived under ignored .build/pre_submission_history. The private inventory docs/phase1_inventory/, all .build/ directories and Git internals are excluded from public checksums and source archives. CHECKSUMS.sha256 covers distributable payload files except itself. .gitattributes preserves line endings for hash integrity.

## Licensing and scope

Copyright (c) 2026 Amirhossein Mozafari. Code is MIT licensed (LICENSE); derived result CSVs and saved predictions are CC BY 4.0 (docs/DATA_LICENSE.md). The manuscript's journal licence footnote follows the supplied IJPHM template. NASA data are not redistributed and remain under NASA's terms. CITATION.cff records the author and repository URL; no Zenodo DOI is assigned.

This is a single-benchmark exploratory study using examined data. The expanded model groups share test engines. Generative AI assistance is disclosed in the final manuscript; original execution/provenance records remain unchanged. The author confirmed personal review and takes responsibility for the submitted work.
