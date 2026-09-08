---
name: lint
description: Unified workspace hygiene, academic papers registry, Excel coding sheet integrity, and agent protocol auditor.
trigger: "/lint"
---

# Unified Project Linter (lint)

The `/lint` skill is the single source of truth for repository health and data integrity across the BSMA project.

## 1. Execution Workflow

When the user types `/lint` or asks for a workspace/data check:
1. Run the Python audit engine:
   ```bash
   python .agents/scripts/linter.py
   ```
2. If temporary caches need cleaning, run:
   ```bash
   python .agents/scripts/linter.py --fix
   ```

## 2. Four Core Audit Pillars

1. **Workspace Hygiene (Rule 18):**
   - Zero root pollution: Only `.gitignore`, `desktop.ini`, and `README.md` permitted in root.
   - All Excel sheets strictly contained within `03_Coding_Sheets/`.
   - Ghost/lock files (`~$*.xlsx`, `.DS_Store`, `Thumbs.db`) detected.
   - Python bytecode/cache (`__pycache__`, `.pyc`) isolation.
   - `scratch/` containment: All temporary processing files kept inside `scratch/`.

2. **Academic Papers Registry (Rule 17):**
   - All 701 PDFs strictly match format: `[ID] Author (Year) - Title.pdf`.
   - Zero non-PDF files and zero subdirectories inside `01_Academic_Papers/`.
   - Continuous ID sequence audit (1..701) for duplicates and omissions.

3. **Excel Data Integrity (Rules 1, 3, 13, 19):**
   - 50-column extraction schema strictly enforced on `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx`.
   - Zero bold markdown (`**`) in header cells.
   - Dual Missing Data Protocol (Rule 1): Missing numbers = `999`, non-applicable text = blank (`None`). `"Not Reported"` is prohibited.
   - Verbatim evidence fidelity (Rule 13): Quotes in Col 16 (Notes) must include section indicators and forbid truncation ellipses (`...`).

4. **Agent Protocols & SSOT Consistency:**
   - Detects obsolete/stale path strings across all scripts and skills.
   - Verifies 1:1 synchronization between disk skills (`.agents/skills/*`) and the `Agent Customizations Index` in `AGENTS.md`.

## 3. Reporting & Remediation

- The full diagnostic report is saved to `04_Reports/workspace_lint_report.md`.
- Present a concise summary highlighting `[CRITICAL]`, `[WARNING]`, and `[PASS]` counts.
- Propose automated remediation for simple hygiene issues or specific data fixes.
