import json

with open('scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)

base_prompt = payload[0]['Prompt'].split('=== END OF PREAMBLE ===')[0] + '=== END OF PREAMBLE ===\n\n'

with open('scratch/batch_chunk_2.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

subagents = []
for item in batch:
    prompt = base_prompt + f\"Now review \{item['id']}\. The PDF is at \{item['pdf']}\. Output to \{item['out']}\.\"
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f\"Reviewer for {item['id']}\",
        'Prompt': prompt
    })

chunks = [subagents[i:i+9] for i in range(0, len(subagents), 9)]

with open('scratch/all_tool_calls.json', 'w', encoding='utf-8') as f:
    json.dump([{'toolAction': 'Invoke subagents', 'toolSummary': 'Invoke chunk', 'Subagents': chunk} for chunk in chunks], f, indent=2)

print('Done')
