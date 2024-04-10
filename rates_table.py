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

def Create_table(folder):
    
    # Import needed packages 
    import pandas as pd
    import glob
    from pathlib import Path
    value = float('nan') 
    # assign directory
    directory = folder
    
    # iterate over files in that directory
    files = Path(directory).glob('*')
        
    # Initializing Dictionary 
    df_dict = {}
    for i in column_names_1:
        df_dict[i] =[]
        
    # Reading through all files in specefied folder   
    for file in files:
        df = pd.read_excel(file,sheet_name=1)

        # Iterate through each column for pulling relevant data
        for i in range(df.shape[1]-4):
            if pd.isna(df.iloc[11,(4+i)]):
                break

            else:
                df_dict['Year'].append(int(df.iloc[3,3].strftime('%Y')))
                df_dict['Carrier-Network'].append(df.iloc[1,3])
                df_dict['Carrier Type'].append('Competitor' if df.iloc[1,3] != 'Kaiser Foundation Health Plan, Inc.' else 'KP')
                df_dict['Plan ID'].append(df.iloc[11,(4+i)])
                df_dict['Region'].append(df.iloc[2,5])
                df_dict['Age'].append(40)                      # Keep age constant at 40 
                df_dict['Plan Name'].append(df.iloc[10,(4+i)])
                df_dict['Metal Tier'].append(df.iloc[12,(4+i)])
                df_dict['Plan Category'].append(df.iloc[14,(4+i)])
                df_dict['Exchange Plan?'].append(df.iloc[16,(4+i)])
                df_dict['Network'].append(df.iloc[15,(4+i)])
                df_dict['Projected Member Months'].append(df.iloc[71,(4+i)])
                df_dict['Benefits in Addition to EHB'].append(df.iloc[49,(4+i)])
                df_dict['Av Metal Value'].append(df.iloc[13,(4+i)])


        # Converts the dictionary into a pandas dataframe            
        urrt_df = pd.DataFrame(data = df_dict)
        return urrt_df

                    
        # Converts the dictionary into a pandas dataframe            
        df_final1 = pd.DataFrame(data = df_dict2)
        df_final2 = pd.DataFrame(data = df_dict3)
        #exports the dataframe into an excel spreadsheet
        
        # Export DataFrames to Excel using ExcelWriter
        with pd.ExcelWriter(to_folder_path) as excel_writer:
            df_final1.to_excel(excel_writer, sheet_name='Wrk2', index=False)
            df_final2.to_excel(excel_writer, sheet_name='Wrk1', index=False)