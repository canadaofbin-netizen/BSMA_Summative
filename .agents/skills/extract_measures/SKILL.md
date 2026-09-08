---
name: extract_measures
description: Automates the extraction of 50-column statistical data from included PDF papers using a specialized 3-Specialist Subagent Swarm (Study/Sample, Table Matrix, and Measure Descriptors).
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
     - **If Verdict is `0 = exclude` (Construct Homonymy, Level of Analysis / Aggregated Data):**
       - **ABORT EXTRACTION IMMEDIATELY.** Do NOT spawn Specialist B or C (preventing token waste, cognitive overload, and forced miscoding).
       - Record in Excel: Col 1 = Coder Initials, Col 2 = Article ID, Col 5 = `'0 = exclude'`, Col 6 = Reason for Exclusion (`3 = Non-individual level (team/firm/org analysis)` for aggregated data; `1 = No effect size of interest` for construct homonymy).
       - Terminate immediately after Col 6: Leave Cols 7–50 completely blank (`None`) per Rule 19 (1 single row). Terminate extraction for this paper.
     - **If Verdict is `1 = include` (Individual-Level Empirical BSB):**
       - Confirmed individual-level empirical BSB study! Proceed immediately to spawn the full **3-Specialist Swarm Extraction Pipeline (Specialists A, B, C)** below.

## 2. 3-Specialist Subagent Swarm (Parallel Role-Separated Extraction)
Use the `invoke_subagent` tool to spawn THREE specialized `research` subagents in parallel. Distributing the extraction across clear functional boundaries eliminates LLM cognitive overload, prevents attention dilution, and ensures 100% Zero-Defect fidelity across the 50-column master schema.

### Specialist A: Study & Sample Specialist (`study_sample_descriptor` — Cols 17–26)
- **Scope & Focus:** Abstract, Methodology ("Sample", "Participants", "Procedure"), and Correlation Table Footnotes.
- **Objectives:**
  1. **Study Design:** Determine if cross-sectional vs. longitudinal/time-lagged (record time points, waves, lags) [Cols 17–18].
  2. **Geographic & Cultural Context:** Extract Country of sample, specify sub-regions, and classify International Context (Domestic vs. Cross-national) [Cols 19–21].
  3. **Effective Sample Size ($N$):** Extract $N$ from Sample description and cross-verify with listwise $N$ in table footnotes (table footnote takes precedence per Extraction Rule 2) [Col 22].
  4. **Demographics:** Extract Mean Age, % Female, Organizational Tenure (years), and Occupation Type/Job Role [Cols 23–26].
  5. **Bias Scanner (Footnote Pre-check):** Check correlation table notes for partial correlations/controls (`is_partial_mixed`) or missing data imputation (`is_imputed`).
  6. **Verbatim Evidence:** Extract exact verbatim sentences into `sample_quote` (strictly no ellipses per Rule 13).
  7. **Zero Guesswork (Dual Missing Data Protocol):** Enforce integer `999` for missing numeric metrics; clean blank (`None`) for non-applicable text fields. `"Not Reported"` is prohibited.
- **Prompt Blueprint:**
  "Scan ONLY the Abstract, Sample/Participants section, and Correlation Table footnotes in the PDF [Path].
  Extract Study & Sample Descriptors (Cols 17-26):
  1. Study design: Cross-sectional vs. Longitudinal. If longitudinal, list time points (e.g. ['T1', 'T2']).
  2. Geographic context: Country of sample, specific region if reported, and international context.
  3. Sample size (N): Cross-verify methodology text N with listwise N in correlation table footnote.
  4. Demographics: Mean Age, % Female, Org Tenure (years), and Occupation Type.
  5. Bias flags: Check table footnotes for partial correlations, controls, or missing data imputation.
  Return clean JSON strictly matching this schema (No Markdown, 999 for missing numbers, null for missing strings):
  {
    \"study_design\": \"Cross-sectional\",
    \"study_design_other\": null,
    \"country\": \"United States\",
    \"country_specify\": null,
    \"international_context\": \"Domestic\",
    \"sample_size_n\": 253,
    \"mean_age\": 41.2,
    \"pct_female\": 24.5,
    \"org_tenure\": 8.3,
    \"occupation_type\": \"R&D Scientists and Engineers\",
    \"is_longitudinal\": false,
    \"time_points\": [\"T1\"],
    \"is_partial_mixed\": false,
    \"is_imputed\": false,
    \"sample_quote\": \"exact verbatim sentence describing sample and N\"
  }"

### Specialist B: Table Matrix Specialist (`boundary_spanning_matrix` — Cols 41–50)
- **Scope & Focus:** ONLY the "Means, Standard Deviations, and Correlations" square matrix table and its immediate notes.
- **Objectives:**
  1. **Stage 1 (CoT Matrix Reasoning):** Output a `<matrix_reasoning>` block identifying table number, lower vs. upper diagonal (zero-order vs. corrected/partial). If ambiguous, return fatal code `[AMBIGUOUS_MATRIX_DIAGONAL]`.
  2. **Circuit Breakers:**
     - **LATENT CIRCUIT BREAKER:** If matrix is CFA/SEM latent without raw zero-order correlations, record latent note or return `[LATENT_CORRELATION_VIOLATION]`.
     - **LoA CIRCUIT BREAKER:** If table notes reveal group/team aggregation ($N = \text{teams}$), return `[LoA_VIOLATION]`.
  3. **Stage 2 (Pruning & Coordinates):** Drop demographic control variables (Age, Gender, Tenure, Education).
  4. **Table Axis Fidelity & Index Pruning (Rule 14):** Copy substantive variable names and abbreviations into `table_anchor_name` character-for-character (e.g., `"External Communication"`, `"Ext. Comm."`, `"Internal COBSB"`). Automatically prune purely table-indexing numeric prefixes (e.g., `"1. "`, `"10. "`). NEVER paraphrase, translate, or normalize the construct wording.
  5. **Descriptive Stats:** Extract `mean`, `sd`, and reliability (alpha) if printed in table or diagonal.
  6. **Zero-Order Correlations ($r$):** Extract raw correlations between variable pairs.
  7. **CELL PROOF AUDITABILITY (Extraction Rule 9):** For every correlation, extract `cell_proof` with exact `row_header_quote`, `col_header_quote`, and unedited `raw_cell_value` (with asterisks, e.g., `"-0.24**"`).
- **Prompt Blueprint:**
  "Focus ONLY on the 'Means, Standard Deviations, and Correlations' square matrix in the PDF [Path].
  - Stage 1 (CoT): Output <matrix_reasoning> explicitly stating table number and lower vs. upper diagonal structure.
  - Drop all demographic variables (Age, Gender, Tenure, Education).
  - Prune table-indexing numbers (e.g., '1. ', '10. ') while strictly copying exact variable construct names/symbols from table axis into table_anchor_name (Rule 14: no paraphrasing or normalization).
  - Extract mean, sd, and table-reported reliability for each variable.
  - Extract zero-order correlations mapping var1_anchor and var2_anchor.
  - CELL PROOF RULE: For every correlation, provide cell_proof with row_header_quote, col_header_quote, and raw_cell_value with asterisks.
  Return JSON strictly matching this schema (No Markdown, 999 for missing numbers):
  {
    \"table_number\": \"Table 2\",
    \"listwise_n\": 253,
    \"is_transformed\": false,
    \"variables\": [
      {
        \"var_index\": 1,
        \"table_anchor_name\": \"1. External Communication\",
        \"mean\": 3.45,
        \"sd\": 0.82,
        \"reliability_table\": 0.88
      }
    ],
    \"correlations\": [
      {
        \"var1_anchor\": \"1. External Communication\",
        \"var2_anchor\": \"2. Role Ambiguity\",
        \"r\": -0.24,
        \"cell_proof\": {
          \"row_header_quote\": \"2. Role Ambiguity\",
          \"col_header_quote\": \"1. External Communication\",
          \"raw_cell_value\": \"-0.24**\"
        }
      }
    ]
  }"

### Specialist C: Measures Text Specialist (`measure_descriptor` — Cols 27–40)
- **Scope & Focus:** ONLY the Methodology "Measures / Measurement Instruments" section.
- **Objectives:**
  1. **Construct Inventory & Classification:** Inspect all candidate variables described in text.
     - **Boundary Spanning Behavior (BS):** Individual behaviors reaching across boundary interfaces (external organizations, clients/customers, other departments).
     - **Non-Boundary Spanning (NB):** Internal behaviors, attitudes (identification, commitment), perceptions, or non-boundary performance.
  2. **ZERO-BSB CIRCUIT BREAKER:** If ZERO variables qualify as `"BS"`, return fatal code `[NO_BSB_CONSTRUCT_VIOLATION]`.
  3. **Anchor Reconciliation Bridge:** Map each textual measure to the candidate table axis names (`table_anchor_name`) from Specialist B to prevent fuzzy join failures.
  4. **Sub-scale Decomposition (Extraction Rule 6):** If a global scale (e.g., 13 items) is broken down into sub-scales in the matrix, decompose and extract exact item counts per sub-scale.
  5. **BSB Measure Descriptors (Cols 27–33):**
     - `number_of_items`: integer (or `999` if not reported).
     - `min_score` / `max_score`: Likert anchors (e.g., 1 to 5, 1 to 7).
     - `report_type`: Self-report / Supervisor-report / Peer-report / Objective / Not Reported.
     - `report_type_note`: Specific details if multi-source.
     - `specific_measure_used`: Exact, unmodified substring of `source_quote` capturing scale citation (Rule 14).
     - `items_quote`: Exact verbatim sentence stating number of items and anchors (strictly no ellipses per Rule 13).
     - `reliability`: polymorphic object `{"type": "Alpha"|"Omega"|"CR"|"Not_Reported"|"Not_Applicable", "value": 0.88}`.
     - `notes`: Specific notes or composite definitions (Rule 7).
  6. **Non-BS Measure Descriptors (Cols 34–40):**
     - Identical rigorous schema for all substantive non-BS variables.
- **Prompt Blueprint:**
  "Focus ONLY on the Methodology ('Measures') section in the PDF [Path].
  - Classify each variable as 'BS' (Boundary Spanning Behavior: actions spanning external boundaries, clients, other departments) or 'NB' (Non-BS: internal behaviors, attitudes, outcomes).
  - ZERO-BSB CIRCUIT BREAKER: If 0 variables qualify as 'BS', return [NO_BSB_CONSTRUCT_VIOLATION].
  - For each variable, extract:
    1. table_anchor_name: Match exactly to candidate correlation table axis names.
    2. number_of_items, min_score, max_score, report_type, report_type_note.
    3. specific_measure_used: Must be an exact, unmodified substring of source_quote (Rule 14).
    4. items_quote: Exact verbatim sentence stating item count and anchors (Rule 13: NO ellipses).
    5. reliability: polymorphic object {type, value}.
    6. source_quote: Full verbatim sentence introducing the scale.
  Return JSON strictly matching this schema (No Markdown):
  {
    \"boundary_spanning_measures\": [
      {
        \"table_anchor_name\": \"1. External Communication\",
        \"number_of_items\": 6,
        \"min_score\": 1,
        \"max_score\": 7,
        \"report_type\": \"Self-report\",
        \"report_type_note\": null,
        \"specific_measure_used\": \"Keller (1994)\",
        \"items_quote\": \"External communication was measured using six items on a 7-point scale.\",
        \"reliability\": {\"type\": \"Alpha\", \"value\": 0.88},
        \"source_quote\": \"Keller (1994) developed the six-item external communication scale...\",
        \"notes\": \"Primary external boundary-spanning facet\"
      }
    ],
    \"non_bs_measures\": [
      {
        \"table_anchor_name\": \"2. Role Ambiguity\",
        \"number_of_items\": 6,
        \"min_score\": 1,
        \"max_score\": 7,
        \"report_type\": \"Self-report\",
        \"report_type_note\": null,
        \"specific_measure_used\": \"Rizzo, House, and Lirtzman (1970)\",
        \"items_quote\": \"Role ambiguity was assessed with six items on a 7-point Likert scale.\",
        \"reliability\": {\"type\": \"Alpha\", \"value\": 0.84},
        \"source_quote\": \"Role ambiguity was measured using the six-item scale from Rizzo, House, and Lirtzman (1970)...\",
        \"notes\": null
      }
    ]
  }"

### Specialist D: Deterministic Integration & Cartesian Join Engine
- **Orchestrator Role:**
  - Await parallel execution of Specialists A, B, and C.
  - If any specialist returns a fatal circuit breaker code (`[LoA_VIOLATION]`, `[NO_BSB_CONSTRUCT_VIOLATION]`, `[AMBIGUOUS_MATRIX_DIAGONAL]`), immediately abort extraction and record screening verdict.
  - Execute deterministic Python Cartesian join:
    - For each BSB Measure ($i \in [1..M]$) and each Non-BS Measure ($j \in [1..K]$):
      - Query Specialist B's matrix for correlation $r_{ij}$ and `cell_proof`.
      - Construct 50-column row:
        - Cols 1–2: Coder Initials & Paper ID.
        - Col 3: Sample ID (leave blank / None).
        - Col 4: Effect size ID (1, 2, 3...).
        - Col 5: Inclusion-Exclusion Judgment ('1 = include').
        - Col 6: Reason for Exclusion (leave blank / None).
        - Cols 7–16: Article Descriptors (leave completely blank / None per Rule 19; already recorded during screening).
        - Cols 17–26: Study/Sample Descriptors from Specialist A.
        - Cols 27–33: BSB Measure Descriptors from Specialist C.
        - Cols 34–40: Non-BS Measure Descriptors from Specialist C.
        - Cols 41–44: BSB Effect Size Stats (Construct Name, Mean, SD, Reliability) from Specialist B.
        - Cols 45–48: Non-BS Effect Size Stats (Construct Name, Mean, SD, Reliability) from Specialist B.
        - Col 49: Correlation $r_{ij}$ from Specialist B.
        - Col 50: Notes (Composite notes + Cell Proof audit trail).
    - Enforce Rule 1 Dual Missing Data Protocol: integer `999` for missing numeric metrics, clean blank (`None`) for non-applicable text fields.

## 3. STRICT JSON ONLY & Hand-off
- Wait asynchronously for all 3 subagents.
- If ANY subagent returns a fatal string code (e.g., `[LoA_VIOLATION]`, `[NO_BSB_CONSTRUCT_VIOLATION]`, `[AMBIGUOUS_MATRIX_DIAGONAL]`), immediately return that string code to the Orchestrator. Do NOT attempt to merge.
  - On `[NO_BSB_CONSTRUCT_VIOLATION]`: Automatically convert the paper judgment to `0 = exclude` with `Reason for Exclusion: No effect size of interest` (or `Construct Homonymy`) and inject verbatim evidence from the Measures text into Col 16.
- Otherwise, merge the 3 valid JSON responses via the Deterministic Integration Engine and return the complete payload to the Orchestrator for Validation.

## 4. Strict Domain Guardrails

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 1: Zero-Order Correlation Preference & Latent Handling:** When extracting correlations, you are strictly forbidden from extracting standardized betas ($\beta$), path coefficients, partial correlations, or correlations with regression residuals from regression tables. You must prioritize extracting raw observed correlations from "Means, Standard Deviations, and Correlations" square matrices. **Latent Exception:** If the article ONLY provides correlations based on latent variables (e.g., CFA/SEM), you MUST STILL EXTRACT the reported value, BUT you must clearly write "Based on latent variables" in the Notes section for that effect size. Do NOT reject the paper just because correlations are latent.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 2: Matrix-Specific N Guardrail:** When extracting the Sample Size ($N$), DO NOT blindly trust the $N$ stated in the Abstract or Methodology text. You MUST prioritize the "Listwise N" (effective sample size) explicitly printed at the bottom of the Correlation Matrix (e.g., in table notes). If they differ, the table's $N$ takes absolute precedence.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 3: Pure Number Enforcement:** When extracting correlation values ($r$) or descriptive statistics, you MUST strictly strip all significance asterisks (e.g., `*`, `**`) and alphabetical letters from numerical values (e.g., convert `0.45**` to `0.45`). Return pure floating-point numbers only.

**[Originally AGENTS.md §C — relocated for context-window optimization]**
**Extraction Rule 4: 3-Specialist Swarm Architecture (Study/Sample, Matrix, Measures):** You must utilize a specialized 3-Specialist Subagent Swarm (`study_sample_descriptor`, `boundary_spanning_matrix`, `measure_descriptor`) followed by deterministic Python Cartesian integration to aggressively prevent cognitive overload and ensure 100% data integrity across all 50 columns.

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
**Extraction Rule 10: 5-Layer Defense-in-Depth & Python Type Coercion:** The data injection engine (`universal_excel_inserter.py`) must enforce 5 defensive layers: (1) Truncation Auto-Repair for cut-off JSON matrices, (2) Prompt Contamination Detection, (3) Quarantine Containment in `scratch/quarantine/`, (4) Automatic Type Coercion mapping missing values (`null`, `"-"`, `""`, `"N/A"`) to `999` for numeric and `None` (blank) for text, and (5) Atomic Excel Commit.

**[Added via Data Integrity Upgrade]**
**Extraction Rule 11: Verbatim Table Axis & Measure Substring Fidelity (Rule 14 Integration):** Correlation table axis variable names (Cols 41 & 45) must character-for-character preserve the author's exact construct name, sub-dimension phrasing (e.g., `"Internal COBSB"`, `"External COBSB"`, `"Internal Com."`, `"External Com."`), and published abbreviations (e.g., `"BSA"`, `"Org. Comm."`, `"Dual Comm."`). Leading numbers that serve solely for table row/column layout indexing (e.g., `"1. "`, `"10. "`) are automatically pruned, while the original coordinate remains preserved in `cell_proof` and Col 50 Notes. Specific measure names (Cols 32 & 39) must be exact unmodified substrings of methodology quotes (`source_quote`), capturing the precise validated instrument author citation. Post-hoc normalization, translation, or guessing is strictly forbidden.

**[Added via Level of Analysis Aggregation Protocol Upgrade]**
**Extraction Rule 12: Level of Analysis Aggregation Protocol:** Studies where variables or correlations represent group, team, project, or department level aggregation ($N = \text{teams/groups/projects}$, e.g., Cummings 2004 with $N=182$ Work Groups, Brion et al. 2012 with $N=73$ NPD projects evaluating project-level performance and team size) are EXCLUDED under Code 3 (`0 = exclude`, `3 = Non-individual level (team/firm/org analysis)`) to prevent cross-level ecological fallacy. Quantitative effect size extraction is halted. The entry terminates immediately after Col 6 (`Reason for Exclusion`), leaving Cols 7–50 completely blank (`None`) (1 single row per Rule 19). Full verbatim evidence is preserved in the screening database.

**[Added via Header Architecture Upgrade]**
**Extraction Rule 13: Canonical 3-Tier Excel Header Protocol (Rule 20 Integration):** Whenever creating or updating Excel coding sheets (batch sheets or paper extractions), all sheets MUST be initialized via `excel_template_util.py` (inheriting from `03_Coding_Sheets/49_53_66.xlsx`). Row 1 (Section Category), Row 2 (Sub-category), and Row 3 (Leaf Column Names) must be completely preserved along with openpyxl cell styles, merged ranges, and column dimensions. Raw pandas `df.to_excel()` exports that introduce `'Unnamed'` headers are strictly prohibited. Data rows strictly begin at Row 4.

## 5. Cross-References (Global DNA)
As a domain skill, this file is governed by the global `.agents/AGENTS.md`. When executing this skill, you must remember:
- **Rule 1 (Dual Missing Data Protocol):** This is why we strictly enforce `999` for missing numeric metrics and clean blank (`None`) for non-applicable text fields. `"Not Reported"` is prohibited.
- **Rule 9 (Dynamic Abstraction):** The Subagent Prompts provided in Section 1 are structural blueprints. The Orchestrator must dynamically deploy and tune them based on the specific paper context, rather than treating them as static strings.
- **Rule 13 (Verbatim Quote Injection):** All subagent verdicts and text extractions must include full verbatim evidence with no ellipsis truncation. *(Formerly Global Rule 30)*
- **Measurement Edge Cases Reference:** Consult [references/extraction_edge_cases.md](file:///references/extraction_edge_cases.md) for detailed matrix and statistical trap warnings.

