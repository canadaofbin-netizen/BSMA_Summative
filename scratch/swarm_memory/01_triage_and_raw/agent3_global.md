# Critical Analysis of AGENTS.md for Domain-Specific Logic Leaks

## Overview
This report evaluates `AGENTS.md` for remaining domain-specific logic leaks that violate a purely "Universal Framework" philosophy. A Universal Framework should ideally be agnostic to specific projects, datasets, and domain terminologies, functioning as a pure orchestration and reasoning engine.

## Findings: Domain-Specific Leaks

1. **Hardcoded Project & Filename References (Rules 3, 4, 6, 25)**
   - **Leak:** The rules heavily reference `BSMA_Master_Coding_Sheet.xlsx`, `BSMA ID`, and the `BSMA Meta-Analysis project`.
   - **Violation:** A universal framework should not hardcode target file names or IDs. These should be passed dynamically as configuration variables (e.g., `TARGET_DATABASE_FILE`, `UNIQUE_IDENTIFIER_KEY`).

2. **Hardcoded Fallback Values (Rule 1)**
   - **Leak:** Missing numeric values are forced to `999` and text fields to `"Not Reported"`.
   - **Violation:** While zero guesswork is universal, the exact null-coalescing values (`999`) are domain-specific statistical conventions. A universal framework should parameterize null/missing data representations.

3. **Specific Domain Terminology / Data Structures (Rule 25)**
   - **Leak:** Mentions of `Raw_Metrics`, `Transformed_Metrics`, `Imputed_Metrics`, and `Salami_Review_Queue`.
   - **Violation:** "Salami_Review_Queue" is a highly specific domain concept (referring to salami-slicing in academic literature). The 4-sheet isolation rule dictates a specific data architecture rather than abstract data separation principles.

4. **Hardcoded Directory Structures (Rule 26)**
   - **Leak:** Hardcodes the directory `03_Coding_Rulebook` for human documentation.
   - **Violation:** A universal framework should expect a configurable path for syncing rules to human-readable documentation.

## Universal Principles Successfully Maintained
- **Rule 2 (Subagent Delegation):** Abstract and framework-oriented.
- **Rule 5 (Read-Only /ask):** Safe universal operational behavior.
- **Rule 21 (JSON Log Parsing Guardrail):** Safe abstract extraction behavior for agent logs.
- **Rule 30 (Dynamic Skill Abstraction & Protection):** Excellent universal enforcement of abstraction in the Swarm OS.

## Recommendations for Refactoring
To achieve a purely universal Swarm/Agent OS framework:
- Extract all `BSMA` references, spreadsheet names, and directory paths into a project-level `config.yaml` or `.env` file.
- Change `AGENTS.md` to reference dynamic environment variables (e.g., "Insert data into the file defined by `MASTER_DATABASE_PATH`").
- Abstract data handling rules to general principles (e.g., "Use the project's defined missing value tokens" instead of `999`).
