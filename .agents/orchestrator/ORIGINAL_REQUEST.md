# Original User Request

## 2026-07-11T06:30:42Z
You are the Project Orchestrator for the BSMA Meta-Analysis project.

Your folder is: g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\orchestrator
Your workspace is: g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY
The original user request is documented in: g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\ORIGINAL_REQUEST.md

Your task:
Verify that the newly created `include_exclude_pipeline` SKILL (g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\skills\include_exclude_pipeline\SKILL.md) exactly matches the logic and expectations of the underlying Python pipeline scripts in `05_Pipeline/1_Include_Exclude_Loop/`.

Follow the Meta-Analysis Global Project Rules (documented in .agents/AGENTS.md).

Specifically:
1. Conduct static code analysis of the SKILL.md against the Python scripts in `05_Pipeline/1_Include_Exclude_Loop/` to confirm that the steps map exactly to the script logic.
2. Run a live dry-run using a minimal mock batch (e.g., batch_size=2) to ensure execution safety, that it successfully processes the 2 items, and that it triggers Excel injection without throwing exceptions.
3. Write a detailed `Verification_Report.md` in the workspace root (`g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY`) mapping the 4 steps of the `include_exclude_pipeline` SKILL to the exact corresponding Python execution logic. Make sure it declares a Pass/Fail for compliance for each step.
4. Update your `progress.md` file regularly with your current plan and progress so the sentinel can report status and monitor liveness.
5. Report completion to the Sentinel when finished.
