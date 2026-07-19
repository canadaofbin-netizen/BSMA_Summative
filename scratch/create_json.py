import json

data = {
  "BSMA_ID": "BSMA0130",
  "Author": "Caldwell & O'reilly",
  "Year": 1982,
  "Included": 0,
  "Exclusion_Code": 1,
  "Notes": "[No effect size of interest]. The study does not measure Boundary Spanning Behavior (BSB) as a quantitative variable. It measures job performance, tenure, and self-monitoring. 'Boundary spanning' is only used to describe the nature of the job positions held by the sample (field representatives), not as a measured construct. Verbatim Evidence: \"[Subjects] Respondents were field representatives for a large franchise organization. Job duties involved servicing franchised outlets. ... To verify the boundary-spanning and social information processing requirements of the job, a brief job analysis was conducted.\" \"[Measures] To test the hypotheses, two constructs were assessed: job performance and attention to social cues.\" \"[Results] Table 1 presents means, standard deviations, and zero-order and partial correlations for all variables. ... 1. Performance 2. Tenure (months) 3. Self-monitoring\""
}

with open("G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0130.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("JSON file created successfully.")
