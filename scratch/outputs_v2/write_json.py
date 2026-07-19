import json
d = {
    'bsma_id': 'BSMA0447',
    'decision': 0,
    'exclusion_code': 1,
    'notes': '[Construct validity] The study focuses on salespeople as boundary-spanning employees, but the dependent variable is \\'behavioural strategies\\' measured solely as the percentage of time spent on tasks, rather than purposive boundary-spanning actions. Rule 18 explicitly states that measuring the percentage of time spent without specifying purposive actions is invalid and must be excluded under Code 1. Verbatim Evidence: \"[Dependent variables: salesperson behavioural strategies and satisfaction] The three facets of behavioural strategies (i.e., focus on the supervisor, the customer and the administrative aspects of the job) were each measured by the percentage of time the salesperson devotes to supervisors, customers and administrative tasks respectively.\"',
    'confidence': 100
}
with open('BSMA0447.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2)
