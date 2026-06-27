import sys, json
sys.path.append('.agents/scripts')
import universal_excel_inserter

with open('temp_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

universal_excel_inserter.insert_data('BSMA_Master_Coding_Sheet.xlsx', data)
