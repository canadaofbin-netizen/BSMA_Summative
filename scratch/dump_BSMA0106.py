import json
import os
import re

notes = '''[No effect size of interest. The study examines optimism, role stressors, and burnout among customer service representatives in boundary-spanning positions, but it does not measure boundary spanning behavior (BSB) itself.] Verbatim Evidence: "[Sample] The sample consisted of customer service representatives from a medium-sized, multifaceted service organization in the Midwestern United States. We selected a predominantly service-oriented organization, as the boundary-spanning nature of the participants' positions increased the likelihood that role stressors (ambiguity and conflict) would be observed." "[Measures] With the exception of performance, variables in the research model were measured using existing scales that have demonstrated acceptable psychometric properties. All surveys were self-report measures. Optimism was measured using Scheier and Carver's (1985) Life Orientation Test." "[Measures] Role ambiguity was conceptualized as the perceived discrepancy between information available and the information needed to perform adequately, and role conflict was conceptualized as the perceived conflicting demands placed upon the employee. The measures for role ambiguity and role conflict were drawn from Rizzo, House, and Lirtzman (1970)." "[Measures] Burnout consists of three dimensions: (a) emotional exhaustion or the feeling of depleted emotional resources, (b) depersonalization or negative excessively detached responses to other people at work, and (c) lack of personal accomplishment (Lee and Ashforth 1990; Melamed et al. 2006)." "[Measures] Job satisfaction was measured using the Cammann et al. (1983) Job Satisfaction Scale. Cronbach's alpha was .788 for the three-item Likert scale (strongly disagree-strongly agree). Finally, performance was assessed using two self-reported items."'''

data = {
    'BSMA_ID': 'BSMA0106',
    'Authors': 'Crosno et al.',
    'Year': 2009,
    'Status': 'Exclude',
    'Exclusion_Code': '1',
    'Notes': notes
}

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0106.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
