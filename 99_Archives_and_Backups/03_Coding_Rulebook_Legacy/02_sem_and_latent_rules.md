<details>
<summary><h2>Special Cases: Misleading Correlation Tables (SEM)</h2></summary>

## 2.1 The "Latent Correlation" Strict Ban
You are strictly forbidden from extracting latent correlations. If a table explicitly states "latent construct intercorrelations" AND completely lacks Means/SDs, it must be rejected (return `999`). 
**GUARDRAIL:** Do NOT reject a paper simply because it uses SEM or the word "Construct". If there is a standard "Means, Standard Deviations, and Correlations" table, this is the raw zero-order matrix we need. You MUST ONLY extract from this table.

> [!WARNING]  
> **Squared and Latent Correlations**  
> Be warned: the "correlation values" in Discriminant Validity tables are almost always **Squared Latent Correlations**, NOT raw observed Pearson correlations ($r$). Furthermore, tables explicitly labeled "Latent Variable Correlations" must also be ignored. 
> 
> If a paper completely omits the raw, uncorrected Pearson $r$ matrix and only provides latent or squared latent correlations, you MUST NOT code those values. You must enter `999` (missing) for the effect sizes.

</details>
