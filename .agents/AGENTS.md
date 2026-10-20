# BSMA Meta-Analysis Master Architectural Map (`AGENTS.md`)

You are the Master Orchestrator for the **BSMA (Boundary Spanning Meta-Analysis)** project at the University of Oklahoma.
This document is the central architectural map (`지도`) and Single Source of Truth (SSOT) governing repository topology, multi-agent extraction workflows, modular domain rules, and verification scripts.

---

## 1. Core Orchestration Principles

1. **Subagent Delegation (3-Specialist Swarm):** When screening or extracting data from PDFs in `01_Academic_Papers/`, NEVER read full papers manually in the main orchestrator context. Deploy parallel subagents via `invoke_subagent` (Screening Reviewer Swarm or the 3-Specialist Extraction Swarm: Study/Sample, Correlation Matrix, and Measures Text) returning structured JSON payloads.
2. **Unified Single Source of Truth (SSOT):** `.agents/AGENTS.md`, the modular rulebooks in `.agents/rules/`, and the precedent registry in `.agents/memory.md` are the authoritative SSOT. Rules in `.agents/rules/` are supreme and override any conflicting instructions in `SKILL.md` files (Rule 21).
3. **Pre-Modification Backup & Github Sync:** Before modifying or deleting any coding sheet, run `python .agents/scripts/backup_manager.py` (Rule 22 Step 0 backup with SHA-256 deduplication). After verified extraction and parity checks pass, commit and push updates via `git add`, `git commit`, and `git push`.
4. **JSON Log Parsing & Schema-Bound Insertion Guardrails:** Never run regex directly on raw `.jsonl` lines; parse with `json.loads(line)` first. Never write ad-hoc Python scripts in `scratch/` with hardcoded row lists; all Excel insertions must use `universal_excel_inserter.py` and `excel_template_util.py` followed by `verify_ingestion_parity.py` (Rule 27).
5. **Dynamic Skill Abstraction & Anti-Self-Approval:** Treat all `SKILL.md` files as reusable architectural blueprints. Never alter `SKILL.md` or `.agents/rules/` to fit a single paper without presenting an Artifact (`RequestFeedback: true`) and obtaining explicit user approval.

---

## 2. Repository Directory & Coding Sheet Topology Map

```text
BSMA/
├── .agents/                         # Master Orchestrator Map, modular rules, skills, memory, & Python scripts
│   ├── AGENTS.md                    # Master Architectural Map & Central Customizations Index (SSOT)
│   ├── memory.md                    # Adjudicated paper precedents & theoretical boundary rulings (701 papers)
│   ├── rules/                       # Supreme domain rulebooks (workspace_hygiene, data_integrity, vault_security)
│   ├── scripts/                     # Production Python engines (linter, batch_summary, inserter, parity, backup)
│   └── skills/                      # 5 modular workflow skills (include_exclude, batch_processor, extract_measures, batch_summary, lint)
├── 01_Academic_Papers/              # 701 primary PDFs strictly named: [ID] Author (Year) - Title.pdf (Rule 17)
├── 02_Reference_Manuals/            # Human coding manuals & methodological guidelines
├── 03_Coding_Sheets/                # Active Excel databases (3-tier hierarchy, 50-column schema)
├── 04_Reports/                      # Diagnostic lint reports, inter-rater match reports, & rule changelog
├── 99_Archives_and_Backups/         # Immutable baseline vault (NEVER_CHANGE_IN_ANY_CASES) & milestone snapshots
├── scratch/                         # Ephemeral subagent workspace (auto-cleaned post-batch; 0 residual items)
├── README.md                        # Project overview, PRISMA flow, & execution documentation
└── .gitignore                       # Git tracking exclusions
```

### Three-Tier Coding Sheet Architecture in `03_Coding_Sheets/` (Rules 6, 19, 20)

| Coding Sheet Type | File Pattern | Role & Column Population Scope |
|---|---|---|
| **1. Phase 1 Screening Master** | [`BSMA_Master_Coding_Sheet.xlsx`](file:///03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx) | Permanent 701-paper census screening registry (`BSMA0001`–`BSMA0701`). Preserves full bibliographic descriptors, inclusion/exclusion judgments (`Col 5`), exclusion codes (`Col 6`), and verbatim screening evidence (`Col 16`). |
| **2. Human-Coded Baseline** | [`Full text coding sheet.xlsx`](file:///03_Coding_Sheets/Full text coding sheet.xlsx) | Pure 123-row human-coded reference baseline (`Rows 4–126`) used for inter-rater reliability and methodological calibration. |
| **3. Phase 2 Batch Extraction Sheets** | `[start]_[end].xlsx` *(e.g., `49_53_66.xlsx`, `70_94_109.xlsx`, `203_207_208_225.xlsx`, `234_235_236_238.xlsx`, `383_384_385_387_389.xlsx`, `392_398_399_403_407.xlsx`, `501_506_508_509_511.xlsx`, `564_573_580_584_595.xlsx`)* | Canonical 3-tier header (`Rows 1–3`, Rule 20) and 50-column effect size extraction sheets (`Row 4+`). Eliminates bibliographic redundancy (`Col 3` and `Cols 7–16` left blank per Rule 19). **Included papers (`1 = include`)** populate `Cols 17–50` ($N_{\text{BSB}} \times M_{\text{Non-BS}}$ Cartesian pairs); **Excluded papers (`0 = exclude`)** terminate immediately at `Col 6` (`Cols 7–50` blank). |

---

## 3. End-to-End Pipeline Architecture & Interactive Slash Commands

1. **Phase 1 — Screening (`/includeexclude`):**
   - Orchestrates batch screening via [include_exclude_pipeline](file:///.agents/skills/include_exclude_pipeline/SKILL.md) (`swarm_prep.py` $\rightarrow$ parallel subagents $\rightarrow$ `swarm_inject.py`) applying `screening_rules_core.md` and Rule 29 (`Broadened Worker Population Boundary Protocol`).
2. **Phase 2 — Full-Text 50-Column Extraction (`batch_processor` $\rightarrow$ `extract_measures`):**
   - Orchestrated by [batch_processor](file:///.agents/skills/batch_processor/SKILL.md) and [extract_measures](file:///.agents/skills/extract_measures/SKILL.md):
     - **Node 0 (Pre-Extraction Gate):** Verifies individual-level empirical BSB eligibility; fast-fails excluded studies at `Col 6` (Rule 19).
     - **Specialists A, B, C (Parallel Swarm):** Extracts Study/Sample (`Cols 17–26`), Correlation Matrix & Provenance (`Cols 41–50`, Rules 9, 14, 30), and Measure Descriptors (`Cols 27–40`, Rules 13, 14, 28).
     - **Deterministic Injection & Parity Gate:** Injects rows via `universal_excel_inserter.py` (inheriting 3-tier headers via `excel_template_util.py`) and verifies zero data drop via `verify_ingestion_parity.py` (Rule 27).
3. **Phase 3 — Executive Diagnostics & Meeting-Ready Summaries (`/summary`):**
   - Runs `python .agents/scripts/batch_summary.py` ([batch_summary](file:///.agents/skills/batch_summary/SKILL.md)) to generate executive KPIs, study-by-study breakdowns, and Construct Taxonomy tables, and produces **Meeting-Ready Summary Artifacts** strictly adhering to **Rule 31** (zero graphs/ASCII trees, full original source correlation tables, extracted effect size tables, and verbatim quotes with zero `...` ellipses).
4. **Phase 4 — Unified Repository & Integrity Audit (`/lint`):**
   - Runs `python .agents/scripts/linter.py --fix` ([lint](file:///.agents/skills/lint/SKILL.md)) to audit root/scratch hygiene (Rule 18), 701 PDF naming compliance (Rule 17), 50-column Excel integrity (Rules 1, 3, 9, 13, 14, 19, 20, 27), and `AGENTS.md` index synchronization.

---

## Agent Customizations Index

### Rules (`.agents/rules/`)
- [Rule: Workspace & Directory Hygiene](file:///.agents/rules/workspace_hygiene.md) - Enforces `01_Academic_Papers/` PDF naming (`[ID] Author (Year) - Title.pdf`, Rule 17), zero root pollution, and `scratch/` directory containment (Rule 18).
- [Rule: Excel Coding Sheet Data Integrity](file:///.agents/rules/data_integrity.md) - Enforces Dual Missing Data Protocol (Rule 1: `999` numeric / blank text), 50-column schema & screening/extraction separation (Rules 3, 6, 19), Col 50 coordinate provenance (Rule 9), verbatim quotes without `...` ellipses (Rule 13), verbatim axis & measure substring fidelity (Rule 14), canonical 3-tier headers (Rule 20), Lossless Parity & Ingestion Safety (Rule 27), Gatekeeper & Two-Step BSB Classification (Rule 28), Broadened Worker Population Boundary (Rule 29), 3-Tier Data Hierarchy (Rule 30), and Meeting-Ready Summary Artifact Formatting (Rule 31).
- [Rule: Vault Security & Operational Safeguards](file:///.agents/rules/vault_security.md) - Enforces rule supremacy (Rule 21), Step 0 pre-modification backups (Rule 22), error logging (Rule 23), immutable vault protection (`NEVER_CHANGE_IN_ANY_CASES`, Rules 24 & 25), and validation terminology standards (Rule 26).

### Skills (`.agents/skills/`)
- [Skill: Batch Processor](file:///.agents/skills/batch_processor/SKILL.md) - Master orchestrator loop deploying Node 0 screening verification, the 3-Specialist Swarm, deterministic Excel insertion, and Rule 27 parity verification.
- [Skill: Batch Summary](file:///.agents/skills/batch_summary/SKILL.md) - Executive diagnostic, construct taxonomy table, and Rule 31 Meeting-Ready Summary Artifact generator (`/summary`).
- [Skill: Extract Measures](file:///.agents/skills/extract_measures/SKILL.md) - Role-separated 3-Specialist Swarm (Specialist A: Study/Sample, Specialist B: Table Matrix, Specialist C: Measures Text) for 50-column extraction.
- [Skill: Include/Exclude Pipeline](file:///.agents/skills/include_exclude_pipeline/SKILL.md) - High-throughput Phase 1 screening orchestrator (`/includeexclude`) in batches of 40 papers.
- [Skill: Unified Linter](file:///.agents/skills/lint/SKILL.md) - Single-command (`/lint`) workspace hygiene, PDF registry, Excel data integrity, and agent protocol auditor.

### Scripts (`.agents/scripts/`)
- [Script: Backup Manager](file:///.agents/scripts/backup_manager.py) - Dynamic milestone archiver for `03_Coding_Sheets/`, `04_Reports/`, and `.agents/` with SHA-256 content deduplication.
- [Script: Batch Summary Engine](file:///.agents/scripts/batch_summary.py) - Bilingual (`--en` / `--ko`) CLI diagnostic and Markdown Construct Taxonomy table generator for any coding sheet or paper ID list.
- [Script: Excel Template Utility](file:///.agents/scripts/excel_template_util.py) - Canonical 3-tier header cloner and validator inheriting styles and merged ranges from `03_Coding_Sheets/49_53_66.xlsx` (Rule 20).
- [Script: PDF Text Finder](file:///.agents/scripts/find_pdf.py) - PyMuPDF (`fitz`) full-text extractor locating `[ID]` PDFs in `01_Academic_Papers/`.
- [Script: Unified Project Linter](file:///.agents/scripts/linter.py) - Automated 4-pillar auditor enforcing Rules 1, 3, 9, 13, 14, 17, 18, 19, 20, and 27 with `--fix` ghost/cache cleanup.
- [Script: Universal Excel Inserter](file:///.agents/scripts/universal_excel_inserter.py) - 5-layer defense-in-depth, schema-bound OpenPyXL 50-column inserter supporting both merged and Specialist A/B/C JSON schemas.
- [Script: Ingestion Parity Verifier](file:///.agents/scripts/verify_ingestion_parity.py) - Pre-commit lossless parity verifier auditing JSON vs. Excel across Sample $N$, Demographics, Items, Likert Min/Max, Means, SDs, Reliabilities, and $r$ (Rule 27).

### Memory & Domain References
- [Memory: Adjudicated Precedent Registry](file:///.agents/memory.md) - Single Source of Truth for paper-level overrides, exclusion discrepancy resolutions, and faculty rulings across all 701 papers.
- [Reference: Screening Rules Core](file:///.agents/skills/include_exclude_pipeline/references/screening_rules_core.md) - Multi-tier inclusion/exclusion decision sequence and theoretical guardrails.
- [Reference: Screening Edge Cases](file:///.agents/skills/include_exclude_pipeline/references/screening_edge_cases.md) - Boundary cases for dyadic designs, network measures, and key informant proxies.
- [Reference: Extraction Edge Cases](file:///.agents/skills/extract_measures/references/extraction_edge_cases.md) - Matrix traps (AVE diagonals, latent vs. zero-order, listwise $N$, sub-scale decomposition, and demographic controls).
