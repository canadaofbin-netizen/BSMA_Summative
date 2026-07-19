import json

with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\subagents_payload_v2.json', encoding='utf-8') as f:
    data = json.load(f)

p = data[0]['Prompt']
idx = p.find('=== END OF PREAMBLE ===')
if idx != -1:
    base_prompt = p[:idx + len('=== END OF PREAMBLE ===\n\n')]
    
    with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\batch_chunk_0.json', encoding='utf-8') as f2:
        batch_data = json.load(f2)
    
    subagents = []
    for item in batch_data:
        new_prompt = base_prompt + f"Now review `{item['id']}`. The PDF is at `{item['pdf']}`. Output to `{item['out']}`."
        subagents.append({
            'TypeName': 'bsma_reviewer_v3',
            'Role': f"Reviewer for {item['id']}",
            'Prompt': new_prompt
        })
    
    with open(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\subagents_payload_v3.json', 'w', encoding='utf-8') as f3:
        json.dump(subagents, f3, indent=2)
    print('Created 40 subagents payload in subagents_payload_v3.json')
else:
    print('Preamble not found')
