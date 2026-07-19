import os
import json
import glob
import re

brain_dir = r"C:\Users\yunky\.gemini\antigravity\brain"
output_dir = r"G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\outputs_v2"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Find all transcript.jsonl files
transcripts = glob.glob(os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript.jsonl"))

count = 0
for t_path in transcripts:
    try:
        with open(t_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'write_to_file' in line:
                    data = json.loads(line)
                    if 'tool_calls' in data:
                        for tc in data['tool_calls']:
                            if tc.get('name') == 'write_to_file':
                                args = tc.get('args', {})
                                target = args.get('TargetFile', '')
                                content = args.get('CodeContent', '')
                                
                                # Strip extraneous quotes from the path if they were hallucinated
                                target = target.strip('"\'')
                                content = content.strip('"\'')
                                
                                # Only process if it belongs to outputs_v2
                                if 'outputs_v2' in target:
                                    filename = os.path.basename(target)
                                    out_path = os.path.join(output_dir, filename)
                                    
                                    # Write the content, removing backslash escaping that might be left over
                                    # Since JSON string encoding might have double escaped it
                                    try:
                                        # attempt to parse as json to verify and re-dump
                                        # sometimes content is a stringified json string
                                        parsed = json.loads(content.encode('utf-8').decode('unicode_escape'))
                                        final_content = json.dumps(parsed, indent=2)
                                    except:
                                        final_content = content
                                        
                                    with open(out_path, 'w', encoding='utf-8') as out_f:
                                        out_f.write(final_content)
                                    count += 1
    except Exception as e:
        print(f"Error processing {t_path}: {e}")

print(f"Recovered {count} JSON files from transcripts.")
