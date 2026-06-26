<details>
<summary><h2>Excel Data Entry Formatting Rules</h2></summary>

When executing Step 2 of the workflow (Writing to the `BSMA_Master_Coding_Sheet.xlsx`), you must strictly adhere to the following formatting and sequencing rules for the first 4 columns and row spacing.

> [!IMPORTANT]  
> **1. Blank Row Separation Rule**  
> When appending a new paper to the Excel sheet, you MUST leave exactly **one completely blank row** between the last data row of the previous paper and the first data row of the new paper. For example, if Paper A ends on row 6, Paper B must begin on row 8. 

> [!IMPORTANT]  
> **2. Identifier Patterns (Cols 1-4)**  
> - **Col 1 (Coder Initials):** Always hardcode `KY` for every extracted row.
> - **Col 2 (Article ID):** Must follow a strict chronological sequence based on the Excel sheet history (e.g., `BSMA0001` -> `BSMA0002` -> `BSMA0003`). Completely ignore the numbering in the PDF filename.
> - **Col 3 (Sample ID):** Must append the sample number to the Article ID. Format: `[Article ID].[Sample Number]`. Example: `BSMA0002.1`.
> - **Col 4 (Effect Size ID):** Must append a chronological extraction number to the Sample ID. Format: `[Sample ID].[Effect Number]`. Example: `BSMA0002.1.1`, `BSMA0002.1.2`, `BSMA0002.1.3`.
> - **Col 5 (Inclusion-Exclusion Judgment):** Since we are actively extracting effect sizes, this must always be hardcoded as `1 = Include` for every extracted row.
> - **Col 12 (Publication Type), Col 17 (Study Design), Col 21 (International Context) & Col 26 (Occupation Type):** Categorical variables MUST NOT be left blank. You must write out the full text label alongside the index number (e.g., `1 = Journal article`, `1 = No (domestic only)`). For **Col 26**, write a descriptive text of the occupation (e.g., `employees from IT companies` or `public sector managers`). Do not leave it blank.
> - **Measure Descriptors (Min Score, Max Score, Report Type, Specific Measure):** These columns MUST NOT be left blank.
>   - **Report Type Strict Classification:** `1 = Self`, `2 = Supervisor` (leaders, formal supervisors), `3 = Others` (coworkers, peers, external stakeholders). Do NOT use `3` as a catch-all.
>   - **Specific Measure Used:** You MUST copy and paste the relevant description sentence EXACTLY as it appears in the paper (e.g., "Four items were used from Williams and Anderson's (1991) original scale..."). Do not merely summarize or list citations.
>   - If demographic information is truly unavailable or inapplicable, hardcode them as `999`.

## Demographic Extraction Rules

> [!TIP]
> **Simplified Measure Descriptors (999)**
> For any demographic or objective variable (e.g., Age, Gender, Education, Tenure, Firm Size, Firm Age), you MUST hardcode the following three Measure Descriptors as `999`:
> - Number of Items
> - Minimum Possible Score
> - Maximum Possible Score
> This saves time as these objective variables do not possess true psychometric scale properties.

> [!WARNING]
> **Strict Tenure Rules (No Conversions)**
> - **No Unit Conversion:** Never attempt to convert tenure values from months to years (e.g., dividing by 12). Extract and enter the exact numerical value reported in the paper.
> - **Log the Unit:** You MUST explicitly note the unit of measurement in **Col 16 (Notes)** (e.g., "Organizational tenure reported in months" or "Organizational tenure reported in years").
> - **Org vs. Team Tenure:** Organizational tenure and team/role tenure are distinct concepts. Ensure you are extracting *Organizational Tenure* for `Col 25 (Org Tenure)`. If the paper only reports Team Tenure, do not forcefully map it into `Col 25`. Leave Col 25 blank or mark it as `999` and treat Team Tenure as a separate correlate if necessary.

## Study Design Rules

> [!TIP]
> **Longitudinal / Time-Lagged Criteria**
> When determining `Col 17 (Study Design)` as longitudinal/time-lagged, the only thing that matters is whether there is a time gap between the measurement of boundary spanning and the measurement of the other focal variable (antecedent or outcome) it is paired with. It does **NOT** matter if boundary spanning itself was measured repeatedly over time. Focus exclusively on the measurement time gap between the two paired variables.

</details>
