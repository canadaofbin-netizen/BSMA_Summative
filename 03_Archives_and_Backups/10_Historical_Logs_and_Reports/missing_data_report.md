# Missing Data Report (Final Restructured)

This report categorizes the entire Boundary Spanning Meta-Analysis dataset into three distinct types based on their current status and exclusion logic.

> [!IMPORTANT]
> **Total Original Dataset: 736 articles**

## 1️⃣ Type 1: Successfully Downloaded Papers (Include Pool)
**Count: 625 articles**

These papers have been successfully downloaded, cross-checked with the Excel list, and securely stored in the `PDFs` folder. 
- The filenames have been standardized to `[ID] Author (Year).pdf`.
- 14 duplicate files were successfully cleaned out from the folder, ensuring exactly 625 unique, perfectly matched PDFs.
- These form the core dataset ready for full-text coding.

## 2️⃣ Type 2: Excluded Duplicate Papers (Exclude Pool)
**Count: 4 articles**

These articles were part of the original 736 list provided by the professor but were excluded to form the final 732 working list. They were removed because they were duplicate entries of the same study.

**Identified Duplicated Studies:**
1. *Boundary Role Spanning Behavior, Conflicts and Performance of Industrial Product Managers* (Lysonski & Woodside, 1989)
2. *Group, Task, and Personality Correlates of Boundary-Spanning Activities* (Keller et al., 1976)
*(Note: These titles appeared multiple times in the original raw data and were deduplicated to prevent double-counting).*

## 3️⃣ Type 3: Full Missing Data (Exclude Pool)
**Count: 107 articles**

These are the remaining articles from the 732 working list that have not been downloaded. Depending on the research criteria, these can be explicitly documented as the "Exclude Pool" due to full-text unavailability.

**Breakdown of the 107 Missing Papers:**
- **Zotero Target Papers (DOI Present)**: 49 articles with valid DOIs that are blocked by strict anti-scraping walls (e.g., SSRN, ProQuest). These require manual download via institutional access.
- **Ghost Papers (DOI Missing)**: 48 articles lacking formal DOIs, such as old conference proceedings, dissertations, and fragmented citations. These are extremely difficult to locate and are strong candidates for the Exclude Pool if manual Google Scholar searches fail.
- **Completely Inaccessible Papers**: 10 articles that are confirmed to be completely inaccessible through any online/institutional databases (including IDs 6, 78, 271, 357, 387, 404, 593, 597, 603, 730).

> [!NOTE]
> For a detailed, item-by-item list of these 107 missing papers, please refer to the `undownloadable_papers.pdf` file saved in your Google Drive.
