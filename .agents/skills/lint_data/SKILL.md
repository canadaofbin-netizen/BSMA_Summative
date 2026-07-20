---
name: lint_data
description: A Data Integrity Linter using Pandera to validate Excel datasets against the Zero Guesswork Policy (Rule 1) and Structural Guardrails (Rule 19).
---
# Skill: Data Linter (Pandera Integrity Shield)

The purpose of this skill is to programmatically enforce data integrity within the project's Excel sheets (`BSMA_Master_Coding_Sheet.xlsx`, `Validation*.xlsx`). When the user issues the `/lint_data` command, you MUST execute the pre-written Pandera script to scan the target dataframe.

## 1. Execution Workflow
1. Execute the python script: `python .agents/scripts/lint_data.py --excel "<Target Excel Path>"`
2. If the user does not specify an excel file, default to `BSMA_Master_Coding_Sheet.xlsx`.
3. If the script outputs `[PASS]`, report success to the user.
4. If the script outputs `[CRITICAL]` or `[ERROR]`, read the stdout which contains the specific rows and columns that failed the schema check (e.g. blanks or NaNs found).

## 2. Interactive Auto-Fix (Option B)
Unlike a hard fail in CI/CD, as an AI Orchestrator you must help the user fix the errors:
- **Interpret the Log:** Summarize the `pandera` error log for the user. (e.g., "Row 35 has a blank Verdict. Row 40 is missing an ID.")
- **Propose a Fix:** Ask the user if you should automatically write a python script (using `pandas` or `openpyxl`) to inject `999` for missing numeric values or `"Not Reported"` for missing string values to resolve the Rule 1 violation.
- **Wait for Permission:** Do not modify the Excel file without explicit user confirmation.

## 3. Security & Isolation
The `lint_data.py` script is purely Read-Only. It will never overwrite data itself. All fixes must be proposed as a separate action.
