# BSMA Archive

> [!IMPORTANT]  
> **AI SYSTEM GUIDELINE**  
> This document serves as the absolute instruction manual and guideline for any AI assistant or coding agent extracting data from academic papers for this meta-analysis project. You must strictly follow all rules, workflows, and extraction protocols defined herein.

This folder contains archived documents and resources for the **Boundary Spanning Meta-Analysis (BSMA)** project, specifically focusing on the actual coding phase.

<details>
<summary><h2>Folder Contents</h2></summary>

- **BSMA_Actual Coding Sheet_v2.gsheet / .xlsx**: The actual coding spreadsheet where data from various articles is recorded.
- **Coding manual for students.docx / .pdf**: The Actual Coding Manual providing instructions on how to code articles.
- **png of coding sheet.png**: A screenshot visually demonstrating the layout of the coding spreadsheet.
- **05_Coding_Rulebook**: A modular directory containing the explicit coding rules and workflows.

</details>

<details>
<summary><h2>Modular Coding Rulebook</h2></summary>

To prevent this document from becoming bloated, all coding rules, paradigms, and edge-case handlers have been split into the `05_Coding_Rulebook` directory. 

Whenever you encounter a specific study design or paradigm, you **MUST** consult the corresponding rule module below:

- [00_core_process.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/00_core_process.md): The basic coding process overview and variable mapping rules.
- [01_dyadic_data_rules.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/01_dyadic_data_rules.md): Rules for Dyadic Data (Anchor Identification, Report Type flip, filtering demographics).
- [02_sem_and_latent_rules.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/02_sem_and_latent_rules.md): Warnings regarding Discriminant Validity tables and entering `999` for missing Pearson *r*.
- [03_automated_workflow.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/03_automated_workflow.md): The mandatory Two-Step Shadow Reports Workflow and the `[UNRECOGNIZED PARADIGM]` flag.
- [04_general_exceptions.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/04_general_exceptions.md): The Table Over Text rule for resolving author discrepancies.
- [05_document_management.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/05_document_management.md): Rules for updating and backing up this rulebook system.
- [06_non_individual_anchors.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/06_non_individual_anchors.md): Rules for bypassing demographics when the Anchor is a Firm or Team.
- [07_scale_oddities.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/05_Coding_Rulebook/07_scale_oddities.md): Rules for bypassing Items and Alphas for dummy and proxy variables.

</details>

<details>
<summary><h2>Error Tracking & Lessons Learned</h2></summary>

To ensure we don't repeat past mistakes, all extraction errors and their root causes are documented here:
- [extraction_errors_report.md](file:///g:/My%20Drive/UCL/BSMA/BSMA%20ANTIGRAVITY/extraction_errors_report.md): A living log of flawed analyses and missing data incidents.

</details>

> [!WARNING]  
> **Unrecognized Paradigms**  
> If you encounter a paradigm that is not covered by any of these modules, halt coding and ask the user. Once a ruling is made, create a new rule module (e.g., `06_new_rule.md`) and link it in this index.
