<details>
<summary><h2>Excel Data Entry Formatting Rules (Cartesian Pair Architecture)</h2></summary>

When the Python Backend (`universal_excel_inserter.py`) writes to the Excel sheet, it strictly adheres to the 23-column Cartesian Mapping Schema. The LLM does NOT format the Excel sheet directly; it merely provides the raw JSON parameters.

> [!IMPORTANT]  
> **1. The 4-Sheet Physical Isolation Rule**  
> Data pairs are not dumped into a single master sheet. They are physically routed based on methodology flags:
> - **Raw_Metrics:** Pure zero-order data.
> - **Transformed_Metrics:** Any data pair where `is_transformed = true` (e.g., Log/Z-score applied).
> - **Imputed_Metrics:** Any data pair where `is_imputed = true` (e.g., FIML used).
> - **Salami_Review_Queue:** Any data pair where `is_salami_suspect = true`.

> [!IMPORTANT]  
> **2. The 23-Column Schema (Cartesian Pair)**  
> Each row represents a mathematically generated Pair ($BS \times NB$) and consists of exactly 23 columns:
> 
> **[Meta Flags (4 Columns)]**
> - Col 1: `is_longitudinal`
> - Col 2: `is_transformed`
> - Col 3: `is_imputed`
> - Col 4: `is_salami_suspect`
> 
> **[Boundary Spanning (BS) Attributes (9 Columns)]**
> - Col 5: Items
> - Col 6: Min
> - Col 7: Max
> - Col 8: Report Type
> - Col 9: Specific Measure (Verbatim Quote)
> - Col 10: Anchor Name
> - Col 11: Mean
> - Col 12: SD
> - Col 13: Reliability (Alpha/Omega)
> 
> **[Non-Boundary (NB) Attributes (9 Columns)]**
> - Col 14: Items
> - Col 15: Min
> - Col 16: Max
> - Col 17: Report Type
> - Col 18: Specific Measure (Verbatim Quote)
> - Col 19: Anchor Name
> - Col 20: Mean
> - Col 21: SD
> - Col 22: Reliability (Alpha/Omega)
> 
> **[Effect Size (1 Column)]**
> - Col 23: Correlation (r)

> [!WARNING]
> **Strict Pruning Rules (Zero Guesswork & Cost Saving)**
> 1. **Demographics Dropped:** Age, Gender, Tenure, Education, and Firm Size are completely DROPPED from the extraction pipeline. Do NOT extract them. Do NOT use the old `999` placeholder rule for demographics. Simply ignore them to save LLM tokens.
> 2. **Formative/Objective Exception:** If an objective variable happens to remain, its reliability type MUST be set to `Not_Applicable` and its value to `999`. Do not hallucinate Alpha scores.
> 3. **Missing Numeric Values:** If any valid variable is missing a statistic (e.g., SD is omitted), the LLM must strictly output the integer `999`.

</details>
