---
name: validator
description: A Critic subagent that cross-checks extracted Data JSON against the Data Integrity Rules.
---

# Validator Subagent (Critic)

The `validator` skill allows you to spawn a subagent dedicated to reviewing extraction output. It serves as a strict quality control layer before any data touches the Master Excel Sheet.

## 1. Invocation
- Use `invoke_subagent` to spawn a subagent with the `self` or `research` type.
- Provide the generated **Merged JSON payload** and the original **Correlation Table / Methodology Text** from the paper to the subagent.

## 2. Validator Prompt Instructions
Instruct the Validator to explicitly check for the following 3 Core Integrity points (15-Round Architecture Rules):

1. **Verbatim Fidelity (Strict Substring Rule):** Cross-check the extracted `specific_measure` texts from Node 4 against the `'source_quote'` field. The `specific_measure` MUST be an exactly identical, unmodified substring of `source_quote`. Reject the extraction immediately (`REJECT_RETRY`) if the Extractor altered any words, paraphrased, summarized, or if the exact source quote is missing.
2. **Partial Mixed Matrix Deep Evaluation:** If Node 2 raised `is_partial_mixed: true`, you MUST evaluate Node 3's `<matrix_reasoning>` block. If Node 3 logically proves it extracted ONLY from the pure Zero-Order half of the matrix (e.g., lower diagonal), allow it to PASS. If Node 3 extracted from the partial correlation side, return `REJECT_RETRY`.
3. **Formative/Objective Reliability Hallucination:** If the `measure_name` refers to an objective demographic (e.g., Age, Firm Size) or a Formative construct, verify that `reliability.type` is exactly `"Not_Applicable"`. If the LLM hallucinated a number or set it to `"Not_Reported"`, return `REJECT_RETRY`.

*(Note: Zero Guesswork on numbers still applies; missing numeric fields must be `999`.)*

## 3. Reflection & Correction Loop (Strict Circuit Breaker)
- If the Validator returns `PASS`, the Orchestrator will proceed to Excel Injection.
- If the Validator returns `REJECT_RETRY` (for formatting issues, zero-guesswork violations, verbatim fidelity, formative reliability mismatches), halt Excel Injection. Pass the feedback to the Extractors and retry.
  - **MAX 3 RETRIES (CRITICAL):** You MUST NOT exceed 3 validation retries. If the payload still fails validation after 3 attempts, abort extraction and mark as `PERMANENT_FAIL`.
- If the Validator returns `FATAL_REJECT` (e.g., Construct Homonymy), DO NOT RETRY. Abort immediately. Mark the paper as `PERMANENT_FAIL` in `batch_queue.csv`, log the Validator's exact failure reason in `error_log.md`, and proceed to the next paper.
