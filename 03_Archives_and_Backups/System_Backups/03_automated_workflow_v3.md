<details>
<summary><h2>Automated Extraction Features (Shadow Reports Workflow)</h2></summary>

To ensure the highest level of accuracy while keeping the official Excel sheet in the conventional format, all AI coding assistants must follow a strict **Two-Step Workflow**:

**Step 1: Generate an Enhanced Metadata Report**
Before modifying the Excel sheet, the AI must create a private markdown report (e.g., `BSMA0001_Metadata.md`) in the `03_Shadow_Reports` folder. This report is for the coder's eyes only and must extract the following 5 features to map out the study's logic:
1. **Data Structure Type**: (e.g., `Single-source`, `Dyadic`, `Triadic`). *Note: Categories are dynamic. If a new structure is found, create a new category.*
2. **Explicit Anchor Identity**: (e.g., `Leader`, `Public Manager`). This explicitly identifies the boundary spanner to determine "Self vs. Other" rules.
3. **Specific Rater Identity**: (e.g., `Self`, `Subordinate`, `Supervisor`). Avoid using the vague "3 = Others" whenever possible to prevent perspective confusion.
4. **Construct Role in Model**: (e.g., `Antecedent`, `Outcome`, `Mediator`, `Moderator`, `Control`).
5. **Pairwise Sample Size (Pairwise N)**: To capture correlation-specific sample sizes resulting from missing data.
6. **Ambiguities & Discrepancies Log**: An explicit log of any mathematical contradictions, text typos, or edge cases found in the paper, along with a justification of how they were resolved using the Rulebook (e.g., applying Rule 04B or 04C).

> [!WARNING]  
> **The `[UNRECOGNIZED PARADIGM]` Flag**  
> If you encounter a study design or variable mapping that fundamentally contradicts or confuses the current rules (e.g., a paper with Dual-Anchors where both Leader and Subordinate are boundary spanners), you MUST **HALT** coding immediately. Append an `[UNRECOGNIZED PARADIGM]` flag to the Shadow Report, summarize the conflict, and explicitly ask the user for a ruling before touching the Excel sheet. Once the user provides a ruling, update `read.md` with the new Special Case so the AI learns from it.

**Step 2: Code the Conventional Excel Sheet**
Once the logic is established in the metadata report, the AI will use those findings to accurately code the paper into the official `BSMA_Actual Coding Sheet_v2.xlsx`. 
You MUST strictly adhere to the formatting, ID naming, and blank row rules defined in `08_data_entry_formatting.md` when writing to the spreadsheet.

**Step 3: Self-Verification Loop (Double-Check All Numeric Entries)**
Before declaring any paper's extraction complete, you MUST dump and review the exact inserted rows using Python. 
- **Double-Check All Numeric Entries:** Pay special attention to Means, SDs, Reliability (Alphas), and Effect Sizes. These are the lifeblood of the meta-analysis. 
- **No Mental Conversions:** You must ensure that every number exactly matches the paper's table character-for-character. Do **NOT** perform mental conversions (e.g., transforming `.43` to `43` for percentages). Loop and fix any discrepancies until the extraction is 100% flawless.

</details>
