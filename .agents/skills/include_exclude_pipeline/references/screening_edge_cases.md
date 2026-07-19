# Screening Edge Cases Reference

> **Note:** This file is an ON-DEMAND reference meant to supplement the core screening rules found in `screening_rules_core.md`. Use this document when encountering ambiguous cases.

## Trap Warning Quick-Reference Index

| Trap | Parent Rule (Tier) | Action |
|---|---|---|
| 1:1 Matched Dyad Safe Harbor | Rule 4 (Tier 2) | Do NOT apply Code 3 |
| AI Tool Interaction | Rule 4 (Tier 2) | Exclude — Code 1 |
| SEM-only Data Warning | Rule 7 (Tier 0) | Exclude — Code 1 |
| Implanted Boundary Spanner | Rule 2 (Tier 1) | INCLUDE |
| Leader BSB Trap (Blau's index) | Rule 1 (Tier 1) | Exclude — Code 1 & 3 |
| N=Leaders=N=Teams | Rule 1 (Tier 1) | INCLUDE (individual-level) |

## Detailed Edge Case Explanations

### 1:1 Matched Dyad Safe Harbor
If a study uses 1-to-1 matched pairs (e.g., 1 expatriate paired with exactly 1 coworker) and each individual appears only once in the dataset, statistical independence IS preserved. Do NOT apply Code 3. Only apply Code 3 when N = relationships (e.g., 87 individuals generating 673 dyadic ties).

### AI Tool Interaction Exclusion
BSB must be an interpersonal, human-to-human behavior. If the "boundary spanning" measured involves using Generative AI tools (e.g., ChatGPT) to gather information, this is human-computer interaction and lacks BSB construct validity → Exclude under Code 1.

### SEM-only Data Warning
If a paper relies entirely on SEM path coefficients and does NOT provide a zero-order correlation matrix (even latent), it must be excluded for lacking extractable effect sizes. Do NOT confuse partial rectangular cross-correlation tables with full square correlation matrices.

### Implanted Boundary Spanner / Knowledge Exchange
If a study's sample consists of employees whose job role is boundary spanning (e.g., logistics implants on-site at client facilities, expatriates) AND the study measures their knowledge exchange, coordination, or information-sharing behavior with the partner organization, this IS a valid BSB construct → INCLUDE. Do NOT exclude just because the paper labels it "knowledge exchange" instead of "boundary spanning behavior".

### Leader BSB Trap (Blau's index)
Do NOT be fooled by the label "Boundary-spanning leadership". If the items measure internal demographic diversity management (e.g., bridging age gaps within a branch using Blau's index), it is inclusive leadership, NOT structural BSB → Exclude under Code 1 & 3.

### N=Leaders=N=Teams Exception
When exactly one leader exists per team, the effective N for BSB is N_leaders (individual-level), NOT N_teams (team-level). Do not apply Code 3 to such designs.

### Time Allocation Trap
If the study measures only the *percentage of time* a salesperson devotes to customers/supervisors (without purposive BSB actions like scanning or representation), it is NOT BSB → Exclude under Code 1. The word "boundary-spanning" used as an adjective for the sample does not make it BSB.

### PLS-SEM Dyadic Trap
If a study uses PLS-SEM with degree-symmetric dyadic consensus variables where N = relationships (not individuals), it violates statistical independence → Exclude under Code 3. Also watch for nested data (e.g., N=158 managers in 58 projects) where project-level outcomes are duplicated.

### CEO BSB Exception
If a CEO rates their OWN individual boundary spanning behavior using "I" referent items (e.g., "I solicit information from external channels") and N=firms=N=CEOs (one respondent per firm), this is valid individual-level BSB → INCLUDE. Do not confuse with firm-level alliance studies.

### Network-Based BSB Inclusion
If a study measures cross-boundary ties using a network generator that asks about purposive actions (e.g., "who do you go to for information or knowledge on work-related topics"), the resulting network variables (bridging ties, cross-boundary contacts, degree centrality) ARE valid BSB operationalizations → INCLUDE. Do NOT exclude simply because BSB is measured via SNA rather than a Likert scale. ONLY Burt's structural constraint is explicitly invalid.

### Rule 5 vs Rule 6 Edge Case (Cross-Departmental Communication)
Cross-departmental communication frequency (e.g., how often employees email members of other departments) without specified purposive boundary-spanning action is merely communication, not purposive BSB. This is an invalid construct and should be excluded under Code 1.
