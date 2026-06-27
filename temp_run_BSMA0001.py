import subprocess
import json

with open("temp_BSMA0001_payload.json") as f:
    data = f.read()

subprocess.run(["python", ".agents/scripts/universal_excel_inserter.py", "--excel", "BSMA_Master_Coding_Sheet.xlsx", "--data", data])
