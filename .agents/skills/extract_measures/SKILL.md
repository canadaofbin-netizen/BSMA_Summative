---
name: extract_measures
description: Automates the extraction of statistical data from included PDF papers using 4-Node subagents.
---

# Skill: Extract Measures

When triggered, you must execute the following automated Two-Tier Verification workflow to verify screening status and extract measurement details from an academic paper.

## 1. Two-Tier Verification Workflow

### Node 0: Pre-Extraction Screening Gate (Mandatory Pre-Flight Filter)
- **Objective:** Prior to deploying measure extraction nodes, re-evaluate and verify the paper's eligibility using the authoritative multi-tier decision sequence defined in `include_exclude_pipeline/references/screening_rules_core.md`.
- **Workflow:**
  1. Evaluate the PDF against the Screening Hierarchy:
     - **Tier 0 (Fast-Exit):** Qualitative-only, SEM-only path models lacking correlation matrices, non-English.
     - **Tier 1 (Override Gates):** Leader BSB (Screening Rule 1), Intra-Organizational BSB (Screening Rule 2), Individual Employee Empirical BSB (Screening Rule 3).
     - **Tier 2 (Traps & Guardrails):** Level of Analysis (Exclude Team/Firm/Group aggregation, e.g., $N = \text{teams}$), Construct Homonymy (attitudes, branch identification, internal meetings are NOT BSB), Key Informant proxies, Purposive action vs mere communication.
  2. **Branching Decision:**
     - **If Verdict is `0 = exclude`:**
       - **ABORT EXTRACTION IMMEDIATELY.** Do NOT spawn Nodes 1 through 4 (preventing token waste, cognitive overload, and forced miscoding).
       - Return fatal string: `[SCREENING_EXCLUDED: <Reason>]`.
       - Record in Excel: Col 5 = `'0 = exclude'`, Col 6 = Reason for Exclusion, Col 16 = Verbatim quotes (no ellipses).
       - Terminate processing for this paper.
     - **If Verdict is `1 = include`:**
       - Confirmed empirical BSB study! Proceed immediately to spawn the **4-Node Extraction Pipeline (Nodes 1 to 4)** below.

## 2. 4-Node Subagent Invocation (Parallel Execution for Confirmed Papers)
Use the `invoke_subagent` tool to spawn FOUR specialized `research` subagents in parallel to prevent LLM cognitive overload and ensure 100% Zero-Defect extraction.
**CRITICAL RULE:** Do NOT extract bibliometrics (Title, Author, Year, Country, N, etc.). They are already coded manually.

### Node 1: Pre-flight Triage Agent
- **Prompt:** "Scan the Methodology section of the PDF [Path] for Time-lag/Longitudinal flags (e.g., 'Time 1', 'Time 2', 'T1', 'T2', 'six months later'). If found, return `{"is_longitudinal": true, "time_points": ["T1", "T2"]}`. If cross-sectional, return `{"is_longitudinal": false}`. Do not extract other data."

### Node 2: Footnote Scanner (Circuit Breaker)
- **Prompt:** "Scan ONLY the footnotes/notes below the 'Means, Standard Deviations, and Correlations' table in the PDF [Path]. 
  - If you detect keywords indicating partial correlations (e.g., 'controlling for', 'partial', 'residuals'), return `{"is_partial_mixed": true}`.
  - If you detect keywords indicating missing data imputation (e.g., 'FIML', 'imputed', 'multiple imputation'), return `{"is_imputed": true}`. Otherwise, return false for both flags."

### Node 3: Table Parser (Flat Statistics)
- **Prompt:** "Focus ONLY on the 'Means, Standard Deviations, and Correlations' square matrix in the PDF [Path]. Refer to `references/extraction_edge_cases.md` for statistical traps.
  - **Stage 1 (CoT):** Before extracting data, output a `<matrix_reasoning>` block. Explicitly state whether the upper or lower diagonal contains the zero-order correlations vs. corrected/partial correlations. If ambiguous, return `[AMBIGUOUS_MATRIX_DIAGONAL]`.
  - **LATENT CIRCUIT BREAKER:** If the table title, labels, or footnotes contain keywords like 'Latent', 'AVE (Average Variance Extracted)', or 'Discriminant Validity', the values are NOT raw correlations. Return `[LATENT_CORRELATION_VIOLATION]`.
  - **Stage 2 (Pruning):** If the table contains both Global (Total) scores and Sub-facet scores for the same construct, extract ONLY the sub-facets to preserve independence. Discard the Global score.
  - **LoA CIRCUIT BREAKER:** If data is aggregated at Team/Unit/Firm level, return `[LoA_VIOLATION]`.
  - Drop all demographic variables (Age, Gender, Tenure). 
  - For remaining variables, copy the exact variable name/symbol from the table axis into `table_anchor_name`. Extract `mean` and `sd`. Include an `is_transformed` boolean (true if Log/Z-score was applied).
  - Extract correlations mapping `var1_anchor` and `var2_anchor` to their `table_anchor_name`.
  - **CELL PROOF RULE:** For every correlation, extract `cell_proof` containing the exact `row_header_quote`, `col_header_quote`, and unedited `raw_cell_value` (with asterisks, e.g., '0.35**') for 100% auditability.
  - Return JSON strictly following this structure (No Markdown):
{
  "is_transformed": false,
  "variables": [{"table_anchor_name": "Exact Axis Name", "mean": 999, "sd": 999}],
  "correlations": [
    {
      "var1_anchor": "Exact Axis Name 1",
      "var2_anchor": "Exact Axis Name 2",
      "r": 999,
      "cell_proof": {
        "row_header_quote": "Exact row header",
        "col_header_quote": "Exact col header",
        "raw_cell_value": "0.35**"
      }
    }
  ]
}
"

### Node 4: Text Analyzer (Delayed Classification & Anchor Reconciliation)
- **Prompt:** "Focus ONLY on the Methodology ('Measures' and 'Sample') section in the PDF [Path]. Refer to `references/extraction_edge_cases.md` for measurement traps.
  - **LoA CIRCUIT BREAKER:** If the Methodology text states the sample is aggregated at the Team/Firm level, return `[LoA_VIOLATION]`.
  - **ANCHOR RECONCILIATION BRIDGE:** Use the candidate `table_anchor_name` list from Node 3 to reconcile textual measure labels with table axis labels, preventing fuzzy join mismatches.
  - Use `<target_analysis>` block to classify the variable. If the measure explicitly targets 'inter-boundary' entities (e.g., outside the department, other teams, customers, external organizations), classify as `"BS"`. If intra-team, vague, or an outcome variable, strictly classify as `"NB"`.
  - **ZERO-BSB CIRCUIT BREAKER:** If after analyzing all candidate variables, ZERO variables qualify as `"BS"` (`count(BS) == 0`), do NOT guess or force non-BS variables (e.g., attitudes, unit identification, internal meetings) into BS slots. Return `[NO_BSB_CONSTRUCT_VIOLATION]`.
  - Extract `items`, `min`, `max`.
  - **ITEMS PROOF RULE:** `items_quote` must be the exact sentence stating the number of items and scale anchor (e.g., 'measured with five items on a 7-point Likert scale').
  - For `reliability`, use a polymorphic object with `type` (Alpha, Omega, CR, Not_Applicable, Not_Reported) and `value`. For objective/formative metrics (Firm Size, Age), type MUST be `"Not_Applicable"` and value `999`.
  - **VERBATIM RULE:** `source_quote` must be the exact sentence. Escape quotes with `\"` and newlines with `\n`. `specific_measure` MUST be an exact, unmodified substring of `source_quote`.
  - Return JSON strictly following this structure (No Markdown):
{
  "dataset_fingerprint": {"sample_origin": "Not Reported", "data_collection_year": 999},
  "measure_details": [
    {
      "table_anchor_name": "Inferred Name Matching Node 3",
      "classification_type": "BS",
      "items": 999,
      "items_quote": "exact sentence stating item count and anchors",
      "min": 999,
      "max": 999,
      "reliability": {"type": "Not_Reported", "value": 999},
      "specific_measure": "escaped string",
      "source_quote": "exact escaped sentence"
    }
  ]
}
"

## 3. STRICT JSON ONLY & Hand-off
- Wait asynchronously for all 4 subagents.
- If ANY subagent returns a fatal string code (e.g., `[LoA_VIOLATION]`, `[NO_BSB_CONSTRUCT_VIOLATION]`, `[AMBIGUOUS_MATRIX_DIAGONAL]`), immediately return that string code to the Orchestrator. Do NOT attempt to merge.
  - On `[NO_BSB_CONSTRUCT_VIOLATION]`: Automatically convert the paper judgment to `0 = exclude` with `Reason for Exclusion: No effect size of interest` (or `Construct Homonymy`) and inject verbatim evidence from the Measures text into Col 16.
- Otherwise, merge the 4 valid JSON responses into a single cohesive payload and return it to the Orchestrator for Validation.

## 4. Strict Domain Guardrails

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 1: Zero-Order Correlation Preference & Latent Handling:** When extracting correlations, you are strictly forbidden from extracting standardized betas ($\beta$), path coefficients, partial correlations, or correlations with regression residuals from regression tables. You must prioritize extracting raw observed correlations from "Means, Standard Deviations, and Correlations" square matrices. **Latent Exception:** If the article ONLY provides correlations based on latent variables (e.g., CFA/SEM), you MUST STILL EXTRACT the reported value, BUT you must clearly write "Based on latent variables" in the Notes section for that effect size. Do NOT reject the paper just because correlations are latent.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 2: Matrix-Specific N Guardrail:** When extracting the Sample Size ($N$), DO NOT blindly trust the $N$ stated in the Abstract or Methodology text. You MUST prioritize the "Listwise N" (effective sample size) explicitly printed at the bottom of the Correlation Matrix (e.g., in table notes). If they differ, the table's $N$ takes absolute precedence.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 3: Pure Number Enforcement:** When extracting correlation values ($r$) or descriptive statistics, you MUST strictly strip all significance asterisks (e.g., `*`, `**`) and alphabetical letters from numerical values (e.g., convert `0.45**` to `0.45`). Return pure floating-point numbers only.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 4: Multi-Node Extraction Pipeline:** You must utilize a 4-Node Pipeline (Pre-flight Triage, Footnote Scanner, CoT Table Parser, Text Analyzer Fingerprinting) to aggressively cross-verify extracted measurements.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 5: Physical Excel Isolation (4-Sheet Rule):** Data must be inserted into one of 4 isolated sheets (Raw_Metrics, Transformed_Metrics, Imputed_Metrics, Salami_Review_Queue) depending on its `is_transformed`, `is_imputed`, and dataset fingerprint flags to maintain 100% purity of the zero-order `Raw_Metrics`.

- **SEM-only Data Warning (Extraction Rule 1 supplement):** If a paper relies entirely on SEM path coefficients and does NOT provide a zero-order correlation matrix (even latent), it must be excluded for lacking extractable effect sizes. Do NOT confuse partial rectangular cross-correlation tables with full square correlation matrices.


**[Added via Rule 9 Feedback]**
**Extraction Rule 6: Sub-scale Item & Reliability Decomposition (Sub-dimension Mapping):** When a global construct is reported in the methodology text (e.g., "COBSBs with 13 items") but the correlation matrix breaks it down into multiple sub-scales/sub-dimensions (e.g., Service Delivery, Internal Influence), you MUST NOT blindly duplicate the global item count or global reliability across all sub-dimensions. The Text Analyzer and Orchestrator must actively parse the text to decompose and map the exact item counts (e.g., 5, 4, 4 instead of 13) and specific reliabilities to each corresponding sub-dimension. If the text does not specify the decomposed numbers, enforce the Zero Guesswork Policy (999).

**[Added via Extraction Upgrade]**
**Extraction Rule 7: Sub-dimension vs. Global Composite Extraction Protocol:** When a study provides both a global composite BSB score (e.g., Tushman gatekeeping BSA combining intra- and extra-unit communication) and an independent external communication sub-facet (e.g., Extraunit Communication):
(a) Prioritize extracting the pure external boundary-spanning facet (`External Communication`) as the primary BSB measure.
(b) If the global composite BSB is also extracted, it must be explicitly labeled with `"Global composite score"` in Col 50 (Notes) to preserve meta-analytic independence.
(c) Purely intra-unit communication (within the team/department) must strictly remain classified as `"NB"`.

**[Added via Extraction Upgrade]**
**Extraction Rule 8: Subagent Quota & Local Python Fallback Protocol:** If `invoke_subagent` fails due to API rate limits or quota exhaustion (`RESOURCE_EXHAUSTED 429`), the Orchestrator must immediately execute an isolated local Python script using `fitz` (PyMuPDF) to extract the PDF text and correlation tables, maintaining 100% operational continuity without halting the pipeline.

**[Added via Data Integrity Upgrade]**
**Extraction Rule 9: Verbatim Cell Proof & Items Evidence Anchoring:** All extracted correlation values ($r$) and scale metrics (items count, scale anchors) must be accompanied by raw verbatim proofs (`cell_proof` with `raw_cell_value`, `row_header_quote`, `col_header_quote` and `items_quote` with the exact sentence describing the scale). Truncation with ellipses (`...`) is strictly forbidden. This ensures 100% auditability against the source PDF without manual re-reading.

**[Added via Data Integrity Upgrade]**
**Extraction Rule 10: 5-Layer Defense-in-Depth & Python Type Coercion:** The data injection engine (`universal_excel_inserter.py`) must enforce 5 defensive layers: (1) Truncation Auto-Repair for cut-off JSON matrices, (2) Prompt Contamination Detection, (3) Quarantine Containment in `scratch/quarantine/`, (4) Automatic Type Coercion mapping missing values (`null`, `"-"`, `""`, `"N/A"`) to `999` and `"Not Reported"`, and (5) Atomic Excel Commit.

## 5. Cross-References (Global DNA)
As a domain skill, this file is governed by the global `.agents/AGENTS.md`. When executing this skill, you must remember:
- **Rule 1 (Zero Guesswork Policy):** This is why we strictly enforce `999` and `"Not Reported"` in the JSON schemas above. Do not deviate.
- **Rule 9 (Dynamic Abstraction):** The Subagent Prompts provided in Section 1 are structural blueprints. The Orchestrator must dynamically deploy and tune them based on the specific paper context, rather than treating them as static strings.
- **Rule 13 (Verbatim Quote Injection):** All subagent verdicts and text extractions must include full verbatim evidence with no ellipsis truncation. *(Formerly Global Rule 30)*
- **Measurement Edge Cases Reference:** Consult [references/extraction_edge_cases.md](file:///references/extraction_edge_cases.md) for detailed matrix and statistical trap warnings.

