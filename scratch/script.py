import json
import os

out_dir = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2'
os.makedirs(out_dir, exist_ok=True)

data = {
    'BSMA_ID': 'BSMA0278',
    'Authors': 'Atuahene-Gima',
    'Year': 2003,
    'Title': 'The Effects of Centrifugal and Centripetal Forces on Product Development Speed and Quality: How Does Problem Solving Matter?',
    'Inclusion_Decision': '0 = Exclude',
    'Exclusion_Reason': '3 = Non-individual level (team/firm/org analysis)',
    'Verbatim_Notes': '[Reason summary] The study uses product development projects as the unit of analysis, with N = 104 projects. Boundary spanning behaviors (Centrifugal and Centripetal forces, e.g., Reach and Connectedness) are measured as team-level properties, with items referring to \"the project team\" or \"team members\", and data collected via consensus ratings from multiple team members. This violates the individual-level boundary spanning behavior requirement. Verbatim Evidence: \"[Sample] Of the 120 firms whose representatives agreed to participate, 104 firms provided responses, for an effective participation rate of 35 percent.\" \"[Sample] The average age of firms in the sample was 11 years; the average number of employees was 410.32; average project team size was 9.40 individuals; and the average project duration was 8.76 months.\" \"[Measures and Validation] Given the prevalence of consensus decision making among the Chinese and the varied natures of centrifugal and centripetal forces, I asked two team members in each participating project to provide a single consensual rating for the measures of these forces.\" \"[Appendix - Reach] Team members put a lot of effort in interacting with potential customers.\" \"[Appendix - Connectedness] The project team had close, personal interactions with other members of the firm regarding the project.\"'
}

with open(os.path.join(out_dir, 'BSMA0278.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
print('JSON saved successfully.')
