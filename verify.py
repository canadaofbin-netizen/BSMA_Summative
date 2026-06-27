import pandas as pd
df = pd.read_excel('BSMA_Master_Coding_Sheet.xlsx')
recent = df[df['Article_ID'] == 'BSMA0006']
for idx, row in recent.iterrows():
    print(f"Non_BS: {row['Non_BS_Measure_Name']}, r: {row['r']}, Alpha: {row['Non_BS_Alpha']}, Mean: {row['Non_BS_Mean']}, SD: {row['Non_BS_SD']}, Items: {row['Non_BS_Items']}")
