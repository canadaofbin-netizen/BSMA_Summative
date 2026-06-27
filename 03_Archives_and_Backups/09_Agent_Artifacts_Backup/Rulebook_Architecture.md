# Detailed Rulebook Network Architecture

The AI extraction process is governed by an interconnected network of 9 Markdown files located in `05_Coding_Rulebook`. Unlike standard conversational AI, the orchestrator agent and its subagents are hard-wired to consult these documents logically based on the phase of extraction and the type of data encountered.

## Rulebook Interdependency Map

```mermaid
graph TD
    %% Base Philosophy Layer
    R0[00_core_process.md<br/><b>Core Philosophy</b><br><i>"Zero Guesswork & Stop on Ambiguity"</i>]
    
    %% Process Layer (The Pipeline)
    R3[03_automated_workflow.md<br/><b>The Orchestrator Pipeline</b>]
    R0 --> R3
    
    %% Data Type Handlers (Triggered by R3 during Step 1)
    subgraph Data Type Resolutions
        R1[01_dyadic_data_rules.md<br/><b>Dyadic/Multi-source</b><br><i>Anchor Identity & Self vs. Others mapping</i>]
        R2[02_sem_and_latent_rules.md<br/><b>Latent Variables</b><br><i>Handling SEM composites & Measurement Models</i>]
        R6[06_non_individual_anchors.md<br/><b>Macro Levels</b><br><i>Team & Organization level Boundary Spanning</i>]
    end
    
    R3 -- "Step 1: Analyzes Data Structure" --> R1
    R3 -- "Step 1: Analyzes Data Structure" --> R2
    R3 -- "Step 1: Analyzes Data Structure" --> R6
    
    %% Edge Case Handlers (Triggered during Step 1 & 1.5)
    subgraph Exception Handlers
        R4[04_general_exceptions.md<br/><b>General Edge Cases</b><br><i>Mathematical impossibilities & Missing N</i>]
        R7[07_scale_oddities.md<br/><b>Measurement Oddities</b><br><i>Reverse scoring, 1-item alphas, unknown scales</i>]
    end
    
    R1 -. "Conflicts trigger" .-> R4
    R2 -. "Conflicts trigger" .-> R4
    R3 -- "Step 1.5: Subagent Scale Extraction" --> R7
    
    %% Output Handlers (Triggered during Step 2)
    R8[08_data_entry_formatting.md<br/><b>Formatting Rules</b><br><i>Excel Column IDs, Blank row spacers, '999' flags</i>]
    
    R3 -- "Step 2: Excel Injection" --> R8
    R4 -. "Forces '999' output" .-> R8
    R7 -. "Forces '999' output" .-> R8
    
    %% Metacognition Layer
    R5[05_document_management.md<br/><b>Rulebook Governance</b><br><i>How the AI updates these very rules</i>]
    
    R4 -. "[UNRECOGNIZED PARADIGM] resolved by User" .-> R5
    R5 --> R0
    R5 --> R1
```

---

## Detailed Component Breakdown

### 1. The Core Directives
*   **`00_core_process.md`**: The constitutional foundation. It explicitly bans the AI from "guessing" missing values (e.g., guessing Alpha = 1.0 just because it's a single item) and establishes the `999` rule for all missing data.
*   **`03_automated_workflow.md`**: The central pipeline the AI strictly executes:
    *   *Step 0*: Abstract Triage (Skip theoretical papers).
    *   *Step 1*: Metadata Shadow Report Generation.
    *   *Step 1.5*: Subagent Delegation (Parallelizing measurement scale extraction).
    *   *Step 2*: Excel Injection using Python.
    *   *Step 3*: Python Self-Verification.

### 2. Data Structure Handlers
When the Orchestrator hits Step 1, it must classify the paper. Depending on what it finds, it opens specific rule files:
*   **`01_dyadic_data_rules.md`**: If the paper involves multiple raters (e.g., Expatriates & Coworkers), this file dictates who is the "Anchor" (the Boundary Spanner). This is critical for deciding whether Report Type is `1 = Self` or `3 = Others`.
*   **`02_sem_and_latent_rules.md`**: If the paper uses Structural Equation Modeling (SEM), this file tells the AI how to handle correlation matrices that report latent construct correlations versus observed variables.
*   **`06_non_individual_anchors.md`**: If the paper is about *Team* Boundary Spanning (like Marrone 2007) or *Organizational* Boundary Spanning, this file dictates how to code the Anchor and sample size (e.g., N = Teams vs. N = Individuals).

### 3. Exception & Ambiguity Handlers
While Subagents extract data, they often find weird anomalies. They consult these files:
*   **`04_general_exceptions.md`**: Handles logic breaks, such as missing Pairwise N matrices, or text contradicting the tables. It establishes the `[UNRECOGNIZED PARADIGM]` flag, which forces the AI to stop and ask the user for help.
*   **`07_scale_oddities.md`**: Handles measurement weirdness. E.g., if an Alpha is missing, force `999`; if a scale is dichotomous (0/1), force Min=0, Max=1.

### 4. Output Formatting & Governance
*   **`08_data_entry_formatting.md`**: The strict schema map. It contains the exact 0-indexed column IDs used by the Python injectors (`v7_inserter.py`) to prevent off-by-one errors. It also dictates inserting a completely blank row between different papers for readability.
*   **`05_document_management.md`**: The "Metacognition" file. When the User solves an `[UNRECOGNIZED PARADIGM]`, this file instructs the AI on exactly how to open and edit the other `.md` files to permanently update the Rulebook so the AI learns from the human feedback.
