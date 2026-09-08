# Rule: Excel Coding Sheet Data Integrity

This document defines the strict data type policies, template schemas, and evidence standards for all BSMA coding sheets.

---

## 1. Universal Zero Guesswork & Dual Missing Data Protocol (Rule 1)
- **Absolute Prohibition on Imputation (Zero Guesswork):** Never guess, fabricate, or impute data. Do NOT calculate averages or deduce missing values under any circumstances.
- **Dual Missing Data Protocol (Numeric 999 vs. Clean Blank Text):**
  - **Numeric Missing Values (Cols 17–50):** Whenever an empirical numeric metric is missing or not reported in the paper (Mean Age [Col 23], % Female [Col 24], Org Tenure [Col 25], Number of Items [Cols 27 & 34], Min/Max Likert Anchors [Cols 28, 29, 35, 36], Mean [Cols 42 & 46], SD [Cols 43 & 47], Reliability/Alpha [Cols 44 & 48]), YOU MUST enter the integer `999`. This ensures statistical analysis software (R, SPSS, CMA, Stata) can unambiguously identify missing data.
  - **Text / Categorical Non-Applicable Fields:** Non-applicable or unneeded text cells (`Reason for Exclusion` for included papers, `Other (specify)`, `Report Type Note`, `Notes`, and `Article Descriptors`) MUST be left as clean BLANK cells (`None`). Writing `"Not Reported"` into Excel cells is strictly prohibited to eliminate visual clutter.
  - **Excluded Papers (Code 0):** Terminate immediately at Col 6 (`Reason for Exclusion`), leaving all subsequent columns (Cols 7–50) as clean BLANK cells (`None`), mirroring Paper #66 in `49_53_66.xlsx`.

---

## 2. Template Structure & Format Compliance (Rules 3, 6, 19)
- **Universal Master Insertion (Rule 6):** ALL successfully processed papers MUST be injected into `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx`. Every paper must retain its assigned BSMA ID.
- **50-Column Full Extraction Schema (Rule 19):** `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx` is the ultimate master template and contains the 50-column "Full Text Data Extraction" structure (Columns A through AX, covering Study/Sample Descriptors and Measure Descriptors).
- **Screening vs Extraction Sheet Separation (Rule 19):**
  - **Screening Master (`BSMA_Master_Coding_Sheet.xlsx`):** Retains full bibliographic metadata in Cols 1–16 (Article ID, Judgments, Reasons, Abstract, Title, Authors, Year, Notes) as the permanent screening record.
  - **Extraction Batch Sheets (`[start]_[end].xlsx`):** Dedicated full-text extraction sheets eliminate bibliographic redundancy:
    - `Col 3 (Sample ID)`: Left blank (`None`).
    - `Cols 7–16 (Article Descriptors)`: Left completely blank (`None`) because this metadata is already preserved in the screening database.
    - `Included Papers (1 = include)`: Data population strictly begins at **Col 17 (Study/Sample Descriptors)** through Col 50 (`Effect Size`).
    - `Excluded Papers (0 = exclude)`: Terminate immediately after **Col 6 (`Reason for Exclusion`)**, leaving all subsequent columns (Cols 7–50) completely blank (`None`).
- **Prohibition of Bold Headers (Rule 3):** Never use markdown bold (`**`) or rich text bolding inside Excel header cells.

---

## 3. Verbatim Quote Evidence Standards (Rule 13)
- **Mandatory Quote Injection:** Whenever a paper is judged—whether `1 = Include` or `0 = Exclude`—you MUST extract and inject exact, character-for-character verbatim quotes from the PDF text into Col 16 (Notes).
- **Strict Prohibition of Ellipses (No Truncation):** NEVER use ellipses (`...`) to summarize, abbreviate, or truncate sentences. You must extract full, complete sentences or paragraphs exactly as they appear in the original text.
- **Maximum Multi-Section Evidence:** Collect the maximum evidence possible from multiple sections (Abstract, Participants, Measures, Discussion) to robustly prove the sample type or exclusion reason.
- **Exact Note Format:** Use brackets to indicate the section of each quote:  
  `[Reason summary]. Verbatim Evidence: "[Section 1] <exact quote 1>" [Section 2] "<exact quote 2>"`

---

## 4. Verbatim Variable & Measure Naming Standards (Rule 14)
- **Table Axis Variable Name Fidelity & Index Number Pruning (Cols 41 & 45):** 
  - Variable names for Boundary Spanning Behavior (Col 41) and Non-BS Variables (Col 45) MUST character-for-character preserve the author's exact phrasing, internal/external sub-construct specifiers (e.g., `"Internal COBSB"`, `"External COBSB"`, `"Internal Com."`, `"External Com."`), and published abbreviations (e.g., `"BSA"`, `"Org. Comm."`, `"Dual Comm."`).
  - **Table Layout Index Pruning:** Leading numbering prefixes (e.g., `"1. "`, `"2) "`, `"(3) "`, `"10. "`) that serve purely as table matrix row/column layout indices MUST be automatically pruned. Such numbers are indexing coordinates, not theoretical construct names. The full original coordinate with number is permanently preserved in Col 50 Notes / `cell_proof` (e.g., `Row: 7. Status, Col: 1`).
  - **Prohibition of Post-Hoc Normalization:** NEVER paraphrase, expand, translate, or "beautify" table variable names (e.g., never arbitrarily convert `"Ext. Comm."` to `"External Communication Behavior"`).
- **Methodology Specific Measure Substring Fidelity (Cols 32 & 39):**
  - The `Specific Measure Used` field for BSB (Col 32) and Non-BS Variables (Col 39) MUST be an exact, unmodified substring of the methodology quote (`source_quote`), capturing the precise validated instrument or scale author citation (e.g., `"Bettencourt et al. (2005)"`, `"Rizzo, House, and Lirtzman (1970)"`).
  - Never guess or construct synthetic instrument names when the author's exact phrasing is available in the text.

---

## 5. Hierarchical 3-Tier Header Protocol (Rule 20)
- **Canonical 3-Tier Structure (Rows 1–3):** ALL Excel coding sheets (batch sheets, paper extracts, master sheets) MUST strictly implement the canonical 3-tier hierarchical header structure:
  - **Row 1 (Section Category):** Section groupings (`Coder Initials`, `Sample ID`, `Effect size ID`, `Inclusion-Exclusion Judgment`, `Reason for Exclusion`, `Article Descriptors`, `Study/Sample Descriptors`, `Measure Descriptors`, `Effect Size`).
  - **Row 2 (Sub-category):** Operational sub-constructs (`Boundary spanning`, `Non-boundary-spanning variable`, `Correlation r`, `Notes`).
  - **Row 3 (Leaf Column Header):** Leaf column names (`Abstract`, `Title`, `Publication Name`, `Authors`, `Year`, ..., `Name`, `Mean`, `SD`, `Reliability (Alpha)`).
  - **Row 4+:** Data rows strictly begin at Row 4.
- **Strict Prohibition of Pandas Flat Header Exports:** NEVER use raw `pandas.DataFrame.to_excel()` to export or overwrite coding sheets. Doing so treats merged/empty cells in Row 1 as missing column labels, injecting corrupted `'Unnamed: X'` headers and destroying the 3-tier hierarchy.
- **Template Inheritance via OpenPyXL:** All new or updated extraction sheets MUST be initialized via `excel_template_util.py` or cloned from the canonical template `03_Coding_Sheets/49_53_66.xlsx`, copying merged cell ranges, fonts, fills, alignments, and column dimensions with openpyxl.

---

## 6. Effect Size Coordinates, Provenance & Verbatim Audit Protocol (Rule 9 / Col 50 Notes)
To ensure that any researcher can cross-verify effect sizes directly against the source PDF in under 3 seconds without manual page scanning, **Col 50 (Notes)** must strictly follow this unified provenance schema:
- **Mandatory Table & Page Coordinate Prefix:** Every extracted correlation MUST begin with its exact physical table number and manuscript/PDF page:  
  `Table X (p. Y), Row: <row_header_quote>, Col: <col_header_quote>, Raw: <raw_cell_value>`
- **Mandatory Verbatim Provenance for Methodological Flags (Rule 13 Integration):** When special methodological conditions occur, a pipe (`|`) delimiter MUST be appended followed by the explicit flag and the exact, character-for-character verbatim sentence or footnote from the paper proving the condition:
  - **Latent Variable Correlation:** When correlations are based on CFA/SEM latent constructs rather than raw observed scores:  
    `... | Latent correlation: [<Table/Page/Section>] "<exact verbatim sentence or footnote proving latent structure/AVE diagonal>"`
  - **Global Composite BSB Score:** When the measure combines multiple sub-dimensions into an overall composite score:  
    `... | Global composite: [<Section, p. Y>] "<exact verbatim sentence defining how the composite/mean rank was calculated>"`
  - **Sample Size / Pairwise N Discrepancy:** When matrix sample size differs from the text or is a pairwise range:  
    `... | Sample N footnote: [<Table Footnote>] "<exact verbatim footnote sentence detailing effective N>"`
  - **Partial / Imputed Correlation:** When correlations control for covariates or use imputed data:  
    `... | Partial correlation: [<Table Footnote>] "<exact verbatim footnote explaining controls>"`
- **Prohibition of Naked Labels:** Never enter naked flags (e.g., writing only `"Based on latent variables"` or `"Global composite score"`) without the corresponding table, page, and verbatim evidence quote.

---

## 7. Lossless Parity & Ingestion Safety Protocol (Rule 27)
- **Strict Prohibition of Ad-Hoc Glue Scripts (Universal Inserter Mandatory):** Agents are strictly forbidden from writing one-off, ad-hoc Python scripts in `scratch/` that construct Excel rows using raw hardcoded value lists (e.g., `[var_name, 999, 999...]`). All Excel row construction and database updates MUST be driven by verified, schema-bound inserters (such as `universal_excel_inserter.py`) where fields are dynamically bound by dictionary keys.
- **Lossless Ingestion Guarantee (Zero Data Drop):** If any subagent extraction output (JSON) contains a valid empirical statistic (Mean, SD, Sample Demographics, or Reliability), that value MUST be faithfully transcribed into the target Excel cell. Under no circumstances may a known extracted numeric value be silently dropped or defaulted to `999`.
- **Pre-Commit Lossless Parity Verification Gate:** Before committing any newly generated or modified Excel extraction sheet, the system MUST execute `verify_ingestion_parity.py` comparing the extraction JSON against the generated Excel sheet. If any valid metric extracted in the JSON is recorded as `999` in Excel, the verification MUST throw a critical assertion error, abort the commit, and quarantine the invalid payload.
- **Heuristic Linter Guard (100% Missing Heuristic):** For all included papers in batch coding sheets, the repository auditor (`linter.py`) checks whether all effect size rows for a given paper have 100% missing (`999`) values for IV Mean/SD and DV Mean/SD. Since over 95% of published correlation tables report Means and SDs, a 100% missing rate triggers an automatic heuristic audit warning to verify whether the source paper's correlation table reported those metrics.



