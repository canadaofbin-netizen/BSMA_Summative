import json

data = {
  "paper_id": "BSMA0314",
  "decision": "Exclude",
  "exclusion_code": 5,
  "exclusion_notes": "[Code 2 & Code 3] Excluded because the sample consists of independent pre-founding entrepreneurs in a venture creation program (not organizational employees) and the boundary spanning correlations are aggregated to the team level. Verbatim Evidence: \"[Abstract] The multilevel mediation model was tested based on data from 196 members of 58 teams of a venture creation programme.\" \"[Sample and Procedure] We gathered data in collaboration with an innovation and start-up centre in Germany. We studied teams who participated in a venture creation programme that combines education and incubation\" \"[Table 1] TABLE 1 Descriptives and Intercorrelations of Study Variables on the Team Level ... Note: N = 58 teams. ... Individual-level variables were aggregated to the team level.\""
}

with open(r'G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0314.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
