import json
with open('scratch/batch_chunk_11.json', 'r', encoding='utf-8') as f:
    chunk = json.load(f)

with open('scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
    base_prompt = d[0]['Prompt'].split('Now review `')[0]

subagents = []
for c in chunk:
    prompt = base_prompt + f"Now review `{c['id']}`. The PDF is at `{c['pdf'].replace(chr(92), '/')}`. Output to `{c['out']}`."
    subagents.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer {c['id']}",
        "Prompt": prompt
    })

payload = {
    "Subagents": subagents,
    "toolSummary": "Invoke reviewers",
    "toolAction": "Running reviewers"
}
import urllib.request
import urllib.parse

# Maybe I can just save it to a file and output the content of the file
with open('scratch/invoke_payload.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=2)
