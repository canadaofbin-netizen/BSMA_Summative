<details>
<summary><h2>Automated Extraction Features (Shadow Reports Workflow)</h2></summary>

To ensure the highest level of accuracy while keeping the official Excel sheet in the conventional format, all AI coding assistants must follow a strict **Three-Step Workflow**:

**Step 0: Inclusion/Exclusion Triage (Absolute Priority 1)**
Before reading correlation tables or extracting metadata, the AI MUST first evaluate the paper's abstract and methodology against the Inclusion/Exclusion criteria.
Specifically, check if the sample involves **individual-level** boundary spanning. If the boundary spanner is a team, organization, or firm, the paper violates the level-of-analysis.
- If the paper violates any exclusion rule (e.g. non-empirical, Team-Level, qualitative, wrong variables), the AI MUST:
  1. Immediately **HALT** any further data extraction (do not look for N, Mean, SD, or correlations).
  2. Generate a 1-row Shadow Report detailing only the `Effect Size ID`, `Inclusion-Exclusion Judgment` (`0 = Exclude`), and the specific `Reason for Exclusion`.
  3. Declare the paper complete and move to the next paper.
- Only papers marked `1 = Include` will proceed to Step 1.

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

**Step 1.5: Subagent Delegation for Measure Descriptors**
Because correlation matrices often contain dozens of Non-Boundary-Spanning variables, manually scanning the text for their specific Measure Descriptors (Items, Min, Max, Report Type, Source) is highly error-prone and can overwhelm the main Orchestrator's context window.
- The Orchestrator AI MUST deploy dedicated **Subagents** (e.g., `research` subagents) to parallelize the extraction of these granular details from the "Measures" section of the paper.
- Provide the Subagent with the specific list of variables found in the correlation matrix, and instruct them to return a structured JSON mapping of the descriptors.
- The Orchestrator MUST wait for the Subagents to return this JSON mapping before proceeding to Excel Injection.

**Step 1.8: Validator Review (Self-Correction Loop)**
Before proceeding to Excel Injection, the Orchestrator MUST deploy a `validator` subagent (or self-validate stringently using the validator skill prompt).
- The Validator must review the Shadow Report to ensure no non-focal variables, team-level samples, or hallucinations are present.
- If the Validator returns `REJECT`, the Orchestrator must fix the Shadow Report.
- Only if the Validator returns `PASS`, proceed to Step 2.

**Step 2: Code the Conventional Excel Sheet**
Once the logic is established in the metadata report, the AI will use those findings to accurately code the paper into the official `BSMA_Master_Coding_Sheet.xlsx`. 

<details>
<summary>Click to view Step 2 rules</summary>

**Step 2: Excel Injection**
1. Read the parsed tables and metadata report.
2. Carefully format the values as per `08_data_entry_formatting.md`.
3. Write the rows to `BSMA_Master_Coding_Sheet.xlsx`.
</details>

**Step 3: Self-Verification Loop (Double-Check All Numeric Entries)**
Before declaring any paper's extraction complete, you MUST dump and review the exact inserted rows using Python. 
- **Double-Check All Numeric Entries:** Pay special attention to Means, SDs, Reliability (Alphas), and Effect Sizes. These are the lifeblood of the meta-analysis. 
- **No Mental Conversions:** You must ensure that every number exactly matches the paper's table character-for-character. Do **NOT** perform mental conversions (e.g., transforming `.43` to `43` for percentages). Loop and fix any discrepancies until the extraction is 100% flawless.

**Step 4: GitHub Synchronization**
After the extraction is complete and verified in Step 3, the Orchestrator AI MUST automatically commit and push the updated `BSMA_Master_Coding_Sheet.xlsx` and any new Shadow Reports to the GitHub repository.
- Run `git add .`
- Run `git commit -m "Auto-backup: Extracted data for [Paper Author Year]"`
- Run `git push`
This ensures the remote repository is always perfectly synchronized with the local progress.

</details>
