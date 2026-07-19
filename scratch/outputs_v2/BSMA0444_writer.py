import json
import os

output_path = "G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/outputs_v2/BSMA0444.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

data = {
    "paper_id": "BSMA0444",
    "decision": "exclude",
    "exclusion_code": "3",
    "exclusion_notes": "[Excluded because the unit of analysis is the firm and it measures firm-level outsourcing and subcontracting-in as a percentage of sales rather than individual-level interpersonal boundary spanning behavior]. Verbatim Evidence: \"[4. Methods and data] A total of 579 cases with a combined response rate of 13.3 per cent were collected as part of the study. [...] Median age of the firms in the sample was 24 and median size of the firm was 41 employees.\" \"[4.1 Data set and measures] The extent of subcontracting-in was measured as work carried out on a subcontract basis for other firms as percent of total sales. Similarly, the extent of outsourcing was measured as work undertaken by the other firms for the business on a subcontract basis as a percent of total sales.\""
}

# The prompt says: "NEVER use ellipses (...) to summarize, abbreviate, or truncate sentences."
# Let me fix the first quote.

data["exclusion_notes"] = "[Excluded because the unit of analysis is the firm and it measures firm-level outsourcing and subcontracting-in as a percentage of sales rather than individual-level interpersonal boundary spanning behavior]. Verbatim Evidence: \"[4. Methods and data] A total of 579 cases with a combined response rate of 13.3 per cent were collected as part of the study.\" \"[4.1 Data set and measures] The extent of subcontracting-in was measured as work carried out on a subcontract basis for other firms as percent of total sales. Similarly, the extent of outsourcing was measured as work undertaken by the other firms for the business on a subcontract basis as a percent of total sales.\""

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
