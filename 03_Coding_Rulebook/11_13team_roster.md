# 11. 13-Agent Swarm OS Individual Agent Roster (Universal Framework)

This document defines the 13 universal roles of the agents within the dynamic Swarm OS. These roles are dynamically spun up by the Orchestrator at runtime to tackle any complex task, from data extraction to code refactoring.

## Layer 1: Command
**1. Master Orchestrator (Agent 1)**
- **Role:** Your personal Chief of Staff (The primary AI).
- **Task:** Analyzes requests, dynamically crafts tailored prompts for the subagents based on the specific task (coding, extraction, writing, etc.), invokes them using `invoke_subagent`, and routes JSON/text files between memory folders.

## Layer 2: The Worker Swarm (Parallel Execution)
*These agents perform the heavy lifting simultaneously. Their exact domains flex based on the Orchestrator's prompt.*
**2. Data Engineer / Extractor**
- **Role:** Extracts raw data, numbers, or specific structures from files, databases, or PDFs.
**3. Scout / Researcher**
- **Role:** Reads large texts or codebases to understand context, summarize intent, or identify edge cases.
**4. Logic Parser / Coder**
- **Role:** Executes logical operations, writes/refactors code, or transforms data formats.
**5. Quality Assurance (QA) Analyst**
- **Role:** Conducts intermediate checks on the other workers' outputs against the task's specific constraints.
**6. Domain Specialist (Wildcard)**
- **Role:** Adopts the specific domain knowledge required for your current task (e.g., acts as the 'Inclusion Guard' for BSMA, or a 'Security Expert' for coding).

## Layer 3: Verification Shields (Output Integrity)
*These agents ensure the final output is flawless before it reaches you or the database.*
**7. Integrity Validator**
- **Role:** Checks for formatting errors, missing data, or syntax compliance.
**8. Logic Auditor**
- **Role:** Cross-checks calculations, logical steps, or structural coherence.
**9. Schema Compliance Checker**
- **Role:** Ensures the final output exactly matches the target schema (e.g., specific JSON structure, Excel columns, or Markdown formats).

## Layer 4: The Troika (Error Resolution)
*Only spawned if the Shields reject the output or a task crashes.*
**10. System Reflector**
- **Role:** Analyzes the failure log and proposes a fix or workaround.
**11. Rule Validator (Devil's Advocate)**
- **Role:** Aggressively challenges the Reflector's fix against the global `AGENTS.md` constraints to ensure no core rules are broken.
**12. Consensus Builder**
- **Role:** Mediates the debate and formulates a final dynamically adjusted prompt for a retry.

## Layer 5: Evolution
**13. DNA Injector (Git Manager)**
- **Role:** If the Troika decides a permanent system rule is needed to prevent future failures, this agent drafts the update to the Rulebook and pushes it to Git.
