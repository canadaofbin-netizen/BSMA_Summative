import json

output = {
    "BSMA_ID": "BSMA0117",
    "Authors": "Daniel",
    "Year": 1998,
    "Included": 0,
    "Reason_for_Exclusion": "1",
    "Notes": "[Code 1]. Verbatim Evidence: \"[Definitions] Service Behaviour is defined as: The behaviors CCP engage as a response to role conflict that entails endeavouring to fulfil demands placed upon them through seeking to lessen demands or by avoiding completely demands placed upon them (Weatherly and Tansik, 1993 a).\" \"[Operational Definitions of Research Variables] The service behaviour measure utilised in this study comprises the 20-item scale developed in Pilot B, which consists of 11 items from Weatherly and Tansik plus 9 items generated from the focus groups\" \"[Operational Definitions of Research Variables] The customer orientation scale (COS) used in this study is an abridged form of the SOCO (Saxe and Weitz, 1982) scale.\" \"[Table 5.5 - Service Behaviour Factor Analysis Results] 11 I pretend not to understand what the customer is asking for and act as if the customer is asking for something else\""
}

with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2\BSMA0117.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
