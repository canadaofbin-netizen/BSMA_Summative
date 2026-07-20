<details>
<summary><h2>Rules for Updating the Rulebook</h2></summary>

> [!IMPORTANT]  
> **Confirmation Required**  
> Any AI or coding assistant attempting to update or modify any file in the `04_Coding_Rulebook` directory MUST draft the proposed changes and ask for explicit confirmation from the user before applying any modifications. Do not update any rule documents without prior user approval.

> [!IMPORTANT]  
> **Modular Archiving & Versioning**  
> Now that the rules are modular, backups must be done on a per-file basis:
> 1. Before modifying any specific rule file (e.g., `01_dyadic_data_rules.md`), you MUST copy the current, unedited version into the `03_Archives_and_Backups` folder.
> 2. **After** the update is complete, you MUST immediately copy the newly updated file into the backups folder, incrementing its specific version number (e.g., `01_dyadic_data_rules_v2.md`).
> 3. If a completely new rule module is added (e.g., `06_new_rule.md`), you must also backup the `read.md` index file, because the index will need to be updated to link to the new module.

</details>

## Section F: Academic Papers Directory Guardrail

**01_Academic_Papers Directory Protection:** The `01_Academic_Papers` directory is strictly reserved for PDF files that follow the exact naming convention `[ID] Author (Year) - Title.pdf` (e.g., `[2] Aaronson et al. (2020) - The Long-Run Effects of the 1930s.pdf`). All agents are STRICTLY FORBIDDEN from creating, moving, or writing scratch files, text logs, Python scripts, JSON outputs, or any other non-conforming files into this directory. Any temporary files or analysis outputs must be saved to the `scratch/` directory or appropriate log folders. If a non-compliant file is discovered in `01_Academic_Papers`, it should be flagged as unnecessary and removed.

## Section G: Temp File Containment

**Scratch Directory Containment Rule (Zero Root Pollution):** ALL agents, subagents, and pipeline scripts are **STRICTLY FORBIDDEN** from creating temporary files (`.txt`, `.json`, `.py`, `.csv`, or any other scratch/debug artifacts) in the project root directory or inside any numbered project directory (`01_Academic_Papers/`, `02_*/`, `03_*/`, `04_*/`). ALL temporary outputs — including but not limited to PDF text extractions, batch payloads, chunk JSONs, OCR outputs, debug scripts, and experiment logs — MUST be written exclusively to the `scratch/` directory.
- **Automatic Cleanup:** After each pipeline batch completes (e.g., after `swarm_inject.py` finishes injecting data), the Orchestrator MUST delete all consumed temporary files from `scratch/` before proceeding to the next batch.
- **Git Exclusion:** The `scratch/` directory is listed in `.gitignore` and MUST NOT be committed to the Git repository.
- **Permitted Root Files:** Only the following file types are permitted in the project root: `.xlsx` (data sheets), `.md` (documentation), `.csv` (batch queue), `.gitignore`, and `desktop.ini`. Everything else MUST go into `scratch/` or the appropriate project subdirectory.

## Section H: Excel Template Integrity

**Validation Sheet Structure Guardrail (Screening vs. Extraction):** `BSMA_Master_Coding_Sheet.xlsx` is the ultimate master template and contains the "Full Text Data Extraction" structure (50 columns, including Study/Sample Descriptors and Measure Descriptors). However, AI Validation files (e.g., `BSMA_AI_Run_Validation[1-3].xlsx`) are designated strictly as **Include/Exclude screening templates**. When syncing or generating Validation sheets from the Master, the AI MUST strip all data extraction columns (Columns Q through AX) and retain only Columns A through P (ID, Judgments, Reasons, Abstract, Title, Notes) to maintain a clean screening format.
