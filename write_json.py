import json, os

data = {
  "id": "BSMA0473",
  "qa_verdict": "Exclude",
  "reason_code": "Code 1",
  "justification": "The study measures boundary spanning solely as the frequency of inter-organizational contact without specifying any purposive boundary-spanning action (e.g., seeking resources, representing, scanning). This violates Rule 18 (Purposive Action vs. Mere Communication). Verbatim Evidence: \"[Measures] Since we were interested in all instances of employees’ inter-organizational contact, we operationalized this variable as frequency of boundary-spanning contact between peacekeepers and members of other organizations such as NGOs, inter-governmental organizations, and local authorities.\" \"[Measures] Participants responded to the question, ‘What parties did you have contact with? Please indicate the frequency of these contacts for your job.’\""
}

path = r"C:\Users\yunky\.gemini\antigravity\brain\75959b0d-11da-4ec8-97cb-bfc5fad81a42\scratch\repo\13team_qa_fp_outputs\BSMA0473_qa.json"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
