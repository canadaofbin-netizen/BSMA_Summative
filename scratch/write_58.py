import json
output = {
    "verification_checklist": {
        "is_construct_valid": False,
        "is_individual_level": False,
        "is_real_employee_sample": True,
        "is_leader_bsb": False,
        "is_intra_org_bsb": False
    },
    "self_correction_logic": "Q1. Checked sample: 120 organizational buyers, not students. Q2. Checked N: N=120 represents buyer-supplier relationships, violating individual level (Code 3). Q3. Respondent is rating the supplier agency and contact employee, not their own behavior. Q4. They measured the supplier's Human Capital and Social Capital, not purposive Boundary Spanning Behavior (Code 1). Q5. No BSB variable exists. Q6. Not Leader BSB; it's a buyer rating a supplier. Q7. Not Intra-organizational BSB. Q8. The construct is explicitly human capital and general social relationships, not BSB. Multiple flaws exist, assigning Code 5 [Code 1 and Code 3].",
    "status": "0",
    "reason_code": "5",
    "reason_summary": "[Code 1 and Code 3] Study measures Human Capital, Social Capital, and firm structural capital rather than Boundary Spanning Behavior (Code 1), and is conducted at the inter-firm B2B relationship level where informants evaluate their supplier agency (Code 3).",
    "verbatim": "[Reason summary] Study measures Human Capital, Social Capital, and firm structural capital rather than Boundary Spanning Behavior (Code 1), and is conducted at the inter-firm B2B relationship level where informants evaluate their supplier agency (Code 3). Verbatim Evidence: \"[Abstract] Methodology /approach: The model is tested on a sample of 120 organizational buyers of advertising services by using partial last squares, a structural equation modelling technique.\" \"[Appendix] Imagine a situation when your key contact employee in agency XYZ leaves to join another agency or to start a new agency. Based on your relationship with agency XYZ and with your contact employee, you have to make a decision whether your company would follow the contact employee to the new agency or remain as a customer in agency XYZ.\" \"[Appendix] Agency XYZ has devoted signi?cant resources to gain insight into our company’s market situation.\""
}
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0058.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
