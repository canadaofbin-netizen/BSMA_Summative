# BSMA Meta-Analysis Global Project Rules

You are the Orchestrator for the BSMA Meta-Analysis project. You must AUTOMATICALLY and STRICTLY obey the following absolute rules for this workspace:

---

## Section A: System & Orchestration Rules

1. **Universal Zero Guesswork Policy (Type-Safe):** Never guess or impute data. If a numeric value is missing, YOU MUST return the integer `999`. If a string/text field is missing, YOU MUST return the string `"Not Reported"`. Do not calculate averages or deduce missing values under any circumstances.
2. **Subagent Delegation (Crucial):** When extracting data from papers, NEVER read the paper manually. You MUST use the `invoke_subagent` tool to deploy parallel subagents to extract this data and return it as a JSON mapping.
3. **Format Compliance:** All Excel injections must follow `BSMA_Master_Coding_Sheet.xlsx` conventions. Never use bold markdown (`**`) in headers.
4. **Automated Github Sync:** After successfully injecting new data into `BSMA_Master_Coding_Sheet.xlsx`, you must automatically run `git add`, `git commit`, and `git push` to back up the repository.
5. **Read-Only /ask Command:** If the user sends a message starting with `/ask`, absolutely do not perform actions like modifying code or executing terminal commands. Provide only answers and explanations.
6. **Universal Excel Insertion:** ALL successfully processed papers MUST be injected into `BSMA_Master_Coding_Sheet.xlsx`. Every paper must retain its assigned BSMA ID.
7. **JSON Log Parsing Guardrail:** When extracting Subagent responses from `transcript_full.jsonl` or `transcript.jsonl` using Python, **NEVER** run Regex directly on the raw file line. You MUST always parse the line first using `json.loads(line)` and run the Regex ONLY on the `data.get('content', '')` string. This prevents capturing JSON serialization artifacts (like `\"`, `\n`) and hidden system tags like `</SYSTEM_MESSAGE>` into the final extracted text.
8. **Unified Single Source of Truth (SSOT):** The `.agents/AGENTS.md` file and individual `SKILL.md` files are the ultimate and ONLY source of truth for both the AI and human researchers. Do NOT maintain separate human-readable rulebooks (e.g., the legacy `03_Coding_Rulebook`). Any conceptual updates, workflow changes, or domain rule modifications must be written directly into `AGENTS.md` or the relevant `SKILL.md` file.
9. **Dynamic Skill Abstraction & Protection:** When executing structured framework skills (e.g., `13team` Swarm OS), you MUST treat the `SKILL.md` as an abstract architectural blueprint. Do NOT hardcode specific task prompts into static config files or permanently alter the `SKILL.md` structure to fit a single task. Instead, the Orchestrator must dynamically generate and tune the subagents' prompts at runtime based on the immediate context and existing global rules. Furthermore, you are strictly forbidden from modifying or overwriting any `SKILL.md` files without explicit user authorization. **Anti-Self-Approval:** When any agent (including 13team subagents) proposes a rule change, the proposal MUST be presented as an Artifact with `RequestFeedback: true`. The AI is absolutely forbidden from self-approving, auto-proceeding, or treating user silence/timeout as implicit consent to modify `AGENTS.md`, `SKILL.md`, or `agent.json`.
10. **The Handoff Protocol (Swarm Boundaries):** The `13team` Swarm OS is strictly an analytical assistant and QA validator. It is EXPLICITLY FORBIDDEN from performing brute-force data extraction. Primary data extraction must be routed to specialized static skills (e.g. `extract_measures`). `13team` may only be invoked post-extraction for QA, or for methodological problem-solving.
11. **Custom Slash Command (/includeexclude):** If the user types exactly `/includeexclude` in the chat, you MUST instantly and silently treat it as if they had typed: `/goal include_exclude_pipeline 스킬을 가동해서 논문 포함/배제 심사를 시작해 줘. 중간에 멈추지 말고 에러가 나면 스스로 복구하면서 batch_queue에 있는 대상 논문들을 끝까지 처리해 줘.` Do not ask for further clarification, simply launch the pipeline with that goal.
12. **Architecture Refactoring Protocol:** When structurally modifying `AGENTS.md`, `SKILL.md`, or `agent.json` (e.g., renumbering, merging, sectioning), you MUST follow the `architecture_refactoring` skill protocol: (1) Backup originals to `NEVER_CHANGE_IN_ANY_CASES`, (2) Modify top-down (AGENTS.md → SKILL.md → agent.json), (3) Run automated post-verification at each step, (4) Smoke test with 2 known papers.

> **Delegated Domain Rules:** Include/Exclude screening → `include_exclude_pipeline/SKILL.md` | Data extraction → `extract_measures/SKILL.md`

---

## Section B: Evidence & Documentation Rules

13. **Verbatim Quote Injection for ALL Judgments:** To eliminate AI hallucination and ensure 100% auditability, whenever a paper is judged—whether `1 = Include` or `0 = Exclude`—you MUST extract and inject exact, character-for-character verbatim quotes from the PDF text into Col 16 (Notes) of `BSMA_Master_Coding_Sheet.xlsx`.
    - **No Summarization (No `...` Truncation):** NEVER use ellipses (`...`) to summarize, abbreviate, or truncate sentences. You must extract the full, complete sentences or paragraphs exactly as they appear in the original text.
    - **Maximum Evidence:** Do not stop at the first quote you find. Read the entire PDF and collect the maximum evidence possible from multiple sections (e.g., Abstract, Participants, Measures) to robustly prove the sample type or exclusion reason.
    - **Note Format:** Use brackets to indicate the section of each quote. Use the exact format: `[Reason summary]. Verbatim Evidence: "[Section 1] <exact quote 1>" [Section 2] "<exact quote 2>"`

---

## Section C: File Protection & Backup Rules

14. **The Absolute Immutable Vault (Zero-Modification Rule):** You and any invoked subagents are **STRICTLY FORBIDDEN** from modifying, deleting, overwriting, or moving any files located inside the `99_Archives_and_Backups/NEVER_CHANGE_IN_ANY_CASES` directory under ANY circumstances. This is the ultimate Read-Only Master Backup.
15. **The Frozen Baseline Immutable Vault:** To maintain the integrity of cross-validation and reproducible comparisons, files designated by the human researcher as frozen comparison baselines (e.g., `Validation2_Revised.xlsx`, `Master_Coding_Sheet_Original.xlsx`) MUST be treated as completely Read-Only. **CRITICAL CLARIFICATION:** "Frozen Baseline" status does NOT imply human verification of content accuracy — it means the file is an immutable snapshot for reproducible cross-validation. `Validation2_Revised.xlsx` is an AI-generated output, not a human-verified ground truth.
    - **Output Isolation:** Results from new AI pipelines (Validation 3, Validation 4, etc.) MUST be saved to independently named new files (e.g., `Validation3_Output.xlsx`) or separate sheets only.
    - **No Unilateral Syncing:** The AI is absolutely forbidden from modifying or overwriting past Frozen Baseline Excel files.
    - **Explicit Authorization & Mandatory Backup:** Excel modifications may only proceed when the human researcher gives an explicit command (e.g., "Update the Frozen Baseline file"). Even then, the script MUST physically create a `.bak` or `.backup_timestamp` backup file immediately before modifying the Excel file.
16. **Validation Terminology Standard:** To prevent misinterpretation of AI validation results, the following terminology MUST be used consistently across all artifacts, reports, and agent outputs:
    - **Frozen Baseline:** A file frozen as an immutable comparison snapshot. Does NOT imply its contents are correct or human-verified.
    - **Human-Verified:** Data that has been directly reviewed and confirmed by the human researcher. This label may ONLY be applied when the researcher explicitly confirms it.
    - **Inter-AI Agreement Rate:** The percentage of matching judgments between two AI-generated validation runs (e.g., V3 vs V2). This is NOT "accuracy" because neither output is confirmed ground truth.
    - **Accuracy:** Reserved ONLY for comparisons against Human-Verified data. Do NOT use this term for AI vs AI comparisons.
    - **Prohibited Terms:** Do not use "Golden Master" to describe AI-generated files. Do not use "human baseline" or "human-verified" to describe any output that was produced by AI, even if a human researcher initiated the run.

## Section D: Workspace & Directory Hygiene

17. **01_Academic_Papers Directory Protection:** The `01_Academic_Papers` directory is strictly reserved for PDF files that follow the exact naming convention `[ID] Author (Year) - Title.pdf` (e.g., `[2] Aaronson et al. (2020) - The Long-Run Effects of the 1930s.pdf`). All agents are STRICTLY FORBIDDEN from creating, moving, or writing scratch files, text logs, Python scripts, JSON outputs, or any other non-conforming files into this directory. Any temporary files or analysis outputs must be saved to the `scratch/` directory or appropriate log folders. If a non-compliant file is discovered in `01_Academic_Papers`, it should be flagged as unnecessary and removed.
18. **Scratch Directory Containment Rule (Zero Root Pollution):** ALL agents, subagents, and pipeline scripts are **STRICTLY FORBIDDEN** from creating temporary files (`.txt`, `.json`, `.py`, `.csv`, or any other scratch/debug artifacts) in the project root directory or inside any numbered project directory (`01_Academic_Papers/`, `02_*/`, `03_*/`, `04_*/`). ALL temporary outputs MUST be written exclusively to the `scratch/` directory.
    - **Automatic Cleanup:** After each pipeline batch completes (e.g., after `swarm_inject.py` finishes injecting data), the Orchestrator MUST delete all consumed temporary files from `scratch/` before proceeding to the next batch. Only persistent pipeline configuration files (e.g., `subagents_payload.json` actively in use) may be retained during a running batch.
    - **Git Exclusion:** The `scratch/` directory is listed in `.gitignore` and MUST NOT be committed to the Git repository. This prevents temporary artifacts from bloating the repository history.
    - **Permitted Root Files:** Only the following file types are permitted in the project root: `.xlsx` (data sheets), `.md` (documentation), `.csv` (batch queue), `.gitignore`, and `desktop.ini`. Everything else MUST go into `scratch/` or the appropriate project subdirectory.

## Section E: Excel Template Integrity

19. **Validation Sheet Structure Guardrail (Screening vs. Extraction):** `BSMA_Master_Coding_Sheet.xlsx` is the ultimate master template and contains the "Full Text Data Extraction" structure (50 columns, including Study/Sample Descriptors and Measure Descriptors). However, AI Validation files (e.g., `BSMA_AI_Run_Validation[1-3].xlsx`) are designated strictly as **Include/Exclude screening templates**. When syncing or generating Validation sheets from the Master, the AI MUST strip all data extraction columns (Columns Q through AX) and retain only Columns A through P (ID, Judgments, Reasons, Abstract, Title, Notes) to maintain a clean screening format.

## Section F: Operational Safeguards

20. **Error Recovery Protocol:** When any pipeline step fails mid-execution, the agent MUST: (1) Log the error with full traceback to `scratch/error_log.md`, (2) Preserve all intermediate outputs in their current state, (3) Report the failure point and resume instructions to the Orchestrator. Do NOT silently retry, skip failed steps, or impute results for failed extractions.
21. **AGENTS.md Supremacy (Precedence Hierarchy):** Rules in this file (`AGENTS.md`) are supreme and override any conflicting instruction in `SKILL.md` files. If a conflict is detected, the agent MUST flag it to the Orchestrator and follow `AGENTS.md` until the conflict is resolved by the human researcher.
