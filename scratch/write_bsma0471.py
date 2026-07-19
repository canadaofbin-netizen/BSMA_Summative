import json

data = {
  "bsma_id": "BSMA0471",
  "decision": 0,
  "exclusion_code": 1,
  "notes": "[Construct Invalidity] The study measures employee flexibility/adaptive selling rather than boundary spanning behavior, which lacks an effect size of interest. Verbatim Evidence: \"[Measures] Boundary-spanning employee flexibility was assessed using four items based on Spiro and Weitz’s (1990) ADAPTS scale. Spiro and Weitz’s study emphasized the importance of boundary-spanning employee flexibility on their performance, and the items used from the scale measure employee flexibility. A sample item includes, 'I believe each customer requires a unique approach'.\"",
  "confidence": 100
}

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0471.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
