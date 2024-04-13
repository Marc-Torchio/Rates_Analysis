def GA_Carrier_Network_adjustment(new_df):
    import numpy as np
    import pandas as pd

    # Define conditions using the correct DataFrame (new_df, not df)
    conditions = [
        new_df['Network Name'].str.contains(r'^Pathway(?:(?!Guided Access).)*$', regex=True), #1
        new_df['Network Name'].str.contains(r'^Pathway Guided Access.*', regex=True), #2
        new_df['Network Name'].isin(['Ambetter Virtual Access GA', 'Plus SELECT GA', 'Wellstar SELECT GA']) #3
    ]

    # Define choices corresponding to each condition
    choices = [
        'BCBS - Pathway X HMO', #1
        'BCBS - Pathway X Guided Access HMO', #2
        'Peach State - Select HMO' #3
    ]

    # Apply conditions to set the 'Carrier-Network'
    new_df['Carrier-Network'] = np.select(conditions, choices, default=new_df['Carrier-Network'])
    return new_df


def GA_Area_adjustment(df):
    df['Plan Name'] = df['Plan Name'].fillna('')
    # Removing rows for KP Signature
    df_adj = df[~((df['Carrier-Network'] == 'KP HMO') & 
                  (df['Plan Name'].str.contains('signature', case=False)) & 
                   (df['Rating Area ID'] == 'Area 2'))]
    
    # Removing rows for KP standard
    df_adj = df_adj[~((df['Carrier-Network'] == 'KP HMO') & 
                      (df['Rating Area ID'] == 'Area 1') & 
                      (~df['Plan Name'].str.contains('signature', case=False)))]
    
    # Removing Area 1 rows for Alliant and BCBS Pathways
    df_adj = df_adj[~((df['Carrier-Network'] == 'Alliant - HMO') |
                      (df['Carrier-Network'] == 'Alliant - PPO') |
                      (df['Carrier-Network'] == 'BCBS - Pathway X HMO'))]
    
    return df_adj