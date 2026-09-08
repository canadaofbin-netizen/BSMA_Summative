---
name: batch_processor
description: Master orchestrator loop for automating the pure data extraction of included academic papers.
---

# Batch Processor Loop (Data Extraction Engine)

When the user asks you to "run the batch processor" or "extract data from papers", you must act as the Master Orchestrator and follow this precise Loop logic:

## 1. Queue Self-Healing & Retrieval (Stateful Poison Pill Defense)
- **Self-Healing:** Before starting, read `batch_queue.csv` (or `scratch/batch_queue.csv`). If any papers are stuck in `PROCESSING` status, increment their `ROLLBACK_COUNT` column by 1 and auto-rollback their status to `PENDING`. 
- **Max 2 Rollbacks (Poison Pill):** If a paper's `ROLLBACK_COUNT` exceeds 2, DO NOT rollback to `PENDING`. Immediately mark it as `PERMANENT_FAIL` to prevent an infinite crash loop.
- Identify the next `PENDING` paper(s) to process where the initial screening status is `1 = Include`.
- Change their status to `PROCESSING` in the CSV immediately.

## 2. Two-Tier Verification & Multi-Agent Extraction (Per Paper)
For each paper in the batch, execute the Two-Tier verification workflow:
- **Tier 1 (Node 0: Pre-Extraction Screening Gate):**
  - Re-evaluate the paper against the multi-tier screening hierarchy in `include_exclude_pipeline/references/screening_rules_core.md`.
  - If Verdict is `0 = exclude` (Construct Homonymy, Level of Analysis Aggregation, Work-Life boundaries):
    - **Fast-fail immediately.** Do NOT spawn Specialists B or C (preventing token waste, cognitive overload, and forced miscoding).
    - Update Excel coding sheet: Col 1 = Coder Initials, Col 2 = Article ID, Col 5 = `'0 = exclude'`, Col 6 = Reason for Exclusion (`3 = Non-individual level (team/firm/org analysis)` for aggregated data; `1 = No effect size of interest` for construct homonymy).
    - Terminate immediately after Col 6: Leave Cols 7–50 completely blank (`None`) per Rule 19 (1 single row). Halt extraction to prevent token waste and ecological fallacy.
    - Mark status in `batch_queue.csv` as `EXCLUDED` and proceed to the next paper.
  - If Verdict is `1 = include` (Individual-Level Empirical BSB):
    - Proceed to Tier 2 extraction below.
- **Tier 2 (3-Specialist Swarm & Deterministic Integration):**
  - Run `python .agents/scripts/find_pdf.py --id [Article_ID]` to automatically locate the `.pdf` file.
  - Deploy the 3-Specialist Subagent Swarm via `invoke_subagent` in parallel:
    - **Specialist A (`study_sample_descriptor`):** Focuses exclusively on Abstract, Methodology Sample, and Table Footnotes to extract Study Design (cross-sectional vs longitudinal), Country, Sample size ($N$), Demographics (Age, Gender, Tenure, Occupation), and Footnote bias flags (Cols 17–26).
    - **Specialist B (`boundary_spanning_matrix`):** Focuses exclusively on the Correlation Matrix table to perform CoT matrix reasoning, extract verbatim table axis variable labels (Rule 14), Means, SDs, reliabilities, and correlations with verbatim `cell_proof` (Cols 41–50).
    - **Specialist C (`measure_descriptor`):** Focuses exclusively on Methodology Measures text to classify BSB vs Non-BS constructs, extract item counts, Likert anchors, specific measure citations (Rule 14), verbatim quotes (Rule 13), and anchor reconciliation (Cols 27–40).
  - **Deterministic Integration Engine:** Orchestrator awaits all 3 specialists and performs a deterministic Python Cartesian join (BSB $\times$ Non-BS) mapped to matrix cells, assembling the complete 50-column dataset with Dual Missing Data Protocol coercion (`999` for numeric, `None` / blank for text).

## 3. Fast-Fail Pre-Check (CRITICAL)
- **Fast-Fail (Fatal Errors):** Before validation, check the merged string for fatal codes: `[DATA_NOT_FOUND]`, `[UNPARSEABLE_PDF]`, `[LoA_VIOLATION]`, `[CONSTRUCT_HOMONYMY_VIOLATION]`, `[PARTIAL_CORRELATION_POISONING]`, or `[AMBIGUOUS_MATRIX_DIAGONAL]`. 
- If ANY of these codes exist, DO NOT pass to Validator. Abort extraction immediately. Mark as `PERMANENT_FAIL` in `batch_queue.csv` and append the reason to `04_Reports/error_report.md`.

## 4. Extraction Validation Chaining
- Cross-check the Merged JSON payload and the original Correlation Table against the strict fidelity and reliability rules in `extract_measures/SKILL.md`.
- If verification returns `PASS`, proceed to step 5.
- If verification returns `REJECT_RETRY`, retry up to 3 times. 
- If verification returns `FATAL_REJECT`, treat it as a Fast-Fail (Abort immediately, mark as `PERMANENT_FAIL`).

## 5. 4-Sheet Excel Routing & Atomic Sync
- **Canonical 3-Tier Header Enforcement (Rule 20):** When generating new coding sheets or batch files (e.g., `[start]_[end].xlsx`), NEVER use pandas flat export (`df.to_excel()`). Always initialize the sheet via `excel_template_util.py` to inherit the exact 3-tier header structure and styles from `03_Coding_Sheets/49_53_66.xlsx`, starting data strictly on Row 4.
- **Excel Injection (Safe CLI Args):** ONLY if validation passed, save the merged JSON payload to a temporary file (e.g., `temp_payload.json`). Invoke `python .agents/scripts/universal_excel_inserter.py --excel 03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx --data-file temp_payload.json`. The script will handle routing to Raw, Transformed, Imputed, or Salami sheets.
- **Atomic Sync:** The moment a paper succeeds or fails, immediately update its status and `ROLLBACK_COUNT` in `batch_queue.csv` and execute `git add .`, `git commit -m "Auto-extracted measures for [Paper ID]"`, and `git push` to save progress atomically.

## 6. Reporting
- Present a summary of the batch run to the user. Provide a link to the `error_log.md` if any failed.
