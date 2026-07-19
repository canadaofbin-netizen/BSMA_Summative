import sys
import json

tool_call = {
    "DirectoryPath": "g:/My Drive/UCL/BSMA/BSMA ANTIGRAVITY/scratch",
    "toolAction": "Listing directory",
    "toolSummary": "List scratch dir"
}
sys.stdout.write('\x0fcall:default_api:list_dir' + json.dumps(tool_call) + '\x10\n')
