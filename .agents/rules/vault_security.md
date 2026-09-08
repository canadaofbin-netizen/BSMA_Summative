# Rule: Vault Security & Operational Safeguards

This document defines the protection rules for immutable baselines, backup protocols, error handling, and operational rollback strategies.

---

## 1. Immutable Vault Protections (Rules 24 & 25)
- **The Absolute Immutable Vault (Rule 24):** All agents and subagents are **STRICTLY FORBIDDEN** from modifying, deleting, overwriting, or moving any files located inside `99_Archives_and_Backups/NEVER_CHANGE_IN_ANY_CASES` under ANY circumstances. This is the permanent Read-Only Master Backup.
- **The Frozen Baseline Immutable Vault (Rule 25):** Files designated as frozen comparison baselines (e.g., snapshot baselines in `99_Archives_and_Backups/NEVER_CHANGE_IN_ANY_CASES/`) MUST be treated as completely Read-Only snapshots for reproducible cross-validation.
  - **Output Isolation:** Results from new AI runs must be saved to independently named files or separate sheets only.
  - **No Unilateral Syncing:** The AI is absolutely forbidden from modifying or overwriting past Frozen Baseline Excel files.
  - **Explicit Authorization & Pre-Modification Backup:** Modifications may only proceed upon explicit human command, and a physical timestamped backup (`.bak` or `backup_timestamp`) must be created immediately before any write operation.

---

## 2. Validation Terminology Standard (Rule 26)
- **Frozen Baseline:** An immutable comparison snapshot. Does NOT imply content correctness or human verification.
- **Human-Verified:** Data directly reviewed and confirmed by the human researcher. Applied ONLY with explicit human confirmation.
- **Inter-AI Agreement Rate:** Percentage of matching judgments between two AI runs (e.g., V3 vs V2). This is NOT "accuracy".
- **Accuracy:** Reserved exclusively for comparisons against Human-Verified ground truth data.
- **Prohibited Terms:** Never use "Golden Master" for AI outputs. Never use "human baseline" for AI-generated files.

---

## 3. Operational Safeguards & Rollback (Rules 21, 22, 23)
- **Supremacy Hierarchy (Rule 21):** Rules in `AGENTS.md` and `.agents/rules/` are supreme and override conflicting instructions in `SKILL.md` files.
- **Rollback Strategy (Rule 22):** For any task involving modifying or deleting files (Write/Delete), the AI MUST execute **"Step 0: Create a timestamped backup in `99_Archives_and_Backups/`"** before any other actions, evaluate risk, and wait for explicit user approval.
- **Error Recovery Protocol (Rule 23):** When any pipeline step fails mid-execution:
  1. Log the full traceback to `scratch/error_log.md` or `04_Reports/error_report.md`.
  2. Preserve all intermediate outputs in their current state.
  3. Report the failure point and resume instructions to the user.
  *(Do NOT silently retry, skip failed steps, or impute results).*
