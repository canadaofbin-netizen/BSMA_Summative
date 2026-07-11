# Original User Request

## 2026-07-11T06:30:26Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Verify that the newly created `include_exclude_pipeline` SKILL exactly matches the logic and expectations of the underlying Python pipeline scripts in `05_Pipeline/1_Include_Exclude_Loop/`.

Working directory: g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY
Integrity mode: benchmark

## Requirements

### R1. Deep Verification via Dry Run
The agent team must perform both a static code analysis of the SKILL.md against the Python scripts AND a live dry run using a minimal mock batch (e.g., batch_size=2) to guarantee execution safety.

### R2. Verification Report
The team must output a detailed `Verification_Report.md` mapping each step of the SKILL to the exact corresponding Python execution logic.

## Acceptance Criteria

### Execution & Verification
- [ ] A dry-run of the pipeline is executed successfully without any Python exceptions.
- [ ] The mock batch successfully processes the 2 items and triggers Excel injection.
- [ ] `Verification_Report.md` is generated in the workspace root.
- [ ] The report explicitly maps the 4 steps of the `include_exclude_pipeline` SKILL against the Python pipeline, declaring a Pass/Fail for compliance.
