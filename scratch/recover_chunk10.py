import json
import os

outputs_dir = "G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/"
os.makedirs(outputs_dir, exist_ok=True)

data = {
    "BSMA0607": {"decision": "0", "exclusion_code": "3", "notes": "The study surveys top or middle managers as key informants to measure firm-level boundary-spanning search, and the survey items explicitly use 'our firm' as the referent."},
    "BSMA0609": {"decision": "0", "exclusion_code": "3", "notes": "The unit of analysis is the firm level (N=110 service-oriented manufacturing enterprises). The authors surveyed three experts per enterprise as key informants."},
    "BSMA0610": {"decision": "0", "exclusion_code": "3", "notes": "Measures boundary spanning at the firm/department level (N=170 firms/IT departments) rather than individual-level behavior."},
    "BSMA0611": {"decision": "1", "exclusion_code": None, "notes": "Measures valid individual-level boundary-spanning behavior ('I can persuade outsiders...') among organizational employees (IT engineers and technicians), and provides a valid correlation matrix (N=452)."},
    "BSMA0612": {"decision": "1", "exclusion_code": None, "notes": "Validly measures intra-organizational boundary-spanning behavior (cross-departmental collaboration) among individual IT employees (N=161) in non-IT organizations. Passes proxy guardrail with 'I' referent."},
    "BSMA0620": {"decision": "0", "exclusion_code": "3", "notes": "Boundary spanning is measured as a team-level construct using individuals as key informants (refer to 'team members' rather than 'I')."},
    "BSMA0621": {"decision": "0", "exclusion_code": "1", "notes": "Surveys consultants but does not measure the construct of Boundary Spanning Behavior (measures demographic age heterogeneity and perceptions of being trusted)."},
    "BSMA0622": {"decision": "0", "exclusion_code": "1", "notes": "Qualitative study utilizing surveys and in-depth interviews, without providing extractable quantitative effect sizes or a correlation matrix."},
    "BSMA0623": {"decision": "0", "exclusion_code": "3", "notes": "Team-level aggregation. Aggregated all individual responses to the group mean, making the project group the unit of analysis."},
    
    "BSMA0624": {"decision": "1", "exclusion_code": None, "notes": "Investigates individual-level informational boundary spanning behavior (idea gathering and dissemination) among frontline employees and provides a latent correlation matrix."},
    "BSMA0625": {"decision": "0", "exclusion_code": "3", "notes": "Uses the team as the unit of analysis (N=73 teams) and aggregates individual responses to the group level."},
    "BSMA0626": {"decision": "0", "exclusion_code": "5", "notes": "[Code 2 & Code 3] Multi-study design where both studies analyze data at the group/team level (N=80 groups and N=40 groups), and Study 1 additionally uses a non-employee student sample."},
    "BSMA0627": {"decision": "1", "exclusion_code": None, "notes": "Measures valid intra-organizational boundary spanning behavior (scout and ambassador activities) among senior managers at the individual level (n=77)."},
    "BSMA0628": {"decision": "0", "exclusion_code": "1", "notes": "Focuses on career entry transition appraisals of boundary spanners, but does not measure boundary spanning behavior itself."},
    "BSMA0629": {"decision": "0", "exclusion_code": "4", "notes": "Conceptual paper that does not report primary empirical data."},
    "BSMA0630": {"decision": "0", "exclusion_code": "3", "notes": "Non-individual level (firm/project level analysis). Uses purchasing managers as key informants to evaluate inter-organizational supplier involvement and information sharing between business units."},
    "BSMA0631": {"decision": "0", "exclusion_code": "3", "notes": "Conducts a firm-level analysis where managers act as key informants for their company's boundary-spanning search, and the survey items explicitly use 'Our company'."},
    "BSMA0632": {"decision": "0", "exclusion_code": "3", "notes": "Unit of analysis is the project team, and the dataset includes repeated measures (124 product managers rating 234 projects), violating statistical independence."},
    
    "BSMA0633": {"decision": "0", "exclusion_code": "3", "notes": "Analyzes network tie formation at the organizational level (directional dyads between government agencies and NGOs on Twitter) rather than interpersonal boundary spanning behavior of individual employees."},
    "BSMA0634": {"decision": "0", "exclusion_code": "3", "notes": "Operates at the team level (N=82) and uses team-referent survey items."},
    "BSMA0635": {"decision": "1", "exclusion_code": None, "notes": "Measures valid individual-level boundary spanning behavior."},
    "BSMA0636": {"decision": "0", "exclusion_code": "4", "notes": "Conceptual/review paper of Customer Lifetime Value models and does not contain primary empirical data or effect sizes."},
    "BSMA0637": {"decision": "0", "exclusion_code": "3", "notes": "Measures firm-level proactive boundary-spanning search using middle/senior managers as key informants (Proxy Guardrail), and the measurement items refer to 'Our firm'."},
    "BSMA0638": {"decision": "0", "exclusion_code": "3", "notes": "Measures boundary spanning at the team level, using respondents as key informants for 'The ICC team'."},
    "BSMA0639": {"decision": "0", "exclusion_code": "3", "notes": "Non-individual level, N=163 enterprises, key informant rating team/firm behavior."},
    "BSMA0640": {"decision": "0", "exclusion_code": "3", "notes": "Unit of analysis is the firm (N=204 firms) and the respondents act as key informants answering firm-level items ('We/Our strategy')."},
    "BSMA0641": {"decision": "0", "exclusion_code": "1", "notes": "Focuses on work-life boundary blurring via SNS coworker friendships, rather than purposive inter- or intra-organizational boundary spanning behavior."}
}

for paper_id, result in data.items():
    result["id"] = paper_id
    output_path = os.path.join(outputs_dir, f"{paper_id}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
print(f"Successfully generated {len(data)} JSON files.")
