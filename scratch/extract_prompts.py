import json

with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

my_ids = [f"BSMA0{i}" for i in range(613, 653)]
found = []
for d in data:
    for mid in my_ids:
        if mid in d['Prompt']:
            found.append(d)

print(f"Found {len(found)} exact prompts in payload for my batch.")
with open('g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch/my_subagents_args.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, indent=2)
