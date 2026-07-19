import json

with open('scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

base_prompt = data[0]['Prompt'].split('Now review `')[0]

with open('scratch/batch_chunk_8.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

payloads = []
for p in batch:
    prompt = f"{base_prompt}Now review `{p['id']}`. The PDF is at `{p['pdf']}`. Output to `{p['out']}`."
    payloads.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Validation2 for {p["id"]}',
        'Prompt': prompt
    })

with open('scratch/subagents_payload_batch8.json', 'w', encoding='utf-8') as f:
    json.dump(payloads, f, indent=2)
