import subprocess
json_str = '{"article_id": "BSMA0001", "inclusion_status": 0, "exclusion_reason": "Not empirical (Qualitative interview study with no correlation matrix)"}'
subprocess.run(['python', '.agents/scripts/universal_excel_inserter.py', '--excel', 'BSMA_Master_Coding_Sheet.xlsx', '--data', json_str])
