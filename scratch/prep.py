import json

with open(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\batch_chunk_10.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

with open(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\subagents_payload_v2.json', 'r', encoding='utf-8') as f:
    payloads = json.load(f)

prompt_0 = payloads[0]['Prompt']
preamble = prompt_0.split('Now review `')[0]

subagents = []
for item in batch:
    paper_id = item['id']
    pdf_path = item['pdf'].replace('\\', '/')
    out_path = item['out']
    prompt = f"{preamble}Now review `{paper_id}`. The PDF is at `{pdf_path}`. Output to `{out_path}`."
    subagents.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': f'Validation2 for {paper_id}',
        'Prompt': prompt
    })

with open(r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\subagents_chunk_10_args.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=4)
