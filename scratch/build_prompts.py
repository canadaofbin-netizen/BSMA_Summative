import json

with open('scratch/batch_chunk_14.json', 'r') as f:
    chunk = json.load(f)

with open('G:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)

first_prompt = payload[0]['Prompt']
parts = first_prompt.split('=== END OF PREAMBLE ===')
base_prompt = parts[0] + '=== END OF PREAMBLE ===\n\n'

subagents = []
for item in chunk:
    pid = item['id']
    pdf = item['pdf']
    out = item['out']
    
    append_str = f"Now review `{pid}`. The PDF is at `{pdf}`. Output to `{out}`."
    
    prompt = base_prompt + append_str
    
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Reviewer for {pid}',
        'Prompt': prompt
    })

with open('scratch/subagents_to_invoke_14.json', 'w') as f:
    json.dump(subagents, f, indent=2)

print(len(subagents))
