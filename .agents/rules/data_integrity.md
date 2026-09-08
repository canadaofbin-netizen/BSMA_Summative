# Rule: Excel Coding Sheet Data Integrity

This document defines the strict data type policies, template schemas, and evidence standards for all BSMA coding sheets.

---

## 1. Universal Zero Guesswork & Clean Blank Cell Protocol (Rule 1)
- **Absolute Prohibition on Imputation (Zero Guesswork):** Never guess, fabricate, or impute data. Do NOT calculate averages or deduce missing values under any circumstances.
- **Clean Blank Cell Protocol for Human Readability:**
  - In Excel coding sheets, cells that are not applicable, conditional, or not reported in the paper MUST be left as clean BLANK cells (`None`), matching the canonical format of `03_Coding_Sheets/49_53_66.xlsx` and `Full text coding sheet.xlsx`.
  - **Conditional / Non-Applicable Columns:**
    - `Col 6 (Reason for Exclusion)`: When a paper is `1 = include`, leave blank (`None`).
    - `Cols 13, 18, 20, 31, 38 ("Other / Specify / Notes")`: When standard categories apply and no additional notes are needed, leave blank (`None`).
    - `Col 16 (Notes)`: When a paper is `1 = include` and has no special screening notes, leave blank (`None`).
  - **Unreported Metrics / Descriptive Stats:**
    - If demographics (Age, % Female, Tenure) or table statistics (Mean, SD, Alpha) are not reported in the paper/table, leave them as clean blank cells (`None`) rather than cluttering with dummy `999` or `"Not Reported"` strings.
  - **Excluded Papers (Code 0):**
    - For excluded papers, record bibliographic metadata, exclusion judgment/reason, and verbatim evidence in Cols 1–16. Leave measurement and effect size columns (Cols 17–50 or Cols 27–50) as clean BLANK cells (`None`), mirroring Paper #66 in `49_53_66.xlsx`.

---

## 2. Template Structure & Format Compliance (Rules 3, 6, 19)
- **Universal Master Insertion (Rule 6):** ALL successfully processed papers MUST be injected into `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx`. Every paper must retain its assigned BSMA ID.
- **50-Column Full Extraction Schema (Rule 19):** `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx` is the ultimate master template and contains the 50-column "Full Text Data Extraction" structure (Columns A through AX, covering Study/Sample Descriptors and Measure Descriptors).
- **Screening vs Extraction Separation (Rule 19):** `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx` contains the full 50-column extraction schema (Col A through AX). Dedicated screening views or test sheets retain only Columns A through P (ID, Judgments, Reasons, Abstract, Title, Notes) to separate high-level screening from full-text data extraction.
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

