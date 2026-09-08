### BSMA Coding Sheet Executive Summary: 70_94_109.xlsx

#### 1. Executive Summary
| Metric | Count / Status | Notes |
|---|:---:|---|
| Total Data Rows | 40 rows | Rows 4 to 43 |
| Total Effect Sizes (r) | 39 correlations | Substantive extracted pairs |
| Included Studies | 2 studies | Individual empirical BSB |
| Excluded Studies | 1 studies | Terminated per Rule 19 |
| Unique BSB Variables | 5 variables | Boundary spanning constructs |
| Unique Non-BS Variables | 18 variables | Correlated organizational constructs |
| Missing Data Protocol | PASS | Rule 1 compliant (Numeric 999 / Blank text) |
| Header Structure | PASS | Rule 20 canonical 3-tier hierarchy |
| Data Ingestion Parity | PASS | Rule 27 zero empirical data loss |

#### 2. Detailed Study-by-Study Breakdown

##### [70] Sexton (1995) — 1 = Include
- **Title:** *Dual commitment and boundary spanning activity of R&D professionals*
- **Sample Profile:** N = 253, Mean Age = 38.65, Tenure = 0.62 yrs, Role = R&D technical professionals
- **Extracted Effect Sizes:** 27 rows
- **Boundary Spanning Variables (2):**
  - `BSA`: M = 50.51, SD = 21.54, alpha = 999 | Scale: boundary spanning score
  - `External Com.`: M = 0.19, SD = 0.12, alpha = 999 | Scale: Extraunit communication frequency
- **Non-BS Variables (14):**
  - **Attitudes & Commitment:** Org. Comm., Prof. Comm., Dual Comm.
  - **Context & Organization:** Org. Size, Industry, Complexity, Uncertainty, Interdepend.
  - **Control & Incentives:** Prof. Control, Prof. Incent.
  - **Individual & Demographics:** Status, Degree, Occupation
  - **Internal Group Dynamics:** Internal Com.
- **Cartesian Pairing Structure:** 2 BSB x 14 Non-BS -> 27 rows total
- **Provenance Coordinates:** Table 3.9 (p. 65), Row: 10. Org. Comm., Col: 1, Raw: .18**, Table 3.9 (p. 65), Row: 10. Org. Comm., Col: 3, Raw: .09, Table 3.9 (p. 65), Row: 11. Prof. Comm., Col: 1, Raw: .01

##### [94] Chien et al. (2021) — 1 = Include
- **Title:** *Hotel frontline service employees’ creativity and customer-oriented boundary-spanning*
- **Sample Profile:** N = 382, Female = 65.2%, Role = Hotel frontline service employees
- **Extracted Effect Sizes:** 12 rows
- **Boundary Spanning Variables (3):**
  - `External Representation`: M = 5.46, SD = 0.8, alpha = 0.871 | Scale: Bettencourt et al. (2005)
  - `Internal Influence`: M = 5.63, SD = 0.88, alpha = 0.872 | Scale: Bettencourt et al. (2005)
  - `Service Delivery`: M = 5.81, SD = 0.81, alpha = 0.876 | Scale: Bettencourt et al. (2005)
- **Non-BS Variables (4):**
  - **Individual & Demographics:** Proactive Personality
  - **Performance & Outcomes:** Employee Creativity
  - **Role Stress:** Role Conflict, Role Ambiguity
- **Cartesian Pairing Structure:** 3 BSB x 4 Non-BS -> 12 rows total
- **Provenance Coordinates:** Table 2 (p. 28), Row: ER, Col: EC, Raw: 0.476**, Table 2 (p. 28), Row: ER, Col: PP, Raw: 0.083, Table 2 (p. 28), Row: ER, Col: RA, Raw: − 0.391**

##### [109] Cummings (2004) — 0 = Exclude
- **Title:** *Work Groups, Structural Diversity, and Knowledge Sharing in a Global Organization*
- **Exclusion Reason:** 3 = Non-individual level (team/firm/org analysis)
- **Extraction Layout:** 1 row (Terminated at Col 6 per Rule 19; Cols 7-50 clean blank)

#### 3. Cross-Study Construct Taxonomy Tree
```text
BSMA Batch Taxonomy [70_94_109.xlsx]
├── Boundary Spanning Behavior (BSB)
│   ├── BSA
│   ├── External Com.
│   ├── External Representation
│   ├── Internal Influence
│   ├── Service Delivery
└── Non-Boundary Spanning Correlates (Non-BS)
    ├── Attitudes & Commitment
    │   ├── Dual Comm.
    │   ├── Org. Comm.
    │   └── Prof. Comm.
    ├── Context & Organization
    │   ├── Complexity
    │   ├── Industry
    │   ├── Interdepend.
    │   ├── Org. Size
    │   └── Uncertainty
    ├── Control & Incentives
    │   ├── Prof. Control
    │   └── Prof. Incent.
    ├── Individual & Demographics
    │   ├── Degree
    │   ├── Occupation
    │   ├── Proactive Personality
    │   └── Status
    ├── Internal Group Dynamics
    │   └── Internal Com.
    ├── Performance & Outcomes
    │   └── Employee Creativity
    └── Role Stress
        ├── Role Ambiguity
        └── Role Conflict
```

#### 4. Data Quality & Compliance Verification
- [x] Rule 1: Dual Missing Data Protocol strictly enforced (Numeric 999 / Text clean blank).
- [x] Rule 14: Correlation table variable names preserved character-for-character with leading layout numbers pruned.
- [x] Rule 19: Excluded papers terminate immediately after Col 6 with zero residual data pollution.
- [x] Rule 20: Canonical 3-tier header structure preserved without pandas Unnamed corruption.
- [x] Rule 27: Lossless Ingestion Parity confirmed (Zero dropped Mean, SD, or demographic metrics).