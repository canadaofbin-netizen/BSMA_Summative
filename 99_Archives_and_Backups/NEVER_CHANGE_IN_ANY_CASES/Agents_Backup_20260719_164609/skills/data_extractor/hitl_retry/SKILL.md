---
name: hitl_retry
description: Human-in-the-Loop review queue for processing papers that failed data extraction.
---

# HITL Retry System (Human-in-the-Loop)

The `hitl_retry` skill is triggered when the user wants to review the backlog of papers that failed during the automated data extraction (marked as `FAILED_EXTRACTION`).

## 1. Review Phase
- Read `03_Archives_and_Backups/error_log.md` and identify all papers marked as `FAILED_EXTRACTION` or `[UNRECOGNIZED PARADIGM]`.
- Present a concise summary of the errors to the User (e.g., "Paper 102 failed because the table formatting is corrupted").
- Ask the User for explicit rulings or provide manual extraction data for those edge cases.

## 2. Retry Phase & Permanent Fails
- Apply the user's manual context/extraction data to the failed papers and invoke the `universal_excel_inserter.py` to save them.
- If successful, remove them from `error_log.md` and update their status to `SUCCESS` in `batch_queue.csv`.
- **PERMANENT FAIL:** If a paper simply cannot be processed even with HITL intervention (e.g., the PDF text is completely missing), mark it as `PERMANENT_FAIL` in `batch_queue.csv` and skip it forever. Do not let it loop.
