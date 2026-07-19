import json, os

batch = json.load(open('scratch/batch_chunk_6.json', 'r'))
payload = json.load(open('scratch/subagents_payload_v2.json', 'r', encoding='utf-8'))

first_prompt = payload[0]['Prompt']
preamble = first_prompt.split('=== END OF PREAMBLE ===')[0] + '=== END OF PREAMBLE ===\n\n'

my_subagents = []
for p in batch:
    prompt = preamble + f"Now review `{p['id']}`. The PDF is at `{p['pdf']}`. Output to `{p['out']}`."
    my_subagents.append({
        "TypeName": "bsma_reviewer_v3",
        "Role": f"Reviewer for {p['id']}",
        "Prompt": prompt
    })

os.makedirs('scratch/invoke_chunks', exist_ok=True)
for i in range(0, len(my_subagents), 5):
    with open(f'scratch/invoke_chunks/chunk_{i//5 + 1}.json', 'w', encoding='utf-8') as f:
        json.dump(my_subagents[i:i+5], f, indent=2)

print(f"Written {len(my_subagents)} subagents.")
