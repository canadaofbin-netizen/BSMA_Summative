<details>
<summary><h2>Special Cases: Author Discrepancies and Errors</h2></summary>

When coding academic papers, authors may make typos or contradict themselves between their written text and their data tables.

> [!IMPORTANT]  
> **Rule 04A: Table Over Text Rule**  
> If an AI coder detects a discrepancy between the body text of a paper and its data tables (e.g., the text claims '13 items' but the table explicitly lists '14 items'), the AI must **always prioritize the Table as the source of truth.**

> [!WARNING]
> **Rule 04B: No Arbitrary Data Conversions (Anti-Inference)**
> Never attempt to "fix" author errors by applying unprompted mathematical conversions. For example, if the paper text states "average tenure is 20 months" but the table mistakenly lists Mean=2.83 and SD=18.77, you must follow the Table Over Text rule and extract 2.83. Do **NOT** assume the table swapped Mean/SD and do **NOT** divide 18.77 by 12 to artificially generate "1.56 years". Extract the exact numbers provided.

> [!WARNING]
> **Rule 04C: Zero Guesswork Policy (Flagging)**
> When in doubt, do **NOT** guess. If an author writes contradictory scale descriptors (e.g., "Items were on a seven-point Likert scale ranging from 1... to 5"), do not act as a detective to deduce the true scale (even if you can prove it mathematically via the Mean). 
> - **Action:** Leave the value as `999` (or blank if permitted by rules).
> - **Documentation:** Write exactly what the text says in the Notes column (e.g., `Text claims 7-point scale but ranges 1 to 5.`).
> - **Flagging:** Append a `[FLAGGED]` tag to the Notes column and the Shadow Report, and request a human ruling. Do not make assumptions.

> [!TIP]
> **Rule 04D: R-squared Extraction (Simple Regressions)**
> While extracting from correlation matrices is the priority, if a paper lacks a formal correlation matrix but reports the $R^2$ value for a *simple* linear regression (one predictor, zero control variables), you MUST extract the zero-order correlation using the formula $r = \sqrt{R^2}$. Do not erroneously exclude the paper for lacking a matrix if this data is present.

</details>
