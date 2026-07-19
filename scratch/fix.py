import os, json, glob
import ast

failed_files = glob.glob(r'G:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\scratch\failed_v2\*.json')
fixed = 0
for f in failed_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # It looks like the file contains literal escape sequences like \n and \". 
        try:
            data = json.loads(content)
            if isinstance(data, str):
                data = json.loads(data) # double encoded
        except Exception as e:
            # Maybe it's not valid JSON at all, try to evaluate it as literal
            s = bytes(content, 'utf-8').decode('unicode_escape')
            data = json.loads(s)
            
        out_path = f.replace('failed_v2', 'outputs_v2')
        with open(out_path, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, indent=2)
        fixed += 1
    except Exception as e:
        print(f'Failed to fix {os.path.basename(f)}: {e}')

print(f'Fixed {fixed} files out of {len(failed_files)}')
