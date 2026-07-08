<details>
<summary><h2>Exclusion Rule: Non-Individual Anchors</h2></summary>

According to the master Inclusion-Exclusion criteria, the boundary spanning behavior must be measured at the **Individual-level**. ONLY Individual-level passes. Any study where the boundary-spanning entity is NOT an individual person (e.g., a team, unit, department, organization, or firm) MUST be excluded.

> [!CAUTION]
> **Individual-Level ONLY Rule**  
> Mixing non-individual-level boundary spanning with individual-level boundary spanning violates the level-of-analysis boundaries of this project. The meta-analysis focuses EXCLUSIVELY on individual-level boundary spanning.
> 
> **NOTE:** The focal boundary spanner CAN be a Leader/Manager. Whoever performs the boundary spanning IS the focal employee regardless of job title. (See Casebook Precedent #001.)
> 
> **Action:** If the boundary spanning construct is measured at a non-individual level (Team, Unit, Department, Organization, Firm, etc.), the paper MUST be excluded. You must **ABORT extraction immediately**. Set `inclusion_status` to 0 and `exclusion_reason` in the JSON, then inject into Excel via `universal_excel_inserter.py`.

</details>
