# Domain Scout Report: Skill Isolation Analysis

## Overview
As a Scout in the 13team Swarm, I have analyzed the following domain skills:
1. `extract_measures` (`.agents\skills\data_extractor\extract_measures\SKILL.md`)
2. `include_exclude_pipeline` (`.agents\skills\include_exclude_pipeline\SKILL.md`)

## 1. Analysis of `extract_measures`
**Isolation of Domain Logic:**
- **Domain Logic Present:** High. It isolates detailed, domain-specific instructions (e.g., handling zero-order correlations, identifying "Latent" correlations, managing LoA violations).
- **Global Systemic Rules Bleed-Through:** 
  - The skill implicitly encodes **Rule 1 (Universal Zero Guesswork Policy)** from `AGENTS.md` by heavily hardcoding `999` and `"Not Reported"` into the required JSON schemas (Nodes 3 & 4), but it fails to explicitly reference the rule that mandates this behavior.
  - It prescribes strictly hardcoded prompts for the 4 Node subagents. This borders on violating **Rule 30 (Dynamic Skill Abstraction)** if `extract_measures` is treated as an abstract framework.

**Need for Cross-Linking to AGENTS.md:**
- **Yes.** It requires explicit cross-linking to `AGENTS.md` to reference:
  - **Rule 1 (Universal Zero Guesswork Policy):** To justify why `999` and `"Not Reported"` are used, ensuring future agents do not alter this standard to `null` or attempt to deduce values.
  - **Rule 2 (Subagent Delegation):** To formally anchor the Node 1-4 execution pattern to the global delegation rule.
  - **Rule 30 (Dynamic Skill Abstraction):** To clarify whether the embedded prompts are an immutable blueprint or if they must be dynamically tuned by the Orchestrator at runtime.

## 2. Analysis of `include_exclude_pipeline`
**Isolation of Domain Logic:**
- **Domain Logic Present:** High. Section 5 purely defines domain-specific exclusion guardrails (Firm/Team Level Ban, Proxy Guardrail, Hidden Guardrails).
- **Global Systemic Rules Bleed-Through:** 
  - Minimal. The skill focuses cleanly on orchestrating Python scripts (`swarm_prep.py`, `swarm_inject.py`) and does not explicitly embed global rules into its text.

**Need for Cross-Linking to AGENTS.md:**
- **Yes.** It is currently missing explicit hooks to global systemic rules that MUST occur as side-effects of running this pipeline:
  - **Rule 4 (Automated Github Sync):** Step 3 injects data into Excel via `swarm_inject.py`, but it fails to remind the Orchestrator to run Git sync commands afterward.
  - **Rule 6 (Universal Excel Insertion) & Rule 25 (Physical Excel Isolation):** To ensure any data injection strictly respects the global 4-Sheet rule.
  - **Rule 26 (Human Rulebook Mirroring):** If the domain guardrails in Section 5 are ever refined, agents must remember to update the corresponding files in the `03_Coding_Rulebook` directory to maintain the Single Source of Truth.

## Conclusion & Recommendations
Neither skill perfectly isolates domain logic because they both lack explicit boundary interfaces to the global rulebook (`AGENTS.md`). 

**Recommendation:**
Add a `# Global Project Rules Constraint` section to both `SKILL.md` files that explicitly cross-links to `.agents/AGENTS.md`. This will ensure that future agents orchestrating these skills are instantly reminded of their systemic obligations (e.g., Git Sync, Zero Guesswork, Rulebook Mirroring) without convoluting the domain logic files themselves.
