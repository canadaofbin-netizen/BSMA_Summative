### BSMA Coding Sheet Executive Summary: 49_53_66.xlsx

#### 1. Executive Summary
| Metric | Count / Status | Notes |
|---|:---:|---|
| Total Data Rows | 22 rows | Rows 4 to 25 |
| Total Effect Sizes (r) | 21 correlations | Substantive extracted pairs |
| Included Studies | 2 studies | Individual empirical BSB |
| Excluded Studies | 1 studies | Terminated per Rule 19 |
| Unique BSB Variables | 5 variables | Boundary spanning constructs |
| Unique Non-BS Variables | 8 variables | Correlated organizational constructs |
| Missing Data Protocol | PASS | Rule 1 compliant (Numeric 999 / Blank text) |
| Header Structure | PASS | Rule 20 canonical 3-tier hierarchy |
| Data Ingestion Parity | PASS | Rule 27 zero empirical data loss |

#### 2. Detailed Study-by-Study Breakdown

##### [49] Bayighomog & Araslı (2019) — 1 = Include
- **Title:** *Workplace spirituality*
- **Sample Profile:** N = 250
- **Extracted Effect Sizes:** 15 rows
- **Boundary Spanning Variables (3):**
  - `External Representation`: M = 999, SD = 999, alpha = 999 | Scale: COBSBs
  - `Internalized Influence`: M = 999, SD = 999, alpha = 999 | Scale: COBSBs
  - `Service Delivery`: M = 999, SD = 999, alpha = 999 | Scale: COBSBs
- **Non-BS Variables (5):**
  - **General Non-BS Variable:** Vision, Hope/Faith, Altruistic love, Calling, Member
- **Cartesian Pairing Structure:** 3 BSB x 5 Non-BS -> 15 rows total
- **Provenance Coordinates:** Table 2 (p. 556), Row: Altruistic love, Col: External Representation, Raw: 0.36, Table 2 (p. 556), Row: Altruistic love, Col: Internalized Influence, Raw: 0.313, Table 2 (p. 556), Row: Altruistic love, Col: Service Delivery, Raw: 0.371

##### [53] Bergami et al. (2021) — 1 = Include
- **Title:** *How and when Identification with a Boundary‐Spanning*
- **Sample Profile:** N = 1461
- **Extracted Effect Sizes:** 6 rows
- **Boundary Spanning Variables (2):**
  - `Branch identification`: M = 5.21, SD = 0.92, alpha = 0.69 | Scale: identification with the branch
  - `CS-related meetings`: M = 2.35, SD = 0.94, alpha = 0.89 | Scale: CS-related meetings between managers and colleagues
- **Non-BS Variables (3):**
  - **Control & Incentives:** Locus of control
  - **General Non-BS Variable:** CS
  - **Performance & Outcomes:** Performance control
- **Cartesian Pairing Structure:** 2 BSB x 3 Non-BS -> 6 rows total
- **Provenance Coordinates:** Table 1 (p. 671), Row: CS, Col: Branch identification, Raw: 0.06, Table 1 (p. 671), Row: CS, Col: CS-related meetings, Raw: 0.02, Table 1 (p. 671), Row: Locus of control, Col: Branch identification, Raw: -0.01

##### [66] Brion et al. (2012) — 0 = Exclude
- **Title:** *Project leaders as boundary spanners Relational antecedents and performance outcomes*
- **Exclusion Reason:** 3 = Non-individual level (team/firm/org analysis)
- **Extraction Layout:** 1 row (Terminated at Col 6 per Rule 19; Cols 7-50 clean blank)

#### 3. Cross-Study Construct Taxonomy Tree
```text
BSMA Batch Taxonomy [49_53_66.xlsx]
├── Boundary Spanning Behavior (BSB)
│   ├── Branch identification
│   ├── CS-related meetings
│   ├── External Representation
│   ├── Internalized Influence
│   ├── Service Delivery
└── Non-Boundary Spanning Correlates (Non-BS)
    ├── Control & Incentives
    │   └── Locus of control
    ├── General Non-BS Variable
    │   ├── Altruistic love
    │   ├── CS
    │   ├── Calling
    │   ├── Hope/Faith
    │   ├── Member
    │   └── Vision
    └── Performance & Outcomes
        └── Performance control
```

#### 4. Data Quality & Compliance Verification
- [x] Rule 1: Dual Missing Data Protocol strictly enforced (Numeric 999 / Text clean blank).
- [x] Rule 14: Correlation table variable names preserved character-for-character with leading layout numbers pruned.
- [x] Rule 19: Excluded papers terminate immediately after Col 6 with zero residual data pollution.
- [x] Rule 20: Canonical 3-tier header structure preserved without pandas Unnamed corruption.
- [x] Rule 27: Lossless Ingestion Parity confirmed (Zero dropped Mean, SD, or demographic metrics).