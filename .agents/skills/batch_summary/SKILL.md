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

## 2. Meeting-Ready Summary Artifact Standard (Rule 31 — Strictly Zero Graphs/Diagrams)

Whenever the user requests a summary artifact, meeting reference document, or batch summary report (e.g., `batch_[start]_to_[end]_summary.md`), you MUST generate a user-facing Markdown artifact in the conversation's artifact directory that strictly follows the canonical structure of `batch_392_to_511_10papers_summary.md` (**Rule 31**):

### Global Formatting Rules
- **Strictly Zero Graphs / Diagrams:** Never include Mermaid diagrams, charts, or ASCII trees in the meeting summary artifact. Use ONLY clean Markdown tables and structured text.
- **Strictly Zero Ellipses (`...`):** Every verbatim quote (`Sample Quote`, `Verbatim Exclusion Evidence`) must be extracted as complete sentences without `...` (Rule 13).
- **100% Source Table Fidelity:** Every paper—both **Included (`1 = Include`)** and **Excluded (`0 = Exclude`)**—must include its original statistical table (or relevant table excerpt for excluded papers) so faculty and co-authors can inspect the raw numbers during meetings.

---

### Canonical 5-Part Artifact Structure

#### 1. Executive Summary Table (`1. 전체 총괄 요약표 / Executive Summary Table`)
- A single table summarizing all evaluated papers in chronological/ID order:
  `| 배치 구분 | Paper ID | 제1저자 및 연도 | 출처 / 학술지 | 최종 판정 | 추출 효과크기 / 배제 코드 | 표본 크기 (N) 및 연구 핵심 특징 |`
- Immediately followed by total batch statistics:
  - **포함(Include):** Total included papers and total extracted effect size ($r$) rows.
  - **배제(Exclude):** Total excluded papers broken down by exclusion code (`Code 1` ~ `Code 6`).

#### 2. 100% Re-Verification Audit Summary Table (`2. 100% 원문 대조 재검증 핵심 수정 내역 요약` — *Include when re-verification is performed*)
- A structured changelog table documenting any discrepancies caught and corrected during 100% PDF cross-verification:
  `| Paper ID | 재검증 점검 항목 | 이전 코딩값 | 원문 대조 후 최종 확정값 | 원문 근거 위치 |`

#### 3. Included Paper Detailed Sections (`[포함 논문] Paper [ID] Author (Year)`)
For each included study (`1 = Include`), provide:
1. **Bibliographic & Study Overview:**
   - **논문 서지:** Full APA citation (Authors, Year, Title, Journal, Volume/Issue, Pages).
   - **최종 판정:** `1 = Include (K개 효과크기 행 추출)`
   - **연구 목적:** 1–2 sentence summary of the theoretical model and empirical objective.
   - **표본 및 설계 정보:** Sample size ($N$), study design (`Cross-sectional` vs `Longitudinal` with wave/lag details), country/international context, and demographics (Mean Age, `% Female`, Mean Org Tenure, explicitly noting `999` where unreported; plus sample independence notes if relevant).
   - **원문 표본 인용 (Verbatim Sample Quote — Zero Ellipses):** Exact blockquote from the Sample/Participants section with page number.
   - **측정 도구 요약:** Concise breakdown of **BSB 변수** (scale citation, item count, Likert range, report type, $\alpha$/CR, $M, SD$) and **Non-BS 변수** (numbered list `①, ②, ...` with scale citations, item counts, $\alpha$/CR, $M, SD$).
2. **Full Original Correlation & Descriptive Table (`원문 Table X (p. Y)`):**
   - Complete Markdown table reproducing the source paper's descriptive statistics ($M, SD, \alpha/\text{CR}$, pairwise $n$ if applicable) and full zero-order correlation matrix with significance stars (`*`, `**`, `***`) and table footnotes.
   - Bold the BSB row(s) and the target correlation cells paired with BSB.
3. **Extracted Effect Sizes Table (`추출된 효과크기 목록 — N BSB × M Non-BS = K개 행`):**
   - Complete table of every extracted row injected into Excel:
     `| 행 번호 | BSB 변수명 (Col 41) | 상대 Non-BS 변수명 (Col 45) | 표본 크기 (N) | 상관계수 (r) | 원문 셀 값 (Col 50) |`

#### 4. Excluded Paper Detailed Sections (`[배제 논문] Paper [ID] Author (Year) — 원문 테이블 및 배제 증명`)
For each excluded study (`0 = Exclude`), provide:
1. **Bibliographic & Exclusion Verdict:**
   - **논문 서지:** Full APA citation.
   - **최종 판정:** `0 = Exclude (Code X = ...)`
   - **왜 배제되었는가? (핵심 배제 사유):** Numbered points (`1, 2, 3`) clearly explaining the unit-of-analysis violation (`Code 3`), missing bivariate correlation matrix (`Code 1`), non-employee sample (`Code 2`), or duplicate dataset (`Code 6`) for meeting defense.
2. **Original Source Table Proof (`원문 Table X (p. Y) — 배제 근거 표`):**
   - Reproduce the relevant table from the excluded paper (e.g., the firm-level correlation matrix for `Code 3` or the univariate/logistic regression Odds Ratio table for `Code 1`) to visually demonstrate why individual-level Pearson correlations ($r$) cannot be extracted.
3. **Verbatim Exclusion Evidence Quotes (`원문 배제 입증 인용구 — Zero Ellipses`):**
   - Exact blockquotes with page/footnote/table coordinates and strictly zero ellipses (`...`).

#### 5. Verified Excel Coding Sheet Links (`관련 코딩 시트 파일 링크`)
- Clickable `file:///` links to the verified `.xlsx` coding sheet(s) in `03_Coding_Sheets/` with total row counts.

---

## 3. Orchestration Protocol

When `/summary` is triggered or the user requests a batch summary / meeting artifact:
1. Run `python .agents/scripts/batch_summary.py [user_arguments]` to verify 100% data integrity (`Rule 1`, `Rule 20`, `Rule 27`) across the target Excel coding sheet(s).
2. Generate or update the **Meeting-Ready Summary Artifact** (`batch_[IDs]_summary.md`) in the conversation artifact directory strictly following Section 2 (**Rule 31**) above.
3. Keep the Excel file pure and untouched; do NOT write summary rows or tables into the Excel data sheet.

