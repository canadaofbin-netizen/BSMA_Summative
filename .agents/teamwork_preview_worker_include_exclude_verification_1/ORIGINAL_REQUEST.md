## 2026-07-11T06:32:50Z

You are a Software Engineer (teamwork_preview_worker).
Your working directory is: g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\teamwork_preview_worker_include_exclude_verification_1
Your task is to:
1. Read the explorer's reports in:
   - g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\teamwork_preview_explorer_include_exclude_verification_1\analysis.md
   - g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\teamwork_preview_explorer_include_exclude_verification_1\handoff.md
2. Apply the permanent fix to `05_Pipeline/1_Include_Exclude_Loop/swarm_prep.py`:
   - Change `EXCEL_PATH` on line 7 from `BSMA_AI_Run_V2.xlsx` to `BSMA_Master_Coding_Sheet.xlsx`.
3. Conduct a safe dry-run of the pipeline with a mock batch of size 2 on a copy of the Excel sheet.
   - Run `python 05_Pipeline/1_Include_Exclude_Loop/setup_test_excel.py` to copy the master sheet to `Test_Coding_Sheet.xlsx` and clear status.
   - Temporarily edit `swarm_prep.py`, `swarm_inject.py`, and `post_highlight.py` to target `Test_Coding_Sheet.xlsx` instead of `BSMA_Master_Coding_Sheet.xlsx`. In `post_highlight.py`, also comment out or disable the git add/commit/push steps.
   - Run `python 05_Pipeline/1_Include_Exclude_Loop/swarm_prep.py --batch 2` to generate `scratch/subagents_payload.json`.
   - Read the payload to see which two paper IDs were prepped.
   - Manually write two mock JSON files under `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs\<ID>.json` with a valid verdict schema:
     ```json
     {
         "status": "1 = Include",
         "reason_code": "I-SPA",
         "reason_summary": "Mock summary",
         "verbatim": "Mock verbatim text showing inclusion."
     }
     ```
   - Run `python 05_Pipeline/1_Include_Exclude_Loop/swarm_inject.py` to inject the mock verdicts, generate the batch report, and highlight.
   - Verify that the injection worked (columns 5, 6, 16 are filled in `Test_Coding_Sheet.xlsx` for those 2 papers, the JSONs are cleaned up, and the batch report is in `04_Reports/`).
   - Restore the temporary file modifications in `swarm_prep.py`, `swarm_inject.py`, and `post_highlight.py` to target `BSMA_Master_Coding_Sheet.xlsx` (with the permanent fix in `swarm_prep.py` retained).
4. Write a detailed `Verification_Report.md` in the workspace root (`g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\Verification_Report.md`) mapping the 4 steps of `include_exclude_pipeline` SKILL.md to the Python execution logic. Declare a Pass/Fail for compliance for each step.
5. Send a message to the orchestrator (conversation ID: 6a76c278-eef7-4cc1-84b2-62955719e557) with your dry-run logs, findings, and verification report path.

Ensure you adhere to the Meta-Analysis Global Project Rules:
- DO NOT CHEAT. All implementations must be genuine.
- Universal Zero Guesswork Policy.
- matrix-specific N Guardrail, etc. (if applicable).
- No bold markdown in Excel headers.
