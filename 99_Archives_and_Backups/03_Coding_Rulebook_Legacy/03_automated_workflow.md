<details>
<summary><h2>Automated Extraction Features (4-Node Hybrid Architecture)</h2></summary>

To ensure the highest level of accuracy and speed, all AI coding assistants must follow the **4-Node Hybrid Cartesian Workflow**. The monolithic extraction process is replaced by a decentralized, double-circuit-breaker system.

**Step 0: Pre-Triage — Read Casebook**
- **Objective:** Before making any inclusion/exclusion decision, the agent MUST read `.agents/skills/batch_processor/triage_casebook.md` in full. Apply established precedents to the current paper. Note: Inclusion/Exclusion and Bibliometrics (Title, Author, N) are now handled manually prior to the extraction pipeline. The AI focuses purely on empirical variable pairs.

**Step 1: 4-Node Parallel Extraction (Delayed Classification)**
- **Objective:** Prevent LLM hallucination and cognitive overload by assigning specialized tasks to 4 concurrent subagents.
- **Node 1 (Pre-flight Triage):** Scans the Methodology section to identify Longitudinal/Time-lag flags.
- **Node 2 (Footnote Scanner):** Scans table footnotes to flag partial correlations (`is_partial_mixed`) or missing data imputations (`is_imputed`).
- **Node 3 (Table Parser):** Extracts pure zero-order statistics (r, Mean, SD) and associates them with a `table_anchor_name` (UPK). Demographic variables (Age, Gender, Tenure) are completely DROPPED to save costs.
- **Node 4 (Text Analyzer):** Extracts the "Specific Measure" text and classifies the variable as 'Boundary Spanning (BS)' or 'Non-Boundary (NB)' based on explicit inter-boundary interaction. Objective/Formative indicators must force reliability to `Not_Applicable`.

**Step 2: Python Cartesian Inner Join ($N \times M$)**
- **Objective:** Eliminate mathematical hallucination. The LLM does NOT map pairs. 
- **Action:** The master orchestrator executes `universal_excel_inserter.py`. The Python script fuzzy-matches Node 3 and Node 4 outputs via `table_anchor_name`. It then calculates the Cartesian product of all [BS] and [NB] variables to form complete pairing rows.
- **Circuit Breaker:** If a fuzzy match fails, a `[JOIN_FAILURE]` exception is raised, and the paper is aborted and sent to human review.

**Step 3: Validator (Critic) Cross-Verification**
- **Objective:** Prevent arbitrary data alteration.
- **Rules:** The Validator enforces the Strict Substring Rule (verbatim quotes only), checks Node 3's reasoning for partial matrices, and ensures objective variables have no hallucinated Alpha scores. A paper failing 3 times is marked `PERMANENT_FAIL`.

**Step 4: 4-Sheet Isolated Routing**
- **Objective:** Preserve zero-order metric purity.
- **Action:** Based on the flags extracted in Step 1, Python routes the Cartesian pairs into one of four physically isolated sheets in the Master Excel file: `Raw_Metrics`, `Transformed_Metrics`, `Imputed_Metrics`, or `Salami_Review_Queue`.

**Step 5: Zero-Agent Dependency Automated Backup**
- **Objective:** Never lose data or provenance.
- **Action:** Immediately after Step 4, the `backup_manager.py` script automatically zips the database state into `99_Archives_and_Backups/02_Database_Milestones` without requiring explicit agent instruction.

</details>
