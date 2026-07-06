---
name: validator
description: A Critic subagent that cross-checks Shadow Reports against the Coding Rulebook.
---

# Validator Subagent (Critic)

The `validator` skill allows you to spawn a subagent dedicated to reviewing extraction output. It serves as a strict quality control layer before any data touches the Master Excel Sheet.

## 1. Invocation
- Use `invoke_subagent` to spawn a subagent with the `self` or `research` type (if it needs to read rules).
- Provide the generated **JSON payload** and the original **Correlation Table** from the paper to the subagent.

## 2. Validator Prompt Instructions
When prompting the Validator subagent, instruct it to explicitly check for the following critical failure points:
1. **Level of Analysis Violation:** Is the boundary spanning measured at the Individual-level? ONLY Individual-level passes. Any non-individual level (Team, Unit, Department, Organization, Firm) must be excluded. (Violates `06_non_individual_anchors.md`)
2. **Focal-Entity Violation:** Did the orchestrator accidentally include cross-entity variables like a subordinate's voice behavior or a coworker's performance when the anchor is the Leader/Expatriate? (Violates `01_dyadic_data_rules.md`)
3. **Level-of-Analysis & Construct Homonymy Audit:** Explicitly verify that the study is NOT a firm-level patent study, an interfirm alliance study, a team-level aggregated analysis ($N = \text{teams}$), or a bibliometric citation analysis. If any macro keywords (`patent`, `optical disk`, `strategic alliance`, `interfirm`, `firm value`, `team boundary work`, `bibliometric`) appear without individual employee dyadic/survey data, flag immediately for exclusion under `Code 3` or `Code 2`.
4. **No Guesswork:** Did the orchestrator hallucinate alphas or ranges instead of safely using `999`? (Violates `00_core_process.md`)
5. **Demographic Rule:** Did the orchestrator properly apply `999` for demographic measure descriptors (Items, Min, Max)? (Violates `08_data_entry_formatting.md`)

## 3. Reflection & Correction Loop
- If the Validator returns `PASS`, proceed to Excel Injection via `universal_excel_inserter.py`.
- If the Validator returns `REJECT`, you (the Orchestrator) MUST **Halt Excel Injection**. Read the Validator's feedback, correct the JSON payload, and repeat the Validation step until it passes.
