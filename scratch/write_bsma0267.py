import json
data = {
    'verification_checklist': {
        'is_construct_valid': True,
        'is_individual_level': True,
        'is_real_employee_sample': True,
        'is_leader_bsb': False,
        'is_intra_org_bsb': True
    },
    'self_correction_logic': 'Q1. Yes, checked. The sample is 229 ISDP employees. Q2. Yes, the correlation matrix represents individuals (N=229). Q3. Focal respondents rate their own boundary spanning behavior. Q4. Construct measures purposive BSB (e.g., represent my department to outsiders) based on Miles and Perrault (1976). Q5. Yes, zero-order correlations are available in Table 5.2. Q6. Not leader BSB. Q7. Yes, it measures intra-organizational BSB. Q8. Construct is indeed BSB. All criteria met for inclusion.',
    'status': '1',
    'reason_code': 'NA',
    'reason_summary': 'Valid measure of boundary spanning behavior among information systems development personnel with extractable zero-order correlations.',
    'verbatim': '[Sample] "In total, nine companies participated in the study with data collected from 229 individuals." [Sample] "The study participants included applications programmers, programmer/analysts, analysts, and project leaders." [Measures] "The second measure, developed by Miles and Perrault [1976], is used to investigate the boundary spanning activities of laboratory research and development personnel. This measure investigates several aspects of boundary spanning, including representational, and is superior to the Keller measure." [Measures] "REWORDEDi Represent my department or work group to outsiders. Review plans with groups or individuals who are not members of my department." [Correlations] "BS \\n1.0 \\nCOMM \\n.164* \\n1.0 \\nRC \\n.275* \\n-.272* \\nRA \\n-.075* \\n-.499* \\nJS \\n.047 \\n.618* \\nIQ \\n-.161* \\n-.692*" [Correlations] "Legend BS = Boundary Spanning COMM = Commitment RC = Role Conflict RA = Role Ambiguity JS = Job Satisfaction IQ = Intention to Quit Table 5.2"'
}
with open('scratch/outputs/BSMA0267.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
