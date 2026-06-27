# Summative Report
### Boundary Spanning Meta-Analysis

*Data De-duplication & Quality Control Audit*

---

## Detailed Duplicate Analysis & Resolution

Below is the detailed audit of each identified duplicate pair from the original Excel sheet, outlining the exact row numbers (1-indexed, including the header row in Excel), title variations, and the deduplication action applied.

This process successfully isolated and resolved 4 pairs of duplicate articles (8 rows in total) to ensure robust sample integrity for the meta-analysis.

### 📊 Duplicate Pair 1: Product Management Boundary Role
* **Original Rows:** Row 85 & Row 86
* **Row 85 Title:** `Boundary role spanning behavior, conflicts and performance of industrial product managers`
* **Row 86 Title:** `Boundary Role Spanning Behavior, Conflicts and Performance of Industrial Product Managers`
* **Differences:** Title casing (Sentence Case vs. Title Case). The abstracts had minor wording variations but described the exact same study.
* **Resolution:** **Row 85 was kept**, and the redundant **Row 86 was removed**.

### 📊 Duplicate Pair 2: Logistics Boundary Interfaces
* **Original Rows:** Row 99 & Row 120
* **Row 99 Title:** `Boundary spanning interfaces between logistics, production, marketing and new product development`
* **Row 120 Title:** `Boundary-spanning interfaces between logistics, production, marketing and new product development: [1]: [1]`
* **Differences:** Hyphenation ("Boundary spanning" vs. "Boundary-spanning") and trailing brackets (`: [1]: [1]`) resulting from database scrape artifacts.
* **Resolution:** **Row 99 (cleaner title) was kept**, and the redundant **Row 120 was removed**.

### 📊 Duplicate Pair 3: Group & Personality Correlates of BSA
* **Original Rows:** Row 299 & Row 300
* **Row 299 Title:** `Group, task, and personality correlates of boundary-spanning activities`
* **Row 300 Title:** `Group, Task, and Personality Correlates of Boundary-Spanning Activities`
* **Differences:** Title casing (Sentence Case vs. Title Case) and capitalization. Both share the exact same normalized text structure.
* **Resolution:** **Row 299 was kept**, and the redundant **Row 300 was removed**.

### 📊 Duplicate Pair 4: Software Outsourcing Controls
* **Original Rows:** Row 667 & Row 668
* **Row 667 Title:** `The Role of Organizational Controls and Boundary Spanning in Software Development Outsourcing: Implications for Project Performance`
* **Row 668 Title:** `The Role of Organizational Controls and Boundary-Spanning in Software Development Outsourcing: Implications for Project Performance 1`
* **Differences:** Trailing number ` 1` and hyphenation differences ("Boundary Spanning" vs. "Boundary-Spanning") representing a citation indexing glitch.
* **Resolution:** **Row 667 (cleaner title) was kept**, and the redundant **Row 668 was removed**.

---

### Summary of Dataset Deduplication Audit:
* **Original Extracted Records:** 736 rows
* **Duplicate Rows Removed:** 4 rows (Excel rows 86, 120, 300, 668)
* **Final Unique Meta-Analysis Sample:** 732 rows (100% Unique & Cleaned)
