---
name: batch_summary
description: Generates an executive diagnostic, variable taxonomy, and Cartesian pairing summary for BSMA Excel coding sheets via paper IDs or file paths.
---

# Skill: Batch Summary (`/summary`)

When the user invokes `/summary` or asks to summarize extracted variables, effect sizes, or batch status, execute this skill to generate an executive diagnostic dashboard.

---

## 1. Input Flexibility & CLI Routing

The underlying engine `.agents/scripts/batch_summary.py` supports multiple flexible input formats:

1. **Direct Paper IDs:**
   ```powershell
   python .agents/scripts/batch_summary.py 70 94 109
   ```
   *Behavior:* Automatically locates which coding sheet in `03_Coding_Sheets/` contains those paper IDs and generates a targeted report for those studies.

2. **Specific Sheet Path:**
   ```powershell
   python .agents/scripts/batch_summary.py 03_Coding_Sheets/70_94_109.xlsx
   ```
   *Behavior:* Evaluates all studies and rows present in the specified Excel file.

3. **Combined Sheet Path and Paper IDs:**
   ```powershell
   python .agents/scripts/batch_summary.py 03_Coding_Sheets/70_94_109.xlsx 70 94
   ```
   *Behavior:* Inspects the specified sheet while filtering outputs to the requested paper IDs.

4. **Zero Arguments (Auto-detect):**
   ```powershell
   python .agents/scripts/batch_summary.py
   ```
   *Behavior:* Automatically selects and evaluates the most recently modified `[start]_[end].xlsx` batch sheet in `03_Coding_Sheets/`.

5. **Optional Flags:**
   - `--report`: Saves the markdown report to `04_Reports/batch_summary_[sheet_name].md`.
   - `--json`: Outputs raw structured JSON for automated test scripts.

---

## 2. Executive Dashboard Standard (No Emojis)

All summary outputs MUST follow this clean, professional academic format with **zero emojis**:

1. **Executive KPI Table:**
   - Total Data Rows, Total Effect Sizes ($r$), Included vs. Excluded Studies, Unique BSB Variables, Unique Non-BS Variables.
   - Core rule compliance status (Rule 1, Rule 20, Rule 27).

2. **Detailed Study-by-Study Breakdown:**
   - `[ID] Author (Year) — Status`: Paper title looked up from `01_Academic_Papers/`.
   - Sample Profile ($N$, Age, Gender, Tenure, Occupation).
   - Extracted Effect Sizes row count.
   - Boundary Spanning Variables with Mean, SD, Reliability $\alpha$, and specific scale citations.
   - Non-BS Variables categorized into domain clusters (Context & Organization, Attitudes & Commitment, Role Stress, Performance & Outcomes, Individual & Demographics, Control & Incentives).
   - Cartesian Pairing Topology ($N_{\text{BSB}} \times M_{\text{Non-BS}} \rightarrow K \text{ rows}$).
   - Provenance Coordinates: Physical table numbers and manuscript pages from Col 50 Notes.
   - Excluded Studies: Clear documentation of Exclusion Reason code and Rule 19 termination at Col 6.

3. **Cross-Study Construct Taxonomy Tree:**
   - ASCII hierarchy mapping all BSB variables and thematic Non-BS clusters across the entire sheet.

4. **Data Quality & Compliance Checklist:**
   - Verification of Rule 1 Dual Missing Data, Rule 14 Index Pruning, Rule 19 Exclude Termination, Rule 20 Canonical 3-Tier Headers, and Rule 27 Lossless Parity.

---

## 3. Orchestration Protocol

When `/summary` is triggered:
1. Run `python .agents/scripts/batch_summary.py [user_arguments]`.
2. Output the exact generated Markdown directly to the user.
3. Keep the Excel file pure and untouched; do NOT write summary rows or tables to the data sheet.
