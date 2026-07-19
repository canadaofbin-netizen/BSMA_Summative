import json
data = {
    'shorthand': 'BSMA0287',
    'paper_id': 287,
    'decision': 'Exclude',
    'exclusion_code': 1,
    'exclusion_notes': '[Work-Family Boundary Management] The study focuses on boundary management between work and family/life domains. Verbatim Evidence: \"[Literature review] The theoretical perspective of boundary management... These are boundary theory (Ashforth et al.,2 0 0 0 ;Allen et al.,2 0 1 4 ;Nippert Eng, 1996 ), which focuses on the work-life domain, and border theory ( Clark, 2000 ), which focuses on the work and family domain. As per these theories, individuals are forced to set boundaries to balance their work and family roles.\" \"[Introduction] This study has two important contributions to make. First, it investigates both individual factors as well as environmental factors based on the boundary fit perspective given by Ammons (2013) to divide individuals into various clusters, and second, it compares both positive and negative behavioral outcomes for all these clusters such as WFC, family-work boundary tactics and works positive spillover.\"'
}
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0287.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
