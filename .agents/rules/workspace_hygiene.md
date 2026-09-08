# Rule: Workspace & Directory Hygiene

This document defines the strict workspace hygiene, directory isolation, and file naming standards for the BSMA project.

---

## 1. 01_Academic_Papers Directory Protection (Rule 17)
- **Strict PDF Reservation:** The `01_Academic_Papers` directory is strictly reserved for PDF files that follow the exact canonical naming convention:
  `[ID] Author (Year) - Title.pdf`  
  *(Example: `[2] Aaronson et al. (2020) - The Long-Run Effects of the 1930s.pdf`)*
- **Prohibited File Types:** All agents, subagents, and scripts are **STRICTLY FORBIDDEN** from creating, moving, or writing scratch files, text logs, Python scripts, JSON outputs, or any non-conforming files into this directory.
- **Subdirectory Prohibition:** No subdirectories (e.g., `scratch/`, `outputs/`) may exist inside `01_Academic_Papers/`.
- **Immediate Remediation:** If any non-compliant file or rogue subdirectory is detected, it must be flagged and removed immediately.

---

## 2. Scratch Containment & Zero Root Pollution (Rule 18)
- **Zero Root Pollution:** The project root directory must remain strictly clean. Only the following files are permitted in the project root:
  - `.gitignore`
  - `desktop.ini`
  - `README.md`
  All coding spreadsheets must reside in `03_Coding_Sheets/`. All reports must reside in `04_Reports/`.
- **Scratch Directory Isolation:** All agents, subagents, and pipeline scripts are **STRICTLY FORBIDDEN** from creating temporary files (`.txt`, `.json`, `.py`, `.csv`, or any scratch/debug artifacts) in the root directory or inside any numbered project directory (`01_*/`, `02_*/`, `03_*/`, `04_*/`).
- **Exclusive Temporary Destination:** ALL temporary outputs MUST be written exclusively to the `scratch/` directory.
- **Automatic Post-Batch Cleanup:** After each pipeline batch completes (e.g., after `swarm_inject.py` finishes injecting data), the Orchestrator MUST delete all consumed temporary files from `scratch/` before proceeding to the next batch. Only persistent configuration files actively in use may be retained during a running batch.
- **Git Exclusion:** The `scratch/` directory is listed in `.gitignore` and MUST NOT be committed to the Git repository.
