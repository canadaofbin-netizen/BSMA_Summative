# 10. 13-Agent Swarm OS (13team)

This document mirrors the core principles defined in the `13team` skill (`.agents/skills/13team/SKILL.md`).

## The 13-Agent Architecture
The system operates on a 5-layer framework designed for 0% error-rate task execution through distributed intelligence:

1. **Command & State Layer:** The main agent acts as the Orchestrator, delegating tasks and relying on persistent disk memory (files) rather than chat history for state management.
2. **Physical Concurrent Execution:** Worker subagents (`DataEngineer`, `Scout`, `Architect`, etc.) are spawned in parallel via `invoke_subagent` to perform the actual labor simultaneously.
3. **Verification & Audit:** `Fact_Checker` / `QA_Auditor` subagents are deployed to rigorously critique and audit worker outputs before acceptance.
4. **Auto-Evolution & Debate (The Troika):** Upon failure, an intervention squad of three subagents (`System_Reflector`, `Rule_Validator`, `Consensus_Builder`) is activated to debate the issue and reach a theoretically sound consensus.
5. **DNA Update Layer (Self-Evolution):** The consensus reached by the Troika is permanently written back into the core logic files (`AGENTS.md` or `SKILL.md` and this Rulebook) to prevent future occurrences of the same failure mode.

## The Dynamic Tuning Philosophy
The `13team` skill is deliberately maintained as an abstract structural framework. It defines the workflow (e.g., Orchestrator -> Parallel Workers -> Shields -> Troika) but does not hardcode the exact prompts for each subagent. 
When the Orchestrator is invoked, it dynamically reads the current project rules (`AGENTS.md`) and the user's immediate context to generate tailored instructions for the subagents on the fly. This ensures the Swarm OS remains infinitely reusable across different tasks (e.g., data extraction, code refactoring) without requiring manual updates to the skill files.
