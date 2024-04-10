# Rate table creation
def rate_table(folder):
    import pandas as pd
    import glob
    import re

    # Creating a list of all file names within the specefied directory
    files = glob.glob(f'{folder}/*.xls')

    dfs = []

    for file in files:
        df = pd.read_excel(file,sheet_name='Rate Table',header=11)
        df = df.iloc[1:,:5]
        df = df.rename(columns=lambda x: re.sub(r'\*$', '', x))
        df['Individual Rate'] = pd.to_numeric(df['Individual Rate'], errors='coerce')
        dfs.append(df)

    rates = pd.concat(dfs,ignore_index=True)
    rates = rates[rates.Age == 40].reset_index()
    return rates


# URRT Table formation

def urrt_table(folder): 