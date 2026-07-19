import json
data = {
  'BSMA_ID': 'BSMA0121',
  'Authors': 'De Regge, Van Baelen, Aerens, Deweer, & Trybou',
  'Year': 2020,
  'Status': '1 = Include',
  'Exclusion_Code': 'NA',
  'Notes': '[Sample] Verbatim Evidence: "The sample consisted of 147 valid responses, yielding a response rate of 53.5%." "[Table 1] Note. N = 151." [Variables] "We concentrate on three distinct forms of nurses boundary-spanning behavior: service delivery (similar to key quality service elements), external representation (as an external advocate of the company), and internal influence (as an internal champion for delivering service excellence) (Bettencourt, Brown, & Mackenzie, 2005; Trybou & Gemmel, 2016)." "Boundary-spanning behavior. The questionnaire of Bettencourt and Brown (2003) was used"',
  'Sample_Size': 151,
  'Metrics': [
    {'Construct': 'Gender', 'r_with_External_representation': -0.075, 'r_with_Internal_influence': -0.005, 'r_with_Service_delivery': -0.077},
    {'Construct': 'Organizational tenure', 'r_with_External_representation': -0.034, 'r_with_Internal_influence': 0.232, 'r_with_Service_delivery': 0.128},
    {'Construct': 'Workload', 'r_with_External_representation': -0.040, 'r_with_Internal_influence': -0.137, 'r_with_Service_delivery': -0.167},
    {'Construct': 'Perceived organizational support', 'r_with_External_representation': 0.439, 'r_with_Internal_influence': 0.284, 'r_with_Service_delivery': 0.074},
    {'Construct': 'Perceived coworker support', 'r_with_External_representation': 0.467, 'r_with_Internal_influence': 0.351, 'r_with_Service_delivery': 0.103},
    {'Construct': 'Perceived Supervisor support', 'r_with_External_representation': 0.464, 'r_with_Internal_influence': 0.244, 'r_with_Service_delivery': 0.080},
    {'Construct': 'Affective organizational commitment', 'r_with_External_representation': 0.421, 'r_with_Internal_influence': 0.390, 'r_with_Service_delivery': 0.130},
    {'Construct': 'External representation', 'r_with_External_representation': 1.0, 'r_with_Internal_influence': 0.435, 'r_with_Service_delivery': 0.345},
    {'Construct': 'Internal influence', 'r_with_External_representation': 0.435, 'r_with_Internal_influence': 1.0, 'r_with_Service_delivery': 0.358},
    {'Construct': 'Service delivery', 'r_with_External_representation': 0.345, 'r_with_Internal_influence': 0.358, 'r_with_Service_delivery': 1.0}
  ],
  'Descriptives': [
    {'Construct': 'Gender', 'Mean': 999, 'SD': 999, 'Reliability': 999},
    {'Construct': 'Organizational tenure', 'Mean': 999, 'SD': 999, 'Reliability': 999},
    {'Construct': 'Workload', 'Mean': 999, 'SD': 999, 'Reliability': 999},
    {'Construct': 'Perceived organizational support', 'Mean': 3.38, 'SD': 0.507, 'Reliability': 0.715},
    {'Construct': 'Perceived coworker support', 'Mean': 4.08, 'SD': 0.577, 'Reliability': 0.892},
    {'Construct': 'Perceived Supervisor support', 'Mean': 4.06, 'SD': 0.664, 'Reliability': 0.900},
    {'Construct': 'Affective organizational commitment', 'Mean': 3.33, 'SD': 0.582, 'Reliability': 0.743},
    {'Construct': 'External representation', 'Mean': 3.89, 'SD': 0.676, 'Reliability': 0.812},
    {'Construct': 'Internal influence', 'Mean': 3.55, 'SD': 0.675, 'Reliability': 0.865},
    {'Construct': 'Service delivery', 'Mean': 4.17, 'SD': 0.502, 'Reliability': 0.762}
  ]
}
with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0121.json', 'w') as f:
    json.dump(data, f, indent=4)
print('JSON created.')
