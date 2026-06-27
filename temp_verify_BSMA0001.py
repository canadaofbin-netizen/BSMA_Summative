import pandas as pd
df = pd.read_excel('BSMA_Master_Coding_Sheet.xlsx')
mask = df.apply(lambda row: row.astype(str).str.contains('BSMA0001').any(), axis=1)
print(df[mask].to_dict(orient='records'))
