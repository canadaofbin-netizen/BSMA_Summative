---
name: lint_workspace
description: A skill that routinely audits the project workspace for hygiene, version fragmentation, and adherence to the Single Source of Truth (SSOT).
---
# Skill: Workspace Linter & Hygiene Auditor

The purpose of this skill is to monitor the BSMA project workspace to prevent technical debt, version fragmentation, and data contamination. When the user issues the `/lint` command or requests a routine audit, you MUST **use local system tools (CLI commands, Python, etc.) to scan the actual directory state** and conduct an audit according to the procedures below.

## 1. Code & Data Fragmentation Check (Version Fragmentation)
Scan pipeline scripts and data folders for the following anti-patterns:
- **Scripts:** Check for duplicated code files with suffixes like `_v2`, `_v3`, `_old`, or `_copy`.
- **Data Sheets:** Check Excel/CSV files for non-standard naming conventions such as `_final`, `_최종`, or `_수정됨` (Validation files must follow strict naming rules).
- **Action:** If found, recommend moving these files to the `99_Archives_and_Backups` folder (`mv`).

## 2. Hardcoded Path & Security Check
- **Absolute Paths:** Scan Python scripts to see if specific user local paths (e.g., `C:\Users\...`) or specific Excel filenames (e.g., `Validation2.xlsx`) are hardcoded as global variables. (If found, recommend refactoring using `argparse` or a `config.json` injection approach).
- **Security Check:** Ensure sensitive tokens like OpenAI API Keys are not exposed in the code. (Recommend using `.env` files).
- **Dependency Check:** Verify that dependency files like `requirements.txt` or `pyproject.toml` exist in the project root.

## 3. Zero Root Pollution Check (Directory Hygiene)
Inspect the workspace for contamination based on the specified folder structure rules:
- **Root Directory:** Check for unnecessary scratch files like temporary scripts (`.py`), dumped `.json`, or `.txt` files in the top-level path.
- **01_Academic_Papers:** Ensure there are no extensions other than `.pdf` (e.g., incomplete downloads like `.crdownload`, or hidden files).
- **scratch/:** Check if leftover `.json` remnants or old error logs (older than 1 week) have been left uncleared.
- **Action:** Rather than immediate deletion (`rm`), recommend safely moving them to `scratch/trash` or `99_Archives`.

## 4. Single Source of Truth (SSOT) Integrity Check
- Scan for duplicated rule documents. (e.g., verify if the legacy `03_Coding_Rulebook` folder or fragmented `.md` documents have re-emerged, despite `AGENTS.md` being the sole SSOT).
- **Action:** State clearly that this is a violation of the "Docs as Code" SSOT principle (Rule 8), and recommend merging duplicate content and deleting the old documents.

## 5. Strict Naming & ls-lint rules
- **Spaces & Special Characters:** Check if any file or folder names in the workspace contain spaces or special characters like parentheses. (If found, recommend replacing them with underscores `_`).
- **Paper Naming Convention (Rule 17 Compliance):** Use regular expressions to scan whether the `.pdf` files inside `01_Academic_Papers` strictly follow the mandated naming convention: `[ID] Author (Year) - Title.pdf`.
- **Extension Consistency:** Ensure data sheets are standardized as `.xlsx` and not fragmented into `.csv`, `.xls`, etc.

## 6. Project Scaffold & Security Check
- **Required Files:** Check if the root directory contains a `README.md` (project guide), `.gitignore`, and package dependency files (e.g., `requirements.txt`).
- **Environment Variable Template:** Ensure a structural `.env.example` file exists so that the actual `.env` file containing API keys is not directly exposed.

## 7. Data Immutability & Ghost Files Check
- **Original Folder Contamination (Immutability):** The `01_Academic_Papers` folder has a [Read-Only] principle. Scan if any derivative files (`.txt`, `.json`) generated during script execution have been saved inside this folder, contaminating the source data.
- **Ghost Files (0-Byte):** Scan for 0-Byte (empty) garbage files generated due to script execution errors, or empty directories left behind.

## 8. Lint Report & Action
Once the audit is complete, output the detailed results to an artifact (`workspace_lint_report.md`) following this format:
- Clearly classify the severity as **[Critical / Warning / Info]** and construct a markdown table.
- As the orchestrator, ask the user the following question and wait for feedback:
  **"Based on the issues above, would you like me to write a shell script (or Python cleanup code) to organize the workspace? Or should I automatically move them to a safe folder (99_Archives) right now (Auto-fix)?"**
