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
- **CRITICAL - MANDATORY CATEGORICALS:** When passing instructions to subagents, you MUST explicitly tell them to extract Publication Type (Col 12), Study Design (Col 17), International Context (Col 21), and Occupation Type (Col 26) alongside the psychometric variables.
- **CRITICAL - EXACT MEASURE TEXT:** You MUST explicitly instruct the subagents to extract the *exact descriptive sentence* from the paper for the 'Specific Measure Used' column, rather than just the author/year citation.
- **CRITICAL - SUBAGENT USE:** Use subagents (`invoke_subagent` with the `extract_measures` skill) to handle detailed extraction of measure descriptors to keep your context window clean.
- **CRITICAL - EXCEL INJECTION:** When injecting data into the Master Excel Sheet, you MUST NOT write custom `ws.append()` Python scripts. You must invoke `python .agents/scripts/universal_excel_inserter.py --excel BSMA_Master_Coding_Sheet.xlsx --data <JSON_STRING>`. This script automatically handles ID generation (KY, BSMA000X.Y.Z) and exact dropdown text mapping for you.

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
