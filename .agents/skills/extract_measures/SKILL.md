---
name: extract_measures
description: Automates the extraction of Measure Descriptors from PDF papers using subagents.
---

# Skill: Extract Measures

When triggered, you must execute the following automated workflow to extract measurement details from an academic paper without suffering from context limits.

## 1. Subagent Invocation
- Use the `invoke_subagent` tool to spawn a specialized `research` subagent.
- **Prompt for Subagent:** "Read the provided PDF paper located at [Path].
  - First, identify the Boundary Spanning construct and all paired variables by reading the Correlation Matrix. Extract `r`, `Mean`, `SD`, and `Alpha` for all variables.
  - Locate the 'Measures' section. Extract Items, Min/Max, Report Type, and the **exact descriptive sentence** used for the citation/source.
  - Return this data EXACTLY using the following nested M:N JSON schema:
  `{ "article_id": "...", "inclusion_status": 1, "samples": [ { "sample_number": 1, "sample_size": 123, "publication_type": 1, "study_design": 1, "international_context": 1, "occupation_type": "...", "bs_measures": [ { "name": "...", "items": 5, "alpha": 0.88, "mean": 4.1, "sd": 0.8, "min": 1, "max": 7, "report_type": 1, "specific_measure": "...", "notes": "Reverse-coded" } ], "correlations": [ { "non_bs_name": "...", "r": 0.26, "alpha": 0.90, "mean": 3.2, "sd": 1.1, "items": 9, "min": 1, "max": 7, "report_type": 1, "specific_measure": "...", "notes": "" } ] } ] }`
  - **CRITICAL EXCEPTION:** If a variable is a demographic, dummy, or proxy (e.g., Age, Gender, Tenure, Firm Size), **DO NOT SEARCH** the text for its properties. **IMMEDIATELY** return `999` for Items, Min, Max, and Alpha. Put the unit (e.g., "Months", "Years") in the `"notes"` field.
  - **REVERSAL FLAG:** If the text explicitly states a scale was reverse-coded or reverse-scored, write `"Reverse-coded"` in the `"notes"` field for that measure."

## 2. Await Response
- Wait asynchronously for the subagent to complete its task and return the JSON. Do not poll in a loop.

## 3. Data Injection
- Once the JSON is received, you MUST NOT write a custom python script.
- Instead, format the JSON to match the Master Coding Sheet column indices and invoke `python .agents/scripts/universal_excel_inserter.py --excel BSMA_Master_Coding_Sheet.xlsx --data <JSON_STRING>`.
- The universal inserter will automatically handle Coder Initials, Sample ID, Effect Size ID auto-generation, and exact string mappings for dropdown columns.

## 4. Verification and Backup
- Read back the modified Excel rows using Python to ensure no numeric hallucination occurred.
- Execute `git add .`, `git commit -m "Auto-extracted measures for [Paper]"`, and `git push` to synchronize with GitHub.
