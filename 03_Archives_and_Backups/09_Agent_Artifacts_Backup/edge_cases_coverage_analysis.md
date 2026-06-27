# Edge Cases Coverage Analysis

**Misleading SEM / Latent Correlation (205 papers):** ✅ **FULLY COVERED!** 
Our rulebook explicitly warns the coder to watch out for "Discriminant Validity" tables and clearly instructs them to enter `999` if raw, uncorrected Pearson $r$ correlations are missing.

**Dyadic or Multi-Source data (118 papers):** ✅ **FULLY COVERED!** 
Our rulebook explicitly has a 3-step guide for handling dyads, flipping the "Report Type" perspective to Self/Others relative to the Anchor, and filtering out cross-entity demographics.

**Non-Individual Anchors (209 papers):** ❌ **NOT COVERED!** 
The current `read.md` defines the Anchor as "the person performing the boundary-spanning behavior". If a paper measures boundary spanning for an entire Team, a Firm, or specifically a CEO, the AI coder would be confused and forced to halt under the `[UNRECOGNIZED PARADIGM]` rule. We need to write a new rule explicitly stating whether organizational/team-level boundary spanning should be included in this meta-analysis, and how to code their demographics (since firms don't have an "age" or "gender" in the same way individuals do).

**Scale Oddities / Binary Indices (78 papers):** ❌ **NOT COVERED!** 
You missed this fourth category in your message! 78 papers measure boundary spanning not with a survey, but with a 0/1 binary index (like Comacchio 2011). `read.md` currently lacks a rule telling the coder to input `999` for the Number of Items and Reliability (Alpha) when encountering these single-item indices.
