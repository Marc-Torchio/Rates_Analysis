def GA_Carrier_Network_adjustment(new_df):
    import numpy as np

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


def GA_flatfile_creation(df, rate_area):
    import tab_iterator
    import pandas as pd
    new_df = GA_Carrier_Network_adjustment(df)
    area_3 = new_df

    # Map Rate Areas and merge based off carrier-network col
    new_df = new_df.drop('Rating Area ID', axis=1)
    new_df = pd.merge(new_df, rate_area, on='Carrier-Network',how='left')
    # Cleaning Rating Area ID to match previous years
    new_df['Rating Area ID'] = new_df['Rating Area ID'].str.replace('Rating Area', 'Area')

    # Pulling relevant col names
    col_names = ['Year', 'Carrier-Network', 'Short Carrier', 'Carrier Type', 'Carrier', 'Plan ID', 'Rating Area ID', 'Region', 'Age', 'Plan Name', 'HRA Flag', 'Metal Tier', 'On/Off Exchange', 'Network','Narrow/Broad Network','Relevant' ,'Individual Rate']
    new_df = new_df[col_names]
    area_3 = area_3[col_names]
    # Adjusting Rate Area for region specific nuances (GA)
    new_df = GA_Area_adjustment(new_df)

    tab_iterator.GA_tab_creator(new_df, area_3)
    return new_df