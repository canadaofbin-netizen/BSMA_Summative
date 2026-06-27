## Automated Extraction Features (Shadow Reports Workflow)
To ensure the highest level of accuracy while keeping the official Excel sheet in the conventional format, all AI coding assistants must follow a strict **Two-Step Workflow**:

**Step 1: Generate an Enhanced Metadata Report**
Before modifying the Excel sheet, the AI must create a private markdown report (e.g., `BSMA0001_Metadata.md`) in the `03_Shadow_Reports` folder. This report is for the coder's eyes only and must extract the following 5 features to map out the study's logic:
1. **Data Structure Type**: (e.g., `Single-source`, `Dyadic`, `Triadic`). *Note: Categories are dynamic. If a new structure is found, create a new category.*
2. **Explicit Anchor Identity**: (e.g., `Leader`, `Public Manager`). This explicitly identifies the boundary spanner to determine "Self vs. Other" rules.
3. **Specific Rater Identity**: (e.g., `Self`, `Subordinate`, `Supervisor`). Avoid using the vague "3 = Others" whenever possible to prevent perspective confusion.
4. **Construct Role in Model**: (e.g., `Antecedent`, `Outcome`, `Mediator`, `Moderator`, `Control`).
5. **Pairwise Sample Size (Pairwise N)**: To capture correlation-specific sample sizes resulting from missing data.

> [!WARNING]  
> **The `[UNRECOGNIZED PARADIGM]` Flag**  
> If you encounter a study design or variable mapping that fundamentally contradicts or confuses the current rules (e.g., a paper with Dual-Anchors where both Leader and Subordinate are boundary spanners), you MUST **HALT** coding immediately. Append an `[UNRECOGNIZED PARADIGM]` flag to the Shadow Report, summarize the conflict, and explicitly ask the user for a ruling before touching the Excel sheet. Once the user provides a ruling, update `read.md` with the new Special Case so the AI learns from it.

**Step 2: Code the Conventional Excel Sheet**
Once the logic is established in the metadata report, the AI will use those findings to accurately code the paper into the official `BSMA_Actual Coding Sheet_v2.xlsx` using the conventional format expected by the project supervisor (without appending extra columns).
