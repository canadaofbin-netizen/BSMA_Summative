import json
with open('scratch/base_prompt.txt', 'r', encoding='utf-8') as f:
    base = f.read()

system_prompt = \"\"\"You are a specialized academic paper data extractor and reviewer for the BSMA Meta-Analysis project.
Your primary task is to read a provided PDF of an academic paper and extract variables, correlations, effect sizes, and demographic data based on the provided instructions.
You must adhere strictly to the BSMA Meta-Analysis Global Project Rules.
Zero Guesswork Policy: Never guess or impute missing data. Use 999 for missing numbers and 'Not Reported' for missing strings.
Return your extraction results strictly in the required JSON format and write the output directly to the specified JSON file path.

\"\"\" + base

with open('scratch/batch_chunk_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

subs = []
for d in data:
    subs.append({
        'TypeName': 'bsma_reviewer_v3',
        'Role': 'Paper Data Extractor',
        'Prompt': 'Now review ' + d['id'] + '. The PDF is at ' + d['pdf'] + '. Output to ' + d['out'] + '.'
    })

with open('scratch/final_invoke.json', 'w', encoding='utf-8') as f:
    json.dump({'Subagents': subs}, f)
    
with open('scratch/reviewer_system_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(system_prompt)
