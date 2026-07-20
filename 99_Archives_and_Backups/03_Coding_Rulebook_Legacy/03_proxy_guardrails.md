# Rule 28: Proxy Guardrail (Firm-Level Informants)

## Rationale
In meta-analyses of organizational behavior, boundary spanning is strictly defined as an **interpersonal behavior performed by an individual employee** (e.g., a frontline worker interacting with a customer, or a team member interacting with another team).

However, many papers in strategic management and marketing survey individuals (like CEOs, Branch Managers, or Lead Sales Representatives) but use them as **Key Informants (Proxies)** to measure a firm-level or team-level construct. 

## The Guardrail
**Even if the survey respondent is an individual (e.g., a manager), if the measured construct represents the "firm's external relationships," "organizational alliances," or "B2B integration," it MUST BE EXCLUDED.**

### Example Case: BSMA0099
* **Paper:** "Bridging the Gap: Managers' External Relationships and Their Effects"
* **Trap:** The paper repeatedly talks about "managers' external relationships," which sounds like individual-level boundary spanning.
* **Reality:** The manager is acting as a proxy for the *firm's* external network and strategic alliances. The analysis is effectively at the firm level.
* **Correct Action:** EXCLUDE.

## Application for Coders and AI
When extracting data, always ask:
1. Is this behavior about the individual's own job performance / role? (-> Include)
2. Or is the individual answering on behalf of the entire company/branch's relationships with other companies? (-> Exclude)
