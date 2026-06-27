---
name: hitl_retry
description: Human-in-the-Loop review queue for processing failed papers.
---

# HITL Retry System (Human-in-the-Loop)

The `hitl_retry` skill is triggered when the user wants to review the backlog of papers that failed during the automated batch processing.

## 1. Review Phase
- Read `04_Archives_and_Backups/error_log.md` and identify all papers marked as failed or `[UNRECOGNIZED PARADIGM]`.
- Present a concise summary of the errors to the User.
- Ask the User for explicit rulings on how to handle each edge case (e.g., "For Paper X, should we exclude it, or is the anchor actually the Supervisor?").

## 2. Retry Phase
- Once the User provides a ruling, apply that specific context to the failed papers.
- Rerun the extraction pipeline (Steps 0 to 3) for those specific papers using the newly provided context.
- If successful, remove them from `error_log.md` and update their status to `SUCCESS` in `batch_queue.csv`.
- If a rule change is permanent, remember to update the corresponding Markdown rulebooks (e.g., `04_general_exceptions.md` or `01_dyadic_data_rules.md`).
