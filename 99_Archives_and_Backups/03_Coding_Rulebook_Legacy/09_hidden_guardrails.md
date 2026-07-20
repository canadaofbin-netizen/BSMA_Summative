# Hidden Guardrails: Nuanced Exclusion Criteria

This document formally captures the nuanced, "hidden" criteria that human coders historically applied to exclude papers that technically measured boundary-spanning but failed to meet specific contextual requirements. 

These rules must be applied during the Include/Exclude screening phase.

## 1. The Student Sample Ban
**Rule:** Exclude the paper if the sample consists of students (e.g., MBA students, undergraduates) participating in simulations, coursework, or academic team projects.
**Rationale:** The meta-analysis requires real-world organizational employees. Boundary spanning in an academic setting lacks the external validity required for our organizational context.
* **Example Case:** `BSMA0325` (Lanaj & Hollenbeck, 2015). This paper measures boundary spanning in self-managing teams, but the participants were MBA students. **Action: EXCLUDE.**

## 2. Purposive Action vs. Mere Communication
**Rule:** Exclude papers that merely measure "communication frequency" (e.g., how often someone emails or chats) without specifying a boundary-spanning purpose.
**Rationale:** Boundary Spanning Behavior (BSB) requires intentional, purposive actions (e.g., seeking resources, scanning for information, coordinating tasks). Measuring communication frequency regardless of purpose causes severe construct contamination. **Action: EXCLUDE (Code 1).**

### 2a. VALID Network BSB (Do NOT Exclude)
The following network-based measures ARE purposive and represent valid BSB:
- **(a)** Advice-seeking network degree centrality (asking for work-related advice across boundaries)
- **(b)** E-I index measuring cross-boundary contacts for knowledge exchange
- **(c)** Ego-network heterogeneity based on purposive boundary-spanning ties (e.g., seeking expertise from other units)

### 2b. INVALID (Exclude under Code 1)
- **(a)** Pure email/phone/chat frequency counts without purposive content
- **(b)** Percentage of time spent with outsiders without specifying action type
- **(c)** Sociometric sensor data measuring mere proximity or speaking events
- **(d)** Burt's structural constraint measures

## 3. Illusion of Data (Moderators & Residuals)
**Rule:** Exclude papers where BSB is only used as a moderator to split a sample (Spanners vs. Non-spanners) or if the reported correlations are explicitly between BSB and *regression residuals* (predictive errors).
**Rationale:** Meta-analysis requires direct, zero-order correlations between BSB and substantive antecedents/consequences. Correlations with predictive errors yield no extractable effect size. **Action: EXCLUDE (Code 1).**

## 4. Adaptive Selling is NOT BSB
**Rule:** Exclude papers that measure "Adaptive Selling" or "Flexibility" (e.g., Spiro & Weitz ADAPTS scale) as their sole boundary-spanning proxy.
**Rationale:** Adjusting a sales pitch to suit a customer is a distinct sales tactic/personality trait, not a purposeful inter-organizational or inter-unit boundary-spanning behavior. **Action: EXCLUDE (Code 1).**

## 5. Survey Referent / Key Informant Guardrail
**Rule:** Exclude papers where the survey items use a collective referent like "We", "Our team", or "My organization" rather than "I", even if the sample consists of individuals.
**Rationale:** Respondents are acting as Key Informants to evaluate a macro-level construct, violating the individual-level boundary spanning requirement. **Action: EXCLUDE (Code 3).**

## 6. Leader BSB Override (AGENTS.md Rule 16) — CHECK FIRST
**Rule:** If a study measures a leader or manager's boundary spanning behavior as rated by their subordinates, **INCLUDE** the paper.
**Rationale:** Leader BSB IS BSB. The construct (boundary spanning) is valid regardless of who rates it. Code 1 applies only when BSB itself is absent (e.g., Work-Family management, Adaptive Selling). Cross-entity rating does not invalidate the construct. This rule takes absolute precedence over any "Cross-Entity Trap" exclusion logic.
**MANDATORY SEQUENCING:** Before applying ANY exclusion rule, agents MUST first check whether Rule 16 or Rule 17 applies. If the paper qualifies, it is INCLUDED — no further exclusion logic may override.
**N=Leaders=N=Teams Exception:** When exactly one leader exists per team, the effective N for BSB is N_leaders (individual-level), NOT N_teams (team-level). Do not apply Code 3 to such designs.

## 7. Intra-Organizational BSB Override (AGENTS.md Rule 17) — CHECK FIRST
**Rule:** If a study measures boundary spanning across internal organizational boundaries (e.g., cross-functional teamwork, IT↔Business knowledge sharing, advice-seeking networks across departmental boundaries), **INCLUDE** the paper.
**Rationale:** Intra-organizational BSB IS BSB. The construct is valid regardless of boundary direction (internal vs. external). Code 1 applies only when BSB itself is absent. Do not exclude a paper simply because the focal employee interacts with other internal departments rather than external organizations.
**Network Degree Centrality Exception:** Ego-network measures (e.g., degree centrality of advice-seeking ties across unit boundaries, E-I index) represent purposive intra-organizational boundary spanning and MUST BE INCLUDED.
