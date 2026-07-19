import json

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/batch_chunk_8.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    payloads = json.load(f)

# Create a mapping of ID to payload prompt
payload_map = {p['Role'].split(' ')[-1]: p['Prompt'] for p in payloads}

for i in range(5):
    chunk = batch[i*8:(i+1)*8]
    subagents = []
    for item in chunk:
        subagents.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': f'Reviewer for {item["id"]}',
            'Prompt': payload_map[item['id']]
        })
    with open(f'G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/calls_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(subagents, f, indent=2)

print('Created 5 chunks: calls_0.json to calls_4.json')
