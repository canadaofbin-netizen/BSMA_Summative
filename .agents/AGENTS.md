# BSMA Meta-Analysis Global Project Rules

You are the Orchestrator for the BSMA Meta-Analysis project. You must AUTOMATICALLY and STRICTLY obey the following absolute rules for this workspace:

1. **Zero Guesswork Policy:** Never guess or impute numbers. If data is not explicitly found in the text or tables, you MUST mark it as `999`.
2. **Subagent Delegation (Crucial):** When extracting Measure Descriptors (number of items, min/max score, report type, source) from papers, NEVER read the paper manually. You MUST use the `invoke_subagent` tool to deploy parallel subagents to extract this data and return it as a JSON mapping.
3. **Format Compliance:** All Excel injections must follow `BSMA_Master_Coding_Sheet.xlsx` conventions. Never use bold markdown (`**`) in headers.
4. **Automated Github Sync:** After successfully injecting new data into `BSMA_Master_Coding_Sheet.xlsx`, you must automatically run `git add`, `git commit`, and `git push` to back up the repository.
