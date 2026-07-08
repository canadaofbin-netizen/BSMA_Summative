# Refined Pipeline Rules

Initial logic and parameters are validated.

## Core Transformation

### 1. Zero Guesswork Policy
* Never guess or impute numbers. Describe ambiguities in "Notes" and add `[FLAGGED]`.
* Copy measure descriptions exactly.
* Explicitly write minimum and maximum scores (do not infer).

### 2. Exclusion Priority & Rules
* **Exclusion Priority:** Identifying exclusions is the top priority. Skip full extraction if excluded.
* **Option 3 Update:** Option 3 is strictly "non-individual level".
* **Dyadic Data:** Focus on the focal sample. Ignore demographics of non-focal samples.

### 3. Workflow Adjustments
* **Confirm Before Inject:** Extract data -> save in memory -> present plan -> wait for confirmation -> inject.
* **Automated GitHub Backups:** Automatically sync updates to the GitHub repository.

### 4. Excel Formatting Requirements
* **Blank Row Separation:** Leave exactly one blank row between papers.
* **Coder Identity:** Must be recorded as "KY".
* **Verbatim Evidence:** Follow strict format: `[Reason summary]. Verbatim Evidence: "<exact quote from PDF>"`.

### 5. Edge Cases Addressed
* **Non-Individual Anchors:** Explicit rules required for organizational/team-level spanning.
* **Scale Oddities:** Enter `999` for Number of Items and Reliability for single-item binary indices.
* **Latent Variables:** Meta-analysis focuses strictly on corrected or observed variables.
