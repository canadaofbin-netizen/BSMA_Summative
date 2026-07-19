import json
with open('scratch/temp_subagents.json', 'r', encoding='utf-8') as f:
    subs = json.load(f)
for s in subs[10:]:
    print(f"{s['Role']}|{s['Prompt']}")
