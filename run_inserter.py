import subprocess
import json

data = {
  "article_id": "BSMA0006",
  "inclusion_status": 1,
  "samples": [
    {
      "sample_number": 1,
      "sample_size": 177,
      "publication_type": 1,
      "study_design": 1,
      "international_context": 1,
      "occupation_type": "expatriates",
      "bs_measures": [
        {
          "name": "Expatriates' boundary-spanning",
          "items": 26,
          "alpha": 0.96,
          "mean": 5.27,
          "sd": 0.74,
          "min": 1,
          "max": 7,
          "report_type": 2,
          "specific_measure": "We developed a new scale for expatriates’ boundary-spanning following Hinkin’s (1998) scale-development procedure. ... our final 26-item scale includes nine items for functional, seven items for linguistic, and ten items for cultural boundary-spanning",
          "notes": ""
        }
      ],
      "correlations": [
        {
          "non_bs_name": "Mutual trust",
          "r": 0.71,
          "alpha": 0.90,
          "mean": 5.25,
          "sd": 0.68,
          "items": 11,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Mutual trust, cognition-based mutual trust, and affect-based mutual trust were reported by both expatriates and host-country coworkers (11 items; McAllister, 1995).",
          "notes": "Reported by both expatriate and coworker, computed using SRP."
        },
        {
          "non_bs_name": "Cognition-based mutual trust",
          "r": 0.63,
          "alpha": 0.80,
          "mean": 5.38,
          "sd": 0.64,
          "items": 999,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Mutual trust, cognition-based mutual trust, and affect-based mutual trust were reported by both expatriates and host-country coworkers (11 items; McAllister, 1995).",
          "notes": "Reported by both expatriate and coworker."
        },
        {
          "non_bs_name": "Affect-based mutual trust",
          "r": 0.70,
          "alpha": 0.87,
          "mean": 5.11,
          "sd": 0.81,
          "items": 999,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Mutual trust, cognition-based mutual trust, and affect-based mutual trust were reported by both expatriates and host-country coworkers (11 items; McAllister, 1995).",
          "notes": "Reported by both expatriate and coworker."
        },
        {
          "non_bs_name": "Role stressors",
          "r": 0.42,
          "alpha": 0.93,
          "mean": 3.64,
          "sd": 0.97,
          "items": 17,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Role stressors were indicated by expatriates (17 items; Rizzo et al., 1970; Beehr et al., 1976).",
          "notes": ""
        },
        {
          "non_bs_name": "Expatriates' subsidiary identification",
          "r": 0.45,
          "alpha": 0.92,
          "mean": 5.30,
          "sd": 0.95,
          "items": 6,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Subsidiary identification (reported by expatriates) and MNE identification (reported by host-country coworkers) were both measured using an organizational identification scale (six items; Mael & Ashforth, 1992).",
          "notes": ""
        },
        {
          "non_bs_name": "Expatriates' emotional exhaustion",
          "r": -0.01,
          "alpha": 0.97,
          "mean": 3.63,
          "sd": 1.49,
          "items": 9,
          "min": 1,
          "max": 7,
          "report_type": 1,
          "specific_measure": "Emotional exhaustion was reported by expatriates (nine items; Maslach & Jackson, 1981)",
          "notes": ""
        },
        {
          "non_bs_name": "Expatriates' outgroup categorization",
          "r": 0.25,
          "alpha": 0.83,
          "mean": 4.35,
          "sd": 0.97,
          "items": 7,
          "min": 1,
          "max": 7,
          "report_type": 2,
          "specific_measure": "outgroup categorization was reported by host-country coworkers (seven items; Leonardelli & Toh, 2011).",
          "notes": ""
        },
        {
          "non_bs_name": "Expatriate age",
          "r": 0.02,
          "alpha": 999,
          "mean": 33.91,
          "sd": 6.64,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "We included expatriates’ and host-country coworkers’ age, gender, industry, tenure in their subsidiaries, and foreign language proficiency (Liu & Jackson, 2008).",
          "notes": "Years"
        },
        {
          "non_bs_name": "Expatriate gender",
          "r": -0.06,
          "alpha": 999,
          "mean": 1.50,
          "sd": 0.50,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "We included expatriates’ and host-country coworkers’ age, gender, industry, tenure in their subsidiaries, and foreign language proficiency (Liu & Jackson, 2008).",
          "notes": "1 = male, 2 = female"
        },
        {
          "non_bs_name": "Expatriate tenure",
          "r": 0.08,
          "alpha": 999,
          "mean": 2.63,
          "sd": 0.88,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "We included expatriates’ and host-country coworkers’ age, gender, industry, tenure in their subsidiaries, and foreign language proficiency (Liu & Jackson, 2008).",
          "notes": "Years"
        },
        {
          "non_bs_name": "Expatriate language proficiency",
          "r": 0.47,
          "alpha": 999,
          "mean": 4.10,
          "sd": 1.46,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "We included expatriates’ and host-country coworkers’ age, gender, industry, tenure in their subsidiaries, and foreign language proficiency (Liu & Jackson, 2008).",
          "notes": "Proxy for language proficiency."
        },
        {
          "non_bs_name": "Industry",
          "r": -0.08,
          "alpha": 999,
          "mean": 5.70,
          "sd": 2.82,
          "items": 999,
          "min": 999,
          "max": 999,
          "report_type": 1,
          "specific_measure": "We included expatriates’ and host-country coworkers’ age, gender, industry, tenure in their subsidiaries, and foreign language proficiency (Liu & Jackson, 2008).",
          "notes": "Dummy control variable."
        }
      ]
    }
  ]
}

data_str = json.dumps(data)

subprocess.run(["python", ".agents/scripts/universal_excel_inserter.py", "--excel", "BSMA_Master_Coding_Sheet.xlsx", "--data", data_str], check=True)
