import json
import os

os.makedirs('scratch/outputs_v2', exist_ok=True)

data = {
    'bsma_id': 'BSMA0344',
    'evaluation': 0,
    'exclusion_code': 3,
    'notes': '[Excluded because the unit of analysis is at the team level (N=89 teams in Study 1, N=139 teams in Study 2) and data was aggregated to team-level constructs.] Verbatim Evidence: "[Abstract] (89 automotive research and development teams, including 724 team mem-bers, 89 team leaders and 18 managers) and a time-lagged survey using two indepen-dent data sources (139 teams working in a Chinese utility company, including 640 team members and 139 team leaders)." "[2.4.2 Sample] Our final sample consisted of 89 teams with matched responses between team leaders and team members(724 team members, 89 team leaders, and 18 managers)" "[2.4.4 Analytical strategy] To justify the aggregation of boundary spanning, boundary buffering,and team workload demand ratings to the team level, we computed within-group interrater agreement ( r wg; James et al., 1993 ) and intraclass correlation (ICC) values."'
}

with open('scratch/outputs_v2/BSMA0344.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
