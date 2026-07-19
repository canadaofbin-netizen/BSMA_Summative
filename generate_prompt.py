import json

with open('scratch/preamble.txt', 'r', encoding='utf-8') as f:
    preamble = f.read()

system_prompt = """You are an expert BSMA paper reviewer. Your task is to evaluate papers for inclusion in a meta-analysis based on strict criteria. You will be provided with the path to a PDF. You must use the `view_file` or Python scripting to read the PDF, evaluate the paper, and save your final output as a JSON file to the specified output path.

Ensure you adhere to the following output format in the JSON file:
{
  "bsma_id": "BSMAXXXX",
  "decision": 0 or 1,
  "exclusion_code": 1,
  "notes": "Verbatim evidence from the paper supporting the decision.",
  "confidence": 95
}
Your JSON output MUST match this structure exactly.

""" + preamble

with open('scratch/subagent_sys_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(system_prompt)

print(f"Done, length: {len(system_prompt)}")
