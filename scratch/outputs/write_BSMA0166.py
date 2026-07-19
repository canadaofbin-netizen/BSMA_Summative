import json
import os
os.makedirs('scratch/outputs', exist_ok=True)
data = {
  'verification_checklist': {
    'is_construct_valid': True,
    'is_individual_level': True,
    'is_real_employee_sample': True,
    'is_leader_bsb': False,
    'is_intra_org_bsb': True
  },
  'self_correction_logic': 'Q1. I verified the sample consists of 91 Self-Initiated Expatriate employees. Q2. The correlation matrix N=87-91 represents individual SIEs, not firms. Q3. The BSB is performed by the focal SIEs and rated by their supervisors (Assigned Expatriates), which is valid individual-level data. Q4. The construct specifically measures acting as a bridge person between distinct groups, which is purposive boundary spanning, not just mere communication. Q5. The BSB variables are included in a full zero-order correlation matrix (Appendix 3). Q6. This is not Leader BSB, but supervisor-rated employee BSB, which is valid. Q7. It is Intra-Organizational BSB (bridging HQ and subsidiary, and bridging AEs and local staff), which MUST BE INCLUDED per Rule 17. Q8. The construct is explicitly conceptualized and measured as boundary spanning. No exclusion rules apply.',
  'status': '1',
  'reason_code': 'NA',
  'reason_summary': 'Included. The study provides a valid zero-order correlation matrix for individual-level intra-organizational boundary spanning behavior (bridge person between HQ and subsidiary, and between assigned expatriates and local staff) for a sample of 91 Self-Initiated Expatriate employees.',
  'verbatim': '[3. 1. Sample] \"Our evidence is drawn from subsidiaries of Japanese MNEs in China.\" [3. 1. Sample] \"We collected the evaluations of 91 Japanese SIEs which cover 57% of the total Japanese SIEs employed.\" [3. 2. Measures] \"To test the boundary-spanning functions of Japanese SIEs, we focused on the two major cross-cultural interfaces which could be influenced by individual skills and/ or human resource management: The interface between Japanese assigned expatriates and Chinese staff in the Chinese subsidiary, and that between the Japanese-affiliates in China and the headquarters in Japan.\" [3. 2. Measures] \"Respondents were asked about the extent to which each SIE acts as a bridge between Japanese AEs and Chinese employees as well as between the Chinese operation and the headquarters in Japan.\" [Table 2] \"①Japanese self-initiated expatriates contribute as a bridge person between cultures (languages and mindset) of Japanese assigned expatriates and Chinese employees. ②Japanese self-initiated expatriates contribute as a bridge person between the local operation and the headquarters in Japan.\" [Appendix 3] \"Appendix 3: Descriptive statistics (Mean and Standard Deviation) and correlations of variables\"'
}
with open('scratch/outputs/BSMA0166.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
