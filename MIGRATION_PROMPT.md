# AI Agent Migration Prompt

If you are migrating to a new AI chat session, simply copy the text block below and paste it as your very first message to the new AI agent. This will ensure the new agent perfectly inherits the entire system architecture, the coding rulebook, and the mandatory subagent workflow without missing a single detail.

---

### 📋 COPY THE TEXT BELOW:

Please set your working directory to `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY`.

Before we begin any data extraction, you MUST read the following 4 files in exact order to fully understand the project's goal, our automated extraction architecture, the strict rulebook, and our current timeline progress.

1. `PROJECT.md` (To understand the overarching meta-analysis goal)
2. `04_Archives_and_Backups\09_Agent_Artifacts_Backup\System_Architecture.md` (To understand the multi-agent system structure, Shadow Reports, and Python execution layers)
3. `05_Coding_Rulebook\03_automated_workflow.md` (To understand the strict Step 0 to Step 3 automated extraction pipeline rules)
4. `04_Archives_and_Backups\09_Agent_Artifacts_Backup\walkthrough.md` (To understand the current progress, noting that we have successfully injected data up to `BSMA_Master_Coding_Sheet.xlsx`)

After reading all 4 files, you must explicitly pledge the following:
**"I understand the system architecture. I swear that I will strictly follow Step 1.5 of `03_automated_workflow.md`. When extracting Measure Descriptors (Number of items, min score, max score, report type, source) for the dozens of variables in correlation matrices, I will NEVER do it manually to prevent context bloat and hallucination. I will ALWAYS use the `invoke_subagent` tool to deploy parallel Subagents to search the text and return the data in a clean JSON mapping."**

Once you have read the files and made this pledge, reply exactly with: 
*"Handover complete. I am fully synchronized and ready to begin extracting the next paper."*
