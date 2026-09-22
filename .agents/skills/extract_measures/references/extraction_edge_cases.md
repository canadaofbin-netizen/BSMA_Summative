# Extraction Edge Cases & Measurement Traps Reference

> **Note:** This document serves as the authoritative on-demand reference for statistical, measurement, and matrix edge cases during data extraction. 하위 에이전트(Node 3 및 Node 4)는 본 문서의 판별 기준과 트랩 방어 규칙을 반드시 준수해야 합니다.

---

## 1. Trap Warning Quick-Reference Index

| Trap Name | Category | Risk / Symptom | Mandatory Action |
|---|---|---|---|
| **Diagonal AVE Trap** | Matrix Diagonal | Diagonal contains numbers like `(0.84)` representing square root of AVE, not 1.00 | Do NOT extract diagonal values as correlations. Verify lower diagonal for raw $r$. |
| **Upper vs. Lower Matrix Trap** | Matrix Asymmetry | Upper diagonal contains latent CFA correlations or $p$-values; lower diagonal contains zero-order $r$ | Extract ONLY zero-order Pearson $r$ (usually lower diagonal). Check table footnote. |
| **Listwise vs. Pairwise N Trap** | Sample Size | Abstract states $N=350$, but table note states "Listwise $N=312$" or "$N=300-345$" | Table listwise $N$ takes absolute precedence. If range, use conservative listwise minimum. |
| **Reliability Polymorphism** | Reliability | Reporting CR ($\rho_c$) or $\omega$ instead of Cronbach's $\alpha$ | Record exact type in `reliability.type` (`Alpha`, `CR`, `Omega`, `Not_Reported`). Never guess. |
| **Demographic & Objective Controls** | Non-BS Classification | Employee Tenure, Age, Gender, Education, Firm Size in correlation matrix | Extract ALL paired variables as Non-BS (NB) constructs (Rule 28). For single-item/objective controls, set items to 1 and reliability to Not_Applicable (999). |
| **Global vs. Sub-facet Redundancy** | Construct Independence | Table reports both "COBSB Total" and "Service Delivery, External Representation" | Extract sub-facets ONLY. If Global must be extracted, label Col 50 with `"Global composite score"`. |
| **Reverse-Coded Scale Distortion** | Scale Direction | Negative correlation due to reversed scale item without textual mention | Rely on raw correlation sign reported in table. Do NOT invert signs post-hoc. |
| **Scanned/Landscape OCR Warp** | Layout / OCR | Table printed landscape or image scanned (column alignment shifted) | Use PyMuPDF zoom/rotation or bounding-box slicing to inspect raw pixel text directly. |

---

## 2. Detailed Edge Case Explanations

### Trap 1: Upper vs. Lower Diagonal & Latent Matrix Traps
- **Pattern:** Many SEM/PLS papers report a correlation table where:
  - The diagonal elements are not `1.00` or `-`, but values in parentheses such as `(0.85)` representing the **square root of the Average Variance Extracted (AVE)** for discriminant validity (Fornell-Larcker criterion).
  - The **lower off-diagonal** represents raw zero-order Pearson correlations between observed/composite variables.
  - The **upper off-diagonal** represents latent construct correlations from a measurement model (CFA) or structural equation model (SEM).
- **Mandatory Guardrail:**
  1. Always inspect the table notes: *"Note: Diagonal elements (in bold/parentheses) are the square root of AVE; below diagonal are correlations."*
  2. Extract from the **lower diagonal** when raw correlations are present.
  3. If the paper ONLY provides latent correlations (no raw matrix), extract them but explicitly flag `"Based on latent variables"` in the notes.
  4. NEVER extract AVE square roots as correlation coefficients.

### Trap 2: Matrix-Specific Listwise $N$ Guardrail
- **Pattern:** The abstract or sample section states: *"A total of 400 questionnaires were distributed and 280 usable responses were obtained ($N=280$)."* However, due to item non-response, the correlation matrix footnote states: *"Listwise $N = 254$."* or *"Pairwise $N$ ranges from 240 to 275."*
- **Mandatory Guardrail:**
  1. The effective sample size for the effect size is the matrix-specific $N$.
  2. The table footnote's listwise $N$ ($N=254$) **takes absolute precedence** over the text's sample description ($N=280$).
  3. If only a pairwise range is provided (e.g., $240-275$), code the conservative minimum ($N=240$) and document the range in Col 50 Notes.

### Trap 3: Sub-dimension Mapping vs. Global Composite
- **Pattern:** The text describes the focal BSB construct using a global label (e.g., *"Customer-oriented boundary-spanning behavior (COBSB) was measured with 13 items from Bettencourt et al. (2005)"*), but Table 1 lists three separate sub-scales: *"1. External Representation"*, *"2. Internal Influence"*, *"3. Service Delivery"*.
- **Mandatory Guardrail:**
  1. Do NOT blindly assign 13 items and the global $\alpha$ to all three sub-dimensions.
  2. Decompose the items based on the text (e.g., External Representation: 5 items; Internal Influence: 4 items; Service Delivery: 4 items).
  3. If the text does NOT report decomposed item counts or reliabilities for each sub-dimension, enforce the **Dual Missing Data Protocol (`999`)**.

### Trap 4: Demographic and Objective Control Variables (Mandatory Lossless Extraction)
- **Pattern:** Correlation matrices frequently include control and demographic variables such as Age, Gender, Organizational Tenure, Education, Experience, and Firm Size.
- **Mandatory Guardrail (Rule 27 & Rule 28 Integration):**
  1. **Zero Dropping Policy:** Do NOT drop demographic or control variables. Every variable reported in the correlation matrix that pairs with BSB MUST be losslessly extracted as a substantive Non-BS (`NB`) variable in Col 45.
  2. **Formative / Single-Item Metrics:** For single-item demographic or objective metrics (e.g., Age in years, Gender dummy, Tenure in years, Firm Size), set `number_of_items = 1`, `min_score = 999`, `max_score = 999`, `report_type = "4 = Objective"` (or `"1 = Self-report"`), and `reliability = {"type": "Not_Applicable", "value": 999}`.

---

## 3. Few-Shot Matrix Extraction Examples

### Example 1: Matrix with AVE on Diagonal & Asterisks
```
Table 2. Descriptive Statistics and Correlations (N = 253)
Variables                   Mean   SD     1        2        3
1. External Communication   4.12  0.65  (0.81)
2. Intra-unit Comm.         3.85  0.72   0.34**  (0.79)
3. Job Performance          4.05  0.58   0.28*    0.41**  (0.85)
Note: Values in parentheses on the diagonal are square roots of AVE. * p < .05, ** p < .01.
```
- **Node 3 CoT Reasoning:**
  - Diagonal values `(0.81)`, `(0.79)`, `(0.85)` are square roots of AVE, not correlations.
  - Lower triangle contains raw Pearson zero-order correlations.
  - Significance asterisks must be stripped: `0.34**` -> `0.34`, `0.28*` -> `0.28`.
- **Node 3 Output Fragment (Rule 28 Two-Step BSB Integration):**
  *(Note: Per Rule 28, 'Intra-unit Comm.' is an internal dissemination BSB sub-dimension, so both BSB variables pair with 'Job Performance')*
  ```json
  {
    "correlations": [
      {
        "var1_anchor": "External Communication",
        "var2_anchor": "Job Performance",
        "r": 0.28,
        "cell_proof": {
          "row_header_quote": "3. Job Performance",
          "col_header_quote": "1. External Communication",
          "raw_cell_value": "0.28*"
        }
      },
      {
        "var1_anchor": "Intra-unit Comm.",
        "var2_anchor": "Job Performance",
        "r": 0.41,
        "cell_proof": {
          "row_header_quote": "3. Job Performance",
          "col_header_quote": "2. Intra-unit Comm.",
          "raw_cell_value": "0.41**"
        }
      }
    ]
  }
  ```

### Example 2: Sub-scale Text Decomposition (Node 4)
- **Text:** *"Boundary-spanning behavior was assessed using the 13-item scale developed by Bettencourt and Brown (2003), comprising external representation (5 items, alpha = .88), internal influence (4 items, alpha = .82), and service delivery (4 items, alpha = .85)."*
- **Node 4 Output Fragment:**
  ```json
  {
    "measure_details": [
      {
        "table_anchor_name": "External Representation",
        "classification_type": "BS",
        "items": 5,
        "items_quote": "external representation (5 items, alpha = .88)",
        "min": 1,
        "max": 7,
        "reliability": {"type": "Alpha", "value": 0.88},
        "specific_measure": "external representation",
        "source_quote": "Boundary-spanning behavior was assessed using the 13-item scale developed by Bettencourt and Brown (2003), comprising external representation (5 items, alpha = .88)..."
      }
    ]
  }
  ```
