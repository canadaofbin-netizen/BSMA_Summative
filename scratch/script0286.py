import json
out = {
    'Handled': True,
    'BSMA_ID': '0286',
    'Title': 'An emergent taxonomy of boundary spanning in the smart city context',
    'Authors': 'Karimikia et al. (2022)',
    'Year': '2022',
    'Source': 'Technological Forecasting & Social Change',
    'Decision': '0 = Exclude',
    'Reason': '1 = No effect size of interest',
    'Notes': '[No effect size] Qualitative single case study. Verbatim Evidence: "[Abstract] Using data from the Dublin smart city projects, this study draws on the concept of boundary spanning to develop a taxonomy of the work of such intermediaries." "[Methodology] In order to elaborate the role of a boundary-spanning organization in conceiving a multidimensional view, we have adopted a holistic single case study methodology"'
}
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0286.json', 'w') as f:
    json.dump(out, f, indent=4)
