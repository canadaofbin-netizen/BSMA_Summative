# Extraction Errors & Lessons Learned Report

> [!IMPORTANT]  
> **Purpose of this Document**  
> This is a living document designed to record all incorrect analyses, flawed data extractions, and procedural mistakes made during the Boundary Spanning Meta-Analysis project. By documenting *what* went wrong and *why*, the AI system will continuously learn and prevent these errors from occurring in the future.

---

<details>
<summary><h2>1. Column Alignment Failure (Excel Write Error)</h2></summary>

* **Incident:** When initially extracting data for Comacchio (2011) and Liu (2024), the extracted effect sizes were placed into the wrong columns in `BSMA_Actual Coding Sheet_v2.xlsx`, creating massive blank gaps.
* **Why it happened:** I used a Python script that attempted to find the correct columns by searching for keyword headers (e.g., searching for "Total Sample Size"). However, because the Excel sheet uses a complex multi-row merged header format (Row 1 has categories, Row 3 has sub-categories), the script failed to match the keywords and defaulted to incorrect columns.
* **Prevention:** Never rely on fuzzy keyword matching for Excel headers. Always manually map and hardcode the exact column indices (e.g., `Column 21 = Sample Size`, `Column 48 = Correlation r`) before writing data to the spreadsheet.
</details>

<details>
<summary><h2>2. Incomplete Extraction (Missing Descriptors)</h2></summary>

* **Incident:** I successfully extracted the correlation effect sizes ($r$) for Comacchio and Liu but completely neglected to extract the **Study/Sample Descriptors** (N, Age, Gender, Tenure, Study Design, Country) and the **Measure Descriptors** (Means, SD, Alphas, Number of Items).
* **Why it happened:** I experienced "tunnel vision", focusing entirely on the correlation matrices (Table 1 and Table 3) without systematically reviewing the full column requirements of the Excel sheet. I declared the task finished without verifying the work against the master column list.
* **Prevention:** Always write a Python validation script (`pandas`) to check for empty cells in required columns *before* declaring an extraction complete. Treat the extraction as a holistic process rather than just a matrix-copying task.
</details>
<details>
<summary><h2>3. Missing Demographic Correlations</h2></summary>

* **Incident:** For Liu (2024), I failed to extract the correlations between the Expatriate (Anchor) demographic variables (Age, Gender, Tenure, Language Proficiency) and the Boundary Spanning variables.
* **Why it happened:** I mistakenly assumed demographic variables were purely descriptive controls and skipped them. This violated the explicit rule in `read.md` that dictates we must "code ALL effect sizes including demographic variables", while only excluding *cross-entity* demographics.
* **Prevention:** Rigorously read the entire correlation matrix, including the demographic blocks. Strictly apply the Anchor rule to include the focal sample's demographics and exclude the non-focal sample's demographics.
</details>
<details>
<summary><h2>4. Premature Edge Case Analysis (Scope Error)</h2></summary>

* **Incident:** During the automated heuristic edge-case scan, I initially presented a report summarizing the findings for only 21 papers, despite the folder containing 625 papers.
* **Why it happened:** I had an internal assumption (a "hallucination") that the folder only contained 21 papers based on an earlier glance. I wrote the report while the background Python scanner was still actively parsing the remaining hundreds of PDFs, rather than waiting for the task to fully complete.
* **Prevention:** Do not hardcode assumptions about file counts. Always ensure background tasks (like text extraction or directory scanning) have explicitly returned a `Completed` status before aggregating and presenting their data.
</details>
---

> [!TIP]
> **Future Tracking**
> Any future mistakes, hallucinations, or failed extractions will be immediately documented in this file, along with a root-cause analysis.
