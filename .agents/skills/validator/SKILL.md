---
name: validator
description: A Critic subagent that cross-checks Shadow Reports against the Coding Rulebook.
---

# Validator Subagent (Critic)

The `validator` skill allows you to spawn a subagent dedicated to reviewing extraction output. It serves as a strict quality control layer before any data touches the Master Excel Sheet.

## 1. Invocation
- Use `invoke_subagent` to spawn a subagent with the `self` or `research` type (if it needs to read rules).
- Provide the generated `Shadow Report` and the original `Correlation Table` to the subagent.

## 2. Validator Prompt Instructions
When prompting the Validator subagent, instruct it to explicitly check for the following critical failure points:
1. **Level of Analysis Violation:** Are there any Firm, Team, or Organization-level variables included? (Violates `06_non_individual_anchors.md`)
2. **Focal-Entity Violation:** Did the orchestrator accidentally include cross-entity variables like a subordinate's voice behavior or a coworker's performance when the anchor is the Leader/Expatriate? (Violates `01_dyadic_data_rules.md`)
3. **No Guesswork:** Did the orchestrator hallucinate alphas or ranges instead of safely using `999`? (Violates `00_core_process.md`)
4. **Demographic Rule:** Did the orchestrator properly apply `999` for demographic measure descriptors (Items, Min, Max)? (Violates `08_data_entry_formatting.md`)

## 3. Reflection & Correction Loop
- If the Validator returns `PASS`, proceed to Step 2 (Excel Injection).
- If the Validator returns `REJECT`, you (the Orchestrator) MUST **Halt Excel Injection**. Read the Validator's feedback, correct the Shadow Report, and repeat the Validation step until it passes.
