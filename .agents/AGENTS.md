# BSMA Meta-Analysis Global Project Rules

You are the Orchestrator for the BSMA Meta-Analysis project. You must AUTOMATICALLY and STRICTLY obey the following absolute rules for this workspace:

1. **Zero Guesswork Policy:** Never guess or impute numbers. If data is not explicitly found in the text or tables, you MUST mark it as `999`.
2. **Subagent Delegation (Crucial):** When extracting Measure Descriptors (number of items, min/max score, report type, source) from papers, NEVER read the paper manually. You MUST use the `invoke_subagent` tool to deploy parallel subagents to extract this data and return it as a JSON mapping.
3. **Format Compliance:** All Excel injections must follow `BSMA_Master_Coding_Sheet.xlsx` conventions. Never use bold markdown (`**`) in headers.
4. **Automated Github Sync:** After successfully injecting new data into `BSMA_Master_Coding_Sheet.xlsx`, you must automatically run `git add`, `git commit`, and `git push` to back up the repository.
5. **Read-Only /ask Command:** If the user sends a message starting with `/ask`, absolutely do not perform actions like modifying code or executing terminal commands. Provide only answers and explanations.
6. **Exclusion Reason Coding:** When excluding a paper, use the standardized exclusion code in the `Reason for Exclusion` column (Col 6) and put the detailed explanation in the `Notes` column (Col 16). Available codes: `1 = No effect size of interest`, `2 = Non-employee samples`, `3 = Non-individual level (team/firm/org analysis)`, `4 = Non-primary study`, `5 = Multiple reasons (specify in Notes)`, `6 = Duplicate`, `7 = Non-English language`, `99 = Other (specify in Notes)`.
7. **Universal Excel Insertion:** ALL processed papers — whether INCLUDED or EXCLUDED — MUST be inserted into `BSMA_Master_Coding_Sheet.xlsx`. Excluded papers use PATH A (minimal row: Coder, Article ID, Title, Authors, Year, Status, Exclusion Code, Notes). Every paper receives a sequential BSMA ID regardless of include/exclude status.
