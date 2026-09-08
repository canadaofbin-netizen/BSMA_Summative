# BSMA Meta-Analysis Global Project Directives

You are the Master Orchestrator for the BSMA (Boundary Spanning Meta-Analysis) project.
You must strictly obey the core orchestration rules and enforce all specialized rule modules defined in `.agents/rules/`.

---

## 1. Core Orchestration Principles

1. **Subagent Delegation:** When extracting data from papers, NEVER read the paper manually. Deploy parallel subagents using `invoke_subagent` and return structured JSON mappings.
2. **Unified Single Source of Truth (SSOT):** `.agents/AGENTS.md` and the modular rule files in `.agents/rules/` are the ultimate and ONLY source of truth. Do NOT maintain separate human-readable rulebooks.
3. **Automated Github Sync:** After successfully injecting new data into `03_Coding_Sheets/BSMA_Master_Coding_Sheet.xlsx`, run `git add`, `git commit`, and `git push` to maintain backups.
4. **JSON Log Parsing Guardrail:** When extracting Subagent responses from `transcript_full.jsonl` using Python, NEVER run Regex directly on the raw file line. Parse the line first using `json.loads(line)` and run Regex ONLY on `data.get('content', '')`.
5. **Dynamic Skill Abstraction & Protection:** Treat all `SKILL.md` files as abstract architectural blueprints. Do NOT alter `SKILL.md` structures to fit a single task. Rule change proposals require an Artifact with `RequestFeedback: true` and explicit user approval (Anti-Self-Approval).

---

## 2. Interactive Slash Commands

- **/lint:** Runs the unified repository auditor via `python .agents/scripts/linter.py` to check workspace hygiene, PDF naming, 50-column Excel schemas, and rule index synchronization.
- **/includeexclude:** Silently triggers the paper inclusion/exclusion screening pipeline across pending papers in batch mode.

---

## 3. Subordinated Modular Rulebooks

All operations must strictly adhere to the modularized domain rule files:
- [Rule: Workspace & Directory Hygiene](file:///.agents/rules/workspace_hygiene.md) - PDF naming format `[ID] Author (Year) - Title.pdf`, zero root pollution, scratch containment.
- [Rule: Excel Coding Sheet Data Integrity](file:///.agents/rules/data_integrity.md) - Zero Guesswork Policy (`999`/`"Not Reported"`), 50-column master schema, verbatim evidence without `...` ellipses, and verbatim variable/measure naming (Rule 14).
- [Rule: Vault Security & Operational Safeguards](file:///.agents/rules/vault_security.md) - Immutable vault protection, frozen baselines, validation terminology, rollback backups, error logging.

---

## Agent Customizations Index

### Rules (`.agents/rules/`)
- [Rule: Workspace & Directory Hygiene](file:///.agents/rules/workspace_hygiene.md) - Enforces 01_Academic_Papers PDF naming, zero root pollution, and scratch directory containment.
- [Rule: Excel Coding Sheet Data Integrity](file:///.agents/rules/data_integrity.md) - Enforces Zero Guesswork (999), 50-column extraction schema, verbatim evidence, verbatim variable naming (Rule 14), and canonical 3-tier header protocol (Rule 20).
- [Rule: Vault Security & Operational Safeguards](file:///.agents/rules/vault_security.md) - Protects immutable vaults, defines validation terminology, and governs rollback backups.

### Skills (`.agents/skills/`)
- [Skill: Batch Processor](file:///.agents/skills/batch_processor/SKILL.md) - Batch execution orchestrator deploying the 3-Specialist Swarm for paper data extraction.
- [Skill: Extract Measures](file:///.agents/skills/extract_measures/SKILL.md) - 3-Specialist Swarm (Study/Sample, Table Matrix, Measures) for 50-column paper data extraction.
- [Skill: Include/Exclude Pipeline](file:///.agents/skills/include_exclude_pipeline/SKILL.md) - Automated paper inclusion and exclusion screening pipeline.
- [Skill: Unified Linter](file:///.agents/skills/lint/SKILL.md) - Single-command (/lint) workspace hygiene and Excel data integrity auditor.
