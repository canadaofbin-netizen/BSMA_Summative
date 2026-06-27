import pandas as pd
df = pd.read_excel('BSMA_Master_Coding_Sheet.xlsx')
row = df[df.apply(lambda r: r.astype(str).str.contains('BSMA0007').any(), axis=1)]
print(row)
