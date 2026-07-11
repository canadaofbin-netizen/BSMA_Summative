# 🔍 Static Code Analysis: Include/Exclude Loop Pipeline Verification

## Executive Summary
This report presents a static code analysis verifying the alignment between `include_exclude_pipeline/SKILL.md` and the Python scripts located in `05_Pipeline/1_Include_Exclude_Loop/`. A critical configuration bug was discovered where the payload generator reads from `BSMA_AI_Run_V2.xlsx` but the injector writes to `BSMA_Master_Coding_Sheet.xlsx`, which breaks the automation loop and causes an infinite loop of reprocessing the same batch.

---

## 📋 1. Detailed Step-by-Step Mapping

### Step 1: Batch Payload Generation
* **SKILL.md Instruction:** Run `python 05_Pipeline/1_Include_Exclude_Loop/swarm_prep.py --batch 40` to check the target Excel file and generate a payload at `scratch/subagents_payload.json` containing up to 40 pending papers.
* **Script Implementation (`swarm_prep.py`):**
  * **Command Arguments:** Accepts `--batch` via `argparse` (integer, default `20`). Thus, running it with `--batch 40` works exactly as expected.
  * **Read Operation:** Reads the active worksheet of `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_V2.xlsx` (hardcoded).
  * **Pending Logic:** Iterates from row 4 to the end. A row is pending if Column 2 (`art_id`) starts with "BSMA" and is not empty, and Column 5 (`status`) is empty, `None`, or whitespace.
  * **PDF Resolution:** Calls `find_pdf_for_id(art_id)`. It extracts the integer from the ID (e.g., `BSMA0001` -> `1`), and searches `01_Academic_Papers/` for a file starting with `[1]` and ending with `.pdf`.
  * **Path Normalization:** Replaces backslashes with forward slashes in the path for prompt compatibility.
  * **Output Generation:** Writes a JSON array of subagent configurations to `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\subagents_payload.json`.
  * **Termination Condition:** If no pending rows are found, it prints `"No more pending papers found!"` and exits without generating a payload.

### Step 2: Real-Swarm Invocation
* **SKILL.md Instruction:** Read `scratch/subagents_payload.json`, spawn `bsma_reviewer_v2` subagents using the `invoke_subagent` tool, and wait for them to output verdict JSONs into `scratch/outputs/`.
* **Script Implementation:**
  * No Python script implements this step because it requires the agent to invoke the `invoke_subagent` native tool.
  * **Subagent Output Path:** The payload defines the output destination as `scratch/outputs/{art_id}.json`. In a real execution, subagents write to their local brain directories (e.g., `C:\Users\yunky\.gemini\antigravity\brain\<session_id>\scratch\outputs\BSMA*.json`).

### Step 3: Data Injection & Loop
* **SKILL.md Instruction:** Run `python 05_Pipeline/1_Include_Exclude_Loop/swarm_inject.py` to write verdicts into the Excel sheet, clean up JSON files, and loop back to Step 1.
* **Script Implementation (`swarm_inject.py`):**
  * **File Gathering:** Before injection, it automatically scans all subagent brain directories (`C:\Users\yunky\.gemini\antigravity\brain\*\scratch\outputs\BSMA*.json`) and the main scratch directory (`C:\Users\yunky\.gemini\antigravity\scratch\outputs\BSMA*.json`), copying matches to the local output folder `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs`.
  * **Write Operation:** Reads `g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx` (hardcoded).
  * **Injection Logic:**
    * Matches the file name (e.g., `BSMA0100.json` -> `BSMA0100`) against Column 2.
    * Injects `status` into Column 5, `reason_code` into Column 6, and a combined notes string (`"{reason_summary}. Verbatim Evidence: \"{verbatim}\""`) into Column 16.
    * Saves `BSMA_Master_Coding_Sheet.xlsx`.
    * Deletes the local JSON file to prevent double-processing.
  * **Batch Reporting:** Runs `generate_batch_report.py --ids <injected_ids>` to compile a Markdown report in `04_Reports/Batch_Report_<timestamp>.md`.
  * **Post-Highlighting:** Runs `post_highlight.py` to highlight specified keywords in Column 16 in red/bold.
  * **Git Auto-Backup:** `post_highlight.py` automatically commits and pushes `BSMA_Master_Coding_Sheet.xlsx` to GitHub.

### Step 4: Final Reporting
* **SKILL.md Instruction:** Once complete, run `python 05_Pipeline/1_Include_Exclude_Loop/grade_test.py` or write a custom cross-validation script.
* **Script Implementation (`grade_test.py`):**
  * Opens both `BSMA_Master_Coding_Sheet.xlsx` and `Test_Coding_Sheet.xlsx`.
  * Standardizes status values ("0 = Exclude" -> "0", "1 = Include" -> "1").
  * Calculates Accuracy, False Positives (FP), and False Negatives (FN).

---

## 🚨 2. Key Discrepancies, Bugs, and Missing Elements

### 1. The Excel File Path Mismatch (Critical Loop Breaker)
* **Finding:** `swarm_prep.py` is configured to read pending papers from `BSMA_AI_Run_V2.xlsx`, but `swarm_inject.py` is configured to write results to `BSMA_Master_Coding_Sheet.xlsx`.
* **Impact:** When the pipeline runs in a loop:
  1. `swarm_prep.py` reads `BSMA_AI_Run_V2.xlsx`, sees empty cells, and creates a payload for 40 papers.
  2. The subagents process them.
  3. `swarm_inject.py` writes the results to `BSMA_Master_Coding_Sheet.xlsx`.
  4. The loop restarts. `swarm_prep.py` reads `BSMA_AI_Run_V2.xlsx` again. Because `BSMA_AI_Run_V2.xlsx` was *never updated*, the status cells are still empty.
  5. `swarm_prep.py` generates the *exact same* payload, leading to an **infinite reprocessing loop**.
* **Evidence:**
  * `swarm_prep.py` (Line 7): `EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_V2.xlsx"`
  * `swarm_inject.py` (Line 8): `EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx"`
  * Active verification confirmed the two Excel sheets are separate and contain different numbers of pending items: `BSMA_AI_Run_V2.xlsx` has **536 pending rows**, whereas `BSMA_Master_Coding_Sheet.xlsx` has **296 pending rows**.
* **Origin of Mismatch:** The LangGraph prototype runner `run_batch.py` and its graph state nodes in `nodes.py` (Line 53) are designed to read and write to `BSMA_AI_Run_V2.xlsx`. `swarm_prep.py` was likely aligned with this prototype file. However, for the Real-Swarm pipeline, the injector `swarm_inject.py` was correctly directed to `BSMA_Master_Coding_Sheet.xlsx` (in line with AGENTS.md rules), but `swarm_prep.py` was not updated.

### 2. Hardcoded Testing Scope in `grade_test.py`
* **Finding:** `grade_test.py` contains a hardcoded list of test articles on Line 27:
  ```python
  test_articles = ["BSMA0100", "BSMA0101", "BSMA0102", "BSMA0103", "BSMA0104"]
  ```
* **Impact:** Running `grade_test.py` will only verify these 5 specific papers. It does not automatically scale to report across all 701 papers as suggested by `SKILL.md` Step 4 unless it is manually edited.

### 3. Lack of Test Sheet Override in `swarm_inject.py`
* **Finding:** `swarm_inject.py` has no command-line argument support or environment variable check to redirect its injection to a test spreadsheet (such as `Test_Coding_Sheet.xlsx`).
* **Impact:** Even though `setup_test_excel.py` copies the master sheet to `Test_Coding_Sheet.xlsx` to support backtesting, there is no way to tell `swarm_inject.py` to write the subagent results to `Test_Coding_Sheet.xlsx` instead of the master sheet. This makes testing the integration risky since it directly modifies production data.

### 4. Outdated `README.md`
* **Finding:** The `README.md` file describes a completely different set of modular scripts:
  * `run_pipeline.py`
  * `module_1_pdf_loader.py`
  * `module_2_agent_dispatcher.py`
  * `module_3_excel_injector.py`
  * `module_4_com_highlighter.py`
  * `module_5_git_sync.py`
* **Impact:** None of these files actually exist in `05_Pipeline/1_Include_Exclude_Loop/`. This is confusing for any developer or agent reviewing the codebase.

### 5. Redundant Utility Script
* **Finding:** `gather_jsons.py` is present in the directory, which copies JSON outputs from subagent directories.
* **Impact:** This script is entirely redundant because its exact logic is already embedded inside the first section of `swarm_inject.py` (lines 11–25).

---

## ⚙️ 3. Environment & Portability Constraints

* **Windows & Excel COM Dependency:**
  `post_highlight.py` imports `win32com.client` and utilizes the Windows COM API to launch a background instance of Excel (`Excel.Application`) to apply cell styling.
  * **Constraint:** This requires the script to run on a Windows machine with a registered installation of Microsoft Excel. If run on Linux/macOS or a server environment without Microsoft Excel, the pipeline will crash at the end of Step 3.

---

## 🛠️ 4. Proposed Fixes (Patch Diff)

To resolve the critical Excel path mismatch and ensure the pipeline loops correctly, `swarm_prep.py` must be aligned with the production master sheet.

### Proposed Change for `05_Pipeline/1_Include_Exclude_Loop/swarm_prep.py`

```markdown
<<<<
EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_AI_Run_V2.xlsx"
====
EXCEL_PATH = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\BSMA_Master_Coding_Sheet.xlsx"
>>>>
```

This single line change resolves the infinite loop and aligns the preparation phase with the injection and reporting phases.
