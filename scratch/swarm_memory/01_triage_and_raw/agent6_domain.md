# Architectural Evaluation: Meta-Analysis Principles

## 1. Strengths in Data Purity & Strict Exclusion
- **Zero-Guesswork Policy (AGENTS.md Rule 1):** Enforcing missing data as `999` or `"Not Reported"` prevents AI hallucination or imputation.
- **Physical Isolation (AGENTS.md Rule 25):** The 4-Sheet Rule (`Raw_Metrics`, `Transformed_Metrics`, `Imputed_Metrics`, `Salami_Review_Queue`) successfully guarantees the pristine nature of zero-order data.
- **Domain Guardrails (include_exclude_pipeline):** Explicit criteria against Firm/Team level spans and proxies ensure strict construct validity.

## 2. Critical Vulnerabilities (Violations of Meta-Analysis Principles)
- **Dynamic Prompt Tuning Breaks Replicability (AGENTS.md Rule 30 & 13team):** 
  - *Issue:* The Orchestrator dynamically generates and tunes subagent prompts at runtime based on context. 
  - *Violation:* Meta-analysis requires a **fixed, static, a priori coding protocol**. If extraction prompts evolve dynamically, papers are coded under shifting rubrics, destroying inter-rater reliability.
- **Self-Evolution & DNA Updates (13team Section 5):**
  - *Issue:* The "Troika" can debate and formulate new rules mid-extraction.
  - *Violation:* Modifying inclusion/exclusion rules mid-pipeline without re-evaluating previously processed papers leads to an inconsistent dataset.
- **Agent 6 (Domain Specialist Wildcard):**
  - *Issue:* Agent 6 dynamically "adopts specific domain knowledge."
  - *Violation:* The AI must strictly adhere *only* to the predefined rulebook. A wildcard agent might introduce external, non-pre-registered theoretical assumptions.
- **Debate-Driven Consensus (13team Section 4):**
  - *Issue:* Subagents debate to formulate fixes and reach consensus.
  - *Violation:* Data extraction should be strictly objective based on the text. Debate-driven consensus risks rationalizing data that isn't explicitly stated, violating the zero-guesswork policy.

## 3. Recommendations
1. **Freeze Prompts for Extraction:** Disable dynamic tuning of prompts for data extraction and include/exclude pipelines; use static templates.
2. **Halt Auto-Evolution during Batches:** Any rule updates must trigger a mandatory re-run of previously processed papers to maintain a uniform dataset.
3. **Restrict Agent 6:** Confine the Domain Specialist to strictly reference the `03_Coding_Rulebook` rather than open-ended knowledge.
