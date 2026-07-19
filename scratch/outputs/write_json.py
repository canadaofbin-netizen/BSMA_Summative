import json
data = {
  'verification_checklist': {
    'is_construct_valid': True,
    'is_individual_level': True,
    'is_real_employee_sample': True,
    'is_leader_bsb': False,
    'is_intra_org_bsb': False
  },
  'self_correction_logic': 'Q1. The sample consists of 158 public managers from Rijkswaterstaat (not students). Q2. The correlation matrix N=158 represents individual managers, with clustered standard errors accounting for nesting in 58 projects. It is not aggregated to team or firm level. Q3. Boundary spanning is performed by the focal respondent (To what extent were you involved in...). Q4. The construct measures purposive boundary spanning activities (relational, mediation, information exchange, coordination), not mere communication frequency. Q5. BSB is an independent variable in a structural model and zero-order latent correlations are provided in Table 4. Q6. This is not cross-entity Leader BSB (managers rate themselves). Q7. It is inter-organizational BSB (boundary spanning with private partner organizations). Q8. The construct is explicitly BSB.',
  'status': '1',
  'reason_code': 'NA',
  'reason_summary': 'The study measures individual-level boundary spanning behaviors of 158 public managers working on inter-organizational infrastructure projects, providing a zero-order latent correlation matrix.',
  'verbatim': '[Sample] \"The data were collected through a survey sent to public managers from Rijkswaterstaat, the executive agency of the Ministry of Infrastructure and Water Management in the Netherlands.\" [Sample Size] \"This brings the number of observations in the dataset to a total of 158 (from 58 projects).\" [Level of Analysis] \"The assumption of independence of observations and errors could be compromised as the data are clustered by projects. This has been accounted for, however, in the analysis by using clustered robust standard errors, which relaxes the assumption of independence of errors to the assumption of independence of clusters.\" [Measures] \"Boundary spanning activities (BS, Cronbach s alpha 0.97, composite reliability 0.97) To what extent were you involved in...\" [Measures] \"RA1: Building and maintaining lasting relationships with the partner organization.\"'
}
with open('scratch/outputs/BSMA0512.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
