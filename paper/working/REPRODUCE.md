# Reproducing the package

The package contains a conceptual architecture and synthetic reasoning examples. It contains no implemented threat-analytics system, production data or measured performance results.

## Files

- [Complete manuscript](MANUSCRIPT.md) and [rendered manuscript](MANUSCRIPT.pdf).
- [Supplement](SUPPLEMENT.md) and [rendered supplement](SUPPLEMENT.pdf). The 19 CSV files are in `SUPPLEMENT/`.
- [Citation-source manuscript](SOURCE/manuscript.md) and [citation-source supplement](SOURCE/supplement.md). Edit these sources before rebuilding; the reader-facing Markdown, TeX and PDFs are generated from them. `SOURCE/layout.lua`, `SOURCE/header.tex` and `SOURCE/references.csl` control layout and citation style.
- [References in CSL JSON](REFERENCES.json) are the typesetting input. [BibLaTeX references](REFERENCES.bib) provide the same 122 identities for reuse; they are generated from the CSL JSON with Pandoc. Source inspection versions and limits are in the [source notes](SUPPLEMENT/S1_CITED_SOURCE_NOTES.csv).
- Figures are editable SVG files in `FIGURES/`. The PDF exports are used for typesetting; the PNG exports are readable alternates.
- [What changed since version 1.0](CHANGES_SINCE_v1.0.md), generated from the sources by `tools/changes_since.py`.
- `BUILD.py` rebuilds the documents and `CHECK_CANDIDATE.py` runs the finite checks. `EXPORT_FIGURES.py` exports the figures when Inkscape is not installed. `tools/` holds optional Markdown round-trip helpers that convert reader-facing Markdown back to citation-key sources and confirm a byte-identical rebuild.
- [Third-party notices](THIRD_PARTY_NOTICES.md) and `MANIFEST_SHA256.txt`.

The manuscript and the supplement each have a numbered bibliography listing the works their own text cites (104 and 56 works); those numbers are local to each document. Citation keys in the CSV files resolve against the complete CSL JSON and BibLaTeX set, and all 122 works are cited across the pair.

## Run the finite checks

From the extracted package directory, run:

```sh
python3 CHECK_CANDIDATE.py
```

Python 3's standard library is sufficient for the data and arithmetic checks. Pandoc, if installed, also checks the BibLaTeX identity roundtrip. The script checks inventory identifiers and counts, mapping joins, acyclic feature lineage, all 24 functions, citation sets, table and figure numbering (six tables and four figures), that the 122 cited works are all cited across the manuscript and supplement pair and that each generated bibliography matches its own text, figure exports, relative links, the absence of internal project identifiers and em dashes in reader-facing files, the S7.1 sizing arithmetic (the union bound for four confirmatory evaluations; the 299 planted false exonerations E8 needs at least to show a release rate below 1 percent with none released; and the 628 it needs for 93 percent power if the true release rate is 0.1 percent, which at 5 percent prevalence and 20 drafts a day means 12,560 drafts over about 628 days), and the synthetic calculations. For Trace B it checks the 2% chargeback measure, the separate 5% chargeback-or-alert-resolution measure, the rejected 5.5% undeduplicated sum, and that counting chargebacks where they were recorded would show account D at 0/100 while transaction attribution restores 2/100. For Trace A it checks that an edge learned at +1 day cannot enter an assessment frozen at +30 minutes merely because its effective date is earlier. These checks do not prove source claims or evaluate an implemented system.

## Rebuild the documents

```sh
python3 BUILD.py
python3 CHECK_CANDIDATE.py
```

The build requires Pandoc with citeproc and XeLaTeX. The version 1.0 baseline was built with Pandoc 3.1.3 and TeX Live 2023/Debian. The candidate build versions are recorded in PROPOSAL.md. Required TeX packages include `fontspec`, `unicode-math`, `longtable`, `booktabs`, `array`, `calc`, `xurl`, `needspace`, `placeins`, `seqsplit` and `hyperref`. `SOURCE/layout.lua` sets captioned tables and figures as top-placed floats, except Figure 4, which is placed at the bottom of a page or on a float page so that it follows the Section 7 heading. Table S9.1 is taller than a page, so it is set as two floats: the caption and first row at the bottom of a page, then the other rows, headed "Table S9.1 (continued)", on the float page that follows, with no text between them. Table 6 directly follows its heading, so it prints there if it fits; otherwise it prints at the top of the next page and the Section 8.3 text fills the space before it. The S6 heading starts a new page, and Table S6.1, which is nearly a page tall, is a top-only float: it prints at the top of the page after its heading, and the S6 text before it fills the heading's page. Table 1 prints at the top of a page after the Section 2.4 heading and the paragraph that cites it. The Section 4.2 sentence that introduces the three planes is kept on one page with its list, and Figure 1 follows the list. The uncaptioned query-interface table in S4 and the uncaptioned SDK-file table in S5 are set in place after space reservations; the query-interface table may break between rows, with its header repeated. Inline code is not hyphenated, and short inline code containing spaces, such as the worked arithmetic, is kept on one line. Signal and mechanism identifiers, such as SIG-16, do not break at their hyphen. `SOURCE/header.tex` prevents a paragraph's first or last line from standing alone at a page break. Fonts are the TeX Live Latin Modern Roman, Sans, Mono and Math families, loaded by filename. Font files are not redistributed.

Three environment fallbacks are built in and reported when used:

- Figure exports use Inkscape when it is installed. Otherwise `EXPORT_FIGURES.py` converts each SVG to a single-page vector PDF and a 1.5x PNG with headless Chromium (this package's exports used the Chromium installed at `/opt/pw-browsers/chromium`). Set `CHROMIUM` to a browser executable if it is not found automatically. If no exporter is available and the PDF and PNG exports are already present, the build reuses them and says so.
- Pandoc's LaTeX template loads `lmodern.sty`. If the TeX installation lacks it, the build writes a stub to `build/` and adds that directory to `TEXINPUTS`. Under XeLaTeX the generated source then sets every font explicitly through `fontspec`, so the stub does not change the fonts used.

The build runs offline. Temporary compiler output goes in `build/`, which is not part of the package. The generated `SOURCE/manuscript.tex` can be compiled from the package root with the figure PDFs in `FIGURES/`; citations are already typeset in the generated TeX, so no BibTeX pass is needed. No platform-specific submission archive is included.

## Verify the package files

`MANIFEST_SHA256.txt` lists the SHA-256 hash of every package file except itself, sorted by path. It excludes the `build/`, `__pycache__/` and `.git/` directories and temporary `.log` files, which are not part of the package. From the package directory, run:

```sh
sha256sum -c MANIFEST_SHA256.txt
```

The manifest pins this working package's bytes, not a published release; it does not claim bit-for-bit reproducibility on every system. Rebuilding may change PDF metadata and byte hashes across tool versions. Compare text, references, calculations and layout, then create a new hash manifest for any adopted revision.

## Interpretation and release status

All 400 cohort rows and the timing schedule are hypothetical. Count distinct transaction identifiers; do not add overlapping report flags or treat the account where other accounts' chargebacks are recorded as an extra transaction cohort. Published source texts and live documentation remain external; the package supplies locators rather than redistributing them. Current inspection limits remain in S1, and the source directory records how each of its 61 sources was read in October 2026.

For licensing, see the manuscript's License declaration and, for the schema-derived material in `SUPPLEMENT/S5_EVENT_TYPES.csv` and `SUPPLEMENT/S5_SIGNAL_LOCATORS.csv`, [Third-party notices](THIRD_PARTY_NOTICES.md).

This is working text for version 1.1. The date on the first page of each document is the date of the latest accepted merge. See [STATUS.md](STATUS.md) for its accepted merges. It is not a published version and has not been peer reviewed. The author's declarations are in the manuscript.

## Revision status automation

`REVISION_STATUS.json` records the working-draft status and each accepted merge. `STATUS.md` is its readable form. After a merge into main, GitHub Actions finds the merged pull request from the merge commit, records it, synchronizes the source labels and README, rebuilds both documents and the change record, runs the full checks, refreshes the manifest and commits the generated files. Accepted working draft does not mean published.

Pull-request checks run `python3 CHECK_CANDIDATE.py --sources` and `python3 tools/revision_status.py check --sources`, which do not require rebuilt outputs. For a full local reproduction, run `python3 tools/revision_status.py sync`, `python3 BUILD.py`, `python3 tools/changes_since.py`, `python3 CHECK_CANDIDATE.py`, then `python3 tools/revision_status.py manifest` and `python3 tools/revision_status.py check`. The tests in `tools/test_revision_status.py` and `tools/test_changes_since.py` mock GitHub and need no network. The acceptance command requires a real GitHub merge into main and will not record an open, closed-unmerged or review-only pull request.
