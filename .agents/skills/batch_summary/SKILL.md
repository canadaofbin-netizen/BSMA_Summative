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

5. **Language Control Protocol:**
   - **Default Language: English (`lang="en"`):** All `/summary` executions produce English markdown by default.
   - **Korean on Demand (`lang="ko"`):** Automatically triggered if Korean characters are detected in user prompts or arguments, or when `--ko` / `-k` is explicitly passed:
     ```powershell
     python .agents/scripts/batch_summary.py 70 94 109 --ko
     ```
   - **Explicit English Override:**
     ```powershell
     python .agents/scripts/batch_summary.py 70 94 109 --en
     ```

6. **Optional Flags:**
   - `--report`: Saves the markdown report to `04_Reports/batch_summary_[sheet_name]_[lang].md`.
   - `--json`: Outputs raw structured JSON for automated test scripts.

---

## 2. Immutable 3-Section Executive Dashboard Standard (No Emojis)

All summary outputs in both English and Korean MUST strictly follow this exact 3-section layout with **zero emojis**:

### Section 1: Sheet Diagnostic Overview Table (`구분 | 수치 | 비고` / `Category | Metric | Notes`)
- **Total Data Rows:** Total extracted data rows (Row 4 ~ Row N+3, excluding 3 header rows).
- **Total Effect Sizes ($r$):** Sum of extracted correlation pairs broken down per included paper.
- **Unique BSB Variables:** Total count of distinct boundary-spanning variables across studies.
- **Unique Non-BS Variables:** Total count of distinct non-boundary-spanning variables across studies.
- **Study Screening Judgments:** Summary of Included vs. Excluded studies with exact exclusion reasons.
- **Data Integrity Verification:** 100% PASS confirmation for Rule 1 (999 missing), Rule 20 (3-tier headers), Rule 27 (Lossless parity).

### Section 2: Study-by-Study Detailed Analysis
For each study (enumerated with circled numbers `①`, `②`, `③`):
- Header: `#### ① Paper [ID] Author (Year)` followed by blockquote title `> *Title*`.
- **Included Studies:**
  - **Judgment:** `1 = include` with sample demographics (`Sample N = ...`, occupation, mean age).
  - **Extracted Rows:** Total rows extracted and row span (`Row X ~ Row Y`).
  - **BSB Variables:** Bulleted list with English/Korean descriptions.
  - **Non-BS Variables:** Bulleted list with English/Korean descriptions.
  - **Pairing Topology:** Precise Cartesian product formulation (`N BSB × M Non-BS = K rows`) or explicit subcomponent exclusions.
  - **Empirical Stats Status:** 100% completion status of Mean, SD, and Reliability $\alpha$ (or Rule 1 missing data `999` status).
  - **Provenance Coordinates (Col 50):** Table numbers and manuscript page numbers.
- **Excluded Studies:**
  - **Judgment:** `0 = exclude`.
  - **Exclusion Reason:** Exact exclusion category code and rationale.
  - **Extracted Rows:** `1 row` (Row X).
  - **Variables:** `0` (Strictly blank from Col 7–50 per Rule 19).

### Section 3: Cross-Study Construct Taxonomy Tree
ASCII tree mapping all unique constructs across the evaluated sheet:
- `[BSB Variables — N Total]` branch listing BSB variables grouped by paper ID.
- `[Non-BS Variables — M Total]` branch categorizing all Non-BS variables into 8 standard domain clusters:
  1. Context & Organization (`조직/환경 특성`)
  2. Individual & Demographics (`개인/인구통계 특성`)
  3. Attitudes & Commitment (`태도/몰입 변수`)
  4. Control & Incentives (`업무/조직 통제`)
  5. Internal Group Dynamics (`내부 행동/소통` — Note: applies strictly to non-boundary internal dynamics such as team conflict or internal support; internal dissemination/influence BSBs reside under BSB Variables per Rule 28)
  6. Role Stress (`역할 스트레스`)
  7. Performance & Outcomes (`직무 성과`)
  8. General Non-BS Variables (`기타 변수`)

---

## 3. Orchestration Protocol

When `/summary` is triggered:
1. Determine language preference (Default English; activate Korean if prompt contains Korean text or user explicitly requests Korean).
2. Run `python .agents/scripts/batch_summary.py [user_arguments]`.
3. Output the exact generated Markdown directly to the user.
4. Keep the Excel file pure and untouched; do NOT write summary rows or tables to the data sheet.
