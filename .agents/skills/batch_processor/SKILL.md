---
name: batch_processor
description: Master orchestrator loop for automating the extraction of academic papers.
---

# Batch Processor Loop (Loop Engineering)

When the user asks you to "run the batch processor" or "process the next N papers", you must act as the Master Orchestrator and follow this precise Loop logic:

## 1. Queue Retrieval
- Read `04_Archives_and_Backups/batch_queue.csv` using a Python script.
- Identify the next `PENDING` paper(s) to process.
- Change their status to `PROCESSING` in the CSV.

## 2. Delegation (Per Paper)
For each paper in the batch, you must:
- Read the PDF text.
- Follow the Three-Step Workflow in `03_automated_workflow.md` (Step 0 Triage, Step 1 Shadow Report, Step 2 Excel Injection).
- **Step 0.5 (CRITICAL) - Variable Identification:** Before extracting measures, you MUST spawn a subagent to read the "Means, Standard Deviations, and Correlations" table. It must identify the Boundary Spanning construct, the sample size (N), and all paired variables, and extract their `r` values, Means, SDs, and Cronbach's Alphas.
- **CRITICAL - ZERO-ORDER LOCK:** You MUST explicitly command the subagents to ONLY extract Pearson correlations (`r`). They are absolutely forbidden from pulling path coefficients (betas) from structural equation models (SEM) or regression tables.
- **CRITICAL - MANDATORY CATEGORICALS:** You MUST explicitly tell subagents to extract Publication Type, Study Design, International Context, and Occupation Type.
- **CRITICAL - EXACT MEASURE TEXT:** You MUST instruct subagents to extract the *exact descriptive sentence* for specific measures, not just the citation.
- **CRITICAL - EXCEL INJECTION:** When injecting data into the Master Excel Sheet, you MUST invoke `python .agents/scripts/universal_excel_inserter.py --excel BSMA_Master_Coding_Sheet.xlsx --data <JSON_SCHEMA_STRING>`. Do not write custom inserters.

## 3. Fault Tolerance
- If you or a subagent encounters an edge case that violates rules, or a fundamentally unparseable correlation table (`[UNRECOGNIZED PARADIGM]`), **DO NOT STOP THE BATCH**.
- Mark the paper as `FAILED` or `EXCLUDED` in `batch_queue.csv`.
- Append a detailed error entry to `04_Archives_and_Backups/error_log.md`.
- Immediately proceed to the next paper in the loop.

## 4. State Persistence (Auto-Save)
- After completing the requested batch, update `batch_queue.csv` with final statuses (`SUCCESS`, `FAILED`, `EXCLUDED`).
- Run `git add .`, `git commit -m "Batch processor: completed N papers"`, and `git push` to save progress.

## 5. Reporting
- Present a summary of the batch run to the user (e.g. "Processed 5 papers: 3 Success, 1 Excluded, 1 Failed").
- Provide a link to the `error_log.md` if any failed.
