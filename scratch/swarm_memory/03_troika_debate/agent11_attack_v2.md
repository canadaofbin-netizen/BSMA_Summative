# Agent 11 (Devil's Advocate) - Attack on Agent 10's Implementation v2

**Position:** Agree with the User's mediation, but strongly critique Agent 10's naive approach to enforcement.

**The Critique:**
While the User is absolutely correct that `13team` is a universal verification assistant and NOT a data extraction tool, Agent 10's likely proposal—simply adding a rule that "bans" `13team` from extracting data—is operationally insufficient and brittle. A static ban does not survive contact with ambiguous user prompts. 

What happens when a user submits a prompt like *"Analyze this paper"* or *"Verify the metrics in this study"*? The boundary between "verify" and "extract" is incredibly porous. If we just tell `13team` "don't extract," it will inevitably stumble into extraction-like behavior while trying to fulfill an "analysis" or "verification" request because it lacks a clear structural alternative. A ban without a routing mechanism is a dead end.

**The Solution: Strict Operational Guardrails (The Handoff Protocol)**

To enforce this boundary systemically, we must implement a **Handoff Protocol** rather than just a passive ban. `13team` must be explicitly programmed with an operational workflow to detect, intercept, and delegate extraction tasks.

1. **Trigger Recognition:** `13team` must be trained to recognize extraction-adjacent verbs in user prompts (e.g., "analyze," "gather," "pull," "find metrics," "extract").
2. **The Handoff Protocol:** When an extraction-adjacent trigger is detected, `13team` is strictly forbidden from processing the text itself. Instead, it must instantly act as a router:
    * It must invoke the `invoke_subagent` tool to deploy the specific extraction pipeline (e.g., the `extract_measures` skill).
    * `13team` then waits for the extraction pipeline to return the structured JSON.
3. **Post-Extraction Verification:** Only *after* the extraction pipeline returns the structured data does `13team` resume its intended role: verifying the extracted data against the source, running QA validation, and orchestrating debate if anomalies are found.

**Conclusion:**
We don't just ban `13team` from extracting data; we must architecturally wire `13team` to become the *trigger* for the extraction pipeline when confronted with raw papers. The boundary is maintained not by a rule, but by a rigid delegation workflow.
