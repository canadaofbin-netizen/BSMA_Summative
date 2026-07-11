# Handoff Report: Include/Exclude Pipeline Codebase Verification

This report provides the results of the static code analysis of the `include_exclude_pipeline` skill definition against the Python scripts in `05_Pipeline/1_Include_Exclude_Loop/`.

---

## 1. Observation

1. **Excel File Path Definition in Prep Script:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\swarm_prep.py`
   * Line 7:
     ```python
     EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_V2.xlsx"
     ```
2. **Excel File Path Definition in Injection Script:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\swarm_inject.py`
   * Line 8:
     ```python
     EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx"
     ```
3. **Pending Items in Excel Files:**
   * Python command run:
     ```python
     python -c "import openpyxl; wb1 = openpyxl.load_workbook(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_V2.xlsx'); wb2 = openpyxl.load_workbook(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx'); ws1 = wb1.active; ws2 = wb2.active; p1 = [ws1.cell(r, 2).value for r in range(4, 1001) if not ws1.cell(r, 5).value or str(ws1.cell(r, 5).value).strip() in ('', 'None')]; p2 = [ws2.cell(r, 2).value for r in range(4, 1001) if not ws2.cell(r, 5).value or str(ws2.cell(r, 5).value).strip() in ('', 'None')]; print('V2 pending count:', len(p1)); print('Master pending count:', len(p2))"
     ```
   * Result:
     ```
     V2 pending count: 536
     Master pending count: 296
     ```
4. **Hardcoded Test Articles in Grading Script:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\grade_test.py`
   * Line 27:
     ```python
     test_articles = ["BSMA0100", "BSMA0101", "BSMA0102", "BSMA0103", "BSMA0104"]
     ```
5. **Excel COM Automation Import:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\post_highlight.py`
   * Line 1:
     ```python
     import win32com.client
     ```
6. **Redundant Code in Inject Script:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\swarm_inject.py`
   * Lines 11–25:
     ```python
     def inject_swarm_results():
         brain_dir = r"C:\Users\yunky\.gemini\antigravity\brain"
         target_dir = OUTPUTS_DIR
         
         # 1. Gather scattered JSONs
         if not os.path.exists(target_dir):
             os.makedirs(target_dir)
             
         scattered = glob.glob(os.path.join(brain_dir, "*", "scratch", "outputs", "BSMA*.json"))
         scattered.extend(glob.glob(r"C:\Users\yunky\.gemini\antigravity\scratch\outputs\BSMA*.json"))
         for f in scattered:
             try:
                 shutil.copy2(f, os.path.join(target_dir, os.path.basename(f)))
             except:
                 pass
     ```
7. **Outdated README Contents:**
   * File: `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop\README.md`
   * Lines 17–22:
     ```
     1. **`run_pipeline.py`**: The master orchestrator.
     2. **`module_1_pdf_loader.py`**: Scans the input folder and chunks PDFs into batches.
     3. **`module_2_agent_dispatcher.py`**: Connects to the LLM API to process the papers.
     4. **`module_3_excel_injector.py`**: Uses `openpyxl` to fast-write the AI results into `BSMA_Master_Coding_Sheet.xlsx`.
     5. **`module_4_com_highlighter.py`**: Uses `win32com` to apply highlights.
     6. **`module_5_git_sync.py`**: Automatically pushes changes to GitHub.
     ```
   * None of these 6 files exist in the directory.

---

## 2. Logic Chain

1. **Excel Path Discrepancy Verification:**
   * Step 1 (`swarm_prep.py`) reads pending papers from `EXCEL_PATH` (`BSMA_AI_Run_V2.xlsx`) (Observation 1).
   * Step 3 (`swarm_inject.py`) writes verdicts to `EXCEL_PATH` (`BSMA_Master_Coding_Sheet.xlsx`) (Observation 2).
   * The two files are verified to be distinct with different states: `BSMA_AI_Run_V2.xlsx` has 536 pending rows while `BSMA_Master_Coding_Sheet.xlsx` has 296 pending rows (Observation 3).
   * Because `swarm_prep.py` is configured with `BSMA_AI_Run_V2.xlsx`, its pending status check will never see the results injected into `BSMA_Master_Coding_Sheet.xlsx` by `swarm_inject.py`.
   * Therefore, running `swarm_prep.py` again in the loop (Step 3 to Step 1 loop in SKILL.md) will result in selecting the exact same papers, creating an **infinite reprocessing loop**.

2. **Grading Script Verification:**
   * Step 4 (`SKILL.md` final reporting) states that `grade_test.py` should be run to generate a final Match Rate Report across all 701 papers.
   * `grade_test.py` only iterates over a hardcoded array `test_articles` of 5 specific IDs (Observation 4).
   * Therefore, the script cannot be used out-of-the-box for all 701 papers and must be adapted as noted in the analysis.

3. **Portability and Environment Verification:**
   * The post-highlighting step in `swarm_inject.py` executes `post_highlight.py`, which imports and relies on `win32com.client` (Observation 5).
   * `win32com` requires a Windows OS environment and an installed copy of Microsoft Excel.
   * Therefore, the pipeline is bound to Windows and will fail if run in non-Windows environments or environments without Excel.

---

## 3. Caveats

* **Active Swarm Execution:** This investigation was strictly static analysis. The actual swarm subagents were not invoked during this analysis to conserve API tokens, but the local Python logic was compared and verified.
* **Test Sheets vs Master Sheet:** While `setup_test_excel.py` copies the Master sheet to `Test_Coding_Sheet.xlsx` to prevent production damage, the injector `swarm_inject.py` is hardcoded to `BSMA_Master_Coding_Sheet.xlsx`, which means running the actual pipeline will overwrite the Master sheet unless manually edited.

---

## 4. Conclusion

There is a critical mismatch between `swarm_prep.py` (which targets `BSMA_AI_Run_V2.xlsx`) and `swarm_inject.py` (which targets `BSMA_Master_Coding_Sheet.xlsx`). This configuration error breaks the automation loop, leading to infinite reprocessing of the first batch. Furthermore, `grade_test.py` has a hardcoded grading scope restricted to 5 articles, and `post_highlight.py` introduces a strict dependency on Windows and Microsoft Excel.

**Actionable Recommendations:**
1. Align the `EXCEL_PATH` variable in `swarm_prep.py` to point to `BSMA_Master_Coding_Sheet.xlsx`.
2. Adapt `grade_test.py` to dynamically load all non-empty articles in the sheets rather than using a hardcoded list.
3. Add command-line argument support in `swarm_prep.py` and `swarm_inject.py` to dynamically override the target Excel file path for safer testing on `Test_Coding_Sheet.xlsx`.
4. Update `README.md` to reflect the actual scripts in the folder.

---

## 5. Verification Method

To verify the findings and the proposed path alignment fix:
1. **Confirm Excel Path Definitions:**
   Inspect line 7 of `swarm_prep.py` and line 8 of `swarm_inject.py` using `view_file` to confirm the mismatched filenames.
2. **Reproduce Mismatch via Output:**
   Run `python 05_Pipeline/1_Include_Exclude_Loop/swarm_prep.py --batch 10` and inspect the generated `scratch/subagents_payload.json`. Note that it will prepare papers based on `BSMA_AI_Run_V2.xlsx`.
3. **Verify Git Backup Command:**
   View lines 49–58 of `post_highlight.py` to verify that `git add BSMA_Master_Coding_Sheet.xlsx` is hardcoded.
4. **Invalidation Condition:**
   This analysis is invalidated only if the orchestrator intended to run the pipeline on `BSMA_AI_Run_V2.xlsx` exclusively and never on `BSMA_Master_Coding_Sheet.xlsx`, which would contradict the project's global rules in `AGENTS.md` (Rules 3, 4, 6) requiring master sheet injection.
