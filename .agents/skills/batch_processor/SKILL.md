---
name: batch_processor
description: Master orchestrator loop for automating the pure data extraction of included academic papers.
---

# Batch Processor Loop (Data Extraction Engine)

When the user asks you to "run the batch processor" or "extract data from papers", you must act as the Master Orchestrator and follow this precise Loop logic:

## 1. Batch Identification & Target Sheet Setup
- Identify the target paper IDs requested by the user or next in sequence where the Phase 1 screening status in `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx` is `1 = Include`.
- Initialize or load the dedicated batch extraction coding sheet `03_Coding_Sheets/[start]_[end].xlsx` using `.agents/scripts/excel_template_util.py` (inheriting the canonical 3-tier header and worksheet `"Extracted Data"` from `03_Coding_Sheets/49_53_66.xlsx`).
- **Stateful Retry Limit (Poison Pill Defense):** If a paper encounters repeated validation or subagent extraction failures across more than 2 retry attempts, halt retries for that paper and quarantine its temporary payload in `scratch/quarantine/` for manual inspection before deleting temporary files.

## 2. Two-Tier Verification & Multi-Agent Extraction (Per Paper)
For each paper in the batch, execute the Two-Tier verification workflow:
- **Tier 1 (Node 0: Pre-Extraction Screening Gate):**
  - Re-evaluate the paper against the multi-tier screening hierarchy in `include_exclude_pipeline/references/screening_rules_core.md`.
  - If Verdict is `0 = exclude` (Construct Homonymy, Level of Analysis Aggregation, Work-Life boundaries):
    - **Fast-fail immediately.** Do NOT spawn Specialists B or C (preventing token waste, cognitive overload, and forced miscoding).
    - Update the batch Excel coding sheet (`03_Coding_Sheets/[start]_[end].xlsx`): Col 1 = Coder Initials, Col 2 = Article ID, Col 5 = `'0 = exclude'`, Col 6 = Reason for Exclusion (`3 = Non-individual level (team/firm/org analysis)` for aggregated data; `1 = No effect size of interest` for construct homonymy).
    - Terminate immediately after Col 6: Leave Cols 7–50 completely blank (`None`) per Rule 19 (1 single row). Also synchronize `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx` Col 5/6/16 if the Phase 1 verdict was overturned during full-text inspection.
  - If Verdict is `1 = include` (Individual-Level Empirical BSB):
    - Proceed to Tier 2 extraction below.
- **Tier 2 (3-Specialist Swarm & Deterministic Integration):**
  - Run `python .agents/scripts/find_pdf.py --id [Article_ID]` to automatically locate the `.pdf` file in `01_Academic_Papers/`.
  - Deploy the 3-Specialist Subagent Swarm via `invoke_subagent` in parallel:
    - **Specialist A (`study_sample_descriptor`):** Focuses exclusively on Abstract, Methodology Sample, and Table Footnotes to extract Study Design (cross-sectional vs longitudinal), Country, Sample size ($N$), Demographics (Age, Gender, Tenure, Occupation), and Footnote bias flags (Cols 17–26).
    - **Specialist B (`boundary_spanning_matrix`):** Focuses exclusively on the Correlation Matrix table to perform CoT matrix reasoning, extract verbatim table axis variable labels (Rule 14), Means, SDs, reliabilities, and correlations with verbatim `cell_proof` (Cols 41–50).
    - **Specialist C (`measure_descriptor`):** Focuses exclusively on Methodology Measures text to classify BSB vs Non-BS constructs, extract item counts, Likert anchors, specific measure citations (Rule 14), verbatim quotes (Rule 13), and anchor reconciliation (Cols 27–40).
  - **Deterministic Integration Engine:** Orchestrator awaits all 3 specialists and performs a deterministic Python Cartesian join (BSB $\times$ Non-BS) mapped to matrix cells, assembling the complete 50-column dataset with Dual Missing Data Protocol coercion (`999` for numeric, `None` / blank for text).

## 3. Fast-Fail Pre-Check (CRITICAL)
- **Fast-Fail (Fatal Errors):** Before validation, check the merged string for fatal codes: `[DATA_NOT_FOUND]`, `[UNPARSEABLE_PDF]`, `[LoA_VIOLATION]`, `[CONSTRUCT_HOMONYMY_VIOLATION]`, `[NO_BSB_CONSTRUCT_VIOLATION]`, `[PARTIAL_CORRELATION_POISONING]`, or `[AMBIGUOUS_MATRIX_DIAGONAL]`. 
- If ANY of these codes exist, DO NOT proceed with effect-size matrix insertion. On `[LoA_VIOLATION]`, `[CONSTRUCT_HOMONYMY_VIOLATION]`, or `[NO_BSB_CONSTRUCT_VIOLATION]`, record the single excluded row (`0 = exclude`) in the batch sheet per Rule 19 and synchronize the verdict in `BSMA_Master_Coding_Sheet.xlsx`.

## 4. Extraction Validation Chaining
- Cross-check the Merged JSON payload and the original Correlation Table against the strict fidelity and reliability rules in `extract_measures/SKILL.md`.
- If verification returns `PASS`, proceed to Step 5.
- If verification returns `REJECT_RETRY`, retry up to 2 times.
- If verification returns `FATAL_REJECT`, treat it as a Fast-Fail and abort insertion.

## 5. Batch Coding Sheet Injection, Parity Verification & Atomic Sync
- **Canonical 3-Tier Header Enforcement (Rule 20):** When generating new coding sheets or batch files (e.g., `03_Coding_Sheets/[start]_[end].xlsx`), NEVER use pandas flat export (`df.to_excel()`). Always initialize the sheet via `.agents/scripts/excel_template_util.py` to inherit the exact 3-tier header structure and styles from `03_Coding_Sheets/49_53_66.xlsx`, starting data strictly on Row 4 of worksheet `"Extracted Data"`.
- **Excel Injection (Safe CLI Args):** ONLY if validation passed, save the merged JSON payload to a temporary file in `scratch/` (e.g., `scratch/temp_payload.json`). Invoke `python .agents/scripts/universal_excel_inserter.py --excel 03_Coding_Sheets/[start]_[end].xlsx --data-file scratch/temp_payload.json`. Handcrafting ad-hoc scratch scripts with hardcoded value lists is strictly forbidden (Rule 27).
- **Lossless Ingestion Parity Gate (Rule 27):** Immediately following injection, execute `python .agents/scripts/verify_ingestion_parity.py --excel 03_Coding_Sheets/[start]_[end].xlsx --json scratch/temp_payload.json --paper-id [Article_ID]`. If any valid empirical statistic in JSON was dropped or converted to `999` in Excel, the script aborts with code 1, immediately halting git commit and reverting changes.
- **Scratch Cleanup & Atomic Sync:** Delete temporary payload files from `scratch/` so `scratch/` remains 100% empty, run `python .agents/scripts/linter.py` to confirm 0 errors/warnings, and execute `git add`, `git commit -m "Auto-extracted measures for [Batch IDs]"`, and `git push` to save progress atomically.

## 6. Reporting & Meeting-Ready Summary Artifact (Rule 31)
- Upon completing batch extraction and verification, generate a **Meeting-Ready Summary Artifact** strictly adhering to **Rule 31 (`Meeting-Ready Summary Artifact Formatting Protocol`)** in `.agents/rules/data_integrity.md` and `.agents/skills/batch_summary/SKILL.md` (zero graphs/diagrams, executive summary table, full original correlation/descriptive tables for included papers, original proof tables for excluded papers, extracted effect size tables, verbatim quotes with zero ellipses, and clickable Excel coding sheet links).
- Run `python .agents/scripts/batch_summary.py 03_Coding_Sheets/[start]_[end].xlsx` to verify construct taxonomy and compliance metrics.

