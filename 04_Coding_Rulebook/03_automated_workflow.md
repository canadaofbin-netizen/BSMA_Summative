<details>
<summary><h2>Automated Extraction Features (Two-Step Workflow)</h2></summary>

To ensure the highest level of accuracy and speed, all AI coding assistants must follow a strict **Two-Step Workflow**:

**Step 0: Pre-Triage — Read Casebook**
- **Objective:** Before making any inclusion/exclusion decision, the agent MUST read `.agents/skills/batch_processor/triage_casebook.md` in full. Apply established precedents to the current paper.

**Step 1: Triage & Measure Extraction**
- **Objective:** Evaluate if the paper should be included or excluded, and extract empirical variables.
- **Triage Criteria (Exclusion):**
  1. Not empirical (e.g. theoretical, review, conceptual).
  2. The boundary spanning behavior is NOT measured at the **Individual-level**. ONLY Individual-level passes. Any non-individual unit of analysis (Team, Unit, Department, Organization, Firm, etc.) → EXCLUDE. (See Casebook Precedent #002.)
  - NOTE: The focal boundary spanner CAN be a Leader/Manager. Whoever performs the boundary spanning IS the focal employee regardless of job title. (See Casebook Precedent #001).
  - If EXCLUDED: Immediately halt numerical extraction. Set `inclusion_status` to 0 and log the exclusion reason in the JSON schema. **IMPORTANT: Excluded papers MUST still be inserted into Excel** (PATH A of the inserter: Coder, Article ID, Title, Authors, Year, Inclusion Status = "0 = Exclude", Exclusion Reason). Assign a sequential BSMA ID (e.g. BSMA0004) regardless of include/exclude status.
- **Bibliometrics Extraction:** Extract `title`, `publication_name` (full, unabbreviated journal name, e.g. 'Journal of Applied Psychology'), `author` (all authors' full names, e.g. 'Jihye Lee, Dongwon Choi, Minyoung Cheong'), and `year` from the paper header. These must be included in the JSON payload.
- **Measure Extraction:** If INCLUDED, deploy subagents to extract the items, alphas, N, Means, SDs, and Pearson correlations (r) for the focal boundary spanning construct and all paired variables. 
  - Subagents must rigorously enforce the Zero-Order Lock (no betas), Dyadic Data rules (Focal Employee only), and Dummy Variable Alpha exceptions.
  - Compile the extracted data into a structured M:N JSON payload.

**Step 2: Excel Injection & JSON Backup**
- **Objective:** Inject the extracted JSON payload directly into the Master Excel sheet AND save a raw backup.
- **Action:** The master orchestrator MUST execute the python script `universal_excel_inserter.py` to securely write the data into the `BSMA_Master_Coding_Sheet.xlsx` file, bypassing human formatting errors and automatically allocating sample numbers.
- **Automatic JSON Backup:** The inserter script automatically saves a raw copy of the JSON payload to `03_Archives_and_Backups/extracted_jsons/BSMAxxxx.json`. This backup allows free restoration of data without re-running costly LLM extraction.
- **Cleanup Rule:** If any temporary `.json` or `.py` files were created to bypass terminal limits, they MUST be deleted immediately after injection. Do not leave scratch files in the workspace root.

**Step 3: Self-Verification Loop**
Before declaring any paper's extraction complete, you MUST dump and review the exact inserted rows using Python. 
- **Double-Check All Numeric Entries:** Pay special attention to Means, SDs, Reliability (Alphas), and Effect Sizes. 
- **No Mental Conversions:** You must ensure that every number exactly matches the paper's table character-for-character. Loop and fix any discrepancies until the extraction is 100% flawless.

**Step 4: GitHub Synchronization**
After the extraction is complete and verified in Step 3, the Orchestrator AI MUST automatically commit and push the updated `BSMA_Master_Coding_Sheet.xlsx` to the GitHub repository.
- Run `git add .`
- Run `git commit -m "Auto-backup: Extracted data for [Paper Author Year]"`
- Run `git push`

**Step 5: Infinite Loop Prevention (Circuit Breaker)**
- Maintain a `Retry_Count` for each paper. If a subagent crashes, returns an error, or hallucinates data, you may retry extraction.
- However, if a paper fails **3 times**, you MUST immediately mark its status as `FAILED (Aborted)`. NEVER attempt to process the same paper more than 3 times.

</details>
