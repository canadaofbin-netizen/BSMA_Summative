import subprocess
import json

data = {
  "article_id": "BSMA0008",
  "inclusion_status": 1,
  "samples": [
    {
      "sample_number": 1,
      "sample_size": 190,
      "publication_type": 1,
      "study_design": 1,
      "international_context": 1,
      "occupation_type": "MBA students / Consulting",
      "bs_measures": [
        {
          "name": "Boundary-spanning behavior",
          "items": 6,
          "alpha": 0.86,
          "mean": 2.91,
          "sd": 0.70,
          "min": 1,
          "max": 5,
          "report_type": 3,
          "specific_measure": "six items adapted directly from Ancona and Caldwell's (1992) study and modified to reflect the current consulting team context.",
          "notes": ""
        }
      ],
      "correlations": [
        {
          "non_bs_name": "Boundary-spanning role",
          "r": 0.40,
          "alpha": 0.86,
          "mean": 3.09,
          "sd": 0.82,
          "items": 6,
          "min": 1,
          "max": 5,
          "report_type": 1,
          "specific_measure": "all participants rate the extent to which they perceived each of the six boundary spanning behaviors as an expected part of their responsibilities",
          "notes": ""
        },
        {
          "non_bs_name": "Boundary-spanning self-efficacy",
          "r": 0.25,
          "alpha": 0.92,
          "mean": 4.07,
          "sd": 0.69,
          "items": 8,
          "min": 1,
          "max": 5,
          "report_type": 1,
          "specific_measure": "Scale items were based in part upon Parker's (1998) role breadth self-efficacy scale",
          "notes": ""
        },
        {
          "non_bs_name": "Asian ethnicity",
          "r": -0.23,
          "alpha": 999,
          "mean": 0.31,
          "sd": 0.46,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "Asian ethnicity (1, Asian, and 0, other)",
          "notes": "Demographic"
        },
        {
          "non_bs_name": "GMAT score",
          "r": 0.08,
          "alpha": 999,
          "mean": 653.90,
          "sd": 57.89,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "GMAT score (a continuous score)",
          "notes": "Proxy"
        },
        {
          "non_bs_name": "Role overload",
          "r": 0.18,
          "alpha": 0.83,
          "mean": 2.47,
          "sd": 0.85,
          "items": 3,
          "min": 1,
          "max": 5,
          "report_type": 1,
          "specific_measure": "Three items were adapted from Beehr et al. (1976) and modified for the current context.",
          "notes": ""
        }
      ]
    }
  ]
}

# Dump as JSON string
json_str = json.dumps(data)

# Call the script safely
subprocess.run(['python', '.agents/scripts/universal_excel_inserter.py', '--excel', 'BSMA_Master_Coding_Sheet.xlsx', '--data', json_str], check=True)
