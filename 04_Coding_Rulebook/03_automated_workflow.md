<details>
<summary><h2>Automated Extraction Features (Two-Step Workflow)</h2></summary>

To ensure the highest level of accuracy and speed, all AI coding assistants must follow a strict **Two-Step Workflow**:

**Step 1: Triage & Measure Extraction**
- **Objective:** Evaluate if the paper should be included or excluded, and extract empirical variables.
- **Triage Action:** Before extracting any numerical data, evaluate the paper's abstract and methodology against the Inclusion/Exclusion criteria. If the boundary spanner is a team, organization, or firm, or if the paper is not empirical, it must be EXCLUDED.
  - If EXCLUDED: Immediately halt numerical extraction. Set `inclusion_status` to 0 and log the exclusion reason in the JSON schema.
- **Extraction Action:** If INCLUDED, deploy subagents to extract the items, alphas, N, Means, SDs, and Pearson correlations (r) for the focal boundary spanning construct and all paired variables. 
  - Subagents must rigorously enforce the Zero-Order Lock (no betas), Dyadic Data rules (Focal Employee only), and Dummy Variable Alpha exceptions.
  - Compile the extracted data into a structured M:N JSON payload.

**Step 2: Excel Injection**
- **Objective:** Inject the extracted JSON payload directly into the Master Excel sheet.
- **Action:** The master orchestrator MUST execute the python script `universal_excel_inserter.py` to securely write the data into the `BSMA_Master_Coding_Sheet.xlsx` file, bypassing human formatting errors and automatically allocating sample numbers.

**Step 3: Self-Verification Loop**
Before declaring any paper's extraction complete, you MUST dump and review the exact inserted rows using Python. 
- **Double-Check All Numeric Entries:** Pay special attention to Means, SDs, Reliability (Alphas), and Effect Sizes. 
- **No Mental Conversions:** You must ensure that every number exactly matches the paper's table character-for-character. Loop and fix any discrepancies until the extraction is 100% flawless.

**Step 4: GitHub Synchronization**
After the extraction is complete and verified in Step 3, the Orchestrator AI MUST automatically commit and push the updated `BSMA_Master_Coding_Sheet.xlsx` to the GitHub repository.
- Run `git add .`
- Run `git commit -m "Auto-backup: Extracted data for [Paper Author Year]"`
- Run `git push`

</details>
