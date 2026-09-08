# BSMA Validation Rule Changelog

> Documents the rule changes between Validation versions and the resulting differences.

---

## Version Summary

| Version | File Name | Include | Exclude | Rule Characteristics |
|---|---|---|---|---|
| **V1** | `BSMA_AI_Run_V1_AggRecovery.xlsx` | 115 | 586 | Strict + Aggregation Recovery |
| **V2** | `BSMA_AI_Run_V2_Broad.xlsx` | 179 | 522 | Broad (Researcher Decision) |

---

## V1 -> V2: Addition of Aggregation Recovery Rule

**Git Commits:** `0820472` -> `da6da1a`  
**Result Change:** Include 106 -> 115 (+9 papers)

### Changed Rules

#### Rule 4 (Tier 2): Team Level Aggregation -- Added Aggregation Recovery Exception

```diff
- Studies reporting team as the unit of analysis MUST be excluded under Code 3.
+ NOTE (Individual-Measurement Aggregation Recovery):
+ If a study collected individual-level responses using "I" referent survey items
+ but subsequently aggregated them to team-level or dyad-level for analysis,
+ the underlying individual-level data may still exist.
+ Such papers should be coded as 1 = Include with a note indicating that
+ author contact is required to obtain the individual-level zero-order
+ correlation matrix.
+
+ This exception applies ONLY when:
+ (1) Survey items explicitly use individual referents ("I", "My")
+ (2) Individual-level responses were collected before aggregation
+ (3) Aggregation was a methodological choice, not measurement design
```

### Affected Papers (Example)

- `BSMA0385`, `BSMA0413`: Data collected with individual-level surveys then aggregated to team-level -> Switched from Exclude to Include

---

## V2 -> V3: Researcher Decision 2026-07-28 (Broad Rules)

**Git Commit:** `8086302`  
**Result Change:** Include 115 -> 179 (+64 papers)

### Changed Rules (3 Major Changes)

---

### 1. Rule 4: Aggregation Recovery -- Removed "Author Contact Required"

```diff
- NOTE (Individual-Measurement Aggregation Recovery):
-   coded as 1 = Include with a note indicating that
-   author contact is required
 
+ NOTE (Individual-Measurement Aggregation Recovery -- UNCONDITIONAL INCLUDE):
+   the paper MUST be coded as 1 = Include unconditionally.
+   [Researcher Decision 2026-07-28]
+   The previous "author contact required" qualifier has been removed.
```

> **Impact:** Conditional Includes from V2 become unconditional Includes. May add additional papers.

---

### 2. Rule 6: Communication Frequency -- Significantly Relaxed

```diff
- Variables that merely measure "communication frequency" (e.g., how often
-   someone emails or chats) without specifying a purposive boundary-spanning
-   action are INVALID and MUST be excluded under Code 1.
-
- NOTE (Test Case): Cross-departmental communication frequency
-   without specified purposive boundary-spanning action
-   -> INVALID (Code 1). This is mere communication, not purposive BSB.
 
+ [Researcher Decision 2026-07-28] Work-related communication frequency
+   across organizational or functional boundaries (e.g., "how often do you
+   discuss work-related issues with members of other departments")
+   IS a valid BSB operationalization and MUST BE INCLUDED.
+   Only purely non-work social communication frequency remains invalid.
```

> **Impact:** Many papers previously Excluded due to "simple communication frequency" are now Included. **This change has the largest impact.**

---

### 3. Rule 6: Network Measures -- Broad Inclusion

```diff
- VALID Network BSB (Do NOT Exclude):
-   (a) Advice-seeking network degree centrality
-   (b) E-I index
-   (c) Ego-network heterogeneity
- INVALID (Exclude):
-   (d) Burt's structural constraint measures
-   (c) Sociometric sensor data measuring mere proximity
 
+ VALID Network BSB (Do NOT Exclude):
+   ALL network-based measures of cross-boundary interaction ARE valid:
+   (a) Advice-seeking network degree centrality
+   (b) E-I index
+   (c) Ego-network heterogeneity
+   (d) Burt's structural constraint/structural holes     <-- NEW Include
+   (e) Sociometric sensor data (work-related)             <-- NEW Include
+   (f) ERGM parameters                                    <-- NEW Include
+   (g) Betweenness centrality and brokerage measures      <-- NEW Include
- INVALID (Exclude):
+   (a) Pure non-work social media interaction counts
+   (b) Adaptive Selling scales
```

> **Impact:** Previously Excluded targets such as Burt's structural holes, ERGM, and sociometric data are now fully Included.

---

### Quick Reference Table Changes

```diff
- | Individual-Measurement Aggregation Recovery | Rule 4 | INCLUDE (author contact required) |
+ | Individual-Measurement Aggregation Recovery | Rule 4 | INCLUDE (unconditional) |
+ | Work-related Communication Frequency         | Rule 6 | INCLUDE (if cross-boundary) |
+ | All Network Structural Metrics               | Rule 6 | INCLUDE (Burt, ERGM, etc.) |
```

---

## Comparing Rule Files Directly via Git

```bash
# V1 vs V2 (Strict -> AggRecovery)
git diff 0820472 da6da1a -- .agents/skills/include_exclude_pipeline/references/
 
# V2 vs V3 (AggRecovery -> Broad)
git diff da6da1a 8086302 -- .agents/skills/include_exclude_pipeline/references/
 
# V1 vs V3 (Strict -> Broad, Full Diff)
git diff 0820472 8086302 -- .agents/skills/include_exclude_pipeline/references/
```

---

## V3 -> V4: 3-Specialist Extraction Swarm & Level-of-Analysis Aggregation Exclusion Protocol (2026-09-08)

**Architectural & Methodological Upgrades:**

1. **3-Specialist Subagent Swarm Architecture (`.agents/skills/extract_measures/SKILL.md`):**
   - Upgraded full-text statistical extraction into three specialized roles running in parallel:
     - **Specialist A (`study_sample_descriptor`):** Scope restricted to Sample/Participants text and table footnotes (Cols 17–26).
     - **Specialist B (`boundary_spanning_matrix`):** Scope restricted to the correlation matrix table, extracting exact table axes, raw correlations ($r$), and verbatim `cell_proof` (Cols 41–50).
     - **Specialist C (`measure_descriptor`):** Scope restricted to Methodology Measures text, classifying BSB vs Non-BS, scale anchors, item counts, and verbatim citations (Cols 27–40).
   - Coordinated via a **Deterministic Integration Engine** executing Cartesian product mapping and Zero Guesswork coercion (`999`, `"Not Reported"`).

2. **Rule 14 Codification (`.agents/rules/data_integrity.md`):**
   - **Table Axis Fidelity (Cols 41 & 45):** Variable names must character-for-character preserve exact printed table axis labels, numbers, and abbreviations without post-hoc normalization or paraphrasing.
   - **Specific Measure Substring Fidelity (Cols 32 & 39):** Scale instrument names must be exact, unmodified substrings of the methodology text quote (`source_quote`).

3. **Level-of-Analysis Aggregation Exclusion Protocol (Code 3):**
   - Studies where data or variables represent group-, team-, project-, or department-level aggregation ($N = \text{teams/groups/projects}$, e.g., Paper #66 Brion et al. 2012 with $N=73$ NPD projects; Paper #109 Cummings 2004 with $N=182$ Work Groups) are **strictly EXCLUDED under Code 3** (`0 = exclude`, `3 = Non-individual level (team/firm/org analysis)`) to prevent cross-level ecological fallacy.
   - Bivariate effect size extraction is halted. Cols 17–26 retain sample descriptors; Cols 27–50 are padded with `999` (1 single row); Col 16 records full verbatim evidence of aggregation.
   - **Screening Rule 1 Scope Clarification:** Leader BSB override priority strictly protects rater identity (subordinate rating leader), but is explicitly subordinate to the Level of Analysis aggregation exclusion.

---

## V4 -> V5: Dual Missing Data Protocol, Rule 14 Pruning, Rule 19 Streamlining & Rule 20 3-Tier Headers (2026-09-08)

**Architectural & Data Integrity Upgrades:**

1. **Dual Missing Data Protocol (Rule 1 Upgraded):**
   - **Numeric Missing Values (Cols 17–50):** Integer `999` is strictly enforced for missing empirical numbers ($N$, Mean, SD, $\alpha$, $r$, item counts, Likert anchors) for unambiguous parsing by statistical software (R, SPSS, CMA, Stata).
   - **Text / Non-Applicable Cells:** Left as clean BLANK cells (`None`). Writing `"Not Reported"` into Excel cells is strictly **prohibited** everywhere.
   - Purged all hardcoded `"Not Reported"` strings from extraction skills, `universal_excel_inserter.py`, and batch sheets (`70_94_109.xlsx`, `49_53_66.xlsx`).

2. **Rule 14 Enhancement: Table Layout Index Pruning (Cols 41 & 45):**
   - Leading numbers that serve solely as table row/column coordinates (e.g., `"1. "`, `"7. "`, `"10. "`) are automatically pruned from variable names.
   - The author's exact construct phrasing, sub-dimension wording (e.g., `"Internal COBSB"`, `"External COBSB"`), and published abbreviations (e.g., `"BSA"`, `"Org. Comm."`) remain 100% character-for-character preserved.
   - The original coordinate with number is permanently preserved in Col 50 Notes / `cell_proof`.

3. **Rule 19: Streamlined Extraction Layout & Exclude Termination:**
   - **Separation of Concerns:** `BSMA_Master_Coding_Sheet.xlsx` serves as the permanent screening database containing bibliographic metadata in Cols 1–16.
   - **Batch Extraction Sheets (`[start]_[end].xlsx`):**
     - `Col 3 (Sample ID)`: Left clean blank (`None`).
     - `Cols 7–16 (Article Descriptors)`: Left clean blank (`None`) to eliminate redundancy.
     - `Included Papers (1 = include)`: Data population strictly begins at **Col 17**.
     - `Excluded Papers (0 = exclude)`: Terminate immediately after **Col 6 (`Reason for Exclusion`)**, leaving all subsequent columns (Cols 7–50) clean blank (`None`).

4. **Rule 20: Canonical 3-Tier Hierarchical Header Protocol:**
   - Standardized Row 1 (Section Category), Row 2 (Sub-category), and Row 3 (Leaf Header) across all batch extraction sheets.
   - Created `.agents/scripts/excel_template_util.py` to copy merged cell ranges, fonts, fills, and dimensions via openpyxl.
   - Raw pandas `df.to_excel()` exports that inject `'Unnamed'` headers are strictly prohibited and actively caught by the linter.

5. **Rule Numbering Deduplication (Rules 21–26):**
   - Renumbered `vault_security.md` rules to Rules 21–26 to eliminate rule numbering collisions with `data_integrity.md` (Rule 14 and Rule 20).
   - Entire rule system across `.agents/rules/` now possesses 100% unique rule numbers.

