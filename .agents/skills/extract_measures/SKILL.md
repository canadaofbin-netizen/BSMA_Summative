---
name: extract_measures
description: Automates the extraction of Measure Descriptors from PDF papers using subagents.
---

# Skill: Extract Measures

When triggered, you must execute the following automated workflow to extract measurement details from an academic paper without suffering from context limits.

## 1. Subagent Invocation
- Use the `invoke_subagent` tool to spawn a specialized `research` subagent.
- **Prompt for Subagent:** "Read the provided PDF paper located at [Path]. Locate the 'Measures' section. For the following variables: [List of variables], extract the Number of Items, Anchor Range (Min/Max), Report Type (Self vs Others), and the original citation/source. Return this data EXACTLY as a JSON array of objects. **CRITICAL EXCEPTION:** If a variable is a demographic or objective control variable (e.g., Age, Gender, Tenure, Education, Firm Size), do not search for its scale properties. Immediately return `999` for its Number of Items, Min Score, and Max Score."

## 2. Await Response
- Wait asynchronously for the subagent to complete its task and return the JSON. Do not poll in a loop.

## 3. Data Injection
- Once the JSON is received, write a Python script (e.g., `inject_measures.py` in the scratch directory) that loads `BSMA_Master_Coding_Sheet.xlsx`.
- Match the variables in the JSON to the `Non-BS Variable Name` column in the Excel file.
- Populate the Measure Descriptor columns (Items, Min, Max, Source).
- Save the Excel file.

## 4. Verification and Backup
- Read back the modified Excel rows using Python to ensure no numeric hallucination occurred.
- Execute `git add .`, `git commit -m "Auto-extracted measures for [Paper]"`, and `git push` to synchronize with GitHub.
