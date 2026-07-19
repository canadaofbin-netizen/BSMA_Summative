import os, json, glob, re

log_files = glob.glob(r'C:\Users\yunky\.gemini\antigravity\brain\*\.system_generated\logs\transcript_full.jsonl')
out_dir = r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2'
os.makedirs(out_dir, exist_ok=True)

recovered = 0
for file_path in log_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    step = json.loads(line)
                    content = step.get('content', '')
                    # Look for ```json ... ``` blocks
                    matches = re.findall(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                    # Also look for raw JSON objects starting with { "paper_id"
                    if not matches:
                        matches = re.findall(r'(\{[\s\r\n]*"paper_id"[\s\r\n]*:.*?\}\s*\})', content, re.DOTALL)
                    
                    for match in matches:
                        try:
                            data = json.loads(match)
                            if 'paper_id' in data and 'verification_checklist' in data:
                                paper_id = data['paper_id'].strip()
                                out_path = os.path.join(out_dir, f'{paper_id}.json')
                                with open(out_path, 'w', encoding='utf-8') as out_f:
                                    json.dump(data, out_f, indent=2)
                                recovered += 1
                        except:
                            pass
                except:
                    pass
    except:
        pass

print(f"Recovered {recovered} valid JSON verdicts from transcript_full.jsonl files.")
