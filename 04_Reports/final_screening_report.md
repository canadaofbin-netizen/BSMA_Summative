# 📊 BSMA Meta-Analysis: Final AI Coding Report (701 Papers)

This report summarizes the comprehensive 1st screening judgments automatically executed by the AI pipeline across all 701 academic papers.

## 📈 Overall Summary Statistics

| Metric | Count | Percentage |
| :--- | :--- | :--- |
| **Total Papers Processed** | 701 | 100.0% |
| **Included (Status = 1)** | 119 | 17.0% |
| **Excluded (Status = 0)** | 582 | 83.0% |

<br/>

## 🚫 Exclusion Reasons Breakdown

A detailed breakdown of why the 582 papers were excluded according to the project's strict methodology rules.

| Reason Code | Description | Count | Percentage of Excluded |
| :---: | :--- | :---: | :---: |
| **Code 3** | **Non-individual level (Team/Firm/Org analysis)**<br/>*Aggregated correlations, patent-level, or firm-level strategy studies.* | 305 | 52.4% |
| **Code 1** | **No effect size of interest**<br/>*Qualitative, descriptive, or missing Pearson correlation matrices.* | 186 | 32.0% |
| **Code 4** | **Non-primary study**<br/>*Conceptual papers, literature reviews, or conceptual modeling without primary data.* | 52 | 8.9% |
| **Code 2** | **Non-employee samples**<br/>*Studies analyzing consumers, students, or general citizens.* | 30 | 5.2% |
| **Code 5** | **Multiple reasons (Specified in Notes)** | 5 | 0.9% |
| **Code 7** | **Non-English language** | 2 | 0.3% |
| **Code 99** | **Other (Specified in Notes)**<br/>*e.g., massive dissertations/theses.* | 2 | 0.3% |
| | **Total Excluded** | **582** | **100.0%** |

> [!NOTE]
> **Observation on Code 3:** As per your strict rules against *Construct Homonymy*, over half (52.4%) of all excluded papers were filtered out because they analyzed the firm, team, or inter-organizational level rather than individual employee boundary-spanning behavior.

> [!IMPORTANT]
> **Auditability Guarantee:** Every single one of the 582 excluded papers has a precise **Verbatim Evidence** string extracted and saved into the `Notes` column of the Excel sheet to guarantee 100% auditability without relying on AI hallucination.
