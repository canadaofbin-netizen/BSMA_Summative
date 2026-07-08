---
name: extract_measures
description: Automates the extraction of statistical data from included PDF papers using 4-Node subagents.
---

# Skill: Extract Measures

When triggered, you must execute the following automated workflow to extract measurement details from an academic paper.
> **PREREQUISITE:** This paper has already passed rigorous screening and is **CONFIRMED for inclusion**.
> **EXCEPTION (Exclusion Authority):** Even though included, if you discover a clear Level of Analysis violation, Construct Homonymy, or Ambiguous Diagonal during data extraction, you possess explicit authority to Fast-Fail and return the corresponding fatal string code (e.g., `[LoA_VIOLATION]`) to exclude the data.

## 1. 4-Node Subagent Invocation (Parallel Execution)
Use the `invoke_subagent` tool to spawn FOUR specialized `research` subagents in parallel to prevent LLM cognitive overload and ensure 100% Zero-Defect extraction.
**CRITICAL RULE:** Do NOT extract bibliometrics (Title, Author, Year, Country, N, etc.). They are already coded manually.

### Node 1: Pre-flight Triage Agent
- **Prompt:** "Scan the Methodology section of the PDF [Path] for Time-lag/Longitudinal flags (e.g., 'Time 1', 'Time 2', 'T1', 'T2', 'six months later'). If found, return `{"is_longitudinal": true, "time_points": ["T1", "T2"]}`. If cross-sectional, return `{"is_longitudinal": false}`. Do not extract other data."

### Node 2: Footnote Scanner (Circuit Breaker)
- **Prompt:** "Scan ONLY the footnotes/notes below the 'Means, Standard Deviations, and Correlations' table in the PDF [Path]. 
  - If you detect keywords indicating partial correlations (e.g., 'controlling for', 'partial', 'residuals'), return `{"is_partial_mixed": true}`.
  - If you detect keywords indicating missing data imputation (e.g., 'FIML', 'imputed', 'multiple imputation'), return `{"is_imputed": true}`. Otherwise, return false for both flags."

### Node 3: Table Parser (Flat Statistics)
- **Prompt:** "Focus ONLY on the 'Means, Standard Deviations, and Correlations' square matrix in the PDF [Path].
  - **Stage 1 (CoT):** Before extracting data, output a `<matrix_reasoning>` block. Explicitly state whether the upper or lower diagonal contains the zero-order correlations vs. corrected/partial correlations. If ambiguous, return `[AMBIGUOUS_MATRIX_DIAGONAL]`.
  - **Stage 2 (Pruning):** If the table contains both Global (Total) scores and Sub-facet scores for the same construct, extract ONLY the sub-facets to preserve independence. Discard the Global score.
  - **LoA CIRCUIT BREAKER:** If data is aggregated at Team/Unit/Firm level, return `[LoA_VIOLATION]`.
  - Drop all demographic variables (Age, Gender, Tenure). 
  - For remaining variables, copy the exact variable name/symbol from the table axis into `table_anchor_name`. Extract `mean` and `sd`. Include an `is_transformed` boolean (true if Log/Z-score was applied).
  - Extract correlations mapping `var1_anchor` and `var2_anchor` to their `table_anchor_name`.
  - Return JSON strictly following this structure (No Markdown):
{
  "is_transformed": false,
  "variables": [{"table_anchor_name": "Exact Axis Name", "mean": 999, "sd": 999}],
  "correlations": [{"var1_anchor": "Exact Axis Name 1", "var2_anchor": "Exact Axis Name 2", "r": 999}]
}
"

### Node 4: Text Analyzer (Delayed Classification)
- **Prompt:** "Focus ONLY on the Methodology ('Measures' and 'Sample') section in the PDF [Path].
  - **LoA CIRCUIT BREAKER:** If the Methodology text states the sample is aggregated at the Team/Firm level, return `[LoA_VIOLATION]`.
  - Use `<anchor_inference>` block to infer the `table_anchor_name` from the text to match the table's abbreviation.
  - Use `<target_analysis>` block to classify the variable. If the measure explicitly targets 'inter-boundary' entities (e.g., outside the department, other teams, customers, external organizations), classify as `"BS"`. If intra-team, vague, or an outcome variable, strictly classify as `"NB"`.
  - Extract `items`, `min`, `max`. 
  - For `reliability`, use a polymorphic object with `type` (Alpha, Omega, CR, Not_Applicable, Not_Reported) and `value`. For objective/formative metrics (Firm Size, Age), type MUST be `"Not_Applicable"` and value `999`.
  - **VERBATIM RULE:** `source_quote` must be the exact sentence. Escape quotes with `\"` and newlines with `\n`. `specific_measure` MUST be an exact, unmodified substring of `source_quote`.
  - Return JSON strictly following this structure (No Markdown):
{
  "dataset_fingerprint": {"sample_origin": "Not Reported", "data_collection_year": 999},
  "measure_details": [
    {
      "table_anchor_name": "Inferred Name",
      "classification_type": "BS",
      "items": 999,
      "min": 999,
      "max": 999,
      "reliability": {"type": "Not_Reported", "value": 999},
      "specific_measure": "escaped string",
      "source_quote": "exact escaped sentence"
    }
  ]
}
"

## 2. STRICT JSON ONLY & Hand-off
- Wait asynchronously for all 4 subagents.
- If ANY subagent returns a fatal string code (e.g., `[LoA_VIOLATION]`), immediately return that string code to the Orchestrator. Do NOT attempt to merge.
- Otherwise, merge the 4 valid JSON responses into a single cohesive payload and return it to the Orchestrator for Validation.
