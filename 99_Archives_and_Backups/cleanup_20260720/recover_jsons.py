import os
import json
import glob

brain_dir = r"C:\Users\yunky\.gemini\antigravity\brain"
output_dir = r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs"

os.makedirs(output_dir, exist_ok=True)

transcripts = glob.glob(os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript_full.jsonl"))

recovered = 0

for tpath in transcripts:
    try:
        with open(tpath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    
                    tool_calls = data.get('tool_calls', [])
                    if tool_calls:
                        for tc in tool_calls:
                            if 'write_to_file' in tc.get('name', ''):
                                args = tc.get('args', {})
                                target_file = args.get('TargetFile', '')
                                code_content = args.get('CodeContent', '')
                                
                                filename = os.path.basename(target_file)
                                if filename.startswith("BSMA") and filename.endswith(".json"):
                                    out_path = os.path.join(output_dir, filename)
                                    with open(out_path, 'w', encoding='utf-8') as out_f:
                                        out_f.write(code_content)
                                    recovered += 1
                                    print(f"Recovered {filename}")
                except Exception as e:
                    pass
    except Exception as e:
        pass

print(f"Total recovered JSONs: {recovered}")
