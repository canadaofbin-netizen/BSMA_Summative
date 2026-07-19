import json

with open('scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
base_prompt = data[0]['Prompt'].split('Now review')[0]

with open('scratch/batch_chunk_2.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for i in range(4):
    chunk = papers[i*10 : (i+1)*10]
    payload = []
    for p in chunk:
        prompt_text = f"{base_prompt}Now review `{p['id']}`. The PDF is at `{p['pdf']}`. Output to `{p['out']}`."
        payload.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': f'Reviewer for {p["id"]}',
            'Prompt': prompt_text
        })
    with open(f'scratch/chunk_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f)

print('Chunks created')
