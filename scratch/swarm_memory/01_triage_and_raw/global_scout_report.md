# Global Scout Report: Analysis of AGENTS.md
**Target File**: `G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\AGENTS.md`
**Date**: 2026-07-11

## 1. Isolation of Global System Rules vs. Domain-Specific Logic
**Conclusion:** The rulebook does **NOT** perfectly isolate global system rules. It heavily mixes global system architecture rules with domain-specific logic tied to the BSMA meta-analysis project. 

**Evidence of Domain-Specific Logic:**
- **Rule 1 (Zero Guesswork Policy):** Explicitly lists specific statistical variables (r, Mean, SD, Alpha, Items, Min, Max, N) which are specific to the meta-analysis scope.
- **Rule 2 (Subagent Delegation):** Specifically directs behavior for "extracting data from papers."
- **Rules 3, 4, 6 (Excel Injection & Formatting):** Hardcodes the target file `BSMA_Master_Coding_Sheet.xlsx` and project identifiers like `BSMA ID`.
- **Rule 25 (Physical Excel Isolation):** Hardcodes specific Excel sheet names (`Raw_Metrics`, `Transformed_Metrics`, `Imputed_Metrics`, `Salami_Review_Queue`) and dataset flags.

**Evidence of Global System Rules:**
- **Rule 5:** Instructions on handling the `/ask` command safely.
- **Rule 21:** Technical guardrails on JSON Log Parsing.
- **Rules 26 & 30:** Swarm system protocols and documentation mirroring.

*Recommendation:* Extract domain-specific meta-analysis rules (like target Excel sheets, specific variables, and paper extraction specifics) into a separate domain configuration or specialized skill to keep `AGENTS.md` strictly focused on universal OS behaviors.

## 2. Referencing and Linking to SKILLs
**Conclusion:** The rulebook **DOES** properly link to and reference the existence of SKILLs.

**Evidence:**
- **Rule 26 (Human Rulebook Mirroring):** Explicitly mandates that updates to any `SKILL.md` must be mirrored in the human-readable `03_Coding_Rulebook` directory to maintain a Single Source of Truth.
- **Rule 30 (Dynamic Skill Abstraction & Protection):** Correctly references the `13team` Swarm OS and provides strict architectural directives. It establishes that `SKILL.md` files are abstract blueprints, forbids hardcoding prompts or permanently altering the skill structure for single tasks, and mandates dynamic prompt generation for subagents. It also strictly forbids unauthorized modification of `SKILL.md` files.
