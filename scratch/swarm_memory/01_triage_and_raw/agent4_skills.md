# Skills Cross-Reference Report

## 1. `extract_measures` Skill
**File:** `G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\skills\data_extractor\extract_measures\SKILL.md`

Cross-references to `AGENTS.md`:
- **Rule 1 (Zero Guesswork Policy):** Enforces strict adherence to outputting `999` and `"Not Reported"` instead of guessing or deviating from JSON schemas.
- **Rule 30 (Dynamic Abstraction):** Requires the Orchestrator to treat provided subagent prompts as structural blueprints to be dynamically deployed and tuned based on specific paper contexts, rather than static strings.

## 2. `include_exclude_pipeline` Skill
**File:** `G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\skills\include_exclude_pipeline\SKILL.md`

Cross-references to `AGENTS.md`:
- **Rule 4 (Automated Github Sync):** Mandates running git commands to back up `BSMA_Master_Coding_Sheet.xlsx` after successfully running the injection script (`swarm_inject.py`).
- **Rule 6 & 25 (Excel Insertion Rules):** Ensures that any injected data adheres strictly to the 4-Sheet physical isolation rule (Raw_Metrics, Transformed_Metrics, Imputed_Metrics, Salami_Review_Queue).
