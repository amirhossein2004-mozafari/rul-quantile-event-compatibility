# IJPHM full-paper source package

Author: Amirhossein Mozafari.

This directory contains the final IJPHM submission. Earlier editorial drafts are excluded from the public tree; protocols and provenance remain unchanged. Compile with python -B build.py from this directory.

## Build

Run `python -B build.py` from this folder. The build requires Python, XeLaTeX, BibTeX, Times New Roman, and standard TeX packages: the supplied class dependencies (including sttools/flushend, apacite, wrapfig, footmisc, setspace and caption), plus fontspec, amsmath/amssymb, graphicx, booktabs, tabularx, array, etoolbox, xurl and microtype. Auxiliary files stay under .build/ and are excluded from the source archive. The included .bbl is generated with the APA bibliography style; build.py regenerates it.

The local build used a CTAN flushend dependency under ignored build directories. It is not a system installation or a modification of the original project. A complete TeX installation should provide the required package.

## Files

- manuscript.tex: editable LaTeX using the requested `\documentclass[IJPHM, 2026, 0]{phmsociety}`.
- phmsociety.cls: byte-identical copy of the supplied official class, with lowercase filename for portability.
- references.bib: unchanged manuscript bibliography, not the example bibliography.
- manuscript.bbl: generated APA bibliography of the cited works.
- projection_brier_44_groups.png: unchanged manuscript graphic, not the template example.
- manuscript.pdf: compiled journal-format article.
- manuscript.md: corresponding readable source with the authorized name, numbering and disclosure changes.
- table_values.json: exact scientific cell strings and captions.
- format_verification.json: numerical-preservation and document/layout check results.
- CHECKSUMS.sha256: package file hashes, excluding the manifest itself.

## Formatting and preservation

The abstract is unnumbered and remains 200 words. Numbering starts at Introduction and ends at Limitations and conclusion; cross-references are updated. The author name is unified in the title, single-author licence footnote, authorship statement and PDF metadata.

All four scientific tables use table* for legibility; their original identifiers remain 2, 1, 3, 4 in topical order. Figure 1 uses figure*. Equation alignment and URL/identifier break points were adjusted without changing mathematical content. Numeric atoms retain their signs and decimal digits.

The empirical numeric stream is unchanged after excluding the requested heading and cross-reference renumbering. All 40 scientific rows are verbatim, citation keys and multiplicities are unchanged, and the graphic is byte-identical; the bibliography differs only by the author-requested deletion of the Gneiting-Ranjan note and duplicate DOI URL. PDF checks pass for all 40 rows and 341 narrative windows. There are zero overfull hbox/vbox warnings, unresolved citations or missing glyphs. These are editorial checks, not new statistical analysis or independent scientific review.

The legacy class gives two cosmetic warnings: its internal name uses PHMSociety while the requested filename is lowercase, and option 0 is not declared in the class. The manuscript explicitly sets paperNumber to 0 as a submission placeholder. The original class bytes remain unchanged; the single-author licence adjustment is in the manuscript preamble.

## AI disclosure exception

The requested exclusive-use sentence conflicts with the documented assistance on code correction, analysis scripts, manuscript revision and numerical checks. A two-sentence disclosure preserves the scope of assistance. The same-tool-checking clause was removed at the author’s request. The second sentence uses the requested author-review and responsibility wording, supported by the author's confirmation. It does not claim independent review.

## Reference cleanup

At the author’s request, the Gneiting-Ranjan entry no longer contains its editorial verification note or duplicate DOI URL. Its authors, title, year, journal, volume, pages and DOI are unchanged. The build exports the newly generated bibliography before the final LaTeX passes to prevent a stale .bbl from being typeset.

## Authoritative formatting sources

The uploaded class and template were used as reference material. Their example figures, biography photo and fictional bibliography were not substituted into the manuscript.

- [Official PHM template guidance](https://phmsociety.org/international-journal-of-prognostics-and-health-management-issn-2153-2648/phm-society-publication-templates/)
- [Official IJPHM author guidance](https://phmsociety.org/international-journal-of-prognostics-and-health-management-issn-2153-2648/information-for-authors/)

The article licence note is CC BY 3.0 United States as requested. Existing release code and derived-data licences remain unchanged. The supplied class retains its original notices and TeX dependencies retain their respective licences.
