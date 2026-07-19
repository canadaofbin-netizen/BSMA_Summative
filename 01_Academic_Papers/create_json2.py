import json
import os

data = {
    'verification_checklist': {
        'is_construct_valid': False,
        'is_individual_level': False,
        'is_real_employee_sample': True,
        'is_leader_bsb': False,
        'is_intra_org_bsb': False
    },
    'self_correction_logic': "Q1. The sample consists of local government officers, not students. Q2. The sample N is 234, representing local governments (organizations), not individuals. Q3. The focal respondent is not rating their own individual boundary spanning, but acting as a proxy informant rating their community or local government's collaborative efforts. Q4. Construct is organizational collaboration, not individual purposive BSB. Q5. Not a moderator issue. Q6. Not Leader BSB. Q7. Not Intra-Organizational BSB. Q8. The construct is organizational-level boundary spanning/collaboration, not individual-level BSB, meaning it is a firm-level analysis (Code 3).",
    'status': '0',
    'reason_code': '3',
    'reason_summary': "Non-individual level (firm/team analysis) - The unit of analysis is the local government (N=234) and respondents act as key informants rating their community's collaborative efforts.",
    'verbatim': "[Methodology] \"The data for this research is drawn from the 2016 International City/County Management Association (ICMA) Smart Cities Survey.\" [Methodology] \"Partnering with the Smart Cities Council, ICMA sent the survey in 2016 to 3,423 local government officers working in U.S. cities and counties with populations of 25,000 or greater.\" [Methodology] \"The survey consisted of twenty questions asking officers about their local governments’ smart cities practices including: their commitment to SCT (priorities), their engagement with SCT (activities), their perceived benefits of using SCT, and their barriers to implementing SCT.\" [Methodology] \"After eliminating records with missing data, our final sample includes responses from 234 local governments.\" [Table 2] \"The participants responded to the question 'What collaborative smart city efforts does your community participate in?' and county level efforts was one of the given options.\""
}

out_dir = 'C:/Users/yunky/.gemini/antigravity/brain/75959b0d-11da-4ec8-97cb-bfc5fad81a42/scratch/outputs_v3'
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, 'BSMA0003.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
