---
name: architecture_refactoring
description: Standardized 4-step protocol for safely refactoring AGENTS.md, SKILL.md, and agent.json files with mandatory backup, top-down modification order, automated post-verification, and smoke testing.
---

# Skill: Architecture Refactoring Protocol

When the user requests a structural modification to the rule architecture (e.g., renumbering, merging duplicates, adding sections, reorganizing), you MUST follow this exact 4-step protocol. Do NOT skip any step.

## Prerequisites
- Confirm that the current originals are backed up in `99_Archives_and_Backups/NEVER_CHANGE_IN_ANY_CASES/` with a timestamped filename (e.g., `AGENTS_v3_snapshot_YYYYMMDD_HHMM.md`).
- If not backed up, create the backup BEFORE making any changes.

---

## Step 1: Modify the Parent File (AGENTS.md)

### 1a. Execute Changes
- Apply the structural changes (renumbering, merging, sectioning, etc.)
- **Content Preservation Rule:** Never alter the substance of any rule. Only restructure.

### 1b. Post-Verification (5 Checks)
Run a Python verification script that checks:

| # | Check | Method | Pass Criteria |
|---|---|---|---|
| 1 | Content Integrity | Extract critical unique keywords from backup, verify all exist in new file | 0 missing keywords |
| 2 | Numbering Continuity | Regex `^\d+\.\s+\*\*` to extract all rule numbers | Sequential 1~N, no gaps |
| 3 | Section Structure | Regex `^## Section` to find section headers | All expected sections present |
| 4 | Merge Verification | Check that deleted rules' unique keywords exist in their merge target | All keywords absorbed |
| 5 | Cross-Reference Audit | Grep `Rule \d+` across all `.md`, `.json`, `.py` in `.agents/` | List files with old numbers |

**Gate:** All 5 checks must PASS before proceeding to Step 2.

---

## Step 2: Modify Child Files (SKILL.md)

### 2a. Execute Changes
- Remove duplicated rules that now exist in AGENTS.md
- Replace with cross-reference: `"All screening decisions MUST follow AGENTS.md Section B (Rules X–Y)."`
- Update any subagent version references (e.g., `v2` → `v3`)
- Update `Cross-References` section with new rule numbers

### 2b. Post-Verification (6 Checks)

| # | Check | Method | Pass Criteria |
|---|---|---|---|
| 1 | Agent Version Migration | Search for old version strings | 0 old references |
| 2 | Duplicate Removal | Search for 10+ known duplicated keyword phrases | 0 found |
| 3 | Cross-Reference Insertion | Search for `AGENTS.md Section` string | Found |
| 4 | Rule Number Update | Extract `Rule \d+` from Cross-References section | All within valid range |
| 5 | File Size Reduction | Compare bytes/lines with backup | >30% reduction expected |
| 6 | Conflict Resolution | Search for known conflicting phrases | 0 found |

**Gate:** All 6 checks must PASS before proceeding to Step 3.

---

## Step 3: Modify Agent Prompts (agent.json)

### 3a. Execute Changes
- Update any `Rule X` references in system prompts to new numbers
- Add any new trap/checklist items if rules were added

### 3b. Post-Verification (Final Audit)
Run a comprehensive scan across ALL files in `.agents/` and brain `.agents/`:
- Grep `Rule \d+` in all `.md`, `.json`, `.py` files
- Verify every referenced number falls within the valid new range (1~N)
- **Pass Criteria:** 0 invalid (out-of-range) Rule references

---

## Step 4: End-to-End Smoke Test

### 4a. Data Integrity Check
- Re-run the latest comparison script (e.g., `compare_v3_v2revised.py`)
- **Pass Criteria:** Accuracy and disagreement count identical to pre-refactoring baseline

### 4b. Pipeline Initialization
- Run `swarm_prep.py --batch 2` to verify the pipeline initializes without errors
- **Pass Criteria:** No Python exceptions

### 4c. Live Agent Test (2 Papers)
Invoke `bsma_reviewer_v3` on exactly 2 known papers:
- **Paper A (Expected: Include):** A confirmed individual-level BSB study with a correlation matrix
- **Paper B (Expected: Exclude):** A confirmed firm/team-level study that should trigger Code 3

For each paper, verify:
- Correct Include/Exclude verdict
- QA Checklist (Q1~Q5) fully answered in `self_correction_logic`
- Verbatim evidence contains **zero** ellipses (`...`)
- JSON output written successfully

**Gate:** Both papers must match expected verdicts.

---

## Completion
After all 4 steps pass, update the `walkthrough.md` artifact with:
- Summary of changes made
- Verification results
- New rule number mapping (if renumbered)
