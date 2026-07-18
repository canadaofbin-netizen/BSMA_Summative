# Agent 12: Final Consensus on Architecture & Handoff Protocol

## 1. The "Handoff Protocol" Boundary (Resolving Contradiction 3 & User Mediation)
**Synthesis:** Per the User's mediation, the `13team` Swarm OS is an analytical assistant, **NOT** a primary data extraction tool. The epistemological conflict between Zero-Guesswork (Rule 1) and Swarm Debate is resolved by enforcing a strict operational boundary. 
**Consensus:** Data extraction must be performed by single-shot, non-debating subagents that strictly apply Rule 1 (`999` or `"Not Reported"` for missing data). The `13team` is only invoked *post-extraction* or for high-level methodology, acting as a QA/triage assistant. 

### Architectural Changes Needed:
**For `.agents/AGENTS.md` (Add new rule for Handoff Protocol):**
- **Rule 31 (Handoff Protocol):** The `13team` swarm is explicitly forbidden from performing brute-force data extraction. Primary data extraction must be handled by parallel, single-shot subagents following Rule 1. The `13team` may only be invoked *after* primary extraction for QA validation, or for complex methodology triage as a specialized assistant.

**For `.agents/skills/13team/SKILL.md` (Update core directives):**
- Add **CRITICAL BOUNDARY** warning: "This skill is strictly an analytical assistant and QA validator. Do NOT use `13team` for primary data extraction from papers. It must only receive pre-extracted data (to debate/validate) or methodological queries."

## 2. Resolving Contradiction 2: Rogue Python Code vs. 4-Sheet Isolation
**Synthesis:** Agent 10 correctly identified that Python injection scripts (e.g., `swarm_inject.py`) violate Rule 25 by writing indiscriminately to `wb.active` and using legacy filenames.
**Consensus:** Python injection scripts must be aggressively refactored to enforce the physical isolation of data.

### Architectural Changes Needed:
**For Python Code Generation (Orchestrator Directive / Code Prompts):**
- **Target Excel File:** Scripts must strictly target `BSMA_Master_Coding_Sheet.xlsx`. Legacy targets (e.g. `BSMA_AI_Run_V2.xlsx`) are explicitly banned.
- **Routing Logic:** Indiscriminate writes to `wb.active` are forbidden. Scripts MUST implement explicit sheet-routing logic based on boolean flags:
  - If `is_transformed == False` and `is_imputed == False` -> Write to `Raw_Metrics`
  - If `is_transformed == True` -> Write to `Transformed_Metrics`
  - If `is_imputed == True` -> Write to `Imputed_Metrics`
  - If dataset fingerprint collision detected -> Write to `Salami_Review_Queue`

By implementing these structural boundaries, we enforce strict compliance with Rule 1 (Zero-Guesswork), Rule 25 (Physical Excel Isolation), and the User's explicit architectural mandate for the `13team`.
