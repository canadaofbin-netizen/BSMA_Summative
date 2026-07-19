import json
import re

text = open('scratch/BSMA0601_text.txt', encoding='utf-8').read().replace('\ufb01', 'fi')

def get_quote(pattern):
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0).replace('\n', ' ')
    return ''

q1 = get_quote(r'A\s+cross-sectional\s+mail\s+survey\s+was\s+administered\s+to\s+collect\s+data\s+from\s+the\s+manufacturing\s+.*?rms\s+in\s+Taiwan\.')
q2 = get_quote(r'Demographic\s+characteristics\s+of\s+the\s+responding\s+.*?rms\s+\(n\s*=\s*250\)')
q3 = get_quote(r'CO1\s+Our\s+.*?rm\s+and\s+its\s+major\s+supplier\s+coordinate\s+their\s+efforts\s+harmoniously\.')
q4 = get_quote(r'CO3\s+Our\s+.*?rm\s+and\s+its\s+major\s+supplier\s+meet\s+frequently\s+for\s+both\s+formal\s+and\s+informal\s+discussions\s+of\s+important\s+issues\.')

verbatim = f'[Participants] "{q1}" [Participants] "{q2}" [Measures] "{q3}" [Measures] "{q4}"'

out = {
    'verification_checklist': {
        'is_construct_valid': False,
        'is_individual_level': False,
        'is_real_employee_sample': True,
        'is_leader_bsb': False,
        'is_intra_org_bsb': False
    },
    'self_correction_logic': "Q1. The sample is not students, it is firm managers. Q2. The N=250 represents firms, not individuals. This violates the individual-level requirement. Q3. The boundary spanning (interfirm collaboration and IT skills) is measured at the firm collective level (e.g., 'Our firm', 'Our IT staff'), not the focal respondent nor their manager. Q4. Mere communication? It measures interorganizational integration. Q5. The variable is correlated but at the firm level. Q6. It is not Leader BSB. Q7. It is not Intra-Organizational BSB. Q8. The construct is firm-level B2B integration and firm-level IT skills, lacking valid individual-level effect sizes.",
    'status': '0',
    'reason_code': '3',
    'reason_summary': 'Firm-level analysis (N=250 firms) measuring interfirm collaboration and firm-level IT staff skills, not individual-level boundary spanning behavior.',
    'verbatim': verbatim
}

import os
os.makedirs('scratch/outputs', exist_ok=True)

with open('scratch/outputs/BSMA0601.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=4, ensure_ascii=False)
