import json
data = {
    "paper_id": "BSMA0368",
    "judgment": "0 = Exclude",
    "exclusion_code": "5",
    "notes": "[Code 1 & Code 3] The study analyzes data at the dyadic level, using an Exponential Random Graph Model (ERGM) to predict the probability of advice ties between managers, which violates the requirement for individual-level statistical independence. Furthermore, the paper only reports dyadic network descriptive statistics and ERGM maximum likelihood estimates (log-odds), without providing a zero-order correlation matrix of individual-level variables. Verbatim Evidence: \"[3.2. Fieldwork and Data] Each respondent was presented with a list containing the names of the other 41 individuals in the sample arranged in alphabetical order and was asked to indicate the existence of an advice relation with each of them.\" \"[3.2. Fieldwork and Data] The advice-seeking network may be represented as a 42 ×42 binary adjacency matrix recording the presence or absence of advice relations for each possible pairs of individuals in the sample.\" \"[3.3. Variables and Measures] In the empirical part of the paper, we estimate models for the probability of advice ties as a function of (i) measures of organizational identiﬁcation, (ii) actor-speciﬁc covariates, and (iii) endogenous network effects.\""
}
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0368.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
