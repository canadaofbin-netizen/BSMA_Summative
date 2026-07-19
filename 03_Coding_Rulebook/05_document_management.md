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
