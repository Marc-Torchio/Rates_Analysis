# Rate table creation
def Rate_Table(folder):
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


# Plans and Benefit table creation
def Plan_Table(folder):
    import pandas as pd
    import glob
    import tab_iterator

    # Creating a list of all file names within the specefied directory
    files = glob.glob(f'{folder}/*.xlsm')

    dfs = []
    counter = 0
    for file in files:
        counter +=1
        df = tab_iterator.concat_matching_sheets(file)
        dfs.append(df)
    
    plans = pd.concat(dfs,ignore_index=True)
    plans.reset_index()
    print(f'Successfully pulled {counter} files')
    return plans

# URRT Table formation
def URRT_Table(folder):
    
    # Import needed packages 
    import pandas as pd
    from pathlib import Path
    
    # assign directory
    directory = folder
    
    # iterate over files in that directory
    files = Path(directory).glob('*')
        
    # Initializing Dictionary
    column_names = ['Year','Plan ID','Plan Name','Metal Tier','Av Metal Value','Region','Plan Category','Carrier Type','Exchange Plan?','Network', 'Age', 'Benefits in Addition to EHB','HIOS_ID'] 
    df_dict = {}
    for name in column_names:
        df_dict[name] =[]

    # Reading through all files in specefied folder   
    for file in files:
        df = pd.read_excel(file,sheet_name=1)

        # Iterate through each column for pulling relevant data
        for i in range(df.shape[1]-4):
            if pd.isna(df.iloc[11,(4+i)]):
                break

            else:
                year = int(df.iloc[3,3].strftime('%Y'))
                df_dict['Year'].append(2024 if year == 1900 else year)
                df_dict['HIOS_ID'].append(df.iloc[11,(4+i)][:5])
                df_dict['Carrier Type'].append('Competitor' if df.iloc[1,3] != 'Kaiser Foundation Health Plan, Inc.' else 'KP')
                df_dict['Plan ID'].append(df.iloc[11,(4+i)])
                df_dict['Region'].append(df.iloc[2,5])
                df_dict['Age'].append(40)                      # Keep age constant at 40 
                df_dict['Plan Name'].append(df.iloc[10,(4+i)])
                df_dict['Metal Tier'].append(df.iloc[12,(4+i)])
                df_dict['Plan Category'].append(df.iloc[14,(4+i)])
                df_dict['Exchange Plan?'].append(df.iloc[16,(4+i)])
                df_dict['Network'].append(df.iloc[15,(4+i)])
                df_dict['Benefits in Addition to EHB'].append(df.iloc[49,(4+i)])
                df_dict['Av Metal Value'].append(df.iloc[13,(4+i)])


        # Converts the dictionary into a pandas dataframe            
    urrt_df = pd.DataFrame(data = df_dict)
    urrt_df['HIOS_ID'] = urrt_df['HIOS_ID'].astype(str)
    return urrt_df


