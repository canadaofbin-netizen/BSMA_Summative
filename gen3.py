import json
with open('scratch/batch_chunk_11.json', 'r', encoding='utf-8') as f:
    chunk = json.load(f)

subagents = []
for c in chunk:
    prompt = f"Now review `{c['id']}`. The PDF is at `{c['pdf'].replace(chr(92), '/')}`. Output to `{c['out']}`."
    subagents.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer {c['id']}",
        "Prompt": prompt
    })

with open('scratch/invoke_payload_short.json', 'w', encoding='utf-8') as f:
    json.dump({"Subagents": subagents, "toolSummary": "Invoke reviewers", "toolAction": "Invoke"}, f, indent=2)
