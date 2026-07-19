import json
papers = json.load(open('scratch/batch_chunk_2.json', 'r', encoding='utf-8'))
base_prompt = open('scratch/base_prompt.txt', 'r', encoding='utf-8').read()
payload = []
for p in papers[:5]:
    payload.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Reviewer for {p["id"]}',
        'Prompt': f'{base_prompt}Now review `{p["id"]}`. The PDF is at `{p["pdf"]}`. Output to `{p["out"]}`.'
    })
with open('scratch/call_5.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f)
