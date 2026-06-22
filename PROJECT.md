# Project: Meta-Analytic Data Extraction (Automated Pipeline)

## Architecture
- **Data Flow**: PDF papers (under `01_Academic_Papers/`) -> Information extraction by Main Orchestrator and parallel Subagents -> Shadow Report creation (under `03_Shadow_Reports/`) -> Python Injection to Excel -> Verification.
- **Rulebook Guidelines**: All agents must strictly adhere to the `05_Coding_Rulebook/` rules for table formatting, missing data (`999`), and exceptions before writing any data.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Paper 1 Extraction | Evaluate Paper 1 inclusion/exclusion, extract metadata, deploy Subagent 1 for measures, and write `Paper1_Shadow_Report.md`. | None | PLANNED |
| 2 | Paper 2 Extraction | Evaluate Paper 2 inclusion/exclusion, extract metadata, deploy Subagent 2 for measures, and write `Paper2_Shadow_Report.md`. | None | PLANNED |
| 3 | Paper 3 Extraction | Evaluate Paper 3 inclusion/exclusion, extract metadata, deploy Subagent 3 for measures, and write `Paper3_Shadow_Report.md`. | None | PLANNED |
| 4 | Excel Injection & Sync | Use Python to inject Shadow Reports into `v8.xlsx` and automatically sync to GitHub. | M1, M2, M3 | PLANNED |

## Interface Contracts
- **Shadow Report Schema**:
  - File format: Markdown
  - Directory: `03_Shadow_Reports/`
  - Name convention: `[Author]_[Year]_Shadow_Report.md`
  - Data table requirements: Must contain columns such as Effect Size ID, N, Means, SDs, r, etc., with NO bold text (`**`) in headers.
  - Inclusion/Exclusion Judgments: Coded as `1 = Include` or `0 = Exclude` as per rulebooks.
