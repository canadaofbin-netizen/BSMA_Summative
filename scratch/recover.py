import os
import json
import ast

base_dir = r'C:\Users\yunky\.gemini\antigravity\brain'
output_dir = r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2'
os.makedirs(output_dir, exist_ok=True)

recovered = 0
for root, dirs, files in os.walk(base_dir):
    if 'transcript_full.jsonl' in files:
        filepath = os.path.join(root, 'transcript_full.jsonl')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in data:
                            for call in data['tool_calls']:
                                if call.get('name') == 'write_to_file':
                                    args = call.get('args', {})
                                    target = args.get('TargetFile', '')
                                    content = args.get('CodeContent', '')
                                    
                                    # Use ast.literal_eval to correctly decode the JSON encoded string if it's quoted
                                    try:
                                        if target.startswith('"') and target.endswith('"'):
                                            target = ast.literal_eval(target)
                                        if content.startswith('"') and content.endswith('"'):
                                            content = ast.literal_eval(content)
                                    except:
                                        pass
                                    
                                    if 'BSMA' in target and target.endswith('.json'):
                                        basename = os.path.basename(target)
                                        out_path = os.path.join(output_dir, basename)
                                        with open(out_path, 'w', encoding='utf-8') as out_f:
                                            out_f.write(content)
                                        recovered += 1
                                        print(f'Recovered {basename}')
                    except Exception as e:
                        pass
        except Exception as e:
            pass

print(f'Total recovered: {recovered}')
